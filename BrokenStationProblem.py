def bsp_value(L, m):
    n = len(L)
    # The difference array stores the gaps between consecutive elements
    diff = [L[i+1] - L[i] for i in range(n-1)]
    #print(f"Differences between elements: {diff}")

    # Initialize dp array where dp[i][j] is the minimum possible maximum gap
    dp = [[float('inf')] * (m+1) for _ in range(n)]
    
    # Base case: no elements removed
    for i in range(n-1):
        dp[i][0] = max(dp[i-1][0], diff[i]) if i > 0 else diff[i]
    
    # Fill the dp array
    for i in range(1, n):
        for j in range(1, min(i+1, m+1)):
            # Calculate new gap if this station is removed
            if i < n - 1:
                new_gap = diff[i-1] + diff[i] if i - j > 0 else diff[i-1]
            else:
                new_gap = diff[i-1]  # For the last station

            # Update dp values considering both cases: removing or keeping the station
            if i - j > 0:
                dp[i][j] = min(dp[i][j], max(dp[i-1][j-1], new_gap))
            dp[i][j] = min(dp[i][j], max(dp[i-1][j], diff[i-1]))

            #print(f"dp[{i}][{j}]: {dp[i][j]}")


            # Debugging print statements
            #print(f"dp[{i}][{j}] after considering station {i+1}: {dp[i][j]}")


    
    #print(f"Final DP Table: {dp}")
    return min(dp[i][m] for i in range(m, n))

def bsp_solution(L, m):
    n = len(L)
    max_gap = bsp_value(L, m)
    solution = [L[0]]  # Always include the first element

    # Consider elements from the second to the second-last
    last_added = L[0]
    for i in range(1, n - 1):
        if L[i] - last_added + 1 <= max_gap and m > 0:
            m -= 1  # Remove this element
        else:
            solution.append(L[i])  # Keep this element
            last_added = L[i]

    solution.append(L[-1])  # Always include the last element
    return solution



# List of test cases
test_cases = [
    ([1, 2, 3, 4, 5], 2),
    ([1, 3, 6, 10, 15], 1),
    ([5, 5, 5, 5, 5], 2),
    ([1, 2, 3, 4, 10], 1),
    ([10, 20, 30, 40, 50], 3),
    ([1, 10, 20, 30, 40, 50], 2),
    ([5, 6, 7, 12, 13, 14], 1),
    ([1, 3, 7, 9, 11, 13], 2),
    ([2, 4, 6, 8, 10, 12, 14], 3),
    ([1, 1, 2, 3, 5, 8, 13, 21], 2),
    ([1, 100, 200, 300, 400, 500], 3),
    ([1, 2], 1),
    ([1], 0),
    ([1, 3, 6, 10, 11, 12, 13, 15], 3),
    ([1, 2, 3, 5, 8, 13, 21, 34, 55], 4),
    ([5, 10, 15, 20, 25, 30, 35], 2),
    ([10, 12, 14, 15, 16, 18, 20], 2),
    ([1, 3, 6, 10, 15, 21, 28], 3),
    ([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 5),
    ([1, 2, 4, 8, 16, 32, 64], 2)
]

# Run the test cases
for i, (L, m) in enumerate(test_cases):
    value = bsp_value(L, m)
    solution = bsp_solution(L, m)
    print(f"Test Case {i+1}: L = {L}, m = {m}")
    print(f"  Value: {value}")
    print(f"  Solution: {solution}\n")

