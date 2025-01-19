import os
# 0s at the start and 1 gaps at the end of the list
def find_consecutive_gaps(binary_sequence):
    gaps = {0: [], 1: []}
    current_value = binary_sequence[0]
    current_length = 1
    start_pos = 0

    for i in range(1, len(binary_sequence)):
        if binary_sequence[i] == current_value:
            current_length += 1
        else:
            gaps[current_value].append((current_length, start_pos))
            current_value = binary_sequence[i]
            current_length = 1
            start_pos = i
    gaps[current_value].append((current_length, start_pos))
    return gaps

def save_gaps_to_file(gaps, filename):
    """Save the gaps to a text file with their lengths and start positions."""
    with open(filename, 'w') as file:
        file.write("Gaps of 0s and 1s (Length, Start Position, Gap Type):\n")
        for gap_type, gap_list in gaps.items():
            for length, start_pos in gap_list:
                gap_type_str = '1' if gap_type == 1 else '0'
                file.write(f"Gap Type: {gap_type_str}, Length: {length}, Start Position: X{start_pos + 1}\n")

def main():
    # our rng_values_corrected.txt is required.
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

    gaps = find_consecutive_gaps(binary_sequence)
    
    sorted_gaps = sorted(gaps[0] + gaps[1], key=lambda x: x[0], reverse=True)
    
    # Ensure a minimum of 5 gaps are selected, but we can have more
    minimum_gaps = 5
    top_gaps = sorted_gaps[:minimum_gaps]  # At least 5 gaps, more if available

    # Output the most gaps to a file
    save_gaps_to_file(gaps, 'most_gaps.txt')

    print("Pattern files have been saved.")

if __name__ == "__main__":
    main()
