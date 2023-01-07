from v6 import CubeStep2
from v6 import COLORS, COLORS_LIST
import pygame
import numpy as np
import math

pygame.init()

def main():
    cube = CubeStep2()
    draw(cube)
    print(np.array(cube.get_cube_state(sticker_notation=True)))
    print("#\n#\n#\n\n\n#\n#\n#")
    print(np.array(cube.get_cube_state(sticker_notation=False)))
    print("#\n#\n#\n\n\n#\n#\n#")
    print(np.array(cube.get_cube_state(sticker_notation=True)))

#
# 3D render
#

LINE_THICKNESS = 2

angles = (0, 0, 0)

def get_screen_size():
    try:
        WIDTH, HEIGHT = pygame.display.get_surface().get_size()
    except:
        WIDTH, HEIGHT = 500, 500
    CENTER = WIDTH/2, HEIGHT/2
    SCALE = min(WIDTH, HEIGHT)/12
    return WIDTH, HEIGHT, CENTER, SCALE

WIDTH, HEIGHT, CENTER, SCALE = get_screen_size()

class Button():
    def __init__(self, screen, resizeable, x, y, width, height, text, action, color=COLORS["GREY"], fontname="Arial", fontsize=0, textcolor=COLORS["BLACK"]):
        self.screen = screen
        self.resizeable = resizeable
        if self.resizeable:
            self.x = x / WIDTH
            self.y = y / HEIGHT
            self.width = width / WIDTH
            self.height = height / HEIGHT
        else:
            self.x = x
            self.y = y
            self.width = width
            self.height = height
        self.text = text
        self.action = action
        self.color = color
        self.fontname = fontname
        self.fontsize = fontsize
        self.textcolor = textcolor

    def calc_coords(self):
        if self.resizeable:
            x = self.x * WIDTH
            y = self.y * HEIGHT
            width = self.width * WIDTH
            height = self.height * HEIGHT
        else:
            x, y, width, height = self.x, self.y, self.width, self.height
        if x < 0:
            x += WIDTH
        if y < 0:
            y += HEIGHT
        return x, y, width, height

    def draw(self):
        x, y, width, height = self.calc_coords()

        if self.fontsize:    
            fontsize = self.fontsize
        else:
            fontsize = int(0.8 * height)
        
        font = pygame.font.SysFont(self.fontname, fontsize) 
        self.textrender = font.render(self.text, True, self.textcolor)

        if not width:
            width = 0.5 * height + self.textrender.get_width()

        pygame.draw.rect(self.screen, self.color, (x, y, width, height))

        self.screen.blit(self.textrender, (x+0.25*height, y+(height-fontsize)/2))

    def pressed(self, mouse):
        x, y, width, height = self.calc_coords()
        if not width:
            width = 0.5 * height + self.textrender.get_width()
        if x <= mouse[0] <= x+width and y <= mouse[1] <= y+height:
            button_action(self.action)

def button_action(action):
    if action == "reset_orientation":
        global angles
        angles = (0, 0, 0)

