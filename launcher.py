import pygame
import subprocess
import sys
from battleship.constants import *

def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    font = pygame.font.SysFont(None, 48)
    
    while True:
        screen.fill(BLUE)
        title = font.render("BATTLESHIP", True, WHITE)
        screen.blit(title, (200 - title.get_width()//2, 50))
        
        options = [
            "1. Player vs AI (Single Player)",
            "2. Host PvP Game",
            "3. Join PvP Game"
        ]
        
        for i, text in enumerate(options):
            text_surf = font.render(text, True, WHITE)
            screen.blit(text_surf, (200 - text_surf.get_width()//2, 120 + i*60))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.quit()
                    subprocess.run(["python", "main.py", "--mode", "pve"])
                    return
                elif event.key == pygame.K_2:
                    pygame.quit()
                    subprocess.run(["python", "main.py", "--mode", "server"])
                    return
                elif event.key == pygame.K_3:
                    pygame.quit()
                    host = input("Enter host IP address: ")
                    subprocess.run(["python", "main.py", "--mode", "client", "--host", host])
                    return

if __name__ == "__main__":
    show_menu()
#how to run vs ai mode : python launcher.py --mode pve