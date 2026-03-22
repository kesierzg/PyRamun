import pygame
import sys

pygame.init()

is_dark_mode = True

def get_colors():
    if is_dark_mode:
        return (0, 0, 0), (255, 255, 255)
    else:
        return (255, 255, 255), (0, 0, 0)

language = "EN"

translations = {
    "EN": {
        "start": "START",
        "choose_player": "CHOOSE YOUR PYRAMUN",
        "choose_enemy": "CHOOSE ENEMY",
        "you": "You",
        "enemy": "Enemy",
        "fight": "FIGHT",
        "pyramun": "PYRM",
        "bag": "BAG",
        "run": "RUN"
    },
    "PL": {
        "start": "ZACZNIJ",
        "choose_player": "WYBIERZ PYRAMUNA",
        "choose_enemy": "WYBIERZ PRZECIWNIKA",
        "you": "Ty",
        "enemy": "Przeciwnik",
        "fight": "WALCZ",
        "pyramun": "PYRM",
        "bag": "PLECAK",
        "run": "UCIEKAJ"
    }
}

BASE_WIDTH, BASE_HEIGHT = 320, 240
SCALES = [1, 2, 3]
scale_index = 1
SCALE = SCALES[scale_index]

screen = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

pygame.display.set_caption("PyRamun - Pokemon clone")

def update_title(fps=0):
    pygame.display.set_caption(f"PyRamun - {BASE_WIDTH*SCALE}x{BASE_HEIGHT*SCALE} | {int(fps)} FPS")

update_title(0)

clock = pygame.time.Clock()

enemy_img = pygame.transform.scale(
    pygame.image.load("assets/gfx/enemy.png").convert_alpha(), (80, 80)
)

player_img = pygame.transform.scale(
    pygame.image.load("assets/gfx/frend.png").convert_alpha(), (96, 96)
)
font_small = pygame.font.Font("assets/dogicapixel.otf", 8)
font_big = pygame.font.Font("assets/dogicapixel.otf", 16)

game_state = "MENU"

selected_pyramun = None
enemy_pyramun = None

pyramun_list = ["Chadmandor", "Sqqqrtle", "Bulwazaur", "Pikablu", "Pejot", "Sandskrew", "Psikabra"]

def draw_text(text, x, y, center=False, size="big"):
    current_font = font_small if size == "small" else font_big
    bg, fg = get_colors()
    img = current_font.render(text, True, fg)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    game_surface.blit(img, rect)

menu_index = 0

running = True
while running:
    bg, fg = get_colors()
    game_surface.fill(bg)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                scale_index = (scale_index + 1) % len(SCALES)
                SCALE = SCALES[scale_index]
                screen = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
                update_title()

            if event.key == pygame.K_l:
                language = "PL" if language == "EN" else "EN"

            if event.key == pygame.K_n:
                is_dark_mode = not is_dark_mode

            if game_state == "MENU":
                if event.key == pygame.K_RETURN:
                    game_state = "PLAYER_SELECT"

            elif game_state == "PLAYER_SELECT":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(pyramun_list)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(pyramun_list)
                if event.key == pygame.K_RETURN:
                    selected_pyramun = pyramun_list[menu_index]
                    game_state = "ENEMY_SELECT"
                    menu_index = 0

            elif game_state == "ENEMY_SELECT":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(pyramun_list)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(pyramun_list)
                if event.key == pygame.K_RETURN:
                    enemy_pyramun = pyramun_list[menu_index]
                    game_state = "BATTLE"
                    menu_index = 0

            elif game_state == "BATTLE":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 2) % 4
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 2) % 4
                if event.key == pygame.K_RIGHT:
                    if menu_index % 2 == 0:
                        menu_index += 1
                if event.key == pygame.K_LEFT:
                    if menu_index % 2 == 1:
                        menu_index -= 1
                if event.key == pygame.K_RETURN:
                    if menu_index == 0:
                        print("FIGHT selected")
                    elif menu_index == 1:
                        print("PYRM selected")
                    elif menu_index == 2:
                        print("BAG selected")
                    elif menu_index == 3:
                        print("RUN selected")

    if game_state == "MENU":
        draw_text(translations[language]["start"], BASE_WIDTH // 2, BASE_HEIGHT // 2, center=True)

    elif game_state == "PLAYER_SELECT":
        draw_text(translations[language]["choose_player"], BASE_WIDTH // 2, 30, center=True)
        for i, name in enumerate(pyramun_list):
            prefix = "> " if i == menu_index else "  "
            draw_text(prefix + name, 80, 80 + i * 20)

    elif game_state == "ENEMY_SELECT":
        draw_text(translations[language]["choose_enemy"], BASE_WIDTH // 2, 30, center=True)
        for i, name in enumerate(pyramun_list):
            prefix = "> " if i == menu_index else "  "
            draw_text(prefix + name, 80, 80 + i * 20)

    elif game_state == "BATTLE":
        bg, fg = get_colors()

        #enemy sprite
        game_surface.blit(enemy_img, (200, 10))

        #gracz sprite
        game_surface.blit(player_img, (30, 64))

        #info przeciwnik
        pygame.draw.rect(game_surface, fg, (10, 10, 150, 40), 2)

        draw_text(enemy_pyramun, 20, 18, size="small")
        draw_text("HP:", 20, 32, size="small")

        pygame.draw.rect(game_surface, fg, (46, 32, 90, 6), 1)
        pygame.draw.rect(game_surface, fg, (47, 33, 70, 4))

        #info gracz
        pygame.draw.rect(game_surface, fg, (160, 106, 150, 50), 2)

        draw_text(selected_pyramun, 170, 114, size="small")
        draw_text("HP:", 170, 128, size="small")

        pygame.draw.rect(game_surface, fg, (196, 128, 90, 6), 1)
        pygame.draw.rect(game_surface, fg, (197, 129, 70, 4))
        draw_text("18/20", 240, 144, center=True, size="big")

        #menubox
        pygame.draw.rect(game_surface, fg, (0, 160, BASE_WIDTH, 80), 2)
        pygame.draw.rect(game_surface, fg, (2, 162, BASE_WIDTH - 4, 76), 1)

        options = [
            translations[language]["fight"],
            translations[language]["pyramun"],
            translations[language]["bag"],
            translations[language]["run"]
        ]

        #menu
        draw_text(options[0], 80, 186, center=True, size="big")
        draw_text(options[1], 240, 186, center=True, size="big")
        draw_text(options[2], 80, 216, center=True, size="big")
        draw_text(options[3], 240, 216, center=True, size="big")

        #cursor
        ##w polskim poprawic
        if menu_index == 0:
            draw_text(">", 40, 186, center=True, size="big")
        elif menu_index == 1:
            draw_text(">", 200, 186, center=True, size="big")
        elif menu_index == 2:
            draw_text(">", 40, 216, center=True, size="big")
        elif menu_index == 3:
            draw_text(">", 200, 216, center=True, size="big")

    scaled = pygame.transform.scale(game_surface, (BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    fps = clock.get_fps()
    update_title(fps)
    clock.tick(120)

pygame.quit()
sys.exit()