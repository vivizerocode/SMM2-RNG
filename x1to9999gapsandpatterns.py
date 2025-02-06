import os

# RNG function
def rng(state0, state1, state2, state3):
    temp = state0 ^ ((state0 << 11) & 4294967295)
    temp = temp ^ (temp >> 8)
    state3_new = state3 ^ (state3 >> 19) ^ temp
    return state3_new

state0 = 1
state1 = 1812433255
state2 = 1900727105
state3 = 1208447044  # This is X1 integer value

A1 = 2  # multiplier
shift_amount = 32  # shift amount for BITRSHIFT

# generating RNG values and save to file
output_file = 'rng_values_corrected.txt'
with open(output_file, 'w') as file:
    for i in range(0, 9999): # you can go higher, but doubt youd be able to set this seed lmao
        if i == 1:
            bounce_value = (state3 * A1) >> shift_amount
            bounce_direction = '1' if bounce_value & 1 else '0'
            file.write(f"X{i}: {bounce_direction}\n")
        else:
            next_state = rng(state0, state1, state2, state3)
        
            # now we apply the formula determining 0 or 1: BITRSHIFT(X!$A7 * $A$1, 32)
            bounce_value = (next_state * A1) >> shift_amount
        
            bounce_direction = '1' if bounce_value & 1 else '0'
        
            file.write(f"X{i}: {bounce_direction}\n") # next state was removed because it is so difficult to search after those nums i guess
        
            state0, state1, state2, state3 = state1, state2, state3, next_state

print(f"RNG values and directions saved to {output_file}")
