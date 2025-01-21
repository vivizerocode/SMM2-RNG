import os
import re

# Define the mapping for items to their corresponding numbers
item_to_number = {
    'Mushroom': 5,
    'Red Koopa': 2,
    'Coin': 6,
    'Spiny': 4,
    'Green Koopa': 1,
    'Goomba': 0,
}

# Function to create the pattern with wildcards
def create_pattern_with_wildcards(sequence):
    # Convert the sequence to numbers and insert placeholders
    numbers = [item_to_number[item.strip()] for item in sequence.split(',')]
    pattern = []
    
    for i, number in enumerate(numbers):
        pattern.append(str(number))
        if number == 6:  # Coin requires 8 skips
            pattern.append('?')  # Coin placeholder is followed by 8 '?'
        else:
            pattern.extend(['?'] * 7)  # Non-coin items get 7 placeholders

    return ''.join(pattern)

# Function to read the RNG states from the file
def read_rng_states(file_path):
    rng_states = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                state_value = int(parts[1].strip().split()[0])
                rng_states.append(state_value)
    return rng_states

# Function to find sequences in the RNG states
def find_sequences(pattern, rng_states):
    matches = []
    state_string = "".join([str(state % 8) for state in rng_states])  # Convert values to 0-7

    print(f"Looking for this in sequence: {pattern}")
    
    # Search for the pattern in the RNG states
    for i in range(len(state_string) - len(pattern) + 1):
        match = True
        x_position = i
        
        for j in range(0, len(pattern), 8):
            entity_value = pattern[j]
            skip = 7  # Default skip value for non-coin items
            
            if entity_value == '6':  # Coin case requires 8 skips
                skip = 8

            # Check if the current RNG value matches the entity
            if state_string[i + j] == entity_value:
                i += skip  # Skip forward based on the entity type (7 or 8 spaces)
            else:
                match = False
                break

        if match:
            matches.append(i)
    return matches

# Predict the next 10 values based on the current position in the RNG states
def predict_entities(start_index, rng_states, count=10):
    predicted_entities = []
    for i in range(count):
        next_index = start_index + i
        if next_index >= len(rng_states):
            break
        next_value = rng_states[next_index] % 8
        predicted_entities.append(next_value)
    return predicted_entities

# Main function to handle input and sequence matching
def main():
    input_file = 'rng_0to6.txt'
    if not os.path.exists(input_file):
        print(f"{input_file} does not exist. Please ensure the RNG data file is present.")
        return

    rng_states = read_rng_states(input_file)

    # User input for sequence
    sequence = input("Enter the sequence of items (e.g., 'Mushroom, Red Koopa, Coin, Coin, Spiny'): ")

    pattern = create_pattern_with_wildcards(sequence)
    matches = find_sequences(pattern, rng_states)

    if matches:
        output_filename = "sequence_matches.txt"
        with open(output_filename, 'w') as file:
            for match in matches:
                start_X = match
                last_X = match + len(sequence.split(',')) - 1
                sequence_entities = sequence.split(',')

                # Write the sequence of entities
                sequence_string = ", ".join([entity.strip() for entity in sequence_entities])
                file.write(f"Start X: X{start_X} | Last X: X{last_X} | Sequence: {sequence_string}\n")

                # Predict the next 10 entities
                predicted_entities = predict_entities(last_X, rng_states)
                file.write(f"Predicted next 10 entities: {', '.join(map(str, predicted_entities))}\n\n")

        print(f"Sequence positions and predictions saved to {output_filename}")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
