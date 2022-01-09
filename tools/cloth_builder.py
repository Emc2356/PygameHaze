from tkinter.filedialog import asksaveasfile
from typing import Dict, Union, TextIO
import PygameHaze as pgh
import pygame
import json
import json
import os


class ClothBuilder:
    def __init__(self):
        self.W: int = 650
        self.TB_W: int = 200
        self.H: int = 650
        self.WIN: pygame.surface.Surface = pygame.display.set_mode((self.W + self.TB_W, self.H))

        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.FPS: int = 60

        self.data: Dict[str, list] = {
            "points": [],
            "connections": []
        }

        self.running: bool = True

        self.first_click_location: list[Union[int, float], Union[int, float]] = []

        self.gravity: Union[int, float] = 0.2

        self.point_rad: Union[int, float] = 4
        self.line_width: Union[int, float] = 1

        self.save_button: pgh.Button = pgh.Button(
            self.WIN, self.W + self.TB_W // 2 - 180//2, 5, 180, 45, inactive_color=pgh.GREEN,
            hover_inactive_color=pgh.DK_GREEN, text="save", on_click=self.save, on_release=self.save
        )

        pygame.display.set_caption("Cloth Builder")

    def draw(self) -> None:
        self.WIN.fill(pgh.BLACK)
        pygame.draw.rect(self.WIN, pgh.PURPLE, [self.W, 0, self.TB_W, self.H])
        self.save_button.draw()

        for cn in self.data["connections"]:
            pygame.draw.line(self.WIN, pgh.WHITE, cn.pointA.pos, cn.pointB.pos, self.line_width)

        for point in self.data["points"]:
            pygame.draw.circle(self.WIN, pgh.RED if point.locked else pgh.GREEN, point.pos, self.point_rad)

        pygame.display.update()

    def save(self) -> None:

        file_extensions = [
            ["JSON files", "*.json"],
            ["cloth files", "*.cloth"],
            ["All files", "*.*"]
        ]
        f = asksaveasfile(filetypes=file_extensions, defaultextension=file_extensions, title="Save As",
                          initialfile="untitled", mode="w")
        if f is not None:
            try:
                json.dump(self.data, f, indent=4)
                f.close()
            except IOError:
                f.close()

    def event_handler(self) -> None:
        for event in pygame.event.get():
            self.save_button.event_handler(event)
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit(-1)
            elif pgh.left_click(event):
                if event.pos[0] < self.W - 10:
                    self.first_click_location = list(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.first_click_location:
                    if self.first_click_location == list(event.pos):  # place a point
                        for p in self.data["points"]:
                            if pgh.get_distance(*event.pos, *p.pos) < self.point_rad*2:
                                break
                        else:
                            self.data["points"].append(pgh.Point(*self.first_click_location, False, self.gravity))
                    else:
                        p1: pgh.Point = None
                        p2: pgh.Point = None
                        for point in self.data["points"]:
                            if pgh.get_distance(*point.pos, *self.first_click_location) < self.point_rad:
                                p1 = point
                                break

                        for point in self.data["points"]:
                            if pgh.get_distance(*point.pos, *event.pos) < self.point_rad:
                                p2 = point
                                break

                        if p1 is not None and p2 is not None:
                            for cn in self.data["connections"]:
                                if (cn.pointA == p1 and cn.pointB == p2 and cn.length == pgh.get_distance(*p1.pos, *p2.pos)) or \
                                        (cn.pointB == p1 and cn.pointA == p2 and cn.length == pgh.get_distance(*p1.pos, *p2.pos)):
                                    break
                            else:  # the else statement is triggered when the for loop isn't broken
                                self.data["connections"].append(pgh.Connection(p1, p2, pgh.get_distance(*p1.pos, *p2.pos)))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                for point in self.data["points"]:
                    if pgh.get_distance(*point.pos, *event.pos) < self.point_rad:
                        point.locked = not point.locked
                        break

    def run(self) -> None:
        while self.running:
            self.clock.tick(self.FPS)
            self.event_handler()
            self.draw()


if __name__ == '__main__':
    pygame.init()

    cloth_builder = ClothBuilder()
    cloth_builder.run()
