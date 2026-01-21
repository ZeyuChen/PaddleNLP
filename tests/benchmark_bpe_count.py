
import timeit

def bpe_original(word, first, second):
    new_word = []
    i = 0
    while i < len(word):
        try:
            j = word.index(first, i)
            new_word.extend(word[i:j])
            i = j
        except ValueError:
            new_word.extend(word[i:])
            break

        if word[i] == first and i < len(word) - 1 and word[i + 1] == second:
            new_word.append(first + second)
            i += 2
        else:
            new_word.append(word[i])
            i += 1
    return tuple(new_word)

def bpe_count(word, first, second):
    new_word = []
    i = 0
    # count is O(N) in C. Fast.
    # Note: 'word' is a tuple. tuple.count is fast.
    c = word.count(first)

    for _ in range(c):
        # We know first is present c times.
        # So index will succeed c times.
        j = word.index(first, i)
        new_word.extend(word[i:j])
        i = j

        if i < len(word) - 1 and word[i+1] == second:
            new_word.append(first + second)
            i += 2
        else:
            new_word.append(word[i])
            i += 1

    new_word.extend(word[i:])
    return tuple(new_word)

def benchmark():
    word1 = tuple("banana")
    first1, second1 = "a", "n"

    word2 = tuple("unconstitutionally")
    first2, second2 = "t", "i"

    word3 = tuple("a" + "b"*1000)
    first3, second3 = "a", "c"

    print("Benchmarking...")

    t1_orig = timeit.timeit(lambda: bpe_original(word1, first1, second1), number=100000)
    t1_cnt = timeit.timeit(lambda: bpe_count(word1, first1, second1), number=100000)
    print(f"Test 1 (Short): Original={t1_orig:.4f}, Count={t1_cnt:.4f}")

    t2_orig = timeit.timeit(lambda: bpe_original(word2, first2, second2), number=100000)
    t2_cnt = timeit.timeit(lambda: bpe_count(word2, first2, second2), number=100000)
    print(f"Test 2 (Long): Original={t2_orig:.4f}, Count={t2_cnt:.4f}")

    t3_orig = timeit.timeit(lambda: bpe_original(word3, first3, second3), number=1000)
    t3_cnt = timeit.timeit(lambda: bpe_count(word3, first3, second3), number=1000)
    print(f"Test 3 (Very Long): Original={t3_orig:.4f}, Count={t3_cnt:.4f}")

    assert bpe_original(word1, first1, second1) == bpe_count(word1, first1, second1)
    assert bpe_original(word2, first2, second2) == bpe_count(word2, first2, second2)
    assert bpe_original(word3, first3, second3) == bpe_count(word3, first3, second3)

if __name__ == "__main__":
    benchmark()
