## 2024-05-22 - NumPy append anti-pattern
**Learning:** Found multiple instances of `np.append` usage inside loops, which causes quadratic complexity due to array copying. This seems to be a common pattern in this codebase.
**Action:** Always check for `np.append` in loops when looking for easy performance wins. Replace with list accumulation and single `np.array()` conversion.

## 2024-05-22 - PaddleNLP Dependency Hell
**Learning:** `paddlenlp` relies on `paddle.fluid` which is deprecated/removed in newer `paddlepaddle` versions, causing `ImportError` on package initialization.
**Action:** When testing `paddlenlp` components, avoid importing the top-level package if possible. Use `sys.modules` mocking or `importlib` to load specific modules in isolation.
