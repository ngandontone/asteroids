import pygame, asyncio
from constants import *
from player import *
from asteroid import *
from asteroidfield import *

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
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return        
        
        for obj in updatable:
            obj.update(dt)

        for obj in asteroids:
            if obj.collisions(player) == True:
                print("Game over!")
                raise SystemExit()
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
        pygame.display.flip()

        

        dt = clock.tick(60) / 1000
   
        await asyncio.sleep(0)
if __name__ == "__main__":
    main()

asyncio.run(main())