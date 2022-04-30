import pygame
import numpy as np
import math
import time

def main():

    WIDTH, HEIGHT = 500, 500

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 100, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    cube_vertices = [[-3, -3, -3], [-3, -3, 3], [-3, 3, -3], [-3, 3, 3], [3, -3, -3], [3, -3, 3], [3, 3, -3], [3, 3, 3]]

    projection_matrix = [[1, 0, 0], [0, 1, 0]]

    motion_matrix = [[0.0, -0.02], [0.02, 0], [0.0, 0.0]]


    def get_screen_size():
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
        CENTER = WIDTH/2, HEIGHT/2
        SCALE = min(WIDTH, HEIGHT)/12
        return WIDTH, HEIGHT, CENTER, SCALE

    pygame.init()


    pygame.display.set_caption("3D Cube")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    WIDTH, HEIGHT, CENTER, SCALE = get_screen_size()

    angles = (0, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT, CENTER, SCALE = get_screen_size()
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                motion = pygame.mouse.get_rel()
                motion = np.dot(motion_matrix, motion)
                angles = angles + motion


        rotation_matrix_x = [[1, 0, 0], [0, math.cos(angles[0]), -math.sin(angles[0])], [0, math.sin(angles[0]), math.cos(angles[0])]]
        rotation_matrix_y = [[math.cos(angles[1]), 0, math.sin(angles[1])], [0, 1, 0], [-math.sin(angles[1]), 0, math.cos(angles[1])]]
        rotation_matrix_z = [[math.cos(angles[2]), -math.sin(angles[2]), 0], [math.sin(angles[2]), math.cos(angles[2]), 0], [0, 0, 1]]



        screen.fill(WHITE)

        cube_vertices_projected = [[0 for i in range(2)] for j in range(8)]
        i = 0
        for vertex in cube_vertices:
            cube_vertices_projected[i] = np.dot(projection_matrix, np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, vertex))))
            pygame.draw.circle(screen, BLACK, cube_vertices_projected[i]*SCALE+CENTER, 5)
            i += 1
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()