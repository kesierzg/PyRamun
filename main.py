import pygame
import sys
import random

from attacks import ATTACKS
from stats import generate_stats
from battle import BattleState
from ui import get_colors, draw_text, draw_battle_scene, draw_menu_cursor, AnimState

pygame.init()
pygame.mixer.init()

is_dark_mode = False

BASE_WIDTH, BASE_HEIGHT = 320, 240
SCALES = [1, 2, 3]
scale_index = 1
SCALE = SCALES[scale_index]

screen = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
game_surface = pygame.Surface((BASE_WIDTH, BASE_HEIGHT))

pygame.display.set_caption("PyRamun - Pokemon clone")

clock = pygame.time.Clock()

def update_title(fps=0):
    pygame.display.set_caption(
        f"PyRamun - {BASE_WIDTH * SCALE}x{BASE_HEIGHT * SCALE} | {int(fps)} FPS"
    )


update_title(0)

def _load_sprite(name, side, size=(96, 96)):
    return pygame.transform.scale(
        pygame.image.load(f"assets/gfx/{name}_{side}.png").convert_alpha(), size
    )

enemy_imgs = {
    "Sqqqrtle":   _load_sprite("sqqqrttle",   "front"),
    "Bulwazaur":  _load_sprite("bulwazaur", "front"),
    "Chadmandor": _load_sprite("chadmandor","front"),
    "Pejot":      _load_sprite("pejot",     "front"),
    "Pikablu":    _load_sprite("pikablu",   "front"),
    "Psikabra":   _load_sprite("psikabra",  "front"),
    "Sandskrew":  _load_sprite("sandskrew", "front"),
}
player_imgs = {
    "Sqqqrtle":   _load_sprite("sqqqrttle",   "back"),
    "Bulwazaur":  _load_sprite("bulwazaur", "back"),
    "Chadmandor": _load_sprite("chadmandor","back"),
    "Pejot":      _load_sprite("pejot",     "back"),
    "Pikablu":    _load_sprite("pikablu",   "back"),
    "Psikabra":   _load_sprite("psikabra",  "back"),
    "Sandskrew":  _load_sprite("sandskrew", "back"),
}
font_small = pygame.font.Font("assets/dogicapixel.otf", 8)
font_big = pygame.font.Font("assets/dogicapixel.otf", 16)

howl_sounds = {
    name: pygame.mixer.Sound(f"assets/sounds/{name}.wav")
    for name in ["Chadmandor", "Sqqqrtle", "Bulwazaur", "Pikablu", "Pejot", "Sandskrew", "Psikabra"]
}
faint_sounds  = [pygame.mixer.Sound(f"assets/sounds/faint{i}.wav") for i in range(1, 4)]
attack_sound  = pygame.mixer.Sound("assets/sounds/attack.wav")
damage_sound  = pygame.mixer.Sound("assets/sounds/damage.wav")
winner_sound  = pygame.mixer.Sound("assets/sounds/winner.wav")
loser_sound   = pygame.mixer.Sound("assets/sounds/loser.wav")

def _deals_damage(atk):
    return atk.get("power", 0) > 0 or "fixed_damage" in atk

_current_music = None
def play_music(filename, volume=1.0):
    global _current_music
    if _current_music != filename:
        pygame.mixer.music.load(f"assets/sounds/{filename}")
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        _current_music = filename

play_music("mainmenu.wav")

game_state = "MENU"
menu_index = 0

battle_mode = "single"
team_size = 3
player_team: list = []
enemy_team: list = []
player_remaining: list = []
enemy_remaining: list  = []

pyramun_list = [
    "Chadmandor", "Sqqqrtle", "Bulwazaur",
    "Pikablu", "Pejot", "Sandskrew", "Psikabra",
]

effects = AnimState()
battle = BattleState()

intro_phase = 0
intro_timer = 0
intro_message = ""
last_faint_msg = ""
_enemy_atk_snd_done = False

