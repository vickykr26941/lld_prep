# Follow-up — Dictionary with Prefix & Wildcard Search

**Mirrors:** Problem 16 (Trie, efficient prefix navigation, Strategy) · Implement from scratch — no skeleton, no TODOs.

## Problem
Design an in-memory word dictionary that supports add/exact-match, **prefix** queries, and **wildcard** search where `.` matches any single character (like LeetCode "Add and Search Word" + prefixes).

## Functional requirements
1. `add_word(word)` and `remove_word(word)`.
2. `exists(word) -> bool` — exact match.
3. `starts_with(prefix) -> bool` and `words_with_prefix(prefix, limit) -> [words]` (sorted, capped at `limit`).
4. `search(pattern) -> bool` where `pattern` may contain `.` wildcards matching any one character (e.g. `c.t` matches "cat", "cot"). Full-length match.
5. `count_words()` and `count_with_prefix(prefix)` — efficient (maintain counts in trie nodes, not by scanning).
6. Wildcard search must explore the trie efficiently (prune branches), not enumerate all words.

## Non-functional / constraints
- Lookups are O(pattern length) for exact/prefix; wildcard is O(branches explored), not O(total words).
- Removal must not break shared prefixes of other words (decrement counts, prune dead nodes).
- Normalization policy stated (lowercase? alphabet?).
- (Bonus) thread-safety for concurrent reads + add/remove (read-write lock).

## Driver scenario
1. Add {"cat","cot","car","card","dog"}.
2. `exists("car")` → true; `exists("ca")` → false; `starts_with("ca")` → true.
3. `words_with_prefix("ca", 10)` → `["car","card","cat"]` (sorted).
4. `search("c.t")` → true (cat/cot); `search("c..d")` → true (card); `search("c.")` → false (length mismatch).
5. `remove_word("car")` → `exists("card")` still true; `words_with_prefix("car",10)` → `["card"]`.

## Edge cases
- Remove a word that is a prefix of another (e.g. "car" vs "card"). · Pattern all wildcards (`...`). · Prefix not present. · Empty string. · `limit` smaller than available matches. · Duplicate add.
