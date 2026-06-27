# 17 — In-Memory File System

**Difficulty:** ★★★★ · **Asked at:** Google, Amazon, Dropbox · **Patterns:** Composite, Strategy (path resolution)

## Problem
Design an in-memory file system supporting a directory tree, files with content, and shell-like path operations.

## Functional requirements
1. **Composite tree**: directories contain directories and files; a common `Node` abstraction (Composite pattern).
2. Operations (absolute and relative paths):
   - `mkdir(path)` — create directories, **creating intermediate dirs** (like `mkdir -p`).
   - `ls(path)` — if a directory, list its children **sorted**; if a file, return the file name.
   - `add_file(path, content)` / `read_file(path) -> content` / `append(path, content)`.
   - `rm(path)`, `mv(src, dst)`, `cp(src, dst)`.
3. Path resolution handles `/`, `.`, `..`, and trailing slashes correctly.
4. Track metadata: size (bytes), created/modified time (injectable clock), type.
5. (Senior bonus) Symbolic links, or a glob/`find` by pattern.

## Non-functional / constraints
- Uniform handling of files vs directories via the Composite interface — `ls`, `size`, `rm` shouldn't branch on type with sprawling `if`s.
- Path resolution is centralized (one resolver), not re-implemented per operation.
- Clear errors: no-such-path, not-a-directory, file-exists, rm non-empty dir (require recursive flag?).
- (Bonus) thread-safety for concurrent mutations.

## Driver scenario (your `main()` should show this)
1. `mkdir("/a/b/c")` (creates a, b, c).
2. `add_file("/a/b/file.txt", "hello")`; `read_file(...)` → "hello"; `append(..., " world")` → "hello world".
3. `ls("/a/b")` → `["c", "file.txt"]` (sorted).
4. `mv("/a/b/file.txt", "/a/file.txt")`; `ls("/a/b")` → `["c"]`.
5. `rm("/a/b")`; show error or recursive-rm behaviour per your rule.
6. Resolve a path with `..` (e.g. `ls("/a/b/../")`).

## Edge cases to handle
- `mkdir` where a file already occupies the name. · `read_file` on a directory (error). · `rm` of a non-empty directory. · `mv`/`cp` into a path that doesn't exist. · Root edge cases (`/`, `ls("/")`). · `..` above root (clamp to root).

## TODO checklist
- [ ] `Node` base + `File` and `Directory` (Composite)
- [ ] Central path resolver handling `/`, `.`, `..`
- [ ] `mkdir -p`, `ls` (sorted), file add/read/append
- [ ] `rm`, `mv`, `cp` with clear errors
- [ ] Metadata (size, mtime via injectable clock)
- [ ] `main()` driver covering the scenario above
