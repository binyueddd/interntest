def mask_repeated_chars(s, k):
    output = []
    seen = {}

    for i, char in enumerate(s):
        if char in seen and i - seen[char] <= k:
            output.append('-')
        else:
            output.append(char)
        seen[char] = i

    return ''.join(output)


if __name__ == "__main__":
    s = input("Enter the string: ")
    k = int(input("Enter the number k: "))

    result = mask_repeated_chars(s, k)
    print("Output:", result)
