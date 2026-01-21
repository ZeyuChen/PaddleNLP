
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

def bpe_hybrid(word, first, second):
    new_word = []
    i = 0
    if len(word) < 20: # Tuning threshold
        while i < len(word):
            if i < len(word) - 1 and word[i] == first and word[i+1] == second:
                new_word.append(first + second)
                i += 2
            else:
                new_word.append(word[i])
                i += 1
    else:
        while i < len(word):
            try:
                j = word.index(first, i)
                new_word.extend(word[i:j])
                i = j
            except ValueError:
                new_word.extend(word[i:])
                break

            if i < len(word) - 1 and word[i + 1] == second:
                new_word.append(first + second)
                i += 2
            else:
                new_word.append(word[i])
                i += 1

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
    t1_hyb = timeit.timeit(lambda: bpe_hybrid(word1, first1, second1), number=100000)
    print(f"Test 1 (Short): Original={t1_orig:.4f}, Hybrid={t1_hyb:.4f}")

    t2_orig = timeit.timeit(lambda: bpe_original(word2, first2, second2), number=100000)
    t2_hyb = timeit.timeit(lambda: bpe_hybrid(word2, first2, second2), number=100000)
    print(f"Test 2 (Long): Original={t2_orig:.4f}, Hybrid={t2_hyb:.4f}")

    t3_orig = timeit.timeit(lambda: bpe_original(word3, first3, second3), number=1000)
    t3_hyb = timeit.timeit(lambda: bpe_hybrid(word3, first3, second3), number=1000)
    print(f"Test 3 (Very Long): Original={t3_orig:.4f}, Hybrid={t3_hyb:.4f}")

    assert bpe_original(word1, first1, second1) == bpe_hybrid(word1, first1, second1)
    assert bpe_original(word2, first2, second2) == bpe_hybrid(word2, first2, second2)
    assert bpe_original(word3, first3, second3) == bpe_hybrid(word3, first3, second3)

if __name__ == "__main__":
    benchmark()
