Hidden acceptance tests for task `example-feature`. The agent never sees this folder.

Put one or more `Hidden*Test.java` files here, in the same package as the code
under test (for example `package com.acme.orders;`). The checker reads the
`package` line, copies the files into `src/test/java/<package path>/` of a
scratch copy of the attempt, and runs the whole suite offline.

Class names must start with `Hidden`: that is how the checker tells them from
the repository's own tests. Check both directions before you trust the task:
the tests fail at `base_ref` and pass on the real fix commit.
