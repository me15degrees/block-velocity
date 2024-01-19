import pygame as pg
from entity import Square

FPS = 60
SCREEN_SIZE = (1920, 1080)

def main():
    pg.init()

    # Inicializa o subsistema de exibição antes de carregar a imagem
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption("Jogo com Plano de Fundo")

    original_background = pg.image.load("img/14661403-plano-de-fundo-do-nivel-do-jogo-estrada-magica-e-paisagem-de-fantasia-no-estilo-cartoon-estrada-campo-verde-e-floresta-ilustracaoial-vetor.jpg")
    BACKGROUND_IMAGE = pg.transform.scale(original_background, SCREEN_SIZE).convert()

    screen.blit(BACKGROUND_IMAGE, (0, 0))
    
    clock = pg.time.Clock()
    font = pg.font.Font(None, 33)

    squares = [
        Square((100, 830), 80, color=pg.Color(153, 51, 155), vel=200, screen_size=SCREEN_SIZE),
        Square((100, 830), 80, color=pg.Color(102, 155, 102), vel=0, acc=50, screen_size=SCREEN_SIZE),
        Square((100, 830), 80, color=pg.Color(0, 76, 153), vel=300, acc=-50, screen_size=SCREEN_SIZE, condition=lambda x, y: -y if x < -600 else y),
    ]

    # Inicializa as variáveis para controlar a ativação de quadrados
    current_square = 0
    delay_timer = 0

    # main loop
    running = True
    while running:
        clock.tick(FPS)
        dt = clock.get_time() / 1000  # millisec to sec

        for event in pg.event.get():
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                return

        screen.blit(BACKGROUND_IMAGE, (0, 0))

        # Atualiza e desenha apenas o quadrado atual
        square = squares[current_square]
        
        # Adiciona um atraso se a velocidade for 0
        # if square.velocity == 0:
        #     delay_timer += dt
        #     if delay_timer >= 1:  # 1 segundo de atraso
        #         delay_timer = 0
        #         square.velocity = square.initial_vel
        # else:
            
        square.update(dt)

        square.draw(screen)

        text = font.render(f"Quadrado {current_square + 1} - {square.get_info()}", True, pg.Color('white'))
        text_rect = text.get_rect(left=15, top=20)
        screen.blit(text, text_rect)

        # Verifica se o quadrado atingiu a borda direita
        if square.right >= SCREEN_SIZE[0]:
            current_square += 1

            # Verifica se há mais quadrados
            if current_square < len(squares):
                square.reset_position()
            else:
                running = False  # Sai do loop se todos os quadrados foram exibidos

        # Atualiza o título da janela
        pg.display.set_caption(f"fps: {round(clock.get_fps(), 2)}")
        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
