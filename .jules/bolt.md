## 2025-02-14 - NumPy Append vs List Append Optimization
**Learning:** Optimizing `np.append` in loops to list accumulation (followed by `np.array`) only yields measurable performance gains when the loop iteration count is large (>100s). In `paddlenlp/metrics/chunk.py`, the loop over entity types was too small (3-10 iterations) for the overhead of `np.append` to be significant compared to the rest of the function logic.
**Action:** Before optimizing loop operations, profile or estimate the typical loop iteration count. Focus on inner loops or loops over data samples rather than loops over configuration/classes.

## 2025-02-14 - Memory Bottleneck in Masking
**Learning:** `np.expand_dims(mask, axis).repeat(vocab_size, axis)` is a severe memory and performance anti-pattern found in `paddlenlp/metrics/utils.py`. It explicitly allocates memory for the repeated mask (batch * seq * vocab).
**Action:** Always replace `repeat` based masking with NumPy broadcasting (`output * mask_expanded`) where possible. This saved ~2.5x runtime and significant memory.
