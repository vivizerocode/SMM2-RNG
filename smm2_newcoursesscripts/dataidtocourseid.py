import concurrent.futures

def data_id_to_course_id(did):
    a = 0b1000
    b = (did - 31) % 64
    c = 0
    d = 0
    e = 1
    f = 0

    tmp = did ^ 0b00010110100000001110000001111100
    f = tmp >> 20
    c = tmp & 0b11111111111111111111
    tmp = (a << 40) | (b << 34) | (c << 14) | (d << 13) | (e << 12) | f
    out = ''
    while tmp > 0:
        dig = '0123456789BCDFGHJKLMNPQRSTVWXY'[tmp % 30]
        tmp = tmp // 30
        out += dig
    return out

# Function to handle the writing process
def write_results(start, end):
    results = []
    for i in range(start, end):
        result = f'{i: 9} <-> {data_id_to_course_id(i)}\n'
        results.append(result)
    return results

# Open a file in write mode
with open('output.txt', 'w') as file:
    # Define range and number of threads
    start_range = 53820009
    end_range = 55641495
    num_threads = 1
    step = (end_range - start_range) // num_threads

    # Use ThreadPoolExecutor to handle parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Create a list of future tasks
        futures = []
        for i in range(num_threads):
            start = start_range + i * step
            end = start_range + (i + 1) * step if i < num_threads - 1 else end_range
            futures.append(executor.submit(write_results, start, end))

        # Collect results from all threads
        for future in concurrent.futures.as_completed(futures):
            for result in future.result():
                file.write(result)

print("Data saved to output.txt")
