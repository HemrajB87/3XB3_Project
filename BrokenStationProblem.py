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
            # If we remove this station, calculate the new gap
            if i - j > 0 and i < n-2:  # Ensure there are stations on both sides
                new_gap = diff[i-1] + diff[i]  # Gap created by removing this station
                left_gap = dp[i-1][j-1]  # Maximum gap with one less removal to the left
                dp[i][j] = min(dp[i][j], max(left_gap, new_gap))
            elif i - j > 0:  # Edge case: removing the last station
                dp[i][j] = dp[i-1][j-1]

            # If we keep this station, the maximum gap is the max of the gap to the left and the current gap.
            dp[i][j] = min(dp[i][j], max(dp[i-1][j], diff[i-1]))

            # Debugging print statements
            print(f"dp[{i}][{j}] after considering station {i+1}: {dp[i][j]}")


    
    print(f"Final DP Table: {dp}")
    return min(dp[i][m] for i in range(m, n))

def bsp_solution(L, m):
    n = len(L)
    max_gap = bsp_value(L, m)
    #print(f"Maximum gap allowed: {max_gap}")
    solution = [L[0]]  # always include the first element
    
    # Reconstruct the solution by choosing elements that do not exceed the max_gap
    last_added = L[0]
    for i in range(1, n):
        if L[i] - last_added <= max_gap and m > 0:
            # potentially remove this element, decrement m
            m -= 1
            #print(f"Removing element {L[i]}")
        else:
            # add this element to the solution
            solution.append(L[i])
            last_added = L[i]
            #print(f"Adding element {L[i]}")
    
    return solution


# Example usage:
value = bsp_value([2, 4, 6, 7, 10, 14], 2)
solution = bsp_solution([2, 4, 6, 7, 10, 14], 2)
print(f"Value: {value}")
print(f"Solution: {solution}")
