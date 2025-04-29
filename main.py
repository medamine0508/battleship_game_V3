import pygame
import argparse
import sys
from battleship.game import *
from battleship.player import HumanPlayer
from battleship.ai import AIOpponent
from battleship.constants import *
from battleship.utils import pos_to_grid, Orientation
from battleship.network import *

def draw_game(screen, game, font_small, font_medium):
    """Draw the complete game state"""
    screen.fill(WHITE)
    

    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(
                BOARD_OFFSET + x * CELL_SIZE,
                BOARD_OFFSET + y * CELL_SIZE,
                CELL_SIZE - MARGIN,
                CELL_SIZE - MARGIN
            )
            # Water
            if game.player_board[y][x] == 0:
                pygame.draw.rect(screen, BLUE, rect)
            
            elif game.player_board[y][x] == 1:
                if game.game_phase == "setup":  
                    pygame.draw.rect(screen, GREEN, rect)
                else:
                    pygame.draw.rect(screen, BLUE, rect)  
            # Hit
            elif game.player_board[y][x] == 2:
                pygame.draw.rect(screen, RED, rect)
            # Miss
            elif game.player_board[y][x] == 3:
                pygame.draw.rect(screen, WHITE, rect)

    
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(
                BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE + x * CELL_SIZE,
                BOARD_OFFSET + y * CELL_SIZE,
                CELL_SIZE - MARGIN,
                CELL_SIZE - MARGIN
            )
            
            if game.opponent_board[y][x] == 0 or game.opponent_board[y][x] == 1:
                pygame.draw.rect(screen, GRAY, rect)
            # Hit
            elif game.opponent_board[y][x] == 2:
                pygame.draw.rect(screen, RED, rect)
            # Miss
            elif game.opponent_board[y][x] == 3:
                pygame.draw.rect(screen, WHITE, rect)

    for i in range(BOARD_SIZE + 1):
        # Vertical lines
        pygame.draw.line(screen, BLACK,
                         (BOARD_OFFSET + i * CELL_SIZE, BOARD_OFFSET),
                         (BOARD_OFFSET + i * CELL_SIZE, BOARD_OFFSET + BOARD_SIZE * CELL_SIZE), 2)
        pygame.draw.line(screen, BLACK,
                         (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE + i * CELL_SIZE, BOARD_OFFSET),
                         (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE + i * CELL_SIZE, BOARD_OFFSET + BOARD_SIZE * CELL_SIZE), 2)
        # Horizontal lines
        pygame.draw.line(screen, BLACK,
                         (BOARD_OFFSET, BOARD_OFFSET + i * CELL_SIZE),
                         (BOARD_OFFSET + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET + i * CELL_SIZE), 2)
        pygame.draw.line(screen, BLACK,
                         (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET + i * CELL_SIZE),
                         (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE * 2, BOARD_OFFSET + i * CELL_SIZE), 2)

    
    player_label = font_medium.render("Your Fleet", True, BLACK)
    opponent_label = font_medium.render("Opponent", True, BLACK)
    screen.blit(player_label, (BOARD_OFFSET, BOARD_OFFSET - 40))
    screen.blit(opponent_label, (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET - 40))

    
    message_text = font_medium.render(game.message, True, BLACK)
    screen.blit(message_text, (BOARD_OFFSET, BOARD_OFFSET + BOARD_SIZE * CELL_SIZE + 20))

    
    if game.game_phase == "setup":
        instructions = [
            "Ship placement:",
            "1 - Carrier (5)",
            "2 - Battleship (4)",
            "3 - Cruiser (3)",
            "4 - Submarine (3)",
            "5 - Destroyer (2)",
            "R - Rotate ship",
            "Click to place selected ship"
        ]
        for i, text in enumerate(instructions):
            instr_text = font_small.render(text, True, BLACK)
            screen.blit(instr_text, (BOARD_OFFSET, BOARD_OFFSET + BOARD_SIZE * CELL_SIZE + 60 + i * 25))

    
    if game.last_ai_move:
        x, y = game.last_ai_move
        ai_move_text = font_small.render(f"Last AI move: {chr(65+y)}{x+1}", True, BLACK)
        screen.blit(ai_move_text, (BOARD_OFFSET * 2 + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET + BOARD_SIZE * CELL_SIZE + 20))

    
    if game.game_phase == "game_over":
        winner = "You win!" if game.opponent_ships_remaining == 0 else "You lose!"
        game_over_text = font_medium.render(winner, True, RED)
        restart_text = font_small.render("Press N for new game", True, BLACK)
        text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, BOARD_OFFSET//2))
        screen.blit(game_over_text, text_rect)
        screen.blit(restart_text, (WINDOW_WIDTH//2 - 100, BOARD_OFFSET//2 + 40))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["pve", "server", "client"], default="pve")
    parser.add_argument("--host", default="localhost")
    args = parser.parse_args()
    
    game = BattleshipGame()
    network_manager = None
    ai_opponent = None
    
    print(f"Starting in {args.mode.upper()} mode")
    if args.mode in ["server", "client"]:
        network_manager = NetworkManager(args.mode == "server", args.host, SERVER_PORT)
        try:
            if args.mode == "server":
                network_manager.start_server()
                game.current_player = "player"  
            else:
                network_manager.connect_to_server()
                game.current_player = "opponent"  
        except Exception as e:
            print(f"Network initialization failed: {e}")
            sys.exit(1)
    if args.mode == "pve":
        ai_opponent = AIOpponent(game)

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Battleship")
    clock = pygame.time.Clock()
    font_small = pygame.font.SysFont(None, FONT_SMALL)
    font_medium = pygame.font.SysFont(None, FONT_MEDIUM)


    human_player = HumanPlayer(game)
  

    running = True
    while running:
        if args.mode in ["server", "client"]:
            if game.current_player == ("player" if args.mode == "client" else "opponent"):
        
                received_state = network_manager.receive()
                if received_state:
                    game.load_state(received_state)
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT))  #

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.USEREVENT:
                continue  
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_phase == "setup":
                    game.ship_orientation = Orientation.VERTICAL if game.ship_orientation == Orientation.HORIZONTAL else Orientation.HORIZONTAL
                elif event.key == pygame.K_1 and game.game_phase == "setup":
                    game.selected_ship = "carrier"
                elif event.key == pygame.K_2 and game.game_phase == "setup":
                    game.selected_ship = "battleship"
                elif event.key == pygame.K_3 and game.game_phase == "setup":
                    game.selected_ship = "cruiser"
                elif event.key == pygame.K_4 and game.game_phase == "setup":
                    game.selected_ship = "submarine"
                elif event.key == pygame.K_5 and game.game_phase == "setup":
                    game.selected_ship = "destroyer"
                elif event.key == pygame.K_n and game.game_phase == "game_over":
                    game.reset_game()
                    human_player = HumanPlayer(game)
                    ai_opponent = AIOpponent(game)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x, grid_y, board = pos_to_grid(mouse_x, mouse_y)
                
                if grid_x is not None and 0 <= grid_x < BOARD_SIZE and 0 <= grid_y < BOARD_SIZE:
                    if board == "player" and game.game_phase == "setup":
                        human_player.handle_setup_click(grid_x, grid_y)
                    elif board == "opponent" and game.game_phase == "playing":
                        if game.current_player == "player":
                            human_player.handle_attack_click((grid_x, grid_y))
        
        if (args.mode == "pve" and ai_opponent and game.game_phase == "playing" and game.current_player == "opponent"):
            ai_opponent.make_move()
        elif args.mode in ["server", "client"]:
            
            if game.current_player != ("player" if args.mode == "client" else "opponent"):
                success = network_manager.send(game.get_serializable_state())
                if not success:
                    print("Connection lost!")
                    running = False
        
        if network_manager:
            network_manager.close()
        
        
        winner = game.check_game_over()
        if winner:
            game.game_phase = "game_over"
        
        draw_game(screen, game, font_small, font_medium)
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()