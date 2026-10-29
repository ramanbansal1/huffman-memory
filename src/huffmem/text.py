import re

STOP = set("a an the and or of to in on for with is are was were be it this that at by as from i my we you your our".split())


def tokens(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9']+", s.lower()) if w not in STOP and len(w) > 2]
