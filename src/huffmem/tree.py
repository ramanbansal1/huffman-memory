from .node import Node


def render(n: Node, depth: int = 0) -> str:
    s = f"{'  ' * depth}[{n.ts:.0f}] {n.text}\n"
    return s + "".join(render(c, depth + 1) for c in n.children)
