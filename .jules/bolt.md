## 2024-05-22 - Performance Verification in Broken Environment
**Learning:** When the environment is broken (e.g. missing dependencies like `paddle.fluid`), full test suites cannot run. Verification of performance optimizations must be done via isolated reproduction scripts that mock or avoid the broken parts.
**Action:** Create standalone scripts to verify logic and performance, but ensure they are not committed to the repository.

## 2024-05-22 - Numpy Array Accumulation
**Learning:** `np.append` in a loop is O(N^2). Replacing with list append and single conversion is O(N). This provided ~55% speedup in `paddlenlp/metrics/chunk.py`.
**Action:** Always look for `np.append` inside loops and replace with list accumulation.
