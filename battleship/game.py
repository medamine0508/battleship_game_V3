import numpy as np
from typing import Dict, List, Tuple, Optional
from .constants import *
from .utils import Orientation

def get_serializable_state(self):
    return {
        'player_board': self.player_board.tolist(),
        'opponent_board': self.opponent_board.tolist(),
        'game_phase': self.game_phase,
        'current_player': self.current_player,
        'message': self.message,
        'player_ships_remaining': self.player_ships_remaining,
        'opponent_ships_remaining': self.opponent_ships_remaining}
def load_state(self, state):
    self.player_board = np.array(state['player_board'])
    self.opponent_board = np.array(state['opponent_board'])
    self.game_phase = state['game_phase']
    self.current_player = state['current_player']
    self.message = state['message']
    self.player_ships_remaining = state['player_ships_remaining']
    self.opponent_ships_remaining = state['opponent_ships_remaining']

class BattleshipGame:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.player_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.opponent_board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        self.player_ships: Dict[str, List[Tuple[int, int]]] = {}
        self.opponent_ships: Dict[str, List[Tuple[int, int]]] = {}
        self.player_ships_remaining = len(SHIP_SIZES)
        self.opponent_ships_remaining = len(SHIP_SIZES)
        self.game_phase = "setup"  
        self.current_player = "player"
        self.message = "Place your ships (1-5 to select, R to rotate)"
        self.selected_ship = None
        self.ship_orientation = Orientation.HORIZONTAL
        self.last_ai_move = None

    def place_ship(self, ship_name: str, start_pos: Tuple[int, int], orientation: Orientation) -> bool:
        """Place a ship on the specified board"""
        size = SHIP_SIZES[ship_name]
        x, y = start_pos
        board = self.player_board if self.current_player == "player" else self.opponent_board
        ships = self.player_ships if self.current_player == "player" else self.opponent_ships
        
        if ship_name in ships:
            return False
            
        positions = []
        
        if orientation == Orientation.HORIZONTAL:
            if x + size > BOARD_SIZE:
                return False
            for i in range(size):
                if board[y][x + i] != 0:
                    return False
            for i in range(size):
                board[y][x + i] = 1
                positions.append((x + i, y))
        else:
            if y + size > BOARD_SIZE:
                return False
            for i in range(size):
                if board[y + i][x] != 0:
                    return False
            for i in range(size):
                board[y + i][x] = 1
                positions.append((x, y + i))
                
        ships[ship_name] = positions
        return True

    def attack(self, x: int, y: int) -> Tuple[bool, bool]:
        """Attack a position on the opponent's board"""
        if self.game_phase != "playing":
            raise RuntimeError("Attacks only allowed in playing phase")
        if self.current_player == "player":
            board = self.opponent_board
            ships = self.opponent_ships
        else:
            board = self.player_board
            ships = self.player_ships

        if board[y][x] in (2, 3): 
            return False, False
            
        hit = False
        sunk = False
        
        if board[y][x] == 1:  
            hit = True
            board[y][x] = 2  
            
            
            for ship_name, positions in ships.items():
                if (x, y) in positions:
                    if all(board[py][px] == 2 for px, py in positions):
                        sunk = True
                        if self.current_player == "player":
                            self.opponent_ships_remaining -= 1
                        else:
                            self.player_ships_remaining -= 1
                        break
        else:
            board[y][x] = 3  
            
        return hit, sunk

    def check_game_over(self) -> Optional[str]:
        """Check if the game is over and return the winner"""
        if self.player_ships_remaining == 0:
            return "opponent"
        if self.opponent_ships_remaining == 0:
            return "player"
        return None

    def switch_player(self):
        """Switch the current player"""
        self.current_player = "opponent" if self.current_player == "player" else "player"
        if self.current_player == "player":
            self.message = "Your turn - Attack opponent's board"
        else:
            self.message = "AI is thinking..."