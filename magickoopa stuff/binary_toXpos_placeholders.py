import re

def load_rng_file(file_path):
    """
    Loads the contents of the RNG file and returns it as a list of tuples.
    Each tuple contains the X index and the corresponding value.
    """
    rng_data = []
    with open(file_path, 'r') as file:
        for line in file:
            match = re.match(r"X(\d+):\s*(\d+)\s*(\d)", line.strip())
            if match:
                index = int(match.group(1))  # The X index (e.g., X53)
                value = int(match.group(2))  # The first value (e.g., 994764101)
                rng_data.append((index, value))  # Append tuple (index, value)
    return rng_data

def match_sequence(rng_data, pattern):
    """
    Matches a user-defined pattern with the values from rng_data.
    The pattern may contain '?' as placeholders for any value.
    Returns a list of found sequences with matching values from the X positions.
    """
    matches = []
    pattern_values = [int(x) if x != '?' else '?' for x in pattern]  # Convert pattern to list of values
    print(f"Pattern to match: {pattern_values}")

    # Iterate through the rng_data and try to match the pattern
    for i in range(len(rng_data) - len(pattern_values) + 1):
        sequence_found = True
        matched_indices = []
        for j in range(len(pattern_values)):
            rng_index, rng_value = rng_data[i + j]
            if pattern_values[j] != '?' and rng_value != pattern_values[j]:
                sequence_found = False
                break
            matched_indices.append(f"X{rng_index}")

        if sequence_found:
            matches.append(''.join(matched_indices))  # Store the matched sequence
            print(f"Match found: {''.join(matched_indices)}")

    return matches

def save_matching_sequences(matches):
    """
    Saves the found matching sequences to text files.
    Each file is named based on the matching sequence of X positions.
    """
    for match in matches:
        filename = f"{match}.txt"
        with open(filename, 'w') as file:
            file.write(match)

def main():
    # Get the pattern from user input
    pattern_input = input("Enter the output sequence with placeholders (e.g., 1?0?2??4): ").strip()

    # Load rng data from file
    rng_data = load_rng_file('rng_0to6.txt')

    # Match the pattern against the rng data
    matches = match_sequence(rng_data, pattern_input)

    if matches:
        print(f"Found {len(matches)} matching sequences.")
        save_matching_sequences(matches)
    else:
        print("No matching sequences found.")

if __name__ == "__main__":
    main()
