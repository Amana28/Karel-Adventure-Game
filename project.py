"""
Final Project: karel Adventure Game
Project by: Amanuel Tesfaye
"""


import tkinter
import time
import random
from PIL import ImageTk
from simpleimage import SimpleImage


SUN_SIZE = 100
SUN_NW_X = 200
SUN_NW_Y = 20
GROUND_PIXELS = 18
SIZE_OF_WORLD = 12
OBSTACLE_SIZE = 70
BACKGROUND_SPEED = -2
OBSTACLE_SPEED = -5
SPIKE_SIZE = 30
MAXIMUM_HEIGHT = 300
RAISE_KAREL = -5
LOWER_KAREL = 5


def main():
    background_image = create_bigger_background('images/Background.png')
    width = background_image.width
    height = background_image.height
    canvas = make_canvas(width * SIZE_OF_WORLD, height, 'Karel adventure game')
    time.sleep(5)
    # background
    converted = convert_simple_image(background_image)
    background = canvas.create_image(0, 0, anchor='nw', image=converted)
    # objects in canvas
    canvas.create_oval(SUN_NW_X, SUN_NW_Y, SUN_NW_X+SUN_SIZE, SUN_NW_Y+SUN_SIZE, fill='orange', outline='orange')
    obstacles_list1 = create_obstacles1(canvas, height)
    obstacles_list2 = create_obstacles2(canvas, height)

    # karel avatar
    karel = SimpleImage('images/karel_avatar.png')
    converted2 = convert_simple_image(karel)
    karel_x = 200
    initial_y = height - (karel.height + GROUND_PIXELS)
    karel_y = initial_y  # 518
    karel_avatar = canvas.create_image(karel_x, karel_y, anchor='nw', image=converted2)
    eyes = canvas.create_rectangle(0, 0, 0, 0)

    # Finishing Line
    finishing_line = SimpleImage('images/finishing_line.png')
    converted3 = convert_simple_image(finishing_line)
    finishing_line_image = canvas.create_image(11000, height - (GROUND_PIXELS + finishing_line.height), anchor='nw', image=converted3)

    lowering = False

    # beginning scene
    beginning_scene(canvas, karel_x, karel_y)

    for i in range(100000):
        mouse_y = canvas.winfo_pointery()
        canvas.move(background, BACKGROUND_SPEED, 0)
        canvas.move(finishing_line_image, OBSTACLE_SPEED, 0)
        for j in range(5):
            canvas.move(obstacles_list1[j], OBSTACLE_SPEED, 0)
            canvas.move(obstacles_list2[j], OBSTACLE_SPEED, 0)
        if not lowering:
            if mouse_y < (height * 3/4) and karel_y >= MAXIMUM_HEIGHT:
                canvas.move(karel_avatar, 0, RAISE_KAREL)
                karel_y += RAISE_KAREL
                lowering = False
            else:
                lowering = True
        elif lowering:
            if karel_y < initial_y:
                canvas.move(karel_avatar, 0, LOWER_KAREL)
                karel_y += LOWER_KAREL
                lowering = True
            elif karel_y == initial_y:
                lowering = False
        # delete previously drawn eyes
        canvas.delete(eyes)
        # animate the eyes - f_x and f_y are the distance between nw corner of karel and her eyes
        eyes = animate_eyes(canvas, i, karel_x, karel_y)
        if did_karel_crash(canvas, obstacles_list1, obstacles_list2):
            canvas.create_text(450, 300, anchor='w', text='GAME OVER', font='Times 50', fill='red')
            break
        if finishing_line_reached(canvas, finishing_line_image, finishing_line):
            finishing_scene(canvas)
            break
        canvas.update()
        # pause
        time.sleep(1/100)
    canvas.mainloop()


def create_bigger_background(filename):

    image = SimpleImage(filename)
    width = image.width
    height = image.height
    bigger_background = SimpleImage.blank(width * SIZE_OF_WORLD, height)
    for y in range(height):
        for x in range(width):
            pixel = image.get_pixel(x, y)
            bigger_background.set_pixel(x, y, pixel)
            for i in range(SIZE_OF_WORLD):
                if i != 0:
                    bigger_background.set_pixel(x + (width * i), y, pixel)
    return bigger_background


def convert_simple_image(simple_image):
    converted = ImageTk.PhotoImage(simple_image.pil_image)
    return converted


def did_karel_crash(canvas, obstacle_list1, obstacle_list2):
    overlapping = False
    for i in range(5):
        obstacle_coordinates1 = canvas.coords(obstacle_list1[i])
        x1 = obstacle_coordinates1[0]
        y1 = obstacle_coordinates1[1]
        x4 = obstacle_coordinates1[6]
        y4 = obstacle_coordinates1[7]
        result = canvas.find_overlapping(x1, y1 + SPIKE_SIZE, x4, y4)
        if len(result) > 2:
            canvas.itemconfig(obstacle_list1[i], fill='red', outline='black')
            overlapping = True
            break
    for i in range(5):
        obstacle_coordinates2 = canvas.coords(obstacle_list2[i])
        x1 = obstacle_coordinates2[0]
        y1 = obstacle_coordinates2[1]
        x2 = obstacle_coordinates2[2]
        y2 = obstacle_coordinates2[3]
        x3 = obstacle_coordinates2[4]
        y3 = obstacle_coordinates2[5]
        result = canvas.find_overlapping(x1, y1, x3, y2)
        if len(result) > 2:
            canvas.itemconfig(obstacle_list2[i], fill='red', outline='black')
            overlapping = True
            break
    return overlapping


