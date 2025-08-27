import copy

# Algo v1
buffer_block_period = 20001333
analog_sample_period = 2000
analog_sample_steps = 10000
compensation_steps = 1333
compensation_distance = 7

analog_sample_index = 0
compensation_dist_count = 0

for _ in range(analog_sample_steps):
    value = copy.deepcopy(analog_sample_index)
    value = value + analog_sample_period
    compensation_dist_count += 1

    if (compensation_dist_count >= compensation_distance) and (compensation_steps > 0):
        value += 1
        compensation_steps -= 1
        compensation_dist_count = 0

    if value > buffer_block_period:
        print(f"Value={value}, bigger than {buffer_block_period}")
        value = buffer_block_period

    analog_sample_index = value

print(f"Final value = {analog_sample_index}, expected = {buffer_block_period}")

# Algo v2
buffer_block_period = 20001333
analog_sample_period = 2000
analog_sample_steps = 10000
compensation_steps = 1333
compensation_increment = 1333
analog_sample_index = 0
compensation_counter = 0

for _ in range(analog_sample_steps):
    value = copy.deepcopy(analog_sample_index)
    value = value + analog_sample_period
    compensation_counter += compensation_increment

    if (compensation_counter >= analog_sample_steps) and (compensation_steps > 0):
        value += 1
        compensation_steps -= 1
        compensation_counter -= analog_sample_steps

    if value > buffer_block_period:
        print(f"Value={value}, bigger than {buffer_block_period}")
        value = buffer_block_period

    analog_sample_index = value

print(f"Final value = {analog_sample_index}, expected = {buffer_block_period}")
