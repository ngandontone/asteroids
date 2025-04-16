import pygame, asyncio
from constants import *
from player import *
from asteroid import *
from asteroidfield import *

GAME_RUNNING = 0
GAME_OVER = 1

async def main():
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()

    

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (shots,updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)


    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    dt = 0

    score = 0
    font = pygame.font.SysFont(None, 36)
    game_state = GAME_RUNNING
    game_over_font = pygame.font.SysFont(None, 72)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 

            if game_state == GAME_OVER and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 'R' key to restart
                    # Reset game objects
                    for obj in updatable:
                        obj.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroidfield = AsteroidField()
                    score = 0
                    game_state = GAME_RUNNING       
        if game_state == GAME_RUNNING:
            for obj in updatable:
                obj.update(dt)

            for obj in asteroids:
                if obj.collisions(player) == True:
                    print("Game over!")
                    # raise SystemExit()
                    game_state = GAME_OVER
                for shot in shots:
                    if obj.collisions(shot) == True:
                        if hasattr(obj, 'size'):
                            if obj.size == 'large':
                                score += 20
                            elif obj.size == 'medium':
                                score += 50
                            else:  # small
                                score += 100
                        else:
                            score += 10  # Default if no size attribute
                        obj.split()
                        shot.kill()
        
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if game_state == GAME_OVER:
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            # Center the text on screen
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(game_over_text, text_rect)
            
            # Maybe add instructions to restart
            restart_text = font.render("Press R to restart", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))
            screen.blit(restart_text, restart_rect)
        pygame.display.flip()

        

        dt = clock.tick(60) / 1000
   
        await asyncio.sleep(0)
if __name__ == "__main__":
    main()

asyncio.run(main())