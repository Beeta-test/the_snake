from random import choice, randint
import pygame as pg

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
DEFAULT_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
# Скорость игры.
SPEED = 10

# Цвета объектов и поля.
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
BORDER_COLOR = (93, 216, 228)
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Настройка игрового окна.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
# Заголовок окна игрового поля.
pg.display.set_caption('Змейка')
# Объект для управления временем.
clock = pg.time.Clock()


class GameObject:
    """Родительский класс игры."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализация игрового объекта с указанным цветом тела."""
        self.body_color = body_color
        self.position = DEFAULT_POS

    def draw(self) -> None:
        """Метод для отрисовки объекта на заданной поверхности."""
        raise NotImplementedError('Отрисовка производится в дочерних классах.')


class Apple(GameObject):
    """Дочерний класс GameObject для объекта Apple."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация яблока с указанным цветом тела."""
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self, occupied_positions=[DEFAULT_POS]) -> None:
        """Задает случайные координаты для яблока, избегая занятых позиций."""
        while self.position in occupied_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

    def draw(self) -> None:
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний класс GameObject для объекта Snake."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Инициализация змейки с указанным цветом тела."""
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.last = None

    def update_direction(self) -> None:
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self) -> tuple[int, int]:
        """Возвращает текущее положение головы змейки."""
        return self.positions[0]

    def move(self) -> None:
        """Перемещает змейку в указанном направлении."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (((head_x + (dx * GRID_SIZE)) % SCREEN_WIDTH),
                    ((head_y + (dy * GRID_SIZE)) % SCREEN_HEIGHT))

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self) -> None:
        """Сбрасывает змейку до начального состояния."""
        self.positions = [self.position]
        self.length = 1
        self.direction = choice([RIGHT, LEFT, UP, DOWN])
        self.last = None

    def draw(self) -> None:
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake: Snake) -> None:
    """Обработка нажатий клавиш для изменения направления движения змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main() -> None:
    """Основная функция игры."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
