"""
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


if __name__ == "__main__":
    main()