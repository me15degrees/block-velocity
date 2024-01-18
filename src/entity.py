import pygame as pg
import math

class Square(pg.Rect):
    def __init__(
        self, 
        position: tuple[int, int], 
        size: int, 
        color=pg.Color(0, 0, 255),
        vel=0.0,
        acc=0.0,
        screen_size=(1280, 720),
        condition=None,
    ):
        super().__init__(position, (size, size))

        self.font = pg.font.Font(None, 20)
        self.color = color
        self.velocity = vel
        self.acceleration = acc
        self.screen_x, self.screen_y = screen_size 
        self.condition = condition

        # set real center
        self.center = position

    def update(self, dt):
        self.velocity += self.acceleration * dt
        self.x += self.velocity * dt

        # loop in screen size
        if self.left >= self.screen_x:
            self.reset_position()  #chama o método reset_position ao atingir a borda direita
        elif self.right <= 0:
            self.left = self.screen_x

        # apply condition
        if self.condition is not None:
            self.acceleration = self.condition(self.velocity, self.acceleration)

    def reset_position(self):
        # edefine a posição para as coordenadas iniciais
        self.x = self.center[0] - self.width // 2
        self.y = self.center[1] - self.height // 2

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self)
        
        text = self.font.render(f"Vel: {self.velocity:.2f}, Acc: {self.acceleration:.2f}", True, pg.Color('white'))
        text_rect = text.get_rect(center=(self.center[0], self.top - 20))
        screen.blit(text, text_rect)

        self.draw_arrow(screen, pg.Color('magenta'), self.center, (self.center[0] + self.velocity, self.center[1]))
        if self.acceleration:
            self.draw_arrow(screen, pg.Color('white'), self.center, (self.center[0] + self.acceleration, self.center[1]))

    def draw_arrow(self, screen, color, start, end, size=20):
        # Calcula o ângulo da seta
        angle = math.atan2(end[1] - start[1], end[0] - start[0])

        # Calcula as coordenadas da ponta da seta
        arrow_length = 20
        arrow_end = (end[0] - arrow_length * math.cos(angle), end[1] - arrow_length * math.sin(angle))

        # Desenha a linha do vetor
        pg.draw.line(screen, color, start, arrow_end, 2)

        # Desenha a ponta da seta
        pg.draw.polygon(screen, color, [
            (end[0] - size * math.cos(angle + math.pi/6), end[1] - size * math.sin(angle + math.pi/6)),
            (end[0] - size * math.cos(angle - math.pi/6), end[1] - size * math.sin(angle - math.pi/6)),
            (end[0], end[1])
        ])

    def get_info(self):
        return f"Velocidade: {self.velocity:.2f} | Aceleração: {self.acceleration:.2f}"
