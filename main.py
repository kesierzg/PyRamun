import pygame
import sys
import random
from attacks import ATTACKS, PYRAMUN_TYPES, get_multiplier
from stats import BASE_STATS, generate_stats

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
battle_message = ""
message_timer = 0
message_phase = 0
wait_for_input = False

pending_attack = None

player_stats = None
enemy_stats = None
player_hp = 0
enemy_hp = 0
selected_pyramun = None
enemy_pyramun = None

anim_timer = 0
anim_type = None
blink_timer = 0
blink_visible = True
blink_target = None

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

def draw_battle_scene(fade_target=None, fade_alpha=255):
    bg, fg = get_colors()

    enemy_pos = [200, 10]
    player_pos = [30, 64]

    if anim_type == "player_attack":
        player_pos[0] += 10
    if anim_type == "enemy_attack":
        enemy_pos[0] -= 10

    if True:
        if blink_target != "enemy" or blink_visible:
            if fade_target == "enemy" and "fainted" in battle_message:
                faded = enemy_img.copy()
                faded.set_alpha(fade_alpha)
                game_surface.blit(faded, enemy_pos)
            else:
                game_surface.blit(enemy_img, enemy_pos)

        if blink_target != "player" or blink_visible:
            if fade_target == "player" and "fainted" in battle_message:
                faded = player_img.copy()
                faded.set_alpha(fade_alpha)
                game_surface.blit(faded, player_pos)
            else:
                game_surface.blit(player_img, player_pos)

    #enemy box
    pygame.draw.rect(game_surface, fg, (10, 10, 150, 40), 2)
    draw_text(enemy_pyramun, 20, 18, size="small")
    draw_text("HP:", 20, 32, size="small")
    pygame.draw.rect(game_surface, fg, (46, 32, 90, 6), 1)
    enemy_ratio = max(0, min(1, enemy_hp / enemy_stats["hp"]))
    enemy_bar_width = int(90 * enemy_ratio)
    pygame.draw.rect(game_surface, fg, (47, 33, enemy_bar_width, 4))

    #player box
    pygame.draw.rect(game_surface, fg, (160, 106, 150, 50), 2)
    draw_text(selected_pyramun, 170, 114, size="small")
    draw_text("HP:", 170, 128, size="small")
    pygame.draw.rect(game_surface, fg, (196, 128, 90, 6), 1)
    player_ratio = max(0, min(1, player_hp / player_stats["hp"]))
    player_bar_width = int(90 * player_ratio)
    pygame.draw.rect(game_surface, fg, (197, 129, player_bar_width, 4))
    draw_text(f"{player_hp}/{player_stats['hp']}", 240, 144, center=True, size="big")

    #menu box
    pygame.draw.rect(game_surface, fg, (0, 160, BASE_WIDTH, 80), 2)
    pygame.draw.rect(game_surface, fg, (2, 162, BASE_WIDTH - 4, 76), 1)

menu_index = 0

