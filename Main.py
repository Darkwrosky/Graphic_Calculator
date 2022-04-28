from os import getcwd, chdir, mkdir, path

import matplotlib.pyplot as plt
import pygame
from colors import *
from numpy import array, sqrt, e, pi


def calculate(expression):
    return eval(expression)


def crea_cartella(current_path):
    pathdirdata = current_path + '\plots'
    if not path.isdir(pathdirdata):
        mkdir('plots')
    return pathdirdata


def draw_window(expression, result, graph_name):
    WIN.fill(col_light_grey)
    pygame.draw.rect(WIN, col_White, input_bar)
    pygame.draw.rect(WIN, col_White, result_bar)

    text = font.render(expression, True, col_Black)
    WIN.blit(text, (input_bar.x + space, input_bar.y + input_bar_h // 2 - text.get_height() // 2))
    text = font.render(result, True, col_Black)
    WIN.blit(text, (result_bar.x + space, result_bar.y + input_bar_h // 2 - text.get_height() // 2))
    plot = pygame.transform.scale(pygame.image.load(path.join("plots", graph_name)).convert(),
                                  (plot_width, plot_height))
    WIN.blit(plot, (space, space))
    pygame.display.update()


def graph(expression, nfig):
    x = array([x for x in range(-100, 100, 1)])/10
    try:
        y = eval(expression)
    except Exception as exc:
        return "sfondo.png", str(exc)

    chdir(plot_dir)
    plt.figure(num=1, figsize=(6, 6))
    plt.plot(x, y, label=expression)
    plt.legend()
    plt.grid()
    plt.savefig(f"fig_n{nfig}.png")
    plt.close()
    chdir(curr_path)
    return f"fig_n{nfig}.png", expression


def main():
    run = True
    expression = ""
    result = ""
    graph_name = "sfondo.png"
    nfig = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    expression = expression[:-1]
                elif event.key == pygame.K_RETURN:
                    if "x" in expression:
                        nfig += 1
                        graph_name, result = graph(expression, nfig)
                    else:
                        try:
                            result = str(calculate(expression))
                        except Exception as exc:
                            result = str(exc)
                else:
                    expression += event.unicode
        draw_window(expression, result, graph_name)
    pygame.quit()


width, height = 600, 800
WIN = pygame.display.set_mode((width, height))
FPS = 60
clock = pygame.time.Clock()
pygame.font.init()
font = pygame.font.SysFont("comicsans", 30)
space = 5
input_bar_w, input_bar_h = width - 2 * space, 50
input_bar = pygame.Rect(width // 2 - input_bar_w // 2, height - input_bar_h - space, input_bar_w, input_bar_h)
result_bar = pygame.Rect(width // 2 - input_bar_w // 2, height - 2 * (input_bar_h + space), input_bar_w, input_bar_h)
plot_width, plot_height = width-2*space, height-2*input_bar_h - 4*space
curr_path = getcwd()
plot_dir = crea_cartella(curr_path)
print(curr_path, plot_dir)
if __name__ == "__main__":
    main()
