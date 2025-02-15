import pygame
from jeux.demineur import Demineur

class Game():
    def __init__(self):
        self.size = (960,600)

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Demineur",)

        self.active = Demineur(self.screen, (30,25), 175)

    

    def update_textures(self):
        pass
        
    def run(self):

        pygame.init()
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill((0,0,0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False

            self.active.update(events=events)
            
            pygame.display.flip()
            clock.tick(60)
        


        pygame.quit()