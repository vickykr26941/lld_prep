"""
Problem 17: In-Memory File System
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Composite tree (File/Directory share a Node interface). One central path resolver.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

# ============================================================
# TODO 1: Node base + File and Directory (Composite).
#         Shared interface: name, size(), maybe mtime. Directory holds children.
# ============================================================
class Node(ABC):
    @abstractmethod
    def size(self) -> int:
        ...


# ============================================================
# TODO 2: Path resolver — ONE place that splits a path and walks the tree,
#         handling '/', '.', '..', trailing slashes, and root clamping.
# ============================================================


# ============================================================
# TODO 3: FileSystem facade
#         - mkdir(path)  (mkdir -p)
#         - ls(path)     (sorted children, or file name)
#         - add_file / read_file / append
#         - rm / mv / cp  with clear errors
#         - metadata via injectable clock
# ============================================================
class FileSystem:
    def __init__(self, clock=None) -> None:
        raise NotImplementedError

    def mkdir(self, path: str) -> None:
        raise NotImplementedError

    def ls(self, path: str) -> List[str]:
        raise NotImplementedError

    def add_file(self, path: str, content: str) -> None:
        raise NotImplementedError

    def read_file(self, path: str) -> str:
        raise NotImplementedError


def main() -> None:
    """Driver — see README 'Driver scenario'. TODO: implement."""
    raise NotImplementedError("Run mkdir -p, file IO, ls, mv, rm, and a '..' resolution.")


if __name__ == "__main__":
    main()
