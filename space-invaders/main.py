import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

PURPLE = (45, 5, 51)
YELLOW = (255, 209, 18)

font = pygame.font.Font("C:\\Users\\USER\\Documents\\UAS-EMBEDDED\\uas-embedded\\space-invaders\\fonts\\monogram.ttf", 40)
level_surface = font.render("SPACE INVADERS!", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
team_name_surface = font.render("KYRMIST TEAM", False, YELLOW)
class_name_surface = font.render("TMD 6A", False, YELLOW)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Space Invaders - Embedded TMD 6A")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERY = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERY, random.randint(4000, 8000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MYSTERY and game.run:
            game.create_mystery()
            pygame.time.set_timer(MYSTERY, random.randint(4000, 8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()

    #update
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_laser_group.update()
        game.mystery_group.update()
        game.check_collision()

    #draws
    screen.fill(PURPLE)

    #ui
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)
    
    if game.run:
        screen.blit(level_surface, (520, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740, 50, 50))
    
    x = 50
    for life in range(game.lives):
        screen.blit(game.lives_heart, (x, 745))
        x += 50

    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(team_name_surface, (570, 15, 50, 50))
    screen.blit(class_name_surface, (660, 40, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_laser_group.draw(screen)
    game.mystery_group.draw(screen)

    pygame.display.update()
    clock.tick(60)