running = True
while running:
    bg, fg = get_colors()
    game_surface.fill(bg)

    if anim_timer > 0:
        anim_timer -= 1
        if anim_timer == 0:
            anim_type = None

    if blink_timer > 0:
        blink_timer -= 1
        blink_visible = (blink_timer // 10) % 2 == 0
    else:
        blink_visible = True

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

                    player_stats = generate_stats(selected_pyramun)
                    enemy_stats = generate_stats(enemy_pyramun)

                    player_hp = player_stats["hp"]
                    enemy_hp = enemy_stats["hp"]

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
                        game_state = "FIGHT_MENU"
                        menu_index = 0
                    elif menu_index == 1:
                        print("PYRM selected")
                    elif menu_index == 2:
                        print("BAG selected")
                    elif menu_index == 3:
                        print("RUN selected")

            elif game_state == "FIGHT_MENU":
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
                    attack = ATTACKS[selected_pyramun][menu_index]
                    pending_attack = attack
                    if player_stats["spd"] >= enemy_stats["spd"]:
                        message_phase = 0
                    else:
                        message_phase = 7
                    if player_stats["spd"] >= enemy_stats["spd"]:
                        battle_message = f"Your {selected_pyramun} used {attack['name']}!"
                    else:
                        battle_message = f"Enemy {enemy_pyramun} used Tackle!"
                    if player_stats["spd"] >= enemy_stats["spd"]:
                        anim_type = "player_attack"
                    else:
                        anim_type = "enemy_attack"
                    anim_timer = 20
                    game_state = "MESSAGE"
                    message_timer = 90
                    wait_for_input = False

            elif game_state == "MESSAGE":
                pass

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
        draw_battle_scene()

        options = [
            translations[language]["fight"],
            translations[language]["pyramun"],
            translations[language]["bag"],
            translations[language]["run"]
        ]

        # menu
        draw_text(options[0], 80, 186, center=True, size="big")
        draw_text(options[1], 240, 186, center=True, size="big")
        draw_text(options[2], 80, 216, center=True, size="big")
        draw_text(options[3], 240, 216, center=True, size="big")

        # cursor
        if menu_index == 0:
            draw_text(">", 40, 186, center=True, size="big")
        elif menu_index == 1:
            draw_text(">", 200, 186, center=True, size="big")
        elif menu_index == 2:
            draw_text(">", 40, 216, center=True, size="big")
        elif menu_index == 3:
            draw_text(">", 200, 216, center=True, size="big")

    elif game_state == "FIGHT_MENU":
        draw_battle_scene()

        attacks = ATTACKS[selected_pyramun]

        draw_text(attacks[0]["name"], 80, 186, center=True, size="big")
        draw_text(attacks[1]["name"], 240, 186, center=True, size="big")
        draw_text(attacks[2]["name"], 80, 216, center=True, size="big")
        draw_text(attacks[3]["name"], 240, 216, center=True, size="big")

        if menu_index == 0:
            draw_text(">", 40, 186, center=True, size="big")
        elif menu_index == 1:
            draw_text(">", 200, 186, center=True, size="big")
        elif menu_index == 2:
            draw_text(">", 40, 216, center=True, size="big")
        elif menu_index == 3:
            draw_text(">", 200, 216, center=True, size="big")

    elif game_state == "MESSAGE":
        fade_progress = max(0, min(1, message_timer / 120))
        alpha = int(255 * fade_progress)

        fade_target = "enemy" if "Enemy" in battle_message else "player"

        draw_battle_scene(fade_target=fade_target, fade_alpha=alpha)

        draw_text(battle_message, BASE_WIDTH // 2, 200, center=True, size="small")

        message_timer -= 1

        if message_timer <= 0:
            if message_phase == 0:

                accuracy = pending_attack.get("accuracy", 100)
                hit_roll = random.randint(1, 100)

                if hit_roll > accuracy:
                    print(f"[MISS] {selected_pyramun}'s attack missed!")
                    battle_message = f"{selected_pyramun}'s attack missed!"
                    message_phase = 1
                    message_timer = 60
                    continue

                if "fixed_damage" in pending_attack:
                    damage = pending_attack["fixed_damage"]
                    mult = None
                else:
                    if pending_attack["category"] == "physical":
                        atk = player_stats["atk"]
                        defn = enemy_stats["def"]
                    else:
                        atk = player_stats["spc"]
                        defn = enemy_stats["spc"]

                    power = pending_attack["power"]

                    damage = int((atk / defn) * power)

                    damage = int(damage * random.uniform(0.85, 1.0))

                    mult = get_multiplier(pending_attack["type"], PYRAMUN_TYPES[enemy_pyramun])
                    damage = int(damage * mult)

                    damage = max(1, damage)

                enemy_hp = max(0, enemy_hp - damage)
                print(f"[PLAYER ATTACK] {selected_pyramun} dealt {damage} damage → Enemy HP: {enemy_hp}/{enemy_stats['hp']}")
                message_phase = 1
                message_timer = 60
                blink_timer = 60
                blink_target = "enemy"

                if mult is not None:
                    if mult == 0:
                        battle_message = "It had no effect!"
                        message_phase = 3
                        message_timer = 60
                    elif mult > 1:
                        battle_message = "It's super effective!"
                        message_phase = 3
                        message_timer = 60
                    elif mult < 1:
                        battle_message = "It's not very effective..."
                        message_phase = 3
                        message_timer = 60
                    else:
                        if enemy_hp == 0:
                            battle_message = f"Enemy {enemy_pyramun} fainted!"
                            message_phase = 2
                            message_timer = 120
                        else:
                            message_phase = 1
                            message_timer = 60
                else:
                    if enemy_hp == 0:
                        battle_message = f"Enemy {enemy_pyramun} fainted!"
                        message_phase = 2
                        message_timer = 120
                    else:
                        message_phase = 1
                        message_timer = 60

            elif message_phase == 3:
                message_phase = 1
                message_timer = 120

            elif message_phase == 1:
                message_phase = 7
                message_timer = 60

            elif message_phase == 7:
                battle_message = f"Enemy {enemy_pyramun} used Tackle!"
                message_phase = 4
                message_timer = 90

            elif message_phase == 4:
                anim_type = "enemy_attack"
                anim_timer = 20
                message_phase = 5
                message_timer = 30

            elif message_phase == 5:
                damage = 2
                player_hp = max(0, player_hp - 2)
                print(
                f"[ENEMY ATTACK] {enemy_pyramun} dealt {damage} damage → Player HP: {player_hp}/{player_stats['hp']}")
                blink_timer = 60
                blink_target = "player"

                if player_hp == 0:
                    battle_message = f"Your {selected_pyramun} fainted!"
                    message_phase = 2
                    message_timer = 120
                else:
                    message_phase = 6
                    message_timer = 120

            elif message_phase == 6:
                game_state = "BATTLE"
                menu_index = 0

            elif message_phase == 2:
                player_hp = 20
                enemy_hp = 20
                menu_index = 0
                game_state = "MENU"

    scaled = pygame.transform.scale(game_surface, (BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    fps = clock.get_fps()
    update_title(fps)
    clock.tick(60)

pygame.quit()
sys.exit()