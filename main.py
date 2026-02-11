"""
<<<<<<< HEAD
Simple evaluator that runs deterministic GREEDY (epsilon=0) for a fixed number of games
using two lookup dictionaries:
 - states_random.json
 - states_greedy.json

It runs:
 1) GREEDY (epsilon=0) using the RANDOM dict for lookup (1000 games)
 2) GREEDY (epsilon=0) using the GREEDY dict for lookup (1000 games)

And prints wins / losses / ties, average unknown_ratio and elapsed time for each run.

Adjust constants below if you want different filenames or game counts.
"""
import json
import time

from game import Game

# --- configuration ---
RANDOM_DICT_FILE = "states_random.json"
GREEDY_DICT_FILE = "states_greedy.json"
EVAL_GAMES = 1000  # number of evaluation games per lookup
EPSILON = 0.1      # deterministic greedy during evaluation


def load_states_dict(path):
    print(f"Loading states dict from: {path} ...", end="", flush=True)
    t0 = time.time()
    with open(path, "r") as f:
        d = json.load(f)
    elapsed = time.time() - t0
    print(f" done ({elapsed:.2f}s). Entries: {len(d):,}")
    return d


def evaluate_lookup(lookup_dict, n_games, epsilon=0.0, progress_every=100):
    """
    Run n_games where X uses GREEDY consulting lookup_dict and O is random.
    Returns (stats_dict, avg_unknown_ratio, elapsed_seconds).
    """
    stats = {"VICTORY_X": 0, "VICTORY_O": 0, "TIE": 0}
    unknowns = []
    t0 = time.time()
    for i in range(1, n_games + 1):
        g = Game(play_mode="GREEDY", states_dict=lookup_dict, epsilon=epsilon)
        res = g.play()
        stats[res] += 1
        unknowns.append(g.unknown_ratio())

        if progress_every and i % progress_every == 0:
            print(f"  evaluated {i}/{n_games} games...", end="\r", flush=True)

    elapsed = time.time() - t0
    avg_unknown = sum(unknowns) / len(unknowns) if unknowns else 0.0
    return stats, avg_unknown, elapsed


def print_stats(title, stats, avg_unknown, elapsed, n_games):
    print(f"\n=== {title} (total games={n_games}) ===")
    for k in ("VICTORY_X", "VICTORY_O", "TIE"):
        count = stats.get(k, 0)
        pct = (count / n_games) * 100 if n_games else 0.0
        print(f"{k:10s}: {count:6d} ({pct:6.3f}%)")
    print(f"Average unknown_ratio: {avg_unknown:.4f}")
    print(f"Elapsed time: {elapsed:.2f}s\n")


def main():
    # Load lookup dictionaries
    random_lookup = load_states_dict(RANDOM_DICT_FILE)
    greedy_lookup = load_states_dict(GREEDY_DICT_FILE)

    # Evaluate using RANDOM lookup
    print("\n1) Evaluating GREEDY (epsilon=0) using RANDOM lookup dict...")
    stats_r, avg_unknown_r, elapsed_r = evaluate_lookup(random_lookup, EVAL_GAMES, epsilon=EPSILON)
    print_stats("GREEDY(epsilon=0) using RANDOM dict", stats_r, avg_unknown_r, elapsed_r, EVAL_GAMES)

    # Evaluate using GREEDY lookup
    print("2) Evaluating GREEDY (epsilon=0) using GREEDY lookup dict...")
    stats_g, avg_unknown_g, elapsed_g = evaluate_lookup(greedy_lookup, EVAL_GAMES, epsilon=EPSILON)
    print_stats("GREEDY(epsilon=0) using GREEDY dict", stats_g, avg_unknown_g, elapsed_g, EVAL_GAMES)

    print("Done.")
=======
Main runner that uses Tournament from tournament.py without duplicating its logic.
This file intentionally makes minimal assumptions/changes to Tournament and
does not interfere with the Tournament class responsibilities.

