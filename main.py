import pygame
from constants import *
from player import *
from asteroid import *
from asteroidfield import *

def main():
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
                    obj.split()
                    shot.kill()
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        

        pygame.display.flip()

        

        dt = clock.tick(60) / 1000
   

if __name__ == "__main__":
    main()
