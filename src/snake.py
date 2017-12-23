import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN, wrapper
from random import randint

win_height = 20
win_width = 60

def collision(object1, object2):
    return object1.to_array() == object2.to_array()


curses.initscr()
win = curses.newwin(win_height, win_width, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)


class Object:
    def __init__(self, y_pos, x_pos, char=''):
        self.y_pos=y_pos
        self.x_pos=x_pos
        self.char=char

    def to_array(self):
        return [self.y_pos, self.x_pos]

    def randomize(self):
        self.y_pos = randint(1, 18)
        self.x_pos = randint(1, 58)

    def set_image(self, char):
        self.char = char

    def draw(self):
        win.addch(self.y_pos, self.x_pos, self.char)


class Snake:
    speed = 1
    isBoosted = False

    def __init__(self, char):
        self.char=char
        self.body=[Object(4,10,self.char), Object(4,9,self.char), Object(4,8,self.char)]

    def move_right(self):
        self.body.insert(0, Object(self.body[0].y_pos, self.body[0].x_pos + self.speed, self.char))

    def move_left(self):
        self.body.insert(0, Object(self.body[0].y_pos, self.body[0].x_pos - self.speed, self.char))

    def move_up(self):
        self.body.insert(0, Object(self.body[0].y_pos - self.speed, self.body[0].x_pos, self.char))

    def move_down(self):
        self.body.insert(0, Object(self.body[0].y_pos + self.speed, self.body[0].x_pos, self.char))

    def to_array(self):
        arr = []
        for part in self.body:
            arr.insert(0, [part.y_pos, part.x_pos])
        return arr

    def boost(self):
        if self.isBoosted:
            self.speed = 1
            self.isBoosted = False
            return
        self.speed = 2
        self.isBoosted = True

    def draw(self):
        self.body[0].draw()


def main(stdscr):
    key = KEY_RIGHT
    score = 0

    snake = Snake('#')

    food = Object(10,20, '*')

    food.draw()

    while key != 27:
        win.border(0)
        win.addstr(0, 2, 'Score : ' + str(score) + ' ')
        win.addstr(0, 27, ' SNAKE ')
        win.timeout(150 - (len(snake.body)/5 + len(snake.body)/10)%120)

        prev_key = key
        event = win.getch()
        key = event

        if key == ord(' '):
            key = -1
            while key != ord(' '):
                key = win.getch()
            key = prev_key
            continue

        if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
            key = prev_key

        if key == KEY_RIGHT:
            snake.move_right()
        if key == KEY_LEFT:
            snake.move_left()
        if key == KEY_UP:
            snake.move_up()
        if key == KEY_DOWN:
            snake.move_down()

        if snake.body[0].y_pos == 0: snake.body[0].y_pos = 18
        if snake.body[0].x_pos == 0: snake.body[0].x_pos = 58
        if snake.body[0].y_pos == 19: snake.body[0].y_pos = 1
        if snake.body[0].x_pos == 59: snake.body[0].x_pos = 1

        if snake.to_array()[0] in snake.to_array()[1:]: break

        if collision(snake.body[0], food):
            food.randomize()
            score += 1
            food.draw()
        else:
            last = snake.body.pop()
            win.addch(last.y_pos, last.x_pos, ' ')
        snake.draw()

    curses.endwin()
    print("\nScore - " + str(score))

wrapper(main)