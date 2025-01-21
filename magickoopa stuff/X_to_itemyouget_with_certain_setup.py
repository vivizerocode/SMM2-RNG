import os

def read_rng_states(file_path):
    rng_states = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            state_value = int(parts[1].strip().split()[0])
            rng_states.append(state_value)
    return rng_states

def calculate_entities_from_file(start_X, rng_states, num_entities=20):
    entity_mapping = {
        0: "Goomba",
        1: "Green Koopa",
        2: "Red Koopa",
        3: "Buzzy Beetle",
        4: "Spiny",
        5: "Mushroom",
        6: "Coin",
        7: "Unknown"
    }

    entities = []
    current_X = start_X + 1  # Start from X + 1

    for i in range(num_entities):
        state_value = rng_states[current_X]  # Use the X value directly
        bounce_direction = (state_value * 7) >> 32
        bounce_direction = bounce_direction % 8

        entity = entity_mapping[bounce_direction]
        entities.append(f"X{current_X}: {state_value} {bounce_direction} ({entity})")

        if entity == "Coin":
            current_X += 8
        else:
            current_X += 7

    return entities

if __name__ == "__main__":
    start_X = int(input("Enter your starting X value: "))
    file_path = 'rng_0to6.txt'

    rng_states = read_rng_states(file_path)
    entities = calculate_entities_from_file(start_X, rng_states)

    output_filename = f"X{start_X + 1}_to_X{start_X + 1 + 7 * 20}.txt"
    with open(output_filename, 'w') as file:
        file.write("\n".join(entities))

    print(f"\nSequence saved to {output_filename}")
