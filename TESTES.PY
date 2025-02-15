import pygame

pygame.init()

# Initialisation de l'écran
screen = pygame.display.set_mode((800, 600))
running = True

# Boucle principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.dict['button'])

    # Remplissage de l'écran avec une couleur de fond
    screen.fill((0, 0, 0))

    # Dessin du rectangle
    x, y, tileSize = 5, 5, 50
    pygame.draw.rect(screen, (255, 0, 0), (x * tileSize, y * tileSize, tileSize, tileSize))

    # Mise à jour de l'écran
    pygame.display.flip()

pygame.quit()
