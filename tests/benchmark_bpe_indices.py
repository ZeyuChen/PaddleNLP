
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

def bpe_indices(word, first, second):
    indices = [k for k, x in enumerate(word) if x == first]
    new_word = []
    i = 0
    for idx in indices:
        if idx < i:
            continue

        # Append everything before match
        new_word.extend(word[i:idx])
        i = idx

        # Check merge
        if i < len(word) - 1 and word[i+1] == second:
            new_word.append(first + second)
            i += 2
        else:
            new_word.append(word[i])
            i += 1

    new_word.extend(word[i:])
    return tuple(new_word)

def benchmark():
    # Test cases
    # 1. Short word, frequent match
    word1 = tuple("banana")
    first1, second1 = "a", "n"

    # 2. Long word, sparse match (end)
    word2 = tuple("unconstitutionally")
    first2, second2 = "t", "i"

    # 3. Very long word, sparse match
    word3 = tuple("a" + "b"*1000)
    first3, second3 = "a", "c" # No merge, but 'a' is found at 0.

    print("Benchmarking...")

    t1_orig = timeit.timeit(lambda: bpe_original(word1, first1, second1), number=100000)
    t1_ind = timeit.timeit(lambda: bpe_indices(word1, first1, second1), number=100000)
    print(f"Test 1 (Short): Original={t1_orig:.4f}, Indices={t1_ind:.4f}")

    t2_orig = timeit.timeit(lambda: bpe_original(word2, first2, second2), number=100000)
    t2_ind = timeit.timeit(lambda: bpe_indices(word2, first2, second2), number=100000)
    print(f"Test 2 (Long): Original={t2_orig:.4f}, Indices={t2_ind:.4f}")

    t3_orig = timeit.timeit(lambda: bpe_original(word3, first3, second3), number=1000)
    t3_ind = timeit.timeit(lambda: bpe_indices(word3, first3, second3), number=1000)
    print(f"Test 3 (Very Long): Original={t3_orig:.4f}, Indices={t3_ind:.4f}")

    assert bpe_original(word1, first1, second1) == bpe_indices(word1, first1, second1)
    assert bpe_original(word2, first2, second2) == bpe_indices(word2, first2, second2)
    assert bpe_original(word3, first3, second3) == bpe_indices(word3, first3, second3)

if __name__ == "__main__":
    benchmark()
