from dataclasses import dataclass, field


@dataclass(order=True)
class Node:
    """A memory. ts is the Huffman key. Merged nodes keep their children (the tree)."""
    ts: float
    id: int = field(compare=False)
    text: str = field(compare=False)
    children: tuple = field(default=(), compare=False)

    @property
    def is_leaf(self) -> bool:
        return not self.children

    @property
    def leaves(self) -> int:
        return 1 if self.is_leaf else sum(c.leaves for c in self.children)

    def walk(self, root=None):
        """Yield (node, live_root) for this node and every descendant."""
        root = root or self
        yield self, root
        for c in self.children:
            yield from c.walk(root)
