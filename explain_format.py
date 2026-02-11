"""
Visual demonstration of how board states are stored in the dictionary.
This shows the connection between visual boards and the string format.
"""

from game import hash_board
import numpy as np

print("="*60)
print("BOARD STATE FORMAT DEMONSTRATION")
print("="*60)

# Example 1: Empty board
board1 = np.zeros((5, 5), dtype=int)
print("\nExample 1: Empty Board")
print("  0 1 2 3 4")
for i, row in enumerate(board1):
    symbols = ['.', 'X', 'O']
    print(f"{i} {' '.join(symbols[cell] for cell in row)}")

hash1 = hash_board(board1)
print(f'\nStored as: "{hash1}"')
print(f'Length: {len(hash1)} characters (5x5 = 25)')
print(f'Example in JSON: "{hash1}": [0.022789, 100000]')

# Example 2: Board with some pieces
board2 = np.array([
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1]
])
print("\n" + "-"*60)
print("\nExample 2: Single X at position (4,4)")
print("  0 1 2 3 4")
for i, row in enumerate(board2):
    symbols = ['.', 'X', 'O']
    print(f"{i} {' '.join(symbols[cell] for cell in row)}")

hash2 = hash_board(board2)
print(f'\nStored as: "{hash2}"')
print(f'Example in JSON: "{hash2}": [0.024911, 6373]')

# Example 3: Complex board
board3 = np.array([
    [1, 2, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [1, 0, 0, 0, 2],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]
])
print("\n" + "-"*60)
print("\nExample 3: Multiple Pieces")
print("  0 1 2 3 4")
for i, row in enumerate(board3):
    symbols = ['.', 'X', 'O']
    print(f"{i} {' '.join(symbols[cell] for cell in row)}")

hash3 = hash_board(board3)
print(f'\nStored as: "{hash3}"')
print(f'Example in JSON: "{hash3}": [0.531234, 42]')

# Example 4: Show the mapping
print("\n" + "="*60)
print("\nHOW THE MAPPING WORKS")
print("="*60)
print("\nBoard positions (row, col):")
print("(0,0) (0,1) (0,2) (0,3) (0,4)")
print("(1,0) (1,1) (1,2) (1,3) (1,4)")
print("(2,0) (2,1) (2,2) (2,3) (2,4)")
print("(3,0) (3,1) (3,2) (3,3) (3,4)")
print("(4,0) (4,1) (4,2) (4,3) (4,4)")

print("\nMaps to string indices:")
print(" 0  1  2  3  4")
print(" 5  6  7  8  9")
print("10 11 12 13 14")
print("15 16 17 18 19")
print("20 21 22 23 24")

print("\nCharacter values:")
print("  ' ' (space) = empty cell (value 0)")
print("  'X' = X player piece (value 1)")
print("  'O' = O player piece (value 2)")

print("\n" + "="*60)
print("\nThis format allows efficient storage and lookup!")
print("Dictionary entries: board_string -> [avg_score, count]")
print("="*60)
