from random import choice, randint

import pygame

# Направления движения.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
FIELD_SIZE = GRID_WIDTH * GRID_HEIGHT
#  Скорость игры.
SPEED = 20
#  Цвета объектов и поля.
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BORDER_COLOR = (93, 216, 228)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Настройка игрового окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля.
pygame.display.set_caption('Змейка')
#  Объект для управления временем .
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    def __init__(self, body_color=BOARD_BACKGROUND_COLOR,
                 position=POSITION) -> None:
        self.position = position
        self.body_color = body_color

    #  Базовый метод отрисовки объектов.
    def draw(self) -> None:
        pass


class Apple(GameObject):
    def __init__(self, body_color=APPLE_COLOR,
                 position=POSITION) -> None:
        super().__init__(body_color, position)
        self.randomize_position()

    #  Задаёт объекту случайные координаты.
    def randomize_position(self) -> None:
        self.position = (randint(0, GRID_HEIGHT) * GRID_SIZE,
                         randint(0, GRID_WIDTH) * GRID_SIZE)

    #  Отрисовка яблока.
    def draw(self) -> None:
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):

    def __init__(self, body_color=SNAKE_COLOR,
                 position=POSITION) -> None:
        super().__init__(body_color, position)
        self.reset()
        self.direction = RIGHT
        self.length = 1
        self.next_direction = None
        self.last = None

    #  Начальное состояние после столкновения с собой.
    def reset(self):
        self.position = [self.position]
        self.last = None
        self.direction = choice([RIGHT, LEFT, UP, DOWN])

    #  Метод обновления направления после нажатия на кнопку.
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    #  Возвращает координаты новой головы.
    def new_head(self) -> tuple[int, int]:
        pos_x, pos_y = self.get_head_position()
        return (
            (pos_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (pos_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

    #  Увиличивает змейку на один сегмент.
    def grow_up(self, new_segment: tuple[int, int]) -> None:
        self.position.insert(0, new_segment)

    #  Уменьшает змейку на один сегмент с конца.
    def cut_tail(self) -> None:
        self.position.pop()

    #  Возвращает позицию головы змейки
    def get_head_position(self) -> tuple[int, int]:
        return self.position[0]

    #  Обновляет позицию змейки
    def move(self, new_head: tuple[int, int]) -> None:
        self.position.insert(0, new_head)
        self.last = self.position.pop()

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


#  Функция обработки действий пользователя
def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    running = True
    while running:
        clock.tick(SPEED)
        handle_keys(Snake)
        Snake.update_direction()
        Snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()
        # Тут опишите основную логику игры.
    pygame.quit()


if __name__ == '__main__':
    main()
