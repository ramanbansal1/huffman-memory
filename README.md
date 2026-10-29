# huffman-memory

A memory store with a **fixed number of slots**, built on Huffman-style merging.
Each memory is keyed by its **timestamp**. When a `put` overflows the store, the two
lowest keys (the two **oldest** memories) are merged into one summary node and pushed back in.
Merged nodes keep their children, so the history is a real tree and can be searched later.

```python
from huffmem import HuffmanMemory

mem = HuffmanMemory(capacity=4)
mem.put("Training the VLA on Kaggle T4 GPUs; batch size 8.")
...
mem.get("kaggle")                       # live slots only
mem.get("kaggle", history=True)         # also the originals inside merged nodes
mem.recall(r"batch size \d+")           # regex over the full history
mem.between(t0, t1)                     # originals by timestamp range
```

Parent key = `max(child timestamps)` (not the sum), so old strata keep compacting while recent memories stay verbatim.

## Layout
```
src/huffmem/   core (node, store, search, summarizers, text, tree)
tests/         pytest suite
examples/      runnable demo
web/           static web demo (index.html, JS port of the core; GitHub Pages ready)
```

## Use
```bash
pip install -e ".[dev]"      # add ,llm for the Claude summarizer
pytest
python examples/demo.py
```
Swap the summarizer: `HuffmanMemory(5, summarizer=llm_summary)` (needs `ANTHROPIC_API_KEY`).