Workflow:
1. Generate random dataset (both players RANDOM) into random storage dict.
2. Freeze a copy of the random storage dict and use it as lookup for greedy data generation.
3. Generate greedy dataset (X is GREEDY consulting the frozen random lookup) into greedy storage dict.
4. Evaluate deterministic greedy (epsilon=0) vs random using the greedy dictionary.
5. Sanity check: greedy with epsilon=1 should behave like random.
"""
import time
from copy import deepcopy

from tournament import Tournament  # uses the Tournament implementation from tournament.py

# --- configuration ---
N_RANDOM = 100_000      # number of games to generate random dataset
N_GREEDY = 100_000      # number of games to generate greedy dataset (greedy consults random_dict)
EVAL_GAMES = 1000       # number of evaluation games to compare greedy vs random
EPSILON_GREEDY = 0.1    # exploration probability used during greedy dataset generation
RANDOM_DICT_FILE = "states_random.json"
GREEDY_DICT_FILE = "states_greedy.json"


def print_stats(label, stats):
    total = sum(stats.values())
    print(f"=== {label} (total games={total}) ===")
    for k in ("VICTORY_X", "VICTORY_O", "TIE"):
        print(f"{k:10s}: {stats[k]:6d} ({stats[k]/total:.3%})")
    print()


def save_storage_dict_to_json(storage_dict, filename):
    # Tournament.save_dict already does a safe json dump, but we call it here as well for clarity.
    # storage_dict keys are expected to be strings produced by hash_board.
    import json
    with open(filename, "w") as f:
        json.dump(storage_dict, f)


def main():
    start_time = time.time()

    # 1) Generate random dataset
    print("1) Generating random dataset (both players RANDOM)...")
    t_random = Tournament(games=N_RANDOM, play_mode="RANDOM", epsilon=0.0,
                          lookup_dict=None, storage_dict={})
    t_random.run()
    print_stats("Random dataset stats", t_random.stats)
    t_random.save_dict(RANDOM_DICT_FILE)
    print(f"Saved random states dict to {RANDOM_DICT_FILE} (entries={len(t_random.storage_dict)})\n")

    # Freeze a copy of the random storage dict to use as a read-only lookup for greedy generation.
    # Use deepcopy to ensure no accidental sharing/mutation.
    random_lookup = deepcopy(t_random.storage_dict)

    # 2) Generate greedy dataset (X is GREEDY, consults random_lookup). Store into a fresh dict.
    print("2) Generating greedy dataset (X is GREEDY, consults random dataset for rankings)...")
    t_greedy = Tournament(games=N_GREEDY, play_mode="GREEDY", epsilon=EPSILON_GREEDY,
                          lookup_dict=random_lookup, storage_dict={})
    t_greedy.run()
    print_stats("Greedy dataset stats (games generated by greedy agent)", t_greedy.stats)
    t_greedy.save_dict(GREEDY_DICT_FILE)
    print(f"Saved greedy states dict to {GREEDY_DICT_FILE} (entries={len(t_greedy.storage_dict)})\n")

    # 3) Evaluate deterministic greedy (epsilon=0) vs random opponent, using greedy storage as lookup.
    print(f"3) Evaluating deterministic greedy agent (epsilon=0) for {EVAL_GAMES} games vs random opponent...")
    greedy_lookup_for_eval = deepcopy(t_greedy.storage_dict)
    t_eval = Tournament(games=EVAL_GAMES, play_mode="GREEDY", epsilon=0.0,
                        lookup_dict=greedy_lookup_for_eval, storage_dict={})
    t_eval.run()
    print_stats("Deterministic greedy (eval) stats", t_eval.stats)
    mean_unknown, _ = t_eval.unknown_stats()
    print(f"Average unknown_ratio during eval: {mean_unknown:.4f}\n")

    # 4) Sanity check: greedy with epsilon=1 should behave like random
    print(f"4) Sanity check: greedy agent with epsilon=1 (should behave randomly) for {EVAL_GAMES} games...")
    t_sanity = Tournament(games=EVAL_GAMES, play_mode="GREEDY", epsilon=1.0,
                          lookup_dict=random_lookup, storage_dict={})
    t_sanity.run()
    print_stats("Greedy(epsilon=1) stats", t_sanity.stats)
    mean_unknown_sanity, _ = t_sanity.unknown_stats()
    print(f"Average unknown_ratio during sanity check: {mean_unknown_sanity:.4f}\n")

    total_time = time.time() - start_time
    print(f"All done. Total elapsed time: {total_time:.1f}s")
>>>>>>> 508193cb73bf88f6e3a94476b5e93ce4fe6e2a47


if __name__ == "__main__":
    main()