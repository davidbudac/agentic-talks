"""Read-only, per-slide content/metadata comparison for the Ivory conversion.

Run: python3 ivory-conversion/audit.py source.html result.html > audit.json
Text differences require human review; no normalization removes source words.
"""
import difflib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys


VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
BLOCK = set('div p h1 h2 h3 h4 li ol ul td th tr table section br text tspan'.split())


class Node:
    def __init__(self, tag='', attrs=(), raw=''):
        self.tag, self.attrs, self.raw = tag, dict(attrs), raw
        self.children = []

    @property
    def classes(self):
        return self.attrs.get('class', '').split()

    def walk(self):
        yield self
        for c in self.children:
            if isinstance(c, Node):
                yield from c.walk()

    def text(self, omit=()):
        if self.tag in ('style', 'script') or set(self.classes) & set(omit):
            return ''
        content = ''.join(c.text(omit) if isinstance(c, Node) else c for c in self.children)
        return (' ' + content + ' ') if self.tag in BLOCK else content


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs, self.get_starttag_text())
        self.stack[-1].children.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, text):
        self.stack[-1].children.append(text)

    @property
    def slides(self):
        return [n for n in self.root.walk() if n.tag == 'section' and 'slide' in n.classes]


def norm(text):
    return ' '.join(text.split())


def raw_attr(node, name):
    m = re.search(r'\b' + name + r'\s*=\s*([\"\x27])(.*?)\1', node.raw, re.S)
    return m.group(2) if m else None


def compare(source, output):
    a, b = [Document(Path(p).read_text()) for p in (source, output)]
    result = {'source': str(source), 'output': str(output), 'counts': [len(a.slides), len(b.slides)],
              'structural_errors': [], 'slides': []}
    errors = result['structural_errors']
    if len(a.slides) != len(b.slides):
        errors.append('Slide count differs')
    for n in b.root.walk():
        if n.tag == 'style' or 'style' in n.attrs or (n.tag == 'script' and not n.attrs.get('src')):
            errors.append('Inline style/script: ' + n.raw)
        if 'snum' in n.classes and norm(n.text()):
            errors.append('Nonempty slide number')
        if set(n.classes) & {'dark', 'light', 'reveal'}:
            errors.append('Legacy presentation class: ' + n.raw)
    includes = [(n.tag, n.attrs.get('href') or n.attrs.get('src')) for n in b.root.walk() if n.tag in ('script', 'link')]
    if includes != [('link', 'ivory_design_system/styles.css'), ('script', 'ivory_design_system/deck-stage.js'), ('script', 'ivory_design_system/deck.js')]:
        errors.append('Unexpected includes: ' + repr(includes))
    for i, (old, new) in enumerate(zip(a.slides, b.slides), 1):
        row = {'slide': i, 'label': old.attrs.get('data-label'), 'errors': [], 'text_changes': []}
        for key in ('data-label', 'data-origin-slide', 'data-speaker-notes'):
            if old.attrs.get(key) != new.attrs.get(key):
                row['errors'].append(key + ' changed')
        if raw_attr(old, 'data-speaker-notes') != raw_attr(new, 'data-speaker-notes'):
            row['errors'].append('Raw speaker-notes encoding changed')
        links = [[n.attrs['href'] for n in s.walk() if 'href' in n.attrs] for s in (old, new)]
        row['links'] = links
        if sorted(links[0]) != sorted(links[1]):
            row['errors'].append('Link targets changed')
        texts = [norm(n.text(omit=('snum',))) for n in (old, new)]
        row['source_text'], row['output_text'] = texts
        words = [t.split() for t in texts]
        for op, x, y, u, v in difflib.SequenceMatcher(None, *words, autojunk=False).get_opcodes():
            if op != 'equal':
                row['text_changes'].append({'kind': op, 'source': ' '.join(words[0][x:y]), 'output': ' '.join(words[1][u:v])})
        result['slides'].append(row)
    return result


if __name__ == '__main__':
    result = compare(*sys.argv[1:3])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result['structural_errors'] or any(s['errors'] for s in result['slides'])))
