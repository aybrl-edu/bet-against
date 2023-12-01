import math

from Game import Game
from Team import Team
from optimizer import knapsack

GAMES = ['MNZ:4.10-JUV:1.92-3.45', 'HVR:9.35-PSG:1.28-5.8', 'RMA:1.13-GRD:16.5-8.75']


# Helpers
def parse_game(game, key):
    game.replace(" ", "")
    str_split = game.split('-')
    team_1 = str_split[0].split(':')
    team_2 = str_split[1].split(':')
    draw_p = str_split[2]

    t1_name = team_1[0]
    t1_w_p = team_1[1]

    t2_name = team_2[0]
    t2_w_p = team_2[1]

    t1 = Team(t1_name, t1_w_p)
    t2 = Team(t2_name, t2_w_p)

    new_game = Game(t1, t2, draw_p)

    return new_game


def ask_games():
    print("Game syntax : Host:Ph - Invitee:Pi - Pd")
    nb_games = int(input("Enter the number of games: "))
    a_games = []
    for n in range(nb_games):
        in_game = input(f'Enter game ({n + 1}): ')
        try:
            game = parse_game(in_game, n)
            a_games.append(game)
        except IndexError:
            print("game format invalid")

    return a_games


def ask_bet():
    amount_per_bet = float(input("Enter the initial amount/bet: "))
    nb_bets_to_take = float(input("Enter the number of combinations to bet: "))
    total_possible_amount = float(input("Enter the total amount: "))
    return amount_per_bet, nb_bets_to_take, total_possible_amount


def generate_game_outcomes(games_g, num_games):
    game = games_g[len(games_g) - num_games]
    outcomes = [game.t1.win_p, game.t2.win_p, game.draw_p]
    # Base case: if only one game, return the list of single outcomes
    if num_games == 1:
        return [(outcome,) for outcome in outcomes]

    # Recursive call for fewer games
    previous_outcomes = generate_game_outcomes(games_g, num_games - 1)

    # Generate combinations for the current number of games
    g_combinations = []
    for previous_outcome in previous_outcomes:
        [g_combinations.append(previous_outcome + (outcome,)) for outcome in outcomes]

    return g_combinations


def calculate_profit(c_combinations, c_bet):
    bet_amount = c_bet[0]
    bets_to_take = c_bet[1]

    total_possible_bets_amount = bet_amount * len(c_combinations)  # the total amount if all bets were taken
    total_bet_amount = bets_to_take * bet_amount  # the amount of bets taken if not all

    print(f"Total possible bets amount: 3^{len(c_combinations)} = {total_possible_bets_amount}")
    print(f"Total chosen bets amount: {bets_to_take} * {bet_amount} = {total_bet_amount}")

    e_combinations = []
    for key, combination in enumerate(c_combinations):
        combination_factor = 1
        for fact in combination:
            combination_factor *= round(float(fact), 3)
            combination_factor = round(combination_factor, 3)

        combination_probability = round(100 / combination_factor, 3)
        potential_profit = round(combination_factor * bet_amount - bet_amount,
                                 3)  # profit if the given combination occurred with no relevance to how much was invested in other combinations
        total_potential_profit = round((combination_factor * bet_amount) - total_possible_bets_amount,
                                       3)  # total profit if all bets were taken and this combination event occurred
        profit_per_bets = round((combination_factor * bet_amount) - total_bet_amount,
                                3)  # total profit if only a number of combinations were chosen and this combination event occurred
        p_stat = (
            profit_per_bets, total_bet_amount, combination_probability, combination_factor, potential_profit,
            total_potential_profit)
        e_combinations.append(p_stat)

        print(25 * '-')
        print(f"{key + 1} {combination}")
        print(f"Combination Decimal Factor: {combination_factor}")
        print(f"Combination Probability: {combination_probability}%")
        print(f"Potential Combination Profit: {potential_profit}")
        print(f"All Combinations Potential Profit: {total_potential_profit}")
        print(f"Set Combinations Potential Profit: {profit_per_bets}")

    print(25 * '-', 'End Combinations', 25 * '-')
    return e_combinations


if __name__ == '__main__':
    # Inputs
    games = ask_games()
    bet = ask_bet()
    # Combinations
    combinations = generate_game_outcomes(games, len(games))
    # Profit
    combinations_stats = calculate_profit(combinations, bet)
    # Optimization
    s_combinations = knapsack(bet[2], combinations_stats)

    print(f"Optimal combinations to choose from: {s_combinations}")
