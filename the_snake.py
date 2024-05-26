from random import choice, randint
import pygame

# Направления движения.
UP: tuple[int, int] = (0, -1)
DOWN: tuple[int, int] = (0, 1)
LEFT: tuple[int, int] = (-1, 0)
RIGHT: tuple[int, int] = (1, 0)

# Константы для размеров поля и сетки.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Скорость игры.
SPEED = 10

# Цвета объектов и поля.
APPLE_COLOR: tuple[int, int, int] = (255, 0, 0)
SNAKE_COLOR: tuple[int, int, int] = (0, 255, 0)
BORDER_COLOR: tuple[int, int, int] = (93, 216, 228)
BOARD_BACKGROUND_COLOR: tuple[int, int, int] = (0, 0, 0)

# Настройка игрового окна.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля.
pygame.display.set_caption('Змейка')
# Объект для управления временем.
clock = pygame.time.Clock()


class GameObject:
    def __init__(self, body_color: tuple[int, int, int]):
        self.body_color: tuple[int, int, int] = body_color
        self.position: tuple[int, int] = (0, 0)

    def draw(self) -> None:
        # Метод для отрисовки объекта на заданной поверхности.
        pass


class Apple(GameObject):
    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        # Задает случайные координаты для яблока.
        self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                         randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        # Отрисовывает яблоко на экране.
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    def __init__(self, body_color: tuple[int, int, int] = SNAKE_COLOR):
        super().__init__(body_color)
        self.length: int = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.last = None

    def update_direction(self):
        # Обновление направления движения змейки.
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple[int, int]:
        # Возвращает текущее положение головы змейки.
        return self.positions[0]

    def move(self) -> None:
        # Перемещает змейку в указанном направлении.
        get_head = self.get_head_position()
        dx, dy = self.direction
        new_head = (((get_head[0] + (dx * GRID_SIZE)) % SCREEN_WIDTH),
                    ((get_head[1] + (dy * GRID_SIZE)) % SCREEN_HEIGHT))

        if len(self.positions) > 2 and new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self) -> None:
        # Сбрасывает состояние змейки до начального.
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
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


def handle_keys(snake: Snake) -> None:
    # Обработка нажатий клавиш для изменения направления движения змейки.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    # Основная функция игры.
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
