
def bsp_solution(L, m):
    n = len(L)
    L = L.copy()
    
    if n <= m or n - m == 1:
        return L[:m]  # Return the first m stations
    
    while m > 0:
        min_dist = float('inf')
        min_idx = -1
        sec_min_dist = float('inf')  # Track the second smallest distance
        sec_min_idx = -1
        
        for i in range(1, len(L) - 1):
            dist = L[i + 1] - L[i - 1]
            if dist < min_dist:
                sec_min_dist = min_dist  # Update second smallest distance
                sec_min_idx = min_idx
                min_dist = dist
                min_idx = i
            elif dist < sec_min_dist:
                sec_min_dist = dist
                sec_min_idx = i
        
        if min_idx != -1:
            # Choose the station to remove based on the greater maximum distance
            if bsp_value(L[:min_idx] + L[min_idx + 1:], m - 1) > bsp_value(L[:sec_min_idx] + L[sec_min_idx + 1:], m - 1):
                L.pop(min_idx)
            else:
                L.pop(sec_min_idx)
            m -= 1

    return L




def bsp_value(L, m):
    n = len(L)
    
    if n <= m:
        return float('inf')
    elif m == 0:
        min_dist = float('inf')
        for i in range(1, n):
            min_dist = min(min_dist, L[i] - L[i - 1])
        return min_dist
    else:
        first_idx = 0
        sec_idx = 0
        min_dist = float('inf')
        
        for i in range(1, n):
            if L[i] - L[i - 1] < min_dist:
                min_dist = L[i] - L[i - 1]
                first_idx = i - 1
                sec_idx = i
        
        return max(
            bsp_value(L[:first_idx] + L[first_idx + 1:], m - 1),
            bsp_value(L[:sec_idx] + L[sec_idx + 1:], m - 1)
        )

# Example usage:
L = [2, 4, 6, 7, 10, 14]
m = 2
print("bsp_value:", bsp_value(L, m))
print("bsp_solution:", bsp_solution(L, m))




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
    lengthcheck = (len(solution) == len(L)-m)
    print(lengthcheck)
    print(f"Test Case {i+1}: L = {L}, m = {m}")
    print(f"  Value: {value}")
    print(f"  Solution: {solution}\n")
