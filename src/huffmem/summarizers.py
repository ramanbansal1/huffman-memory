import re
from collections import Counter
from .text import tokens


def extractive_summary(a: str, b: str, limit: int = 160) -> str:
    """Offline default: first clause of each memory plus shared keywords."""
    first = lambda s: re.split(r"[.;\n]", s.strip(), maxsplit=1)[0].strip()
    top = [w for w, _ in Counter(tokens(a) + tokens(b)).most_common(4)]
    out = f"{first(a)}; {first(b)} [{', '.join(top)}]"
    return out if len(out) <= limit else out[: limit - 1] + "…"


def llm_summary(a: str, b: str) -> str:
    """Optional: needs `pip install anthropic` and ANTHROPIC_API_KEY."""
    import anthropic
    r = anthropic.Anthropic().messages.create(
        model="claude-haiku-5-5", max_tokens=120,
        messages=[{"role": "user", "content":
                   f"Merge into one dense sentence; keep names, numbers, decisions.\n1) {a}\n2) {b}"}])
    return r.content[0].text.strip()
