import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Drawing Program")
    clock = pygame.time.Clock()

    radius = 15
    mode = 'blue'
    draw_mode = 'line'
    color = (255, 255, 255)
    points = []
    shapes = []

    start_pos = None  # For shape drawing

    colors = {
        '1': (255, 255, 255),  # White
        '2': (255, 0, 0),      # Red
        '3': (0, 255, 0),      # Green
        '4': (0, 0, 255),      # Blue
        '5': (255, 255, 0),    # Yellow
        '6': (0, 255, 255),    # Cyan
        '7': (255, 0, 255),    # Magenta
        '8': (0, 0, 0),        # Black
    }

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT or \
               (event.type == pygame.KEYDOWN and (
                   (event.key == pygame.K_w and ctrl_held) or
                   (event.key == pygame.K_F4 and alt_held) or
                   event.key == pygame.K_ESCAPE)):
                return

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
                elif event.key == pygame.K_o:
                    draw_mode = 'rectangle'
                elif event.unicode in colors:
                    color = colors[event.unicode]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start_pos = event.pos
                    if draw_mode == 'line':
                        points.append(event.pos)
                        points = points[-256:]
                elif event.button == 4:  # Scroll up
                    radius = min(200, radius + 1)
                elif event.button == 5:  # Scroll down
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and draw_mode in ['rectangle', 'circle']:
                    end_pos = event.pos
                    shapes.append((draw_mode, start_pos, end_pos, radius, color))
                    start_pos = None

            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    if draw_mode == 'line':
                        position = event.pos
                        points.append(position)
                        points = points[-256:]
                    elif draw_mode == 'eraser':
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, radius)

        screen.fill((0, 0, 0))

        # Draw shapes
        for shape in shapes:
            tool, start, end, size, shape_color = shape
            if tool == 'rectangle':
                rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
                pygame.draw.rect(screen, shape_color, rect, size)
            elif tool == 'circle':
                center = ((start[0] + end[0]) // 2, (start[1] + end[1]) // 2)
                rx = abs(end[0] - start[0]) // 2
                ry = abs(end[1] - start[1]) // 2
                pygame.draw.ellipse(screen, shape_color, (center[0] - rx, center[1] - ry, rx * 2, ry * 2), size)

        # Draw line trail
        if draw_mode == 'line':
            i = 0
            while i < len(points) - 1:
                drawLineBetween(screen, i, points[i], points[i + 1], radius, mode)
                i += 1

        pygame.display.flip()
        clock.tick(60)

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == 'blue':
        color = (c1, c1, c2)
    elif color_mode == 'red':
        color = (c2, c1, c1)
    elif color_mode == 'green':
        color = (c1, c2, c1)

    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, color, (x, y), width)

main()
