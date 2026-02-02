## 2024-05-23 - Optimizing Chinese Tokenization
**Learning:** `re.findall` with a pattern like `C|[^C]+` (where C is a character class) is significantly faster (18x on English, 3x on Mixed) than iterating char-by-char in Python for tokenization, while maintaining the same behavior.
**Action:** Use regex for tokenization tasks where we split by a set of characters, instead of Python loops. Avoid `re.split` if it creates too many empty strings; `re.findall` with a complementary pattern is often better.

## 2024-05-23 - BPE Micro-optimization
**Learning:** Attempting to optimize BPE's inner loop by replacing `try-except` with manual bounds checking or loops for short words in Python resulted in no speedup or slowdown. Python's `list.index` (implemented in C) is very fast, even with exception overhead.
**Action:** Trust built-in C-implemented methods like `index` over manual Python loops unless profiling proves otherwise.
