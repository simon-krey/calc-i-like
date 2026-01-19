import pygame
from pygame import gfxdraw
import math


LIGHT_GRAY_BUTTON_COLOR = (92, 92, 95)
GRAY_BUTTON_COLOR = (42, 42, 44)
YELLOW_BUTTON_COLOR = (255, 159, 10)


class Button:
    def __init__(
        self,
        pos,
        text,
        equasion_text,
        color,
        font: pygame.font.Font,
        diameter=115,
        equason_function=None,
    ):
        # pos is the upper left corner
        self.equasion_text = equasion_text
        self.center_pos = pos
        self.pos = (pos[0] - diameter / 2, pos[1] - diameter / 2)
        self.text = text
        self.color = color
        self.diameter = diameter
        self.font = font
        self.equasion_function = equason_function

        # add offset to align calculator to screen so that the coords of the buttons can be relative
        self.offset = (62, 337)
        self.pos = (
            self.pos[0] + self.offset[0],
            self.pos[1] + self.offset[1],
        )
        self.center_pos = (
            self.center_pos[0] + self.offset[0],
            self.center_pos[1] + self.offset[1],
        )

    def render(self, screen: pygame.Surface):
        render_pos = (
            self.center_pos[0] + self.diameter / 2,
            self.center_pos[1] + self.diameter / 2,
        )
        gfxdraw.aacircle(
            screen,
            int(self.center_pos[0]),
            int(self.center_pos[1]),
            int(self.diameter / 2),
            self.color,
        )

        gfxdraw.filled_circle(
            screen,
            int(self.center_pos[0]),
            int(self.center_pos[1]),
            int(self.diameter / 2),
            self.color,
        )

        rendered_text = self.font.render(self.text, True, (255, 255, 255))

        text_render_pos = (
            self.pos[0] + self.diameter / 2 - rendered_text.size[0] / 2,
            self.pos[1] + self.diameter / 2 - rendered_text.size[1] / 2,
        )

        screen.blit(rendered_text, text_render_pos)

    def update(self) -> bool:
        if pygame.mouse.get_just_released()[0]:
            mouse_pos = pygame.mouse.get_pos()
            distance = math.sqrt(
                (self.center_pos[0] - mouse_pos[0]) ** 2
                + (self.center_pos[1] - mouse_pos[1]) ** 2
            )

            if distance <= self.diameter / 2:
                return True

        return False

    def get_equasion(self, current_equasion):
        if self.equasion_function != None:
            return self.equasion_function(current_equasion)

        return current_equasion + self.equasion_text


clear_on_click = False
equasion_historie = []
current_equasion = ""


def _reverse_prefix(e):
    if e == "" or e == "%":
        return ""

    try:
        if e[-1] == "%":
            float(e[:-1])
            return str(round(math_eval("(" + e[:-1] + ")" + "*-1"), 100)) + "%"

        else:
            float(e)
            return str(round(math_eval("(" + e + ")" + "*-1"), 100))

    except Exception:
        return e


def condense(num: str):
    if len(num) > 11:
        return f"{float(num): 9e}"

    else:
        return num


def _solve(e):
    global equasion_historie
    global clear_on_click

    if e == "":
        return ""

    try:
        result = condense(str(round(math_eval(e), 100)))
        equasion_historie.insert(0, e)
        return result

    except Exception as e:
        if type(e) == ZeroDivisionError:
            clear_on_click = True
            return "Are you stupid?"
    
        clear_on_click = True
        return "Fehler"


def _clear(e):
    global equasion_historie

    equasion_historie = []

    return ""


def math_eval(equasion: str):
    equasion = equasion.replace("%", "*0.01")

    return eval(equasion)


