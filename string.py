def replace_repeated_chars():
    while True:
        s = input("Input (or type 'exit' to quit): ")

        if s.lower() == 'exit':
            print("Exiting...")
            break

        output = []
        seen = set()

        for char in s:
            if char in seen:
                output.append('-')
            else:
                output.append(char)
                seen.add(char)

        print('Output:', ''.join(output))

replace_repeated_chars()
