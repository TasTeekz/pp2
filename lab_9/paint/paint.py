import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drawing Program")
    clock = pygame.time.Clock()

    radius = 5
    mode = 'blue'
    draw_mode = 'line'
    color = (255, 255, 255)
    points = []
    shapes = []

    start_pos = None

    # Цвета для горячих клавиш 1-8
    colors = {
        '1': (255, 255, 255),
        '2': (255, 0, 0),
        '3': (0, 255, 0),
        '4': (0, 0, 255),
        '5': (255, 255, 0),
        '6': (0, 255, 255),
        '7': (255, 0, 255),
        '8': (0, 0, 0),
    }

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Обработка нажатий клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    mode = 'red'
                elif event.key == pygame.K_g:
                    mode = 'green'
                elif event.key == pygame.K_b:
                    mode = 'blue'
                elif event.key == pygame.K_c:
                    draw_mode = 'circle'
                elif event.key == pygame.K_e:
                    draw_mode = 'eraser'
                elif event.key == pygame.K_l:
                    draw_mode = 'line'
                    points = []  # сбрасываем точки линии
                elif event.key == pygame.K_o:
                    draw_mode = 'rectangle'
                elif event.key == pygame.K_s:
                    draw_mode = 'square'
                elif event.key == pygame.K_t:
                    draw_mode = 'right_triangle'
                elif event.key == pygame.K_q:
                    draw_mode = 'equilateral_triangle'
                elif event.key == pygame.K_h:
                    draw_mode = 'rhombus'
                elif event.unicode in colors:
                    color = colors[event.unicode]  # установка цвета

            # Обработка нажатия мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos
                    if draw_mode == 'line':
                        points = [event.pos]  # начать новую линию

            # Отпускание мыши: завершить фигуру
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and draw_mode in ['rectangle', 'circle', 'square', 'right_triangle', 'equilateral_triangle', 'rhombus']:
                    end_pos = event.pos
                    shapes.append((draw_mode, start_pos, end_pos, radius, color))
                    start_pos = None

            # Движение мыши с зажатой кнопкой
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if draw_mode == 'line':
                        position = event.pos
                        points.append(position)
                        points = points[-256:]  # ограничение на длину линии
                    elif draw_mode == 'eraser':
                        # Сохраняем "ластик" как черный круг
                        shapes.append(('eraser', event.pos, radius))

        screen.fill((0, 0, 0))  # очищаем экран каждый кадр

        # Отрисовка сохраненных фигур
        for shape in shapes:
            tool, start, end, *rest = shape
            if tool == 'eraser':
                pygame.draw.circle(screen, (0, 0, 0), start, end)  # рисуем черный круг
                continue

            size, shape_color = rest
            x1, y1 = start
            x2, y2 = end

            if tool == 'rectangle':
                rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
                pygame.draw.rect(screen, shape_color, rect, size)
            elif tool == 'square':
                side = min(abs(x2 - x1), abs(y2 - y1))
                rect = pygame.Rect(x1, y1, side if x2 >= x1 else -side, side if y2 >= y1 else -side)
                pygame.draw.rect(screen, shape_color, rect, size)
            elif tool == 'circle':
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                rx = abs(x2 - x1) // 2
                ry = abs(y2 - y1) // 2
                pygame.draw.ellipse(screen, shape_color, (center[0] - rx, center[1] - ry, rx * 2, ry * 2), size)
            elif tool == 'right_triangle':
                pygame.draw.polygon(screen, shape_color, [start, (x1, y2), (x2, y2)], size)
            elif tool == 'equilateral_triangle':
                side = min(abs(x2 - x1), abs(y2 - y1))
                height = int(side * (3 ** 0.5) / 2)
                direction = 1 if y2 > y1 else -1
                points_tri = [
                    (x1, y1),
                    (x1 + side, y1),
                    (x1 + side // 2, y1 + height * direction)
                ]
                pygame.draw.polygon(screen, shape_color, points_tri, size)
            elif tool == 'rhombus':
                mid_x = (x1 + x2) // 2
                mid_y = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2
                rhombus_points = [
                    (mid_x, y1),
                    (x2, mid_y),
                    (mid_x, y2),
                    (x1, mid_y)
                ]
                pygame.draw.polygon(screen, shape_color, rhombus_points, size)

        # Отрисовка линии (если выбрана)
        if draw_mode == 'line' and len(points) > 1:
            for i in range(len(points) - 1):
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)

        pygame.display.flip()
        clock.tick(60)

# Функция рисования линии с градиентом

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))
    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)
    else:
        color = (255, 255, 255)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()