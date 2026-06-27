# 16 — Search Autocomplete / Typeahead

**Difficulty:** ★★★★ · **Asked at:** Google, Amazon, LinkedIn · **Patterns:** Trie, Strategy (ranking), Composite

## Problem
Design a typeahead service: given a prefix, return the **top-K** suggestions ranked by popularity, updating as users search.

## Functional requirements
1. `add_word(word, weight)` / build from an initial dictionary with frequencies.
2. `suggest(prefix, k) -> list[str]` — up to **K** completions of `prefix`, ordered by **rank** (frequency/weight, tie-break lexicographic).
3. `record_search(query)` — increment a query's popularity so future suggestions adapt.
4. Ranking is a **Strategy** (pure frequency now; pluggable to recency-weighted / personalized later) without rewriting the trie.
5. Prefix lookup should be **efficient**: walk the trie to the prefix node, then gather top-K — don't scan all words.

## Non-functional / constraints
- `suggest` should not be O(total words). Aim for O(len(prefix) + cost of top-K gather). Consider **caching top-K at each trie node** (the senior optimization) vs. a bounded DFS + heap — discuss the trade-off (write speed vs read speed).
- Memory: a node-level cache costs memory; note the trade-off.
- (Senior bonus) **Thread-safety** if reads and `record_search` writes happen concurrently (read-write lock).
- Case/normalization policy stated (lowercase? trim?).

## Driver scenario (your `main()` should show this)
1. Seed: {"apple":50, "app":80, "application":30, "apply":40, "banana":60}.
2. `suggest("app", 3)` → `["app", "apple", "apply"]` (by weight, then lexicographic).
3. `record_search("application")` several times → it climbs the ranking.
4. `suggest("app", 3)` again → ranking reflects the updated popularity.
5. `suggest("xyz", 3)` → empty list.

## Edge cases to handle
- Prefix not present → empty. · K larger than available completions. · Empty prefix (top-K overall? state your rule). · Ties broken deterministically. · A word that is itself a prefix of others (e.g. "app").

## TODO checklist
- [ ] `TrieNode` / `Trie` with insert + prefix navigation
- [ ] `RankingStrategy` interface (frequency now; extensible)
- [ ] `suggest(prefix, k)` via bounded gather + heap (or cached top-K per node)
- [ ] `record_search` updating weights (and any cached ranks)
- [ ] Normalization + deterministic tie-break
- [ ] `main()` driver covering the scenario above
