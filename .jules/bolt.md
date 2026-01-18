## 2025-02-18 - Avoid np.append in loops
**Learning:** Using `np.append` repeatedly inside a loop is a performance killer (O(N^2)). It creates a new copy of the array for every iteration.
**Action:** Accumulate results in a Python list and convert to a NumPy array once at the end using `np.array(list)`.
