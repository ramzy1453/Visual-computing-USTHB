import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres
WIDTH, HEIGHT = 600, 400
BACKGROUND_COLOR = (255, 255, 255)
TOWER_COLOR = (0, 0, 0)
DISK_COLOR = (0, 0, 255)
FPS = 30

# Initialisation de l'écran
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tour de Hanoï")


# Fonction pour dessiner les tours et les disques
def draw_tower_and_disks(towers):
    screen.fill(BACKGROUND_COLOR)

    # Dessiner les tours
    for i in range(3):
        pygame.draw.rect(screen, TOWER_COLOR, towers[i])

    # Dessiner les disques
    for disk in towers[3]:
        pygame.draw.rect(screen, DISK_COLOR, disk)

    pygame.display.flip()


# Fonction récursive pour résoudre la tour de Hanoï
def hanoi(n, source, target, auxiliary, towers):
    if n > 0:
        # Déplacer les n-1 disques de la source à l'auxiliaire
        hanoi(n - 1, source, auxiliary, target, towers)

        # Déplacer le n-ème disque de la source à la cible
        disk = towers[source].pop()
        towers[target].append(disk)
        draw_tower_and_disks(towers)
        pygame.time.wait(500)  # Pause pour une meilleure visualisation

        # Déplacer les n-1 disques de l'auxiliaire à la cible
        hanoi(n - 1, auxiliary, target, source, towers)


# Initialiser les tours et les disques
tower_width = 20
tower_height = HEIGHT - 50
disk_height = 20
disks_per_tower = 4

tower_x_positions = [100, WIDTH // 2, WIDTH - 100]

towers = [
    pygame.Rect(
        tower_x_positions[i] - tower_width // 2,
        HEIGHT - tower_height,
        tower_width,
        tower_height,
    )
    for i in range(3)
]

disks = [pygame.Rect(0, 0, (i + 1) * 50, disk_height) for i in range(disks_per_tower)]

# Initialiser les disques sur la première tour
towers[0].height = 20  # Réduire la hauteur de la première tour
for disk in disks:
    disk.bottom = HEIGHT - tower_height - 10
    disk.centerx = tower_x_positions[0]
    towers[0].height += disk_height
    towers[2].append(disk)

draw_tower_and_disks(towers)

# Résoudre la tour de Hanoï
hanoi(disks_per_tower, 0, 2, 1, towers)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

# Assurez-vous de quitter correctement
pygame.quit()
sys.exit()
