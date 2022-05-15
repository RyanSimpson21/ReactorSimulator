import pygame as pg
import math
import numpy as np
import reactor_configs

nx, ny = 900, 600
pg.init()
screen = pg.display.set_mode((nx, ny))


def assembly_type(string):
    if string == 'absorber_rod':
        return AbsorberRod
    elif string == "control_rod":
        return ControlRod
    elif string == "fuel_rod":
        return FuelRod


class Reactor:
    def __init__(self, type_of_reactor):
        self.power_output = 0.0
        self.assemblies = []
        self.width = reactor_configs.reactors[type_of_reactor]["size"][0]
        self.height = reactor_configs.reactors[type_of_reactor]["size"][1]
        for i, (k1, v1) in enumerate(reactor_configs.reactors[type_of_reactor]["assembly_config"].items()):
            self.assemblies.append([])
            for j, (k2, v2) in enumerate(reactor_configs.reactors[type_of_reactor]["assembly_config"][k1].items()):
                self.assemblies[i].append(assembly_type(v2["assembly"])(v2["x_pos"], v2["y_pos"], self))

    def step_update(self):
        pass


class PWR(Reactor):
    def __init__(self, type_of_reactor):
        super().__init__(type_of_reactor)
        self.water_boration = 2500
        self.primary_temp = 293
        self.secondary_temp = 293
        self.primary_pressure = 10
        self.secondary_pressure = 10

    def step_update(self):
        pass


class Assembly:
    def __init__(self, x, y, parent):
        self.reactor = parent
        self.x = x
        self.y = y
        self.temp = 293
        self.rect = pg.Rect(self.x, self.y, 64, 64)
        self.rect.center = (self.x * (nx // 12) + nx//3, self.y * (nx // 12) + nx//6)
        self.clicked = False
        self.color = (255, 255, 255)
        self.default_color = (255, 255, 255)

    def step_update(self):
        pass

    def in_hit_box(self, x, y):

        if self.rect.collidepoint(x, y):
            print(f"clicked on {self}")
            return True
        else:
            return False

    def render(self):
        if self.clicked:
            selecter_rect = self.rect.copy()
            selecter_rect.width += 8
            selecter_rect.height += 8
            selecter_rect.x -= 4
            selecter_rect.y -= 4
            pg.draw.rect(screen, (255, 255, 255), selecter_rect, width=4)

        pg.draw.rect(screen, self.default_color, self.rect)


class ControlRod(Assembly):
    def __init__(self, x, y, parent):
        super().__init__(x, y, parent)
        self.type = "control_rod"
        self.insertion = 1.0
        self.default_color = (64, 64, 64)

    def step_update(self):
        pass


class AbsorberRod(Assembly):
    def __init__(self, x, y, parent):
        super().__init__(x, y, parent)
        self.type = "absorber_rod"
        self.insertion = 1.0
        self.default_color = (102, 17, 25)

    def step_update(self):
        pass


class FuelRod(Assembly):
    def __init__(self, x, y, parent):
        super().__init__(x, y, parent)
        self.type = "fuel_rod"
        self.U235 = 0.02
        self.U238 = 0.98
        self.Pu239 = 0.0
        self.Cs137 = 0.0
        self.Xe135 = 0.0
        self.I135 = 0.0
        self.Tc99 = 0.0
        self.Tc99m = 0.0
        self.Zr93 = 0.0
        self.Pd107 = 0.0
        self.default_color = (40, 255, 0)


class Gui:
    def __init__(self):
        self.buttons = []
        options_button = OptionsButton(self, 0)
        info_button = InfoButton(self, 1)
        self.buttons.append(options_button)
        self.buttons.append(info_button)

    def render(self):
        pg.draw.rect(screen, (255, 255, 255), (nx - 40, 0, 40, 600), width=2)


class Button:
    def __init__(self, gui, pos):
        self.gui = gui
        self.clicked = False
        self.name = "none_button"
        self.pos = pos
        self.rect = pg.Rect(nx - 36, 4 + 36 * pos, 32, 32)

    def render(self):
        if self.clicked:
            pg.draw.rect(screen, (255, 255, 255), self.rect)
        else:
            pg.draw.rect(screen, (0, 0, 0), self.rect)
            pg.draw.rect(screen, (255, 255, 255), self.rect, width=2)

    def in_hit_box(self, x, y):
        return self.rect.collidepoint(x, y)

    def hexagon(self, center_x, center_y, radius, **kwargs):
        points = ((center_x - radius, center_y), (center_x - 0.5 * radius, center_y - 0.866 * radius),
                  (center_x + 0.5 * radius, center_y - 0.866 * radius), (center_x + radius, center_y),
                  (center_x + 0.5 * radius, center_y + 0.866 * radius), (center_x - 0.5 * radius, center_y + 0.866 * radius))
        return points


class OptionsButton(Button):
    def __init__(self, gui, pos):
        super().__init__(gui, pos)
        self.name = "options_button"

    def render(self):
        if self.clicked:
            pg.draw.rect(screen, (255, 255, 255), self.rect)
            pg.draw.circle(screen, (0, 0, 0), (nx - 20, self.pos * 36 + 20), 12)
        else:
            pg.draw.circle(screen, (255, 255, 255), (nx - 20, self.pos * 36 + 20), 12)
            pg.draw.rect(screen, (255, 255, 255), self.rect, width=2)


class InfoButton(Button):
    def __init__(self, gui, pos):
        super().__init__(gui, pos)
        self.name = "info_button"

    def render(self):
        if self.clicked:
            pg.draw.rect(screen, (255, 255, 255), self.rect)
            pg.draw.polygon(screen, (0, 0, 0), self.hexagon(nx - 20, 40 * self.pos + 16, 12), 3)

        else:
            pg.draw.polygon(screen, (255, 255, 255), self.hexagon(nx - 20, 40 * self.pos + 16, 12), 3)
            pg.draw.rect(screen, (255, 255, 255), self.rect, width=2)


def render_all():
    global reactor
    for i in reactor.assemblies:
        for j in i:
            j.render()


reactor = PWR("small_pwr")


def main():
    last_clicked = None
    last_gui_clicked = None
    global reactor
    running = True
    assembly_list = []
    reactor = PWR("small_pwr")
    gui = Gui()

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                event_x, event_y = pg.mouse.get_pos()
                if event.button == 1:
                    if last_clicked is not None:
                        last_clicked.clicked = False
                    for i in reactor.assemblies:
                        for j in i:
                            if j.in_hit_box(event_x, event_y):
                                j.clicked = True
                                if last_clicked is not None and last_clicked != j:
                                    last_clicked.clicked = False
                                last_clicked = j
                                print(j.clicked)
                    for i in gui.buttons:
                        if i.in_hit_box(event_x, event_y):
                            if last_gui_clicked == i:
                                if i.clicked:
                                    i.clicked = False
                                elif not i.clicked:
                                    i.clicked = True
                            else:
                                i.clicked = True
                                if last_gui_clicked is not None:
                                    last_gui_clicked.clicked = False
                            last_gui_clicked = i

        screen.fill((0, 0, 0))

        gui.render()
        for i in gui.buttons:
            i.render()

        render_all()

        pg.display.flip()


main()