def draw(cube, colors_dict=COLORS, colors_numbers=COLORS_LIST[2:]):
    if cube.size != 3:
        raise Exception("The Cube is not of size 3")
    global WIDTH, HEIGHT, CENTER, SCALE, angles

    cube_vertices = [[[[x, y, z] for x in range(-3, 4, 2)] for y in range(-3, 4, 2)] for z in range(-3, 4, 2)]

    projection_matrix = [[1, 0, 0], [0, 1, 0]]

    motion_matrix_1 = [[0.0, -0.02], [0.02, 0], [0.0, 0.0]]
    motion_matrix_2 = [[0.0, -0.02], [0.02, 0], [0.0, 0.0]]

    pygame.display.set_caption("3D Cube")
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    WIDTH, HEIGHT, CENTER, SCALE = get_screen_size()

    # init buttons
    orient_button = Button(screen, True, 20, -40, 0, 20, "reset cube orientation", "reset_orientation")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # all keys on the keyboard in the number row and the first row
                # of letters can be assigned to a string of moves which are
                # executed when the corresponding key is pressed. This can be
                # used to slowly walk through a solution, for example. The
                # current moves (in the correct order) lead to the superflip.
                elif event.key == pygame.K_1:
                    movestring = "U_"
                    cube.turn(movestring)
                elif event.key == pygame.K_2:
                    movestring = "R2"
                    cube.turn(movestring)
                elif event.key == pygame.K_3:
                    movestring = "F_"
                    cube.turn(movestring)
                elif event.key == pygame.K_4:
                    movestring = "B_"
                    cube.turn(movestring)
                elif event.key == pygame.K_5:
                    movestring = "R_"
                    cube.turn(movestring)
                elif event.key == pygame.K_6:
                    movestring = "B2"
                    cube.turn(movestring)
                elif event.key == pygame.K_7:
                    movestring = "R_"
                    cube.turn(movestring)
                elif event.key == pygame.K_8:
                    movestring = "U2"
                    cube.turn(movestring)
                elif event.key == pygame.K_9:
                    movestring = "L_"
                    cube.turn(movestring)
                elif event.key == pygame.K_0:
                    movestring = "B2"
                    cube.turn(movestring)
                elif event.key == pygame.K_q:
                    movestring = "R_"
                    cube.turn(movestring)
                elif event.key == pygame.K_w:
                    movestring = "U'"
                    cube.turn(movestring)
                elif event.key == pygame.K_e:
                    movestring = "D'"
                    cube.turn(movestring)
                elif event.key == pygame.K_r:
                    movestring = "R2"
                    cube.turn(movestring)
                elif event.key == pygame.K_t:
                    movestring = "F_"
                    cube.turn(movestring)
                elif event.key == pygame.K_z:
                    movestring = "R'"
                    cube.turn(movestring)
                elif event.key == pygame.K_u:
                    movestring = "L_"
                    cube.turn(movestring)
                elif event.key == pygame.K_i:
                    movestring = "B2"
                    cube.turn(movestring)
                elif event.key == pygame.K_o:
                    movestring = "U2"
                    cube.turn(movestring)
                elif event.key == pygame.K_p:
                    movestring = "F2"
                    cube.turn(movestring)
            elif event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT, CENTER, SCALE = get_screen_size()
            elif event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                motion = pygame.mouse.get_rel()
                if angles[0] < math.pi:
                    motion = np.dot(motion_matrix_1, motion)
                else:
                    motion = np.dot(motion_matrix_2, motion)
                angles = (angles + motion) % (2*math.pi)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                orient_button.pressed(pygame.mouse.get_pos())


        rotation_matrix_x = [[1, 0, 0], [0, math.cos(angles[0]), -math.sin(angles[0])], [0, math.sin(angles[0]), math.cos(angles[0])]]
        rotation_matrix_y = [[math.cos(angles[1]), 0, math.sin(angles[1])], [0, 1, 0], [-math.sin(angles[1]), 0, math.cos(angles[1])]]
        rotation_matrix_z = [[math.cos(angles[2]), -math.sin(angles[2]), 0], [math.sin(angles[2]), math.cos(angles[2]), 0], [0, 0, 1]]

        screen.fill(COLORS["WHITE"])

        cube_vertices_projected = [[0 for i in range(2)] for j in range(len(cube_vertices)*len(cube_vertices[0])*len(cube_vertices[0][0]))]
        i = 0
        for cv1 in cube_vertices:
            for cv2 in cv1:
                for vertex in cv2:
                    cube_vertices_projected[i] = np.dot(projection_matrix, np.dot(rotation_matrix_z, np.dot(rotation_matrix_y, np.dot(rotation_matrix_x, vertex))))*SCALE+CENTER
                    i += 1
        
        cube_vertices_projected = np.reshape(cube_vertices_projected, (4, 4, 4, 2))

        # face 0 (white)
        if not ((angles[0] > math.pi) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2)):
            #faces
            for i in range(3):
                for j in range(3):
                    pygame.draw.polygon(screen, colors_dict[colors_numbers[cube.get_cube_state(sticker_notation=True)[0][i][j]]], (cube_vertices_projected[i][0][j], cube_vertices_projected[i+1][0][j], cube_vertices_projected[i+1][0][j+1], cube_vertices_projected[i][0][j+1]))
            
            #lines
            for i in range(4):
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[i][0][0], cube_vertices_projected[i][0][3], LINE_THICKNESS)
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[0][0][i], cube_vertices_projected[3][0][i], LINE_THICKNESS)
        
        # face 1 (yellow)
        if (angles[0] > math.pi) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2):
            #faces
            for i in range(3):
                for j in range(3):
                    pygame.draw.polygon(screen, colors_dict[colors_numbers[cube.get_cube_state(sticker_notation=True)[1][i][2-j]]], (cube_vertices_projected[i][3][j], cube_vertices_projected[i+1][3][j], cube_vertices_projected[i+1][3][j+1], cube_vertices_projected[i][3][j+1]))

            #lines
            for i in range(4):
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[i][3][0], cube_vertices_projected[i][3][3], LINE_THICKNESS)
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[0][3][i], cube_vertices_projected[3][3][i], LINE_THICKNESS)

        # face 2 (green)
        if not ((angles[0] < math.pi/2 or angles[0] > 3*math.pi/2) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2)):
            #faces
            for i in range(3):
                for j in range(3):
                    pygame.draw.polygon(screen, colors_dict[colors_numbers[cube.get_cube_state(sticker_notation=True)[2][i][j]]], (cube_vertices_projected[3][i][j], cube_vertices_projected[3][i+1][j], cube_vertices_projected[3][i+1][j+1], cube_vertices_projected[3][i][j+1]))

            #lines
            for i in range(4):
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[3][0][i], cube_vertices_projected[3][3][i], LINE_THICKNESS)
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[3][i][0], cube_vertices_projected[3][i][3], LINE_THICKNESS)

        # face 3 (blue)
        if (angles[0] < math.pi/2 or angles[0] > 3*math.pi/2) != (angles[1] < math.pi/2 or angles[1] > 3*math.pi/2):
            #faces
            for i in range(3):
                for j in range(3):
                    pygame.draw.polygon(screen, colors_dict[colors_numbers[cube.get_cube_state(sticker_notation=True)[3][i][2-j]]], (cube_vertices_projected[0][i][j], cube_vertices_projected[0][i+1][j], cube_vertices_projected[0][i+1][j+1], cube_vertices_projected[0][i][j+1]))
            
            #lines
            for i in range(4):
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[0][0][i], cube_vertices_projected[0][3][i], LINE_THICKNESS)
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[0][i][0], cube_vertices_projected[0][i][3], LINE_THICKNESS)

        # face 4 (red)
        if not (angles[1] < math.pi):
            #faces
            for i in range(3):
                for j in range(3):
                    pygame.draw.polygon(screen, colors_dict[colors_numbers[cube.get_cube_state(sticker_notation=True)[4][i][j]]], (cube_vertices_projected[i][j][3], cube_vertices_projected[i+1][j][3], cube_vertices_projected[i+1][j+1][3], cube_vertices_projected[i][j+1][3]))

            #lines
            for i in range(4):
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[i][0][3], cube_vertices_projected[i][3][3], LINE_THICKNESS)
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[0][i][3], cube_vertices_projected[3][i][3], LINE_THICKNESS)

        # face 5 (orange)
        if (angles[1] < math.pi):
            #faces
            for i in range(3):
                for j in range(3):
                    pygame.draw.polygon(screen, colors_dict[colors_numbers[cube.get_cube_state(sticker_notation=True)[5][i][2-j]]], (cube_vertices_projected[i][j][0], cube_vertices_projected[i+1][j][0], cube_vertices_projected[i+1][j+1][0], cube_vertices_projected[i][j+1][0]))

            #lines
            for i in range(4):
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[i][0][0], cube_vertices_projected[i][3][0], LINE_THICKNESS)
                pygame.draw.line(screen, COLORS["BLACK"], cube_vertices_projected[0][i][0], cube_vertices_projected[3][i][0], LINE_THICKNESS)

        # draw buttons
        orient_button.draw()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()