def animate_eyes(canvas, i, karel_x, karel_y):

    eyes_size = 17
    f_x = 21
    f_y = 8
    blink = 0
    integer_division = i // 5
    # if remainder is even - close eyes
    if integer_division % 16 == 0:
        blink = i % 5
    # if remainder is odd - open eyes
    elif integer_division % 16 == 1:
        blink = 5 - (i % 5)
    x1 = karel_x + f_x
    y1 = karel_y + f_y + (blink * 6)
    x2 = karel_x + f_x + eyes_size
    # 1.5 multiplication is to make a rectangle
    # used 10 instead of f_x because it shouldn't change
    y2 = karel_y + 10 + eyes_size*1.5
    eyes = canvas.create_rectangle(x1, y1, x2, y2, fill='black', outline='blue')
    return eyes


def create_obstacles1(canvas, height):
    starting_points = [1000, 1250, 1500, 1750]
    obstacles_list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(5):
        starting_point = random.choice(starting_points) + (2000*i)
        x1 = starting_point
        y1 = height - (OBSTACLE_SIZE + GROUND_PIXELS)
        x2 = starting_point + OBSTACLE_SIZE//4
        y2 = height - (OBSTACLE_SIZE + GROUND_PIXELS + SPIKE_SIZE)
        x3 = starting_point + (OBSTACLE_SIZE//2)
        y3 = height - (OBSTACLE_SIZE + GROUND_PIXELS)
        x4 = starting_point + (OBSTACLE_SIZE//2)
        y4 = height - GROUND_PIXELS
        x5 = starting_point
        y5 = height - GROUND_PIXELS
        list_of_coordinates = [x1, y1, x2, y2, x3, y3, x4, y4, x5, y5]
        obstacle = canvas.create_polygon(list_of_coordinates, fill='black', activefill='orange')
        obstacles_list1[i] = obstacle
    return obstacles_list1


def create_obstacles2(canvas, height):
    starting_points = [2000, 2250, 2500, 2750]
    obstacles_list2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    for i in range(5):
        starting_point = random.choice(starting_points) + (2000*i)
        x1 = starting_point
        y1 = height - GROUND_PIXELS
        x2 = starting_point + OBSTACLE_SIZE//2
        y2 = height -(GROUND_PIXELS + OBSTACLE_SIZE)
        x3 = starting_point + OBSTACLE_SIZE
        y3 = height - GROUND_PIXELS
        list_of_coordinates = [x1, y1, x2, y2, x3, y3]
        obstacle = canvas.create_polygon(list_of_coordinates, fill='black', activefill='orange')
        obstacles_list2[i] = obstacle
    return obstacles_list2


def absolute(number):
    # get absolute value of a number
    if number < 0:
        number *= -1
    else:
        number = 0
    return number


def beginning_scene(canvas, karel_x, karel_y):
    while True:
        dotdot = canvas.create_text(karel_x, karel_y - 20, anchor='w', fill='black', font='Verdana 10', text='Do doo roo, doo doo', activefill='blue')
        game_name = canvas.create_text(515, 100, anchor='w', fill='black', font='Verdana 20', text='Karel Adventure Game')
        canvas.update()
        time.sleep(5)
        list = ['0', '1', '2', 'Ready', '3', '2', '1', 'GO!', ]
        for item in list:
            x_position = 570
            if item == 'GO!':
                color = 'green'
                x_position = 420
            elif item == '1':
                color = 'yellow'
            elif item == 'Ready':
                color = 'black'
                x_position = 350
            else:
                color = 'red'
            displayed_item = canvas.create_text(x_position, 290, anchor='w', text=item, font='Times 200', fill=color)
            canvas.update()
            time.sleep(2)
            canvas.delete(displayed_item)
            canvas.update()
            time.sleep(1)
        canvas.delete(dotdot)
        canvas.delete(game_name)
        canvas.update()
        break


def finishing_scene(canvas):
    while True:
        text = canvas.create_text(300, 300, anchor='w', text='Congratulations, You Won!', font='Times 50', fill='green')
        canvas.update()
        time.sleep(3)
        canvas.delete(text)
        canvas.update()
        time.sleep(1)
        canvas.create_text(450, 300, anchor='w', text='Code in place 2020!', font='Times 40', fill='black', activefill='orange')
        break


def finishing_line_reached(canvas, finishing_line_image, finishing_line):
    overlapping = False
    passing = 150
    finishing_line_image_coordinates = canvas.coords(finishing_line_image)
    x1 = finishing_line_image_coordinates[0]
    y1 = finishing_line_image_coordinates[1]
    x2 = x1 + finishing_line.width
    y2 = y1 + finishing_line.height
    result = canvas.find_overlapping(x1 + passing, y1, x2 + passing, y2)
    if len(result) > 2:
        overlapping = True
    return overlapping


# Do not modify #
# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.


def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
