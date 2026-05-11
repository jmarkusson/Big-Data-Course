import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from assignment5_problem1_skeleton import murmur3_32

m = 128
seed = 0xee418b6c

file_path = "/data/courses/2026_dat471_dit066/datasets/words"

values = []

with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        word = line.strip()
        if not word:
            continue

        y = murmur3_32(word, seed)
        j = y & (m - 1) 

        values.append(j)

N = len(values)

# Frequency
freq = Counter(values)
counts = [freq[i] for i in range(m)]

# Stats
mean = np.mean(values)
std = np.std(values)

# Collisions
collisions = sum(n * (n - 1) // 2 for n in counts)
total_pairs = N * (N - 1) // 2
collision_prob = collisions / total_pairs

# ---- PRINT NICE OUTPUT ----
print("=" * 50)
print("MurmurHash Evaluation (m = 128)")
print("=" * 50)

print(f"Total keys: {N}")
print(f"Seed: {hex(seed)}")

print("\n--- Distribution Statistics ---")
print(f"Mean: {mean:.4f}")
print(f"Standard deviation: {std:.4f}")

print("\n--- Collision Statistics ---")
print(f"Total pairs: {total_pairs}")
print(f"Total collisions: {collisions}")
print(f"Collision probability: {collision_prob:.6f}")

print("=" * 50)

# ---- SAVE HISTOGRAM ----
plt.figure(figsize=(10,5))
plt.bar(range(m), counts)
plt.title("Hash distribution (m = 128)")
plt.xlabel("Bucket")
plt.ylabel("Frequency")

plt.savefig("histogram.png")