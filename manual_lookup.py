import os

def find_pattern_in_sequence(binary_sequence, pattern):
    """Find all positions where the given pattern appears in the binary sequence."""
    pattern_length = len(pattern)
    found_positions = []

    for i in range(len(binary_sequence) - pattern_length + 1):
        if binary_sequence[i:i + pattern_length] == pattern:
            found_positions.append(i)

    return found_positions

def main():
    input_file = 'rng_values_corrected.txt'
    if not os.path.exists(input_file):
        print(f"{input_file} does not exist. Please ensure the RNG data file is present.")
        return

    with open(input_file, 'r') as file:
        binary_sequence = []
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                parts = line.split(':')
                if len(parts) == 2:
                    value = parts[1].strip().split()[1]
                    binary_sequence.append(int(value))
                else:
                    print(f"Skipping invalid line format: {line}")
                    continue
            except ValueError:
                print(f"Skipping invalid line: {line}")
                continue

    if not binary_sequence:
        print("No valid data found in the input file.")
        return

    pattern_input = input("Enter the binary pattern (e.g., 0101011): ")
    try:
        pattern = [int(char) for char in pattern_input if char in '01']
    except ValueError:
        print("Invalid input. Please enter only 0s and 1s.")
        return

    found_positions = find_pattern_in_sequence(binary_sequence, pattern)

    if found_positions:
        with open('pattern_found_positions.txt', 'w') as file:
            file.write(f"Found pattern: {pattern_input}\n")
            file.write(f"Pattern found at the following X positions (0-based index adjusted):\n")
            for pos in found_positions:
                file.write(f"X{pos}\n")
        print(f"Pattern found and saved to 'pattern_found_positions.txt'.")
    else:
        print(f"The pattern '{pattern_input}' was not found in the sequence.")

if __name__ == "__main__":
    main()
