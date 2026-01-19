## 2024-05-22 - Testing in Broken Environments
**Learning:** `paddlenlp` modules have tightly coupled imports in `__init__.py`. Validating individual files requires bypassing package initialization using `importlib` and mocking `paddle` modules when the full environment is not available (e.g. missing `paddle.fluid`).
**Action:** Use `importlib` and `sys.modules` mocking to isolate components for testing and benchmarking.
