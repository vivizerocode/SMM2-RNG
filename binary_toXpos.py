import os

def convert_letter_to_binary(letter):
    """Converts a single letter to its binary representation (8 bits)."""
    if len(letter) != 1:
        raise ValueError("Please enter a single letter.")
    
    binary_rep = format(ord(letter), '08b')
    return binary_rep

def find_binary_in_sequence(binary_sequence, binary_pattern):
    """Finds all occurrences of a binary pattern in the sequence."""
    positions = []
    sequence_str = ''.join(map(str, binary_sequence))
    
    start = 0
    while True:
        start = sequence_str.find(binary_pattern, start)
        if start == -1:
            break
        positions.append(start)  # append the position
        start += 1  # move one step ahead to continue the search
    
    return positions

def save_positions_to_file(positions, letter):
    """Saves the found positions to a file."""
    output_file = f"{letter}_pattern_positions.txt"
    with open(output_file, 'w') as file:
        for pos in positions:
            file.write(f"X{pos}\n")
    print(f"Positions have been saved to {output_file}.")

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
                continue  # skip empty lines
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

    letter = input("Enter a letter to find its binary pattern: ")
    
    try:
        binary_pattern = convert_letter_to_binary(letter)
        print(f"Binary representation of '{letter}': {binary_pattern}")
    except ValueError as e:
        print(e)
        return

    positions = find_binary_in_sequence(binary_sequence, binary_pattern)

    if positions:
        print(f"The binary sequence for '{letter}' was found at the following positions (X values):")
        for pos in positions:
            print(f"X{pos}")  # offset  +1, the output is now the correct X value
        
        save_positions_to_file(positions, letter)
    else:
        print(f"The binary sequence for '{letter}' was not found in the sequence.")

if __name__ == "__main__":
    main()
