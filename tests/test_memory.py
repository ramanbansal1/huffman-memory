from huffmem import HuffmanMemory

TEXTS = ["alpha one", "beta two kaggle", "gamma three", "delta four", "epsilon five"]


def fresh(cap=3):
    m = HuffmanMemory(cap)
    for i, t in enumerate(TEXTS):
        m.put(t, ts=100 + i)
    return m


def test_capacity_fixed():
    assert len(fresh()) == 3


def test_merges_two_oldest():
    m = fresh()
    assert [n.leaves for n in m.all()] == [3, 1, 1]
    assert m.all()[0].ts == 102          # max of merged keys


def test_get_live_misses_archived():
    assert not any("kaggle" in h.node.text and h.node.is_leaf for h in fresh().get("kaggle", 5))


def test_get_history_finds_leaf():
    h = fresh().get("kaggle", 1, history=True)[0]
    assert h.node.text == "beta two kaggle" and h.archived


def test_recall_regex_and_between():
    m = fresh()
    assert m.recall(r"^gam+a")[0].node.text == "gamma three"
    assert [h.node.text for h in m.between(100, 101)] == ["alpha one", "beta two kaggle"]


if __name__ == "__main__":
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f()
    print("all passed")
