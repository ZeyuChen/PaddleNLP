
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

def bpe_iterative(word, first, second):
    new_word = []
    i = 0
    while i < len(word):
        if i < len(word) - 1 and word[i] == first and word[i+1] == second:
            new_word.append(first + second)
            i += 2
        else:
            new_word.append(word[i])
            i += 1
    return tuple(new_word)

def benchmark():
    word3 = tuple("a" + "b"*1000)
    first3, second3 = "a", "c"

    print("Benchmarking...")

    t3_orig = timeit.timeit(lambda: bpe_original(word3, first3, second3), number=1000)
    t3_iter = timeit.timeit(lambda: bpe_iterative(word3, first3, second3), number=1000)
    print(f"Test 3 (Very Long): Original={t3_orig:.4f}, Iterative={t3_iter:.4f}")

if __name__ == "__main__":
    benchmark()
