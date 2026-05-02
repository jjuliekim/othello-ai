## Othello AI Bot
Run **game.py** to play against the AI opponent!
### How to Play
- Players take turn placing discs to capture the opponent's pieces
- A valid move must bracket at least one opponent disc between the newly placed disc and an existing disc of your color
- Flip all bracketed discs (horizontally, vertically, and diagonally)
- The game ends when neither player has a valid move, and the player with the most discs wins!

## AI Strategy & Gameplay Tips
- Piece difference: Total disc count (AI pieces minus opponent pieces)
- Corner control: Corners are permanent and cannot be flipped (very high priority)
- Edge control: Edge positions are harder to recapture
- Corner adjacency: Penalizes pieces adjacent to empty corners (gives opponent corner access)
- Number of available moves: More options means more flexibility

## Example
<img width="290" height="467" src="https://github.com/user-attachments/assets/fc54098c-a58c-4464-8b13-51cec86a4314" />
