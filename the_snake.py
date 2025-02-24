from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.
    Определяет общую структуру и методы для объектов на игровом поле.
    """

    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = None

    def draw(self):
        """Метод для отрисовки, нужен для наследуемых классов."""
        pass


class Apple(GameObject):
    """Класс для создания игрового объекта Яблоко."""

    def __init__(self):
        super().__init__((0, 0))
        self.body_color = APPLE_COLOR
        self.randomize_position([])

    def randomize_position(self, snake_positions):
        """
        Метод для добавления Яблока в случайной ячейке игрового поля,
        исключая позиции Змейки.
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Метод для отрисовки (отображения) Яблока на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс для создания игрового объекта Змейка."""

    def __init__(self):
        self.length = 1
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.position = self.get_head_position()
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод, который перемещает змейку в выбранном направлении,
        обрабатывает рост и столкновения.
        """
        self.update_direction()

        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        new_head = (
            ((head_x // GRID_SIZE + direction_x) % GRID_WIDTH) * GRID_SIZE,
            ((head_y // GRID_SIZE + direction_y) % GRID_HEIGHT) * GRID_SIZE,
        )

        self.positions.insert(0, new_head)
        self.position = new_head

        # Если не растём, удаляем последний сегмент
        # и запоминаем его для стирания
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

        # Проверка на столкновение (начиная с 1-го сегмента)
        if new_head in self.positions[1:]:
            self.reset()

    # Метод draw класса Snake
    def draw(self):
        """
        Отрисовывает змейку на игровом поле, включая голову и тело.
        Стирает последний сегмент, если змейка не растёт.
        """
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

    def get_head_position(self):
        """Метод, который возвращает координаты головы Змейки."""
        return self.positions[0]

    def reset(self):
        """
        Метод, который возвращает Змейку
        в исходное состояние в случае проигрыша.
        """
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.last = None


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    """
    Основная логика игры: инициализирует объекты,
    обрабатывает ввод и обновляет экран.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == "__main__":
    main()
