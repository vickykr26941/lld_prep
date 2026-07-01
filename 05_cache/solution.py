"""
Problem 05: In-Memory Cache (LRU / LFU)
Read README.md first. Implement YOUR design below — the skeleton is only TODOs.

Hot path must be O(1) — no linear scans.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional
import heapq

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class EvictionPolicy(ABC):
    @abstractmethod
    def evict(self):
        ...
        
class LRUCache(EvictionPolicy):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

        self._node_to_remove = None


    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_tail(self, node):
        node.prev  = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]

        self._node_to_remove = node
        self.evict()
        self._insert_tail(node)
        return node.value

    def put(self, key, value) -> None:
        if key in self.cache:
            self._node_to_remove = self.cache[key]
            self.evict()

        node = Node(key, value)
        self._insert_tail(node)
        self.cache[key] = node

        if len(self.cache) > self.capacity:
            lru_node = self.head.next

            self._node_to_remove = lru_node
            self._remove(lru_node)
            del self.cache[lru_node.key]

    def evict(self):
        if self._node_to_remove:
            self._remove(self._node_to_remove)
            del self.cache[self._node_to_remove.key]
        self._node_to_remove = None


class LFUCache(EvictionPolicy):
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.freq_map = {}
        self.pq = []

        self._tick = 0

    def _touch(self, key):
        self._tick += 1
        self.freq_map[key] += 1

        heapq.heappush(self.pq, (self.freq_map[key], self._tick, key))
    

    def get(self, key):
        if key not in self.cache:
            return -1
        
        self._touch(key)
        return self.cache[key]
    
    def put(self, key, value) -> None:
        if key in self.cache:
            self.cache[key] = value
            self._touch(key=key)
            return
        
        if len(self.cache) >= self.capacity:
            self.evict()
        
        self.cache[key] = value
        self.freq_map[key] = 1
        self._tick += 1
        heapq.heappush(self.pq, (self.freq_map[key], self._tick, key))

    def evict(self):
        while self.pq:
            freq, tick, key = heapq.heappop(self.pq)
            if key in self.cache and self.freq_map[key] == freq:
                del self.cache[key]
                del self.freq_map[key]
                break
            
class Cache:
    def __init__(self, capacity: int, policy: EvictionPolicy) -> None:
        self.capacity = capacity
        self.policy = policy
        self.policy.capacity = capacity

    def get(self, key) -> Optional[object]:
       return self.policy.get(key)

    def put(self, key, value) -> None:
        self.policy.put(key, value)

def main() -> None:
    
    lru_cache = Cache(capacity=2, policy=LRUCache(capacity=2))
    lru_cache.put(1, 1)
    lru_cache.put(2, 2)
    print(lru_cache.get(1)) 
    lru_cache.put(3, 3)      
    print(lru_cache.get(2)) 
    lru_cache.put(4, 4)    
    print(lru_cache.get(1))  
    print(lru_cache.get(3)) 
    print(lru_cache.get(4)) 

    lfu_cache = Cache(capacity=2, policy=LFUCache(capacity=2))
    lfu_cache.put(1, 1)
    lfu_cache.put(2, 2)
    print(lfu_cache.get(1)) 
    lfu_cache.put(3, 3)     
    print(lfu_cache.get(2))  
    print(lfu_cache.get(3))  
    lfu_cache.put(4, 4) 
    print(lfu_cache.get(1)) 
    print(lfu_cache.get(3)) 
    print(lfu_cache.get(4))


if __name__ == "__main__":
    main()
