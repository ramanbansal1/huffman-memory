import re
from collections import Counter
from dataclasses import dataclass
from .node import Node
from .text import tokens


@dataclass
class Hit:
    node: Node      # the matching memory (may be an original leaf)
    live: Node      # the slot currently holding it (same node if never compacted)
    score: float = 0.0

    @property
    def archived(self) -> bool:
        return self.node is not self.live


def _all(heap):
    for root in heap:
        yield from root.walk()


def _score(node: Node, q: Counter) -> float:
    t = Counter(tokens(node.text))
    return sum(min(q[w], t[w]) for w in q) / (len(q) or 1)


def rank(heap, query: str, k: int = 3, history: bool = False) -> list[Hit]:
    """Keyword ranking. history=True also scores the original leaves inside merged nodes."""
    if not heap:
        return []
    q = Counter(tokens(query))
    t0, t1 = min(n.ts for n in heap), max(n.ts for n in heap)
    pairs = _all(heap) if history else ((n, n) for n in heap)
    hits = [Hit(n, live, _score(n, q) + 0.1 * (n.ts - t0) / ((t1 - t0) or 1)) for n, live in pairs]
    hits.sort(key=lambda h: (h.score, h.node.is_leaf), reverse=True)
    return hits[:k]


def recall(heap, pattern: str, regex: bool = True, k: int = 10) -> list[Hit]:
    """Regex (or keyword) match over every node in every tree. Leaves first, newest first."""
    if regex:
        rx = re.compile(pattern, re.I)
        ok = lambda n: bool(rx.search(n.text))
    else:
        ws = set(tokens(pattern))
        ok = lambda n: bool(ws & set(tokens(n.text)))
    hits = [Hit(n, live, 1.0) for n, live in _all(heap) if ok(n)]
    hits.sort(key=lambda h: (not h.node.is_leaf, -h.node.ts))
    return hits[:k]


def between(heap, t0: float, t1: float) -> list[Hit]:
    hits = [Hit(n, live, 1.0) for n, live in _all(heap) if n.is_leaf and t0 <= n.ts <= t1]
    return sorted(hits, key=lambda h: h.node.ts)
