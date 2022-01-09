import pygame
import PygameHaze as pgh


pygame.init()

pygame.display.set_caption("Tic Tac Toe")


class Game:
    def __init__(self):

        self.W, self.H = 500, 500
        self.WIN = pygame.display.set_mode((self.W, self.H))

        self.clock = pygame.time.Clock()
        self.reset_game()

        self.turn = 1
        pygame.display.set_caption("Tic Tac Toe")

    def reset_game(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.spots = pgh.ButtonManager(self.WIN)

        [[self.spots.add_button(x*(self.W//3), y*(self.W//3), self.W//3, self.H//3, pgh.WHITE, pgh.WHITE, pgh.WHITE, pgh.WHITE, font_size=200) for y in range(3)] for x in range(3)]

    def draw(self):
        self.WIN.fill(pgh.WHITE)

        self.spots.draw()

        line_width = 10
        for i in range(3):
            pygame.draw.line(self.WIN, pgh.BLACK, (0, i * (self.H // 3) - (line_width // 2)),
                             (self.W, i * (self.H // 3) - (line_width // 2)), line_width)
            pygame.draw.line(self.WIN, pgh.BLACK, (i * (self.W // 3) - (line_width // 2), 0),
                             (i * (self.W // 3) - (line_width // 2), self.H), line_width)

        self.spots.update()  # u don't have to call this method every time just when the text changes or you want to change the buttons position
        i = 0
        for y, column in enumerate(self.board):
            for x, item in enumerate(column):
                self.spots[i].text = "o" if item == 2 else ("x" if item == 1 else "")
                i += 1

        pygame.display.update()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(-1)
            elif pgh.left_click(event):
                for button in self.spots:
                    if button.button_rect.collidepoint(event.pos) and not button.pressed:
                        button.event_handler(event)
                        self.board[event.pos[0]//(self.W//3)][event.pos[1]//(self.H//3)] = self.turn + 1
                        self.turn += 1
                        pygame.display.set_caption(f"""Tic Tac Toe | {"o's" if self.turn == 1 else "x's"} turn""")
                        self.turn = self.turn % 2

    def check_for_winner(self):
        return (
            self.board[0][0] == self.board[0][1] == self.board[0][2] and self.board[0][2] != 0
        ) or (
            self.board[1][0] == self.board[1][1] == self.board[1][2] and self.board[1][2] != 0
        ) or (
            self.board[2][0] == self.board[2][1] == self.board[2][2] and self.board[2][2] != 0
        ) or (
            self.board[0][0] == self.board[1][0] == self.board[2][0] and self.board[2][0] != 0
        ) or (
            self.board[0][1] == self.board[1][1] == self.board[2][1] and self.board[2][1] != 0
        ) or (
            self.board[0][2] == self.board[1][2] == self.board[2][2] and self.board[2][2] != 0
        ) or (
            self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[2][2] != 0
        ) or (
            self.board[2][0] == self.board[1][1] == self.board[0][2] and self.board[0][2] != 0
        )

    def is_full(self):
        for column in self.board:
            for item in column:
                if item == 0:
                    return False
        return True

    def run(self):
        while True:
            self.clock.tick(60)
            self.draw()
            self.event_handler()
            if self.check_for_winner():
                if self.turn == 1:
                    print("'x' won")
                else:
                    print("'o' won")
                self.reset_game()
            if self.is_full():
                print("tie")
                self.reset_game()


if __name__ == '__main__':
    game = Game()
    game.run()
