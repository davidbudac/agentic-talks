package com.example.invoicing;

import java.text.BreakIterator;
import java.text.Collator;
import java.text.Normalizer;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;
import java.util.regex.Pattern;

/**
 * Customer names, which are Unicode and arrive in every shape.
 *
 * <p>Names come from spreadsheets, web forms and old exports, so the same customer can appear
 * as {@code "Müller GmbH"}, {@code "Müller GmbH"} (a decomposed umlaut) or
 * {@code "  müller   gmbh "}. These helpers make them comparable without changing how they
 * are displayed.
 */
public final class CustomerNames {

    private static final Pattern WHITESPACE = Pattern.compile("\\s+");
    private static final Pattern COMBINING_MARKS = Pattern.compile("\\p{M}+");

    private CustomerNames() {
    }

    /** Canonical display form: NFC, single spaces, no outer whitespace. Case and accents stay. */
    public static String normalise(String name) {
        if (name == null) {
            throw new IllegalArgumentException("customer name is missing");
        }
        String composed = Normalizer.normalize(name, Normalizer.Form.NFC);
        return WHITESPACE.matcher(composed.strip()).replaceAll(" ");
    }

    /** Removes combining marks: {@code "Čapek"} becomes {@code "Capek"}. */
    public static String stripAccents(String text) {
        String decomposed = Normalizer.normalize(text, Normalizer.Form.NFKD);
        return COMBINING_MARKS.matcher(decomposed).replaceAll("");
    }

    /**
     * Human-friendly order: accent- and case-insensitive first (a root-locale {@link Collator}
     * at primary strength), then the normalised name itself, so the order is total and
     * deterministic ({@code "Capek"} before {@code "Čapek"}).
     */
    public static Comparator<String> comparator() {
        Collator collator = Collator.getInstance(Locale.ROOT);
        collator.setStrength(Collator.PRIMARY);
        collator.setDecomposition(Collator.CANONICAL_DECOMPOSITION);
        Comparator<String> primary = (a, b) -> collator.compare(normalise(a), normalise(b));
        return primary.thenComparing(CustomerNames::normalise);
    }

    /** True if {@code query} occurs in {@code name}, ignoring case and accents. */
    public static boolean matches(String name, String query) {
        String haystack = stripAccents(normalise(name)).toLowerCase(Locale.ROOT);
        String needle = stripAccents(normalise(query)).toLowerCase(Locale.ROOT);
        return haystack.contains(needle);
    }

    /** Initials of the first two words, keeping accents: {@code "Élodie Durand"} gives {@code "ÉD"}. */
    public static String initials(String name) {
        StringBuilder out = new StringBuilder();
        for (String word : normalise(name).split(" ")) {
            if (out.length() >= 2) {
                break;
            }
            if (!word.isEmpty() && Character.isLetter(word.codePointAt(0))) {
                out.appendCodePoint(Character.toUpperCase(word.codePointAt(0)));
            }
        }
        return out.toString();
    }

    /**
     * Fits {@code name} into {@code width} user-perceived characters, ending with an ellipsis
     * when cut. Never splits a letter from its combining accent, and replaces the newlines
     * some exports contain with spaces.
     */
    public static String displayName(String name, int width) {
        if (width < 1) {
            throw new IllegalArgumentException("width must be positive");
        }
        String clean = normalise(name.replace('\r', ' ').replace('\n', ' '));
        List<String> clusters = graphemes(clean);
        if (clusters.size() <= width) {
            return clean;
        }
        return String.join("", clusters.subList(0, width - 1)) + "…";
    }

    private static List<String> graphemes(String text) {
        BreakIterator iterator = BreakIterator.getCharacterInstance(Locale.ROOT);
        iterator.setText(text);
        List<String> clusters = new ArrayList<>();
        int start = iterator.first();
        for (int end = iterator.next(); end != BreakIterator.DONE; start = end, end = iterator.next()) {
            clusters.add(text.substring(start, end));
        }
        return clusters;
    }
}
