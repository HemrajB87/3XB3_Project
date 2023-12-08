def minMaxGap(L, i, m, memo):
    if (i, m) in memo:
        return memo[(i, m)]
    if m == 0:
        # Base case: no removals, return the max gap in L[:i+1]
        memo[(i, m)] = max([L[j+1] - L[j] for j in range(i)])
        return memo[(i, m)]
    if i == 0:
        # Base case: only one element, no gap
        return 0
    
    # Include the current station
    include_gap = minMaxGap(L, i-1, m, memo)
    
    # Exclude the current station
    exclude_gap = minMaxGap(L, i-1, m-1, memo)
    
    # The maximum gap after including this station is the max of the current gap and the gap if we were to include the station
    current_gap = L[i] - L[i-1]
    max_gap = max(include_gap, current_gap)
    
    # Choose the minimum of including or excluding this station
    memo[(i, m)] = min(max_gap, exclude_gap)
    return memo[(i, m)]
