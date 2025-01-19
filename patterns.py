import os

def find_consecutive_gaps(binary_sequence):
    """Find the gaps of consecutive 0s and 1s in the binary sequence."""
    gaps = {0: [], 1: []}  # Using integers for the keys
    current_value = binary_sequence[0]
    current_length = 1
    start_pos = 0

    # Iterate through the sequence
    for i in range(1, len(binary_sequence)):
        if binary_sequence[i] == current_value:
            current_length += 1
        else:
            gaps[current_value].append((current_length, start_pos))
            current_value = binary_sequence[i]
            current_length = 1
            start_pos = i
    # Add the last sequence
    gaps[current_value].append((current_length, start_pos))
    return gaps

def find_alternating_patterns(binary_sequence, start_value):
    """Find the longest alternating 1-0 or 0-1 patterns, including X positions."""
    max_pattern = []
    current_pattern = [start_value]
    start_pos = None
    
    for i in range(1, len(binary_sequence)):
        if binary_sequence[i] != binary_sequence[i-1]:
            if not current_pattern:
                start_pos = i - 1  # We mark the start position when an alternating pattern begins
            current_pattern.append(binary_sequence[i])
        else:
            if current_pattern:
                max_pattern.append((len(current_pattern), start_pos))
            current_pattern = [binary_sequence[i]]
            start_pos = i  # Set the new start position for the next sequence
    
    # Add the last pattern if available
    if current_pattern:
        max_pattern.append((len(current_pattern), start_pos))
    
    # Make sure no None start_pos is left
    return [(length, pos if pos is not None else 0) for length, pos in max_pattern]

def main():
    # Read the previous RNG file to get the sequence of 0s and 1s
    input_file = 'rng_values_corrected.txt'
    if not os.path.exists(input_file):
        print(f"{input_file} does not exist. Please ensure the RNG data file is present.")
        return

    with open(input_file, 'r') as file:
        binary_sequence = []
        for line in file:
            # Strip any extra whitespace and skip empty lines
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            try:
                # Extract the bounce direction (last value after the colon)
                parts = line.split(':')  # Split by colon
                if len(parts) == 2:
                    value = parts[1].strip().split()[1]  # Extract the second value (0 or 1)
                    binary_sequence.append(int(value))  # Ensure this is an integer
                else:
                    print(f"Skipping invalid line format: {line}")
                    continue
            except ValueError:
                print(f"Skipping invalid line: {line}")
                continue

    # Check if binary_sequence is empty
    if not binary_sequence:
        print("No valid data found in the input file.")
        return

    # Generate most_gaps.txt
    gaps = find_consecutive_gaps(binary_sequence)
    
    # Sort the gaps by length and select the top 5
    sorted_gaps = sorted(gaps[0] + gaps[1], key=lambda x: x[0], reverse=True)[:5]

    with open('most_gaps.txt', 'w') as file:
        file.write("Top 5 longest gaps of 0s or 1s (Length, Start Position):\n")
        for gap in sorted_gaps:
            length, start_pos = gap
            file.write(f"Length: {length}, Start Position: X{start_pos + 1}\n")  # Add 1 for 1-based index

    # Generate every_other_1.txt (alternating starting with 1)
    alternating_1 = find_alternating_patterns(binary_sequence, 1)

    with open('every_other_1.txt', 'w') as file:
        file.write("Longest alternating pattern starting with 1 (Length, Start Position):\n")
        for pattern in alternating_1:
            length, start_pos = pattern
            file.write(f"Length: {length}, Start Position: X{start_pos + 1}\n")

    # Generate every_other_0.txt (alternating starting with 0)
    alternating_0 = find_alternating_patterns(binary_sequence, 0)

    with open('every_other_0.txt', 'w') as file:
        file.write("Longest alternating pattern starting with 0 (Length, Start Position):\n")
        for pattern in alternating_0:
            length, start_pos = pattern
            file.write(f"Length: {length}, Start Position: X{start_pos + 1}\n")

    print("Pattern files have been saved.")

if __name__ == "__main__":
    main()