def main():
    global equasion_historie
    global current_equasion
    global clear_on_click

    pygame.init()

    screen = pygame.display.set_mode((500, 900))
    pygame.display.set_caption("Calculator")

    clock = pygame.Clock()

    # make shure there are enougth preloadet fonts for all sizes

    preloadet_fonts = [pygame.font.Font("SF-Pro.ttf", i) for i in range(0, 71)]

    button_font = preloadet_fonts[50]
    result_font_size = 70
    history_font_size = 50
    min_font_size = 20

    rendered_history_rect = pygame.rect.Rect(0, 0, 0, 0)

    buttons = [
        Button(
            (0, 0),
            "⌫",
            "",
            LIGHT_GRAY_BUTTON_COLOR,
            button_font,
            equason_function=lambda e: e[:-1] if len(e) > 0 else "",
        ),
        Button(
            (125, 0),
            "AC",
            "",
            LIGHT_GRAY_BUTTON_COLOR,
            button_font,
            equason_function=_clear,
        ),
        Button((250, 0), "%", "%", LIGHT_GRAY_BUTTON_COLOR, button_font),
        Button((375, 0), "/", "/", YELLOW_BUTTON_COLOR, button_font),
        Button((0, 125), "7", "7", GRAY_BUTTON_COLOR, button_font),
        Button((125, 125), "8", "8", GRAY_BUTTON_COLOR, button_font),
        Button((250, 125), "9", "9", GRAY_BUTTON_COLOR, button_font),
        Button((375, 125), "*", "*", YELLOW_BUTTON_COLOR, button_font),
        Button((0, 250), "4", "4", GRAY_BUTTON_COLOR, button_font),
        Button((125, 250), "5", "5", GRAY_BUTTON_COLOR, button_font),
        Button((250, 250), "6", "6", GRAY_BUTTON_COLOR, button_font),
        Button((375, 250), "-", "-", YELLOW_BUTTON_COLOR, button_font),
        Button((0, 375), "1", "1", GRAY_BUTTON_COLOR, button_font),
        Button((125, 375), "2", "2", GRAY_BUTTON_COLOR, button_font),
        Button((250, 375), "3", "3", GRAY_BUTTON_COLOR, button_font),
        Button((375, 375), "+", "+", YELLOW_BUTTON_COLOR, button_font),
        Button(
            (0, 500),
            "+/-",
            "",
            GRAY_BUTTON_COLOR,
            button_font,
            equason_function=_reverse_prefix,
        ),
        Button((125, 500), "0", "0", GRAY_BUTTON_COLOR, button_font),
        Button((250, 500), ",", ".", GRAY_BUTTON_COLOR, button_font),
        Button(
            (375, 500),
            "=",
            "",
            YELLOW_BUTTON_COLOR,
            button_font,
            equason_function=_solve,
        ),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if rendered_history_rect != None:
                        if rendered_history_rect.collidepoint(pygame.mouse.get_pos()):
                            current_equasion = equasion_historie[0]
                            equasion_historie.pop(0)

        for b in buttons:
            if b.update():
                if clear_on_click:
                    clear_on_click = False
                    current_equasion = ""
                current_equasion = b.get_equasion(current_equasion)

        screen.fill((0, 0, 0))

        for b in buttons:
            b.render(screen)

        current_font_size = result_font_size
        result_font = preloadet_fonts[current_font_size]

        while (
            result_font.size(current_equasion)[0] > 480
            and current_font_size > min_font_size
        ):
            current_font_size -= 1
            result_font = preloadet_fonts[current_font_size]

        if result_font.size(current_equasion)[0] > 480:
            current_equasion = current_equasion[:-1]

        rendered_result = result_font.render(current_equasion, True, (255, 255, 255))
        result_render_pos = (490 - rendered_result.size[0], 170)

        screen.blit(rendered_result, result_render_pos)

        current_font_size = history_font_size
        history_font = preloadet_fonts[current_font_size]

        while (
            history_font.size(
                equasion_historie[0] if len(equasion_historie) > 0 else ""
            )[0]
            > 480
            and current_font_size > min_font_size
        ):
            current_font_size -= 1
            history_font = preloadet_fonts[current_font_size]

        rendered_history = history_font.render(
            equasion_historie[0] if len(equasion_historie) > 0 else "",
            True,
            (100, 100, 100),
        )

        history_render_pos = (490 - rendered_history.size[0], 100)

        rendered_history_rect = pygame.Rect(*history_render_pos, *rendered_history.size)

        screen.blit(rendered_history, history_render_pos)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
