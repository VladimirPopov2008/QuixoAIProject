import json
from tournament import Tournament


with open("states_random.json") as f:
    random_dict = json.load(f)

with open("states_greedy.json") as f:
    greedy_dict = json.load(f)



def evaluate(states_dict, label):
    t = Tournament(games=100, play_mode="GREEDY")

    # משתמשים במילון קיים בלבד
    t.states_dict = states_dict

    # מונעים למידה בזמן הבדיקה
    t.save_game_to_dict = lambda game: None

    t.run()
    mean, var = t.unknown_stats()

    print("================================")
    print(label)
    print("Results:", t.stats)
    print("Unknown moves mean:", mean)
    print("Unknown moves variance:", var)
    print("================================\n")


def main():
    print("Loading dictionaries...")

    print(f"Random dict size: {len(random_dict)}")
    print(f"Greedy dict size: {len(greedy_dict)}\n")

    evaluate(random_dict, "Greedy agent + Random-trained dictionary")
    evaluate(greedy_dict, "Greedy agent + Greedy-trained dictionary")


if __name__ == "__main__":
    main()
