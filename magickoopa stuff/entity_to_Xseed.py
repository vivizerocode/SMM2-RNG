import os


def read_numbers_with_prefix(file_path):
    """Reads prefixed numbers from a file and returns them as a list of tuples (prefix, number)."""
    with open(file_path, 'r') as file:
        lines = [line.strip().split(": ") for line in file]
    return [(prefix, number) for prefix, number in lines]



def number_to_entity(number):
    """Maps numbers back to their respective entity names."""
    mapping = {
        '0': 'Goomba',
        '1': 'Green Koopa',
        '2': 'Red Koopa',
        '3': 'Buzzy Beetle',
        '4': 'Spiny',
        '5': 'Mushroom',
        '6': 'Coin'
    }
    return mapping[number]

def entity_to_number(entity):
    """Maps entity names to their respective numbers."""
    mapping = {
        'Goomba': '0',
        'Green Koopa': '1',
        'Red Koopa': '2',
        'Buzzy Beetle': '3',
        'Spiny': '4',
        'Mushroom': '5',
        'Coin': '6'
    }
    return mapping[entity]

def generate_pattern(entities):
    """Generates a pattern with wildcards based on input entities."""
    pattern = ""
    for entity in entities:
        number = entity_to_number(entity)
        wildcards = '?' * (7 if entity == "Coin" else 6)
        pattern += number + wildcards
    return pattern.rstrip('?')


def match_pattern_with_predictions(numbers, pattern):
    """Finds matches for the pattern and predicts the next entities."""
    pattern_length = len(pattern)
    matches = []
    
    for i in range(len(numbers) - pattern_length + 1):
        if all(pattern[j] == '?' or pattern[j] == numbers[i + j] for j in range(pattern_length)):
            start_prefix = f"X{i}"
            end_prefix = f"X{i + pattern_length - 1}"
            predictions = predict_next_entities(numbers, i + pattern_length - 1)
            matches.append((start_prefix, end_prefix, predictions))
    
    return matches




def predict_next_entities(numbers, start_index, entities_count=10):
    """Predicts the next entities based on the end of the found pattern."""
    predictions = []
    index = start_index + 1  # Start right after the last matched entity

    while len(predictions) < entities_count and index < len(numbers):
        # Determine how many entities to "not care" for, based on the current entity
        if numbers[index] == '6':  # If it's a Coin
            index += 8  # Skip 7 numbers, check the 8th
        else:  # For all other entities
            index += 7  # Skip 6 numbers, check the 7th

        if index < len(numbers):
            entity = numbers[index]
            predictions.append(entity)

    return [number_to_entity(num) for num in predictions]

def main():
    file_path = 'rng_0to6.txt'
    output_file = 'nums_found_with_predictions.txt'
    entity_sequence = input("Enter the sequence (e.g., 'Mushroom, Red Koopa, Coin, Coin'): ").strip().split(", ")
    
    pattern = generate_pattern(entity_sequence)
    print(f"Translating, looking for pattern: {pattern}")
    
    numbers_with_prefix = read_numbers_with_prefix(file_path)
    numbers = [num for _, num in numbers_with_prefix]
    
    matching_results = match_pattern_with_predictions(numbers, pattern)
    
    if matching_results:
        with open(output_file, 'w') as file:
            for start, end, predictions in matching_results:
                prediction_entities = ', '.join(predictions)
                file.write(f"Pattern found from {start} to {end}. Next 10 entities: {prediction_entities}\n")
        
        print(f"Pattern found (saved to {output_file}):")
        for start, end, predictions in matching_results:
            prediction_entities = ', '.join(predictions)
            print(f"From {start} to {end}. Next 10 entities: {prediction_entities}")
    else:
        print("Pattern not found.")

if __name__ == "__main__":
    main()
