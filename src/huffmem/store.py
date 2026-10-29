import heapq, itertools, time
from typing import Callable, Optional
from .node import Node
from .summarizers import extractive_summary
from . import search

_ids = itertools.count(1)


class HuffmanMemory:
    """Fixed-capacity store. Overflow merges the two lowest keys (= two oldest timestamps)."""

    def __init__(self, capacity: int = 5, summarizer: Callable[[str, str], str] = extractive_summary):
        assert capacity >= 1
        self.capacity, self.summarize, self._heap = capacity, summarizer, []

    def put(self, text: str, ts: Optional[float] = None) -> list[Node]:
        heapq.heappush(self._heap, Node(ts or time.time(), next(_ids), text))
        return self.shrink()

    def shrink(self) -> list[Node]:
        merged = []
        while len(self._heap) > self.capacity and len(self._heap) >= 2:
            a, b = heapq.heappop(self._heap), heapq.heappop(self._heap)
            # parent key = max(child ts): old strata keep compacting, recent ones stay verbatim
            m = Node(max(a.ts, b.ts), next(_ids), self.summarize(a.text, b.text), (a, b))
            heapq.heappush(self._heap, m)
            merged.append(m)
        return merged

    def all(self) -> list[Node]:
        return sorted(self._heap)

    def __len__(self):
        return len(self._heap)

    # ---- retrieval (see search.py) ----
    def get(self, query: str, k: int = 3, history: bool = False):
        return search.rank(self._heap, query, k, history)

    def recall(self, pattern: str, regex: bool = True, k: int = 10):
        """Search the FULL history (original memories inside the tree) by regex or keyword."""
        return search.recall(self._heap, pattern, regex, k)

    def between(self, t0: float, t1: float):
        """Original memories whose timestamp falls in [t0, t1]."""
        return search.between(self._heap, t0, t1)
