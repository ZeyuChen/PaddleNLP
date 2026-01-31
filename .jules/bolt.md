# Bolt's Journal

## 2024-05-22 - [Initialization]
**Learning:** Initialized Bolt's journal.
**Action:** Record critical performance learnings here.

## 2024-05-22 - [NumPy Append Anti-pattern]
**Learning:** `np.append` inside a loop leads to quadratic complexity because it copies the array on every iteration.
**Action:** Use list accumulation and convert to NumPy array at the end. In `paddlenlp/metrics/chunk.py`, this yielded a ~13.5x speedup for the accumulation loop with 5000 types.
