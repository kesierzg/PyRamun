import pygame


def get_colors(is_dark_mode):
    dark, light = (0, 0, 0), (255, 255, 255)
    return (dark, light) if is_dark_mode else (light, dark)


def draw_text(surface, text, x, y, fg, center=False, size="big", font_small=None, font_big=None):
    font = font_small if size == "small" else font_big
    img = font.render(text, True, fg)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)


def draw_battle_scene(
    surface, fg, bg,
    enemy_img, player_img,
    enemy_pyramun, selected_pyramun,
    enemy_hp, enemy_stats,
    player_hp, player_stats,
    anim_type, blink_target, blink_visible,
    battle_message,
    fade_target=None, fade_alpha=255,
    font_small=None, font_big=None,
    BASE_WIDTH=320,
    enemy_status_label="", player_status_label="",
):
    def _text(text, x, y, **kw):
        draw_text(surface, text, x, y, fg, font_small=font_small, font_big=font_big, **kw)

    def _blit(img, pos, side):
        if blink_target != side or blink_visible:
            if fade_target == side and "fainted" in battle_message:
                faded = img.copy()
                faded.set_alpha(fade_alpha)
                surface.blit(faded, pos)
            else:
                surface.blit(img, pos)

    enemy_pos = [200, 10]
    player_pos = [30, 64]

    if anim_type == "player_attack":
        player_pos[0] += 10
    if anim_type == "enemy_attack":
        enemy_pos[0] -= 10

    _blit(enemy_img, enemy_pos, "enemy")
    _blit(player_img, player_pos, "player")

    pygame.draw.rect(surface, fg, (10, 10, 150, 40), 2)
    _text(enemy_pyramun, 20, 18, size="small")
    if enemy_status_label:
        _text(enemy_status_label, 130, 18, size="small")
    _text("HP:", 20, 32, size="small")
    pygame.draw.rect(surface, fg, (46, 32, 90, 6), 1)
    pygame.draw.rect(surface, fg, (47, 33, int(90 * max(0, min(1, enemy_hp / enemy_stats["hp"]))), 4))

    pygame.draw.rect(surface, fg, (160, 106, 150, 50), 2)
    _text(selected_pyramun, 170, 114, size="small")
    if player_status_label:
        _text(player_status_label, 280, 114, size="small")
    _text("HP:", 170, 128, size="small")
    pygame.draw.rect(surface, fg, (196, 128, 90, 6), 1)
    pygame.draw.rect(surface, fg, (197, 129, int(90 * max(0, min(1, player_hp / player_stats["hp"]))), 4))
    _text(f"{player_hp}/{player_stats['hp']}", 240, 144, center=True)

    pygame.draw.rect(surface, fg, (0, 160, BASE_WIDTH, 80), 2)
    pygame.draw.rect(surface, fg, (2, 162, BASE_WIDTH - 4, 76), 1)


def draw_menu_cursor(surface, fg, menu_index, labels, positions, font_small, font_big):
    if not (0 <= menu_index < len(positions)):
        return
    x, y = positions[menu_index]
    text_w = font_big.size(labels[menu_index])[0]
    cursor_w = font_big.size(">")[0]
    draw_text(surface, ">", x - text_w // 2 - cursor_w - 4, y, fg, size="big", font_small=font_small, font_big=font_big)

class AnimState:

    def __init__(self):
        self.anim_timer = 0
        self.anim_type = None
        self.blink_timer = 0
        self.blink_visible = True
        self.blink_target = None

    def trigger_attack(self, anim_type, duration=20):
        self.anim_type = anim_type
        self.anim_timer = duration

    def trigger_blink(self, target, duration=60):
        self.blink_target = target
        self.blink_timer = duration

    def update(self):
        if self.anim_timer > 0:
            self.anim_timer -= 1
            if self.anim_timer == 0:
                self.anim_type = None

        if self.blink_timer > 0:
            self.blink_timer -= 1
            self.blink_visible = (self.blink_timer // 10) % 2 == 0
        else:
            self.blink_visible = True
