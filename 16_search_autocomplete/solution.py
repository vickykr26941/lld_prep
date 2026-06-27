"""
Problem 16: Search Autocomplete / Typeahead
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

suggest() should NOT scan all words: walk to the prefix node, then gather top-K.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

# ============================================================
# TODO 1: RankingStrategy — compare/score candidates (frequency now; pluggable).
# ============================================================
class RankingStrategy(ABC):
    @abstractmethod
    def key(self, word: str, weight: int):  # sort key for ranking
        ...


# ============================================================
# TODO 2: TrieNode / Trie — insert(word, weight), navigate to a prefix node.
#         (Optional senior opt: cache top-K completions at each node.)
# ============================================================


# ============================================================
# TODO 3: Autocomplete service
#         - add_word(word, weight)
#         - suggest(prefix, k) -> top-K ranked completions
#         - record_search(query) -> bump popularity (update caches if any)
# ============================================================
class Autocomplete:
    def __init__(self, ranking: RankingStrategy) -> None:
        raise NotImplementedError

    def add_word(self, word: str, weight: int) -> None:
        raise NotImplementedError

    def suggest(self, prefix: str, k: int) -> List[str]:
        raise NotImplementedError

    def record_search(self, query: str) -> None:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Seed words, suggest by prefix, bump popularity, re-suggest.")


if __name__ == "__main__":
    main()
