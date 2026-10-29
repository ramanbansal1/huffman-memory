from huffmem import HuffmanMemory, render

mem = HuffmanMemory(capacity=4)
for i, t in enumerate([
    "User prefers concise technical answers.",
    "Training the VLA on Kaggle T4 GPUs; batch size 8.",
    "Deadline for the lab application is Friday.",
    "Switched optimizer from AdamW to Sep-CMA-ES.",
    "MobileCLIP embeddings precomputed for all frames.",
    "Drone transport env uses PyBullet with 4 drones.",
]):
    mem.put(t, ts=1000 + i * 60)

print("store:")
for n in mem.all():
    print(f"  [{n.ts:.0f}] ({n.leaves} leaves) {n.text}")

print("\nget('kaggle')  -> live slots only, the original was compacted away:")
for h in mem.get("kaggle", 1):
    print("  ", h.node.text)

print("\nget('kaggle', history=True) -> reaches into the tree:")
for h in mem.get("kaggle", 1, history=True):
    print("  ", h.node.text, "| archived:", h.archived)

print("\nrecall(r'batch size \\d+') regex over full history:")
for h in mem.recall(r"batch size \d+"):
    print("  ", h.node.text, "| now inside slot", f"[{h.live.ts:.0f}]")

print("\nbetween(1000, 1100):")
for h in mem.between(1000, 1100):
    print("  ", h.node.text)

print("\ntree of oldest slot:\n" + render(mem.all()[0]))
