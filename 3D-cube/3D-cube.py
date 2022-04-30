import pygame
import numpy as np
import math
import time

def main():

    WIDTH, HEIGHT = 500, 500

    GREY = (150, 150, 150)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    RED = (255, 0, 0)
    ORANGE = (255, 100, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

    cube_vertices = [[[[x, y, z] for x in range(-3, 4, 2)] for y in range(-3, 4, 2)] for z in range(-3, 4, 2)]


    projection_matrix = [[1, 0, 0], [0, 1, 0]]

    motion_matrix = [[0.0, -0.02], [0.02, 0], [0.0, 0.0]]

    LINE_THICKNESS = 2

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
                angles = (angles + motion) % (2*math.pi)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 20 <= pygame.mouse.get_pos()[0] <= 170 and HEIGHT-40 <= pygame.mouse.get_pos()[1] <= HEIGHT-20:  # button reset cube orientation
                    angles = (0, 0, 0)


        rotation_matrix_x = [[1, 0, 0], [0, math.cos(angles[0]), -math.sin(angles[0])], [0, math.sin(angles[0]), math.cos(angles[0])]]
        rotation_matrix_y = [[math.cos(angles[1]), 0, math.sin(angles[1])], [0, 1, 0], [-math.sin(angles[1]), 0, math.cos(angles[1])]]
        rotation_matrix_z = [[math.cos(angles[2]), -math.sin(angles[2]), 0], [math.sin(angles[2]), math.cos(angles[2]), 0], [0, 0, 1]]

        screen.fill(WHITE)

        cube_vertices_projected = [[0 for i in range(2)] for j in range(len(cube_vertices)*len(cube_vertices[0])*len(cube_vertices[0][0]))]
        i = 0
        for cv1 in cube_vertices:
            for cv2 in cv1:
                for vertex in cv2:
                    cube_vertices_projected[i] = np.dot(projection_matrix, np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, vertex))))*SCALE+CENTER
                    #pygame.draw.circle(screen, BLACK, cube_vertices_projected[i], 5)
                    i += 1
        
        cube_vertices_projected = np.reshape(cube_vertices_projected, (4, 4, 4, 2))

        # face 1 (blue)
        if (angles[0] < math.pi/2 or angles[0] > 3*math.pi/2) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2):
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][0], cube_vertices_projected[0][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][3], cube_vertices_projected[0][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][3], cube_vertices_projected[0][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][0], cube_vertices_projected[0][0][0], LINE_THICKNESS)

            pygame.draw.line(screen, BLUE, cube_vertices_projected[0][1][0], cube_vertices_projected[0][1][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][2][0], cube_vertices_projected[0][2][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][1], cube_vertices_projected[0][3][1], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][2], cube_vertices_projected[0][3][2], LINE_THICKNESS)
    
        # face 2 (green)
        if not ((angles[0] < math.pi/2 or angles[0] > 3*math.pi/2) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2)):
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][0], cube_vertices_projected[3][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][3], cube_vertices_projected[3][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][3], cube_vertices_projected[3][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][0], cube_vertices_projected[3][0][0], LINE_THICKNESS)

            pygame.draw.line(screen, GREEN, cube_vertices_projected[3][1][0], cube_vertices_projected[3][1][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][2][0], cube_vertices_projected[3][2][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][1], cube_vertices_projected[3][3][1], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][2], cube_vertices_projected[3][3][2], LINE_THICKNESS)
            
        # face 3 (black)
        if not ((angles[0] > math.pi) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2)):
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][0], cube_vertices_projected[0][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][3], cube_vertices_projected[3][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][3], cube_vertices_projected[3][0][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][0], cube_vertices_projected[0][0][0], LINE_THICKNESS)

            pygame.draw.line(screen, BLACK, cube_vertices_projected[1][0][0], cube_vertices_projected[1][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][1], cube_vertices_projected[3][0][1], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[2][0][3], cube_vertices_projected[2][0][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][2], cube_vertices_projected[0][0][2], LINE_THICKNESS)
        
        # face 4 (yellow)
        if (angles[0] > math.pi) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2):
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][0], cube_vertices_projected[0][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][3], cube_vertices_projected[3][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][3], cube_vertices_projected[3][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][0], cube_vertices_projected[0][3][0], LINE_THICKNESS)

            pygame.draw.line(screen, YELLOW, cube_vertices_projected[1][3][0], cube_vertices_projected[1][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][1], cube_vertices_projected[3][3][1], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[2][3][3], cube_vertices_projected[2][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][2], cube_vertices_projected[0][3][2], LINE_THICKNESS)

        # face 5 (orange)
        if (angles[1] < math.pi):
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][0], cube_vertices_projected[0][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][0], cube_vertices_projected[3][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][0], cube_vertices_projected[3][0][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][0], cube_vertices_projected[0][0][0], LINE_THICKNESS)

            pygame.draw.line(screen, ORANGE, cube_vertices_projected[1][0][0], cube_vertices_projected[1][3][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][1][0], cube_vertices_projected[3][1][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[2][3][0], cube_vertices_projected[2][0][0], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][2][0], cube_vertices_projected[0][2][0], LINE_THICKNESS)

        # face 6 (red)
        if not (angles[1] < math.pi):
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][0][3], cube_vertices_projected[0][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][3][3], cube_vertices_projected[3][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][3][3], cube_vertices_projected[3][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][0][3], cube_vertices_projected[0][0][3], LINE_THICKNESS)

            pygame.draw.line(screen, RED, cube_vertices_projected[1][0][3], cube_vertices_projected[1][3][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[0][1][3], cube_vertices_projected[3][1][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[2][3][3], cube_vertices_projected[2][0][3], LINE_THICKNESS)
            pygame.draw.line(screen, BLACK, cube_vertices_projected[3][2][3], cube_vertices_projected[0][2][3], LINE_THICKNESS)
            

        # button (reset cube orientation)
        pygame.draw.rect(screen, GREY, (20, HEIGHT-40, 150, 20))

        smallfont = pygame.font.SysFont('Corbel', 20) 
        text = smallfont.render('reset cube orientation', True, BLACK)
        
        screen.blit(text, (25, HEIGHT-35))

        pygame.display.update()
        print(angles)

    pygame.quit()

if __name__ == "__main__":
    main()