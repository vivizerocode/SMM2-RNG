import os



def read_numbers_with_prefix(file_path):
    """Reads prefixed numbers from a file and returns them as a list of tuples (prefix, number)."""
    with open(file_path, 'r') as file:
        lines = [line.strip().split(": ") for line in file]
    return [(prefix, number) for prefix, number in lines]



def match_pattern_with_user_input(numbers, pattern):
    """
    Finds all occurrences of a user-defined pattern with wildcards in a list of numbers.
    Returns a list of tuples (start_prefix, end_prefix).
    """
    pattern_length = len(pattern)
    matches = []
    
    for i in range(len(numbers) - pattern_length + 1):
        if all(pattern[j] == '?' or pattern[j] == numbers[i + j] for j in range(pattern_length)):
            start_prefix = f"X{i}"
            end_prefix = f"X{i + pattern_length - 1}"
            matches.append((start_prefix, end_prefix))
    
    return matches

def main():
    file_path = 'rng_0to6.txt'
    output_file = 'wildcard_matches.txt'
    
    # Ask the user to input the wildcard pattern
    pattern = input("Enter the sequence with wildcards (e.g., '6???????2??????'): ").strip()
    print(f"Looking for pattern: {pattern}")
    
    # Read the numbers from the modified file
    numbers_with_prefix = read_numbers_with_prefix(file_path)
    numbers = [num for _, num in numbers_with_prefix]
    
    # Find all matching sequences
    matching_results = match_pattern_with_user_input(numbers, pattern)
    
    if matching_results:
        # Save matches to a file
        with open(output_file, 'w') as file:
            for start, end in matching_results:
                file.write(f"Pattern found from {start} to {end}\n")
        
        # Print results to the console
        print(f"Pattern found (saved to {output_file}):")
        for start, end in matching_results:
            print(f"From {start} to {end}")
    else:
        print("Pattern not found.")

if __name__ == "__main__":
    main()
