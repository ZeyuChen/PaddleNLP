## 2024-05-23 - BPE Tokenization Optimization
**Learning:** `try-except` blocks inside tight loops (like BPE token merging) can introduce significant overhead, especially when exceptions are raised frequently or when the loop body is very fast (short strings).
**Action:** Replace `try-except` control flow with explicit conditional checks when the condition is cheap to check and the loop iterates over Python objects. In this case, checking `word[i] == first` in a Python loop was faster than `word.index(first)` + `try-except` for the typical short token lengths encountered in BPE.
