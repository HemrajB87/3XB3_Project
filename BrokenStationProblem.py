def bsp_value(L, m):
    """
    Takes in a list of sorted (increasing) numbers and an integer value m.
    Returns the minimum possible value of the maximum difference between
    consecutive numbers after removing m elements.
    """
    n = len(L)
    # The difference array stores the gaps between consecutive elements
    diff = [L[i+1] - L[i] for i in range(n-1)]
    
    # Initialize dp array where dp[i][j] is the minimum possible maximum gap
    # after considering the first i gaps and removing j elements
    dp = [[float('inf')] * (m+1) for _ in range(n)]
    
    # Base case: no elements removed
    for i in range(n-1):
        dp[i][0] = max(dp[i-1][0], diff[i]) if i > 0 else diff[i]
    
    # Fill the dp array
    for i in range(1, n-1):
        for j in range(1, min(i+1, m+1)):
            # Case 1: Remove the current element
            dp[i][j] = min(dp[i][j], dp[i-1][j-1])
            # Case 2: Keep the current element and update the gap
            dp[i][j] = min(dp[i][j], max(dp[i-1][j], diff[i]))
    
    # The answer is the minimum possible maximum gap after considering all elements
    # and removing m elements
    return dp[n-2][m]

def bsp_solution(L, m):
    """
    Reconstructs the solution list based on the dp array from bsp_value.
    """
    n = len(L)
    max_gap = bsp_value(L, m)
    solution = [L[0]]  # always include the first element
    
    # Reconstruct the solution by choosing elements that do not exceed the max_gap
    last_added = L[0]
    for i in range(1, n):
        if L[i] - last_added <= max_gap and m > 0:
            # potentially remove this element, decrement m
            m -= 1
        else:
            # add this element to the solution
            solution.append(L[i])
            last_added = L[i]
    
    return solution

# Example usage:
value = bsp_value([2, 4, 6, 7, 10, 14], 2)  # Expected output should be a value <= 4
solution = bsp_solution([2, 4, 6, 7, 10, 14], 2)  # Expected output: [2, 6, 10, 14]
print(f"Value: {value}")
print(f"Solution: {solution}")
