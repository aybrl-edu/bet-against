def adjust_profit_probability(ap_combinations):
    return [(profit * probability, cost) for profit, cost, probability, p_4, p_5, p_6 in ap_combinations]


def knapsack(max_amount, kp_combinations):
    kn_combinations = adjust_profit_probability(kp_combinations)

    [print(f"{key + 1} {org_combination} -> {kn_combinations[key]}") for (key, org_combination) in enumerate(kp_combinations)]

    n = len(kn_combinations)
    max_amount = int(max_amount)
    # Create a 2D array to store the maximum value that can be attained with different budgets
    dp = [[0 for x in range(max_amount + 1)] for x in range(n + 1)]

    # Build the table dp[][] in a bottom-up manner
    for i in range(1, n + 1):
        for w in range(1, max_amount + 1):

            profit, cost = kn_combinations[i - 1]
            cost = int(cost)

            if cost <= w:
                # Current combination can be included
                dp[i][w] = max(profit + dp[i - 1][w - cost], dp[i - 1][w])
            else:
                # Current combination cannot be included
                dp[i][w] = dp[i - 1][w]

    # Store the result of Knapsack
    result = dp[n][max_amount]

    # To find the combinations included in the optimal solution
    selected_combinations = []
    w = int(max_amount)
    for i in range(n, 0, -1):
        if result <= 0:
            break
        if result == dp[i - 1][w]:
            continue
        else:
            # This item is included.
            selected_combinations.append(kn_combinations[i - 1])
            result = result - kn_combinations[i - 1][0]
            w = w - kn_combinations[i - 1][1]

    return selected_combinations


def example():
    # Example usage
    combinations = [(100, 50), (60, 20), (120, 30)]  # Each tuple is (profit, cost)
    max_budget = 50
    optimal_combinations = knapsack(max_budget, combinations)
    print("Optimal combinations to choose:", optimal_combinations)
