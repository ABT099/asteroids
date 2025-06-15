import sys
import pygame
from src.entities.asteroid import Asteroid
from src.entities.asteroidfield import AsteroidField
from src.game.constants import *
from src.game.game import Game
from src.entities.player import Player
from src.entities.shot import Shot

def initialize_game():
    """Initialize/reset all game objects and sprite groups"""
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)
    Game.containers = (updatable, drawable)
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    return updatable, drawable, asteroids, shots, player, asteroid_field

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    background_image = pygame.image.load("assets/background.png").convert() 
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


    game = Game(screen, font)
    clock = pygame.time.Clock()
    dt = 0

    updatable, drawable, asteroids, shots, player, asteroid_field = initialize_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
    
        screen.blit(background_image, (0, 0))
        for thing in updatable:
            thing.update(dt)
        
        game.render_scores()

        for asteroid in asteroids:
            if asteroid.collide(player):
                game.die(player)

                if player.could_respawn():
                    player.respawn()
                    for ast in asteroids:
                        ast.kill()
                    break
                else:
                    game.render_game_over()
                    pygame.display.flip()

                    waiting_for_input = True
                    while waiting_for_input:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                                # Restart the game
                                updatable, drawable, asteroids, shots, player, asteroid_field = initialize_game()
                                game.reset_game(player)
                                waiting_for_input = False
                                break

            for shot in shots:
                if asteroid.collide(shot):
                    asteroid.split()
                    shot.kill()
                    game.update_score(5)
                    break

        for thing in drawable:
            thing.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()