switch_intro_side  = "player"
switch_intro_phase = 0
switch_intro_timer = 0

_end_won   = False
_end_timer = 0

def start_ending(won):
    global game_state, _end_won, _end_timer, menu_index
    _end_won   = won
    _end_timer = 120
    game_state = "ENDING"
    menu_index = 0

def go_to_end(won):
    global game_state, menu_index
    game_state = "WIN" if won else "LOSE"
    menu_index = 0
    pygame.mixer.music.stop()
    (winner_sound if won else loser_sound).play()

def start_intro():
    global game_state, intro_phase, intro_timer, intro_message, menu_index
    intro_phase = 0
    intro_timer = 30
    intro_message = ""
    game_state = "INTRO"
    menu_index = 0

def start_switch_intro(side):
    global game_state, switch_intro_side, switch_intro_phase, switch_intro_timer, menu_index, _enemy_atk_snd_done
    switch_intro_side  = side
    switch_intro_phase = 0
    switch_intro_timer = 30
    game_state = "SWITCH_INTRO"
    menu_index = 0
    _enemy_atk_snd_done = False

def blit_text(text, x, y, center=False, size="big"):
    _, fg = get_colors(is_dark_mode)
    draw_text(game_surface, text, x, y, fg,
              center=center, size=size,
              font_small=font_small, font_big=font_big)

def draw_two_choice(title, options):
    blit_text(title, BASE_WIDTH // 2, 40, center=True)
    for i, label in enumerate(options):
        prefix = "> " if i == menu_index else "  "
        blit_text(prefix + label, BASE_WIDTH // 2, 100 + i * 30, center=True)

def draw_team_select(label, team):
    blit_text(f"{label} ({len(team)}/{team_size})", BASE_WIDTH // 2, 18, center=True, size="small")
    for i, name in enumerate(pyramun_list):
        if name in team:
            prefix = "[X] "
        elif i == menu_index:
            prefix = ">   "
        else:
            prefix = "    "
        blit_text(prefix + name, 60, 40 + i * 18, size="small")

def draw_list_select(title, lst):
    blit_text(title, BASE_WIDTH // 2, 30, center=True)
    for i, name in enumerate(lst):
        prefix = "> " if i == menu_index else "  "
        blit_text(prefix + name, 80, 80 + i * 20)


#mainloop
running = True
while running:
    bg, fg = get_colors(is_dark_mode)
    game_surface.fill(bg)

    effects.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #r - resolution; n - darkmode
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                scale_index = (scale_index + 1) % len(SCALES)
                SCALE = SCALES[scale_index]
                screen = pygame.display.set_mode((BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
                update_title()

            if event.key == pygame.K_n:
                is_dark_mode = not is_dark_mode

            if game_state == "MENU":
                if event.key == pygame.K_RETURN:
                    game_state = "MODE_SELECT"
                    menu_index = 0

            elif game_state == "MODE_SELECT":
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    menu_index = 1 - menu_index
                if event.key == pygame.K_RETURN:
                    if menu_index == 0:
                        battle_mode = "single"
                        game_state = "PLAYER_SELECT"
                    else:
                        battle_mode = "multi"
                        team_size = 3
                        player_team.clear()
                        enemy_team.clear()
                        game_state = "TEAM_SIZE_SELECT"
                    menu_index = 0

            elif game_state == "TEAM_SIZE_SELECT":
                if event.key == pygame.K_UP:
                    team_size = min(6, team_size + 1)
                if event.key == pygame.K_DOWN:
                    team_size = max(2, team_size - 1)
                if event.key == pygame.K_RETURN:
                    player_team.clear()
                    game_state = "PLAYER_TEAM_SELECT"
                    menu_index = 0

            elif game_state == "PLAYER_TEAM_SELECT":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(pyramun_list)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(pyramun_list)
                if event.key == pygame.K_RETURN:
                    name = pyramun_list[menu_index]
                    if name not in player_team:
                        player_team.append(name)
                        if len(player_team) == team_size:
                            enemy_team.clear()
                            game_state = "ENEMY_MODE_SELECT"
                            menu_index = 0

            elif game_state == "ENEMY_MODE_SELECT":
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    menu_index = 1 - menu_index
                if event.key == pygame.K_RETURN:
                    if menu_index == 0:
                        enemy_team[:] = random.sample(pyramun_list, team_size)
                        player_remaining[:] = list(player_team[1:])
                        enemy_remaining[:] = list(enemy_team[1:])
                        p_stats = generate_stats(player_team[0])
                        e_stats = generate_stats(enemy_team[0])
                        battle.setup(player_team[0], enemy_team[0], p_stats, e_stats)
                        start_intro()
                    else:
                        enemy_team.clear()
                        game_state = "ENEMY_TEAM_SELECT"
                    menu_index = 0

            elif game_state == "ENEMY_TEAM_SELECT":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(pyramun_list)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(pyramun_list)
                if event.key == pygame.K_RETURN:
                    name = pyramun_list[menu_index]
                    if name not in enemy_team:
                        enemy_team.append(name)
                        if len(enemy_team) == team_size:
                            player_remaining[:] = list(player_team[1:])
                            enemy_remaining[:] = list(enemy_team[1:])
                            p_stats = generate_stats(player_team[0])
                            e_stats = generate_stats(enemy_team[0])
                            battle.setup(player_team[0], enemy_team[0], p_stats, e_stats)
                            start_intro()

            elif game_state == "PLAYER_SWITCH":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(player_remaining)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(player_remaining)
                if event.key == pygame.K_RETURN:
                    chosen = player_remaining.pop(menu_index)
                    p_stats = generate_stats(chosen)
                    battle.setup_next_player(chosen, p_stats)
                    start_switch_intro("player")

            elif game_state == "VOLUNTARY_SWITCH":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(player_remaining)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(player_remaining)
                if event.key == pygame.K_RETURN:
                    chosen = player_remaining.pop(menu_index)
                    player_remaining.append(battle.selected_pyramun)
                    p_stats = generate_stats(chosen)
                    battle.setup_voluntary_switch(chosen, p_stats)
                    start_switch_intro("player")
                if event.key == pygame.K_ESCAPE:
                    game_state = "BATTLE"
                    menu_index = 0

            elif game_state == "PLAYER_SELECT":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(pyramun_list)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(pyramun_list)
                if event.key == pygame.K_RETURN:
                    battle.selected_pyramun = pyramun_list[menu_index]
                    game_state = "ENEMY_SELECT"
                    menu_index = 0

            elif game_state == "ENEMY_SELECT":
                if event.key == pygame.K_DOWN:
                    menu_index = (menu_index + 1) % len(pyramun_list)
                if event.key == pygame.K_UP:
                    menu_index = (menu_index - 1) % len(pyramun_list)
                if event.key == pygame.K_RETURN:
                    enemy_pyramun = pyramun_list[menu_index]
                    player_stats = generate_stats(battle.selected_pyramun)
                    enemy_stats = generate_stats(enemy_pyramun)
                    battle.setup(battle.selected_pyramun, enemy_pyramun, player_stats, enemy_stats)
                    start_intro()

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
                        if battle_mode == "multi" and player_remaining:
                            game_state = "VOLUNTARY_SWITCH"
                            menu_index = 0
                    elif menu_index == 2:
                        battle.battle_message = "BAG is empty :("
                        battle.message_timer  = 120
                        battle.message_phase  = 3
                        game_state = "MESSAGE"
                    elif menu_index == 3:
                        choices = [
                            "What are you running from?",
                            "Grow some balls!",
                            "There's no escape!",
                            "Just use the OS exit function..."]
                        battle.battle_message = random.choice(choices)
                        battle.message_timer  = 120
                        battle.message_phase  = 3
                        game_state = "MESSAGE"

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
                    attack = ATTACKS[battle.selected_pyramun][menu_index]
                    anim_type = battle.start_turn(attack)
                    _enemy_atk_snd_done = False
                    if anim_type == "player_attack":
                        effects.trigger_attack(anim_type)
                        if _deals_damage(attack):
                            attack_sound.play()
                    battle.message_timer = 90
                    game_state = "MESSAGE"

            elif game_state in ("WIN", "LOSE"):
                if event.key == pygame.K_RETURN:
                    game_state = "MENU"
                    menu_index = 0

            elif game_state == "MESSAGE":
                pass

    def _scene_kwargs(fade_target=None, fade_alpha=255):
        return dict(
            surface=game_surface, fg=fg, bg=bg,
            enemy_img=enemy_imgs[battle.enemy_pyramun],
            player_img=player_imgs[battle.selected_pyramun],
            enemy_pyramun=battle.enemy_pyramun,
            selected_pyramun=battle.selected_pyramun,
            enemy_hp=battle.enemy_hp, enemy_stats=battle.enemy_stats,
            player_hp=battle.player_hp, player_stats=battle.player_stats,
            anim_type=effects.anim_type,
            blink_target=effects.blink_target,
            blink_visible=effects.blink_visible,
            battle_message=battle.battle_message,
            fade_target=fade_target, fade_alpha=fade_alpha,
            font_small=font_small, font_big=font_big,
            BASE_WIDTH=BASE_WIDTH,
            enemy_status_label=battle.enemy_status.status_label(),
            player_status_label=battle.player_status.status_label(),
        )

    if game_state == "MENU":
        play_music("mainmenu.wav")
        blit_text("START", BASE_WIDTH // 2, BASE_HEIGHT // 2, center=True)

    elif game_state == "MODE_SELECT":
        draw_two_choice("Select Mode", ["Single", "Multi"])

    elif game_state == "TEAM_SIZE_SELECT":
        blit_text("Team Size", BASE_WIDTH // 2, 40, center=True)
        blit_text(f"  {team_size}  ", BASE_WIDTH // 2, 100, center=True)
        blit_text("UP / DOWN to change", BASE_WIDTH // 2, 140, center=True, size="small")
        blit_text("ENTER to confirm", BASE_WIDTH // 2, 155, center=True, size="small")

    elif game_state == "PLAYER_TEAM_SELECT":
        draw_team_select("Your team", player_team)

    elif game_state == "ENEMY_MODE_SELECT":
        draw_two_choice("Enemy team?", ["Random", "Manual"])

    elif game_state == "ENEMY_TEAM_SELECT":
        draw_team_select("Enemy team", enemy_team)

    elif game_state == "PLAYER_SWITCH":
        draw_list_select("Choose next!", player_remaining)

    elif game_state == "VOLUNTARY_SWITCH":
        draw_battle_scene(**_scene_kwargs())
        blit_text("Switch to?", BASE_WIDTH // 2, 170, center=True, size="small")
        for i, name in enumerate(player_remaining):
            prefix = "> " if i == menu_index else "  "
            blit_text(prefix + name, BASE_WIDTH // 2, 190 + i * 16, center=True, size="small")

    elif game_state == "PLAYER_SELECT":
        draw_list_select("CHOOSE YOUR PYRAMUN", pyramun_list)

    elif game_state == "ENEMY_SELECT":
        draw_list_select("CHOOSE ENEMY", pyramun_list)

    elif game_state == "INTRO":
        if intro_phase >= 1:
            game_surface.blit(enemy_imgs[battle.enemy_pyramun], [200, 10])
            pygame.draw.rect(game_surface, fg, (10, 10, 150, 40), 2)
            blit_text(battle.enemy_pyramun, 20, 18, size="small")
            pygame.draw.rect(game_surface, fg, (46, 32, 90, 6), 1)
            pygame.draw.rect(game_surface, fg, (47, 33, 90, 4))
        if intro_phase >= 2:
            game_surface.blit(player_imgs[battle.selected_pyramun], [30, 64])
            pygame.draw.rect(game_surface, fg, (160, 106, 150, 50), 2)
            blit_text(battle.selected_pyramun, 170, 114, size="small")
            pygame.draw.rect(game_surface, fg, (196, 128, 90, 6), 1)
            pygame.draw.rect(game_surface, fg, (197, 129, 90, 4))
            blit_text(f"{battle.player_hp}/{battle.player_stats['hp']}", 240, 144, center=True)
        pygame.draw.rect(game_surface, fg, (0, 160, BASE_WIDTH, 80), 2)
        pygame.draw.rect(game_surface, fg, (2, 162, BASE_WIDTH - 4, 76), 1)
        if intro_message:
            blit_text(intro_message, BASE_WIDTH // 2, 200, center=True, size="small")

        intro_timer -= 1
        if intro_timer <= 0:
            intro_phase += 1
            if intro_phase == 1:
                play_music("battle.wav", volume=0.1)
                howl_sounds[battle.enemy_pyramun].play()
                intro_message = f"{battle.enemy_pyramun} appeared!"
                intro_timer = 120
            elif intro_phase == 2:
                howl_sounds[battle.selected_pyramun].play()
                intro_message = f"You send out {battle.selected_pyramun}!"
                intro_timer = 120
            elif intro_phase >= 3:
                game_state = "BATTLE"
                menu_index = 0

    elif game_state == "SWITCH_INTRO":
        show_enemy  = switch_intro_side != "enemy"  or switch_intro_phase >= 1
        show_player = switch_intro_side != "player" or switch_intro_phase >= 1
        if show_enemy:
            game_surface.blit(enemy_imgs[battle.enemy_pyramun], [200, 10])
            pygame.draw.rect(game_surface, fg, (10, 10, 150, 40), 2)
            blit_text(battle.enemy_pyramun, 20, 18, size="small")
            if battle.enemy_status.status_label():
                blit_text(battle.enemy_status.status_label(), 130, 18, size="small")
            pygame.draw.rect(game_surface, fg, (46, 32, 90, 6), 1)
            pygame.draw.rect(game_surface, fg, (47, 33, int(90 * max(0, min(1, battle.enemy_hp / battle.enemy_stats["hp"]))), 4))
        if show_player:
            game_surface.blit(player_imgs[battle.selected_pyramun], [30, 64])
            pygame.draw.rect(game_surface, fg, (160, 106, 150, 50), 2)
            blit_text(battle.selected_pyramun, 170, 114, size="small")
            if battle.player_status.status_label():
                blit_text(battle.player_status.status_label(), 280, 114, size="small")
            pygame.draw.rect(game_surface, fg, (196, 128, 90, 6), 1)
            pygame.draw.rect(game_surface, fg, (197, 129, int(90 * max(0, min(1, battle.player_hp / battle.player_stats["hp"]))), 4))
            blit_text(f"{battle.player_hp}/{battle.player_stats['hp']}", 240, 144, center=True)
        pygame.draw.rect(game_surface, fg, (0, 160, BASE_WIDTH, 80), 2)
        pygame.draw.rect(game_surface, fg, (2, 162, BASE_WIDTH - 4, 76), 1)
        if switch_intro_phase >= 1:
            blit_text(battle.battle_message, BASE_WIDTH // 2, 200, center=True, size="small")

        switch_intro_timer -= 1
        if switch_intro_timer <= 0:
            switch_intro_phase += 1
            if switch_intro_phase == 1:
                name = battle.selected_pyramun if switch_intro_side == "player" else battle.enemy_pyramun
                howl_sounds[name].play()
                switch_intro_timer = 120
            elif switch_intro_phase >= 2:
                battle.message_timer = 1
                game_state = "MESSAGE"

    elif game_state == "BATTLE":
        draw_battle_scene(**_scene_kwargs())
        options = ["FIGHT", "PYRM", "BAG", "RUN"]
        positions = [(80, 186), (240, 186), (80, 216), (240, 216)]
        for label, (x, y) in zip(options, positions):
            blit_text(label, x, y, center=True, size="big")
        draw_menu_cursor(game_surface, fg, menu_index, options, positions, font_small, font_big)

    elif game_state == "FIGHT_MENU":
        draw_battle_scene(**_scene_kwargs())
        attacks = ATTACKS[battle.selected_pyramun]
        positions = [(80, 186), (240, 186), (80, 216), (240, 216)]
        labels = [a.get("label", a["name"]) for a in attacks]
        for label, (x, y) in zip(labels, positions):
            blit_text(label, x, y, center=True, size="big")
        draw_menu_cursor(game_surface, fg, menu_index, labels, positions, font_small, font_big)

    elif game_state == "MESSAGE":
        fade_progress = max(0, min(1, battle.message_timer / 120))
        alpha = int(255 * fade_progress)
        fade_target = "enemy" if "Enemy" in battle.battle_message else "player"
        draw_battle_scene(**_scene_kwargs(fade_target=fade_target, fade_alpha=alpha))
        blit_text(battle.battle_message, BASE_WIDTH // 2, 200, center=True, size="small")

        if "fainted" in battle.battle_message and battle.battle_message != last_faint_msg:
            random.choice(faint_sounds).play()
            last_faint_msg = battle.battle_message

        prev_blink_timer = effects.blink_timer
        next_state = battle.advance(effects)
        if effects.blink_timer > prev_blink_timer:
            damage_sound.play()
        if effects.anim_type == "enemy_attack" and not _enemy_atk_snd_done:
            if _deals_damage(battle.enemy_pending_attack):
                attack_sound.play()
            _enemy_atk_snd_done = True
        if next_state is not None:
            if next_state == "BATTLE_END":
                won = battle.last_fainted == "enemy"
                if battle_mode == "single":
                    start_ending(won)
                else:
                    if won:
                        if enemy_remaining:
                            next_name = enemy_remaining.pop(0)
                            battle.setup_next_enemy(next_name, generate_stats(next_name))
                            start_switch_intro("enemy")
                        else:
                            start_ending(True)
                    else:
                        if player_remaining:
                            game_state = "PLAYER_SWITCH"
                            menu_index = 0
                        else:
                            start_ending(False)
            else:
                game_state = next_state
                menu_index = 0

    elif game_state == "ENDING":
        fade_side = "enemy" if battle.last_fainted == "enemy" else "player"
        draw_battle_scene(**_scene_kwargs(fade_target=fade_side, fade_alpha=0))
        blit_text(battle.battle_message, BASE_WIDTH // 2, 200, center=True, size="small")
        _end_timer -= 1
        if _end_timer <= 0:
            go_to_end(_end_won)

    elif game_state == "WIN":
        blit_text("YOU WIN!", BASE_WIDTH // 2, BASE_HEIGHT // 2 - 20, center=True)
        blit_text("ENTER to continue", BASE_WIDTH // 2, BASE_HEIGHT // 2 + 20, center=True, size="small")

    elif game_state == "LOSE":
        blit_text("YOU LOSE!", BASE_WIDTH // 2, BASE_HEIGHT // 2 - 20, center=True)
        blit_text("ENTER to continue", BASE_WIDTH // 2, BASE_HEIGHT // 2 + 20, center=True, size="small")

    scaled = pygame.transform.scale(game_surface, (BASE_WIDTH * SCALE, BASE_HEIGHT * SCALE))
    screen.blit(scaled, (0, 0))
    pygame.display.flip()
    fps = clock.get_fps()
    update_title(fps)
    clock.tick(60)

pygame.quit()
sys.exit()