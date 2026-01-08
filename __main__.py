import pygame
import math
from random import random
from essentials import *


def remove(x: float, y: float) -> None:
    x_int, y_int = int(x), int(y)
    if 0 <= y_int < len(world) and 0 <= x_int < len(world[y_int]):
        world[y_int][x_int] = 0


def clear(p: Pathway, dir: int) -> None:
    if dir == 1:
        remove(p.x, p.y - 1)
        remove(p.x, p.y - 2)
        remove(p.x, p.y - 3)
        remove(p.x + 1, p.y - 1)
        remove(p.x + 1, p.y - 2)
        remove(p.x + 1, p.y - 3)
        p.y -= 3
    elif dir == 2:
        remove(p.x, p.y + 1)
        remove(p.x, p.y + 2)
        remove(p.x, p.y + 3)
        remove(p.x, p.y + 4)
        remove(p.x + 1, p.y + 1)
        remove(p.x + 1, p.y + 2)
        remove(p.x + 1, p.y + 3)
        remove(p.x + 1, p.y + 4)
        p.y += 3
    elif dir == 3:
        remove(p.x - 1, p.y)
        remove(p.x - 2, p.y)
        remove(p.x - 3, p.y)
        remove(p.x - 1, p.y + 1)
        remove(p.x - 2, p.y + 1)
        remove(p.x - 3, p.y + 1)
        p.x -= 3
    elif dir == 4:
        remove(p.x + 1, p.y)
        remove(p.x + 2, p.y)
        remove(p.x + 3, p.y)
        remove(p.x + 4, p.y)
        remove(p.x + 1, p.y + 1)
        remove(p.x + 2, p.y + 1)
        remove(p.x + 3, p.y + 1)
        remove(p.x + 4, p.y + 1)
        p.x += 3
    p.dist = p.dist + 1


def available(x: float, y: float) -> bool:
    x_int, y_int = int(x), int(y)
    if 0 <= y_int < len(world) and 0 <= x_int < len(world[y_int]):
        return world[y_int][x_int] == 1
    return False


def generate_world(size: int) -> None:
    global world, enemies
    size = size * 3 + 1
    enemies = []

    world = []
    for i in range(size):
        world.append([1] * size)

    pathways: list[Pathway] = []
    pathways.append(Pathway(x=1, y=1, dist=0))
    remove(1, 1)
    remove(1, 2)
    remove(2, 1)

    max_pathway = pathways[0]

    while pathways:
        for i in range(len(pathways) - 1, -1, -1):
            p = pathways[i]
            directions = []
            if available(p.x, p.y - 3):
                directions.append(1)
            if available(p.x, p.y + 4):
                directions.append(2)
            if available(p.x - 3, p.y):
                directions.append(3)
            if available(p.x + 4, p.y):
                directions.append(4)

            for j in range(len(directions) - 1, -1, -1):
                if random() > 0.95:
                    pathway = Pathway(x=p.x, y=p.y, dist=p.dist)
                    clear(pathway, directions[j])
                    pathways.append(pathway)
                    directions.pop(j)

            if not directions:
                if p.dist > max_pathway.dist:
                    max_pathway = p
                elif spawn_enemies and p.dist > 5 and len(enemies) < enemy_max:
                    if random() > 0.75:
                        enemies.append(Enemy(
                            x=p.x + 0.5,
                            y=p.y + 0.5,
                            x_vel=0,
                            y_vel=0,
                            type=enemy_type,
                            dir=0,
                            state=0
                        ))
                pathways.pop(i)

    world[int(max_pathway.y)][int(max_pathway.x)] = 2


def cast_ray(px: float, py: float, dir: float) -> Color:
    x_comp = math.cos(dir)
    y_comp = math.sin(dir)

    if x_comp == 0:
        m = float('inf') if y_comp > 0 else float('-inf')
    else:
        m = y_comp / x_comp

    rx = px
    ry = py

    facing_right = x_comp >= 0
    x_world_edge = len(world[0]) if facing_right else -1

    facing_down = y_comp >= 0
    y_world_edge = len(world) if facing_down else -1

    while True:
        next_x = math.floor(rx) + 1 if facing_right else math.ceil(rx) - 1
        next_y = math.floor(ry) + 1 if facing_down else math.ceil(ry) - 1

        dist_x = abs(next_x - rx)
        dist_y = abs(next_y - ry)

        bx = 0
        by = 0

        facing_vert_edge = False
        if m == float('inf') or m == float('-inf'):
            facing_vert_edge = True
        else:
            facing_vert_edge = dist_y / dist_x > abs(m)

        if facing_vert_edge:
            rx = next_x
            ry = py + (rx - px) * m
            bx = rx if facing_right else rx - 1
            by = math.floor(ry)
        else:
            ry = next_y
            rx = px + (ry - py) / m if m != 0 else px
            by = ry if facing_down else ry - 1
            bx = math.floor(rx)

        if bx == x_world_edge or by == y_world_edge:
            return (0, 0, 0)

        bx = int(bx)
        by = int(by)

        if world[by][bx] == 0:
            continue

        if world[by][bx] == 2:
            from typing import cast
            return cast(Color, portal_color)

        color = None
        if world[by][bx] < 0:
            tile_bits = -world[by][bx]
            enemy_bits = tile_bits >> enemy_offset
            bullet_bits = (tile_bits & (
                ~(enemy_bits << enemy_offset))) >> bullet_offset

            for i in range(bullet_max):
                if bullet_bits == 0:
                    break
                if (bullet_bits & 1) == 0:
                    bullet_bits >>= 1
                    continue
                bullet_bits >>= 1

                if i < len(bullets):
                    b = bullets[i]
                    b_dist_x = b.x - player.x
                    b_dist_y = b.y - player.y
                    bDist = math.sqrt(b_dist_x ** 2 + b_dist_y ** 2)

                    if bDist == 0:
                        continue

                    numerator = abs((rx - px) * (py - b.y) -
                                    (px - b.x) * (ry - py))
                    denominator = math.sqrt((rx - px) ** 2 + (ry - py) ** 2)
                    if denominator == 0:
                        continue
                    dist = numerator / denominator

                    if dist > 0.125:
                        continue

                    blue = int((dist / 0.125) * 255)
                    color = (255, 255, blue)
                    break

            if color is None:
                for i in range(enemy_max):
                    if enemy_bits == 0:
                        break

                    if (enemy_bits & 1) == 0:
                        enemy_bits >>= 1
                        continue
                    enemy_bits >>= 1

                    if i < len(enemies):
                        e = enemies[i]
                        if e is None:
                            continue

                        e_dist_x = e.x - player.x
                        e_dist_y = e.y - player.y

                        x_int = 0
                        y_int = 0

                        if e_dist_x == 0:
                            y_int = e.y
                            x_int = px + (y_int - py) / m if m != 0 else px
                        elif e_dist_y == 0:
                            x_int = e.x
                            y_int = py + (x_int - px) * m
                        else:
                            e_dist = math.sqrt(e_dist_x ** 2 + e_dist_y ** 2)

                            if e_dist == 0:
                                continue

                            x_comp_e = -e_dist_y / e_dist
                            y_comp_e = e_dist_x / e_dist

                            a1 = -y_comp
                            b1 = x_comp
                            a2 = -y_comp_e
                            b2 = x_comp_e

                            denominator = a1 * b2 - a2 * b1
                            if denominator == 0:
                                continue

                            c1 = a1 * px + b1 * py
                            c2 = a2 * e.x + b2 * e.y

                            y_int = (a1 * c2 - a2 * c1) / (a1 * b2 - a2 * b1)
                            x_int = e.x + (y_int - e.y) * (x_comp_e /
                                                           y_comp_e) if y_comp_e != 0 else e.x

                        dist_to_int = math.sqrt(
                            (x_int - e.x) ** 2 + (y_int - e.y) ** 2)

                        if dist_to_int > 0.25:
                            continue

                        color_index = math.floor(
                            dist_to_int / 0.25 * len(enemy_texture_1d))
                        color_index = max(
                            0, min(color_index, len(enemy_texture_1d) - 1))
                        color = enemy_texture_1d[color_index]
                        break

            if color is not None:
                pass
            else:
                continue

        else:
            tile_pos = 0
            if facing_vert_edge:
                tile_pos = ry % 1
                if facing_right:
                    tile_pos = 1 - tile_pos
            else:
                tile_pos = rx % 1
                if facing_down:
                    tile_pos = 1 - tile_pos

            color_index = math.floor(tile_pos * len(textures[tex_index]))
            color_index = max(
                0, min(color_index, len(textures[tex_index]) - 1))
            color = textures[tex_index][color_index]

        distance = math.sqrt((rx - px) ** 2 + (ry - py) ** 2)
        brightness = 1.0 - (min(distance, max_view_dist) / max_view_dist)

        if anaglyph:
            brightness = min(1.0, brightness + 0.3)

        return (
            int(color[0] * brightness),
            int(color[1] * brightness),
            int(color[2] * brightness)
        )


def check_collision(entity: Player | Enemy, moving_horiz: bool) -> None:
    left_bound_x = math.floor(entity.x - 0.25)
    right_bound_x = math.ceil(entity.x + 0.25)

    top_bound_y = math.floor(entity.y - 0.25)
    bottom_bound_y = math.ceil(entity.y + 0.25)

    for y in range(top_bound_y, bottom_bound_y):
        for x in range(left_bound_x, right_bound_x):
            if 0 <= y < len(world) and 0 <= x < len(world[y]):
                if world[y][x] > 0:
                    if entity == player and world[y][x] == 2:
                        global level, max_view_dist
                        level += 1
                        generate_world(level + 2)
                        player.x = 1.5
                        player.y = 1.5
                        player.x_vel = 0
                        player.y_vel = 0
                        player.ang_vel = 0
                        player.direction = 0
                        max_view_dist = level_max_view_dist
                        return

                    if moving_horiz:
                        if entity.x_vel > 0:
                            entity.x = x - 0.25
                        elif entity.x_vel < 0:
                            entity.x = x + 1.25
                        entity.x_vel = 0
                    else:
                        if entity.y_vel > 0:
                            entity.y = y - 0.25
                        elif entity.y_vel < 0:
                            entity.y = y + 1.25
                        entity.y_vel = 0
                    return

                elif entity != player and player.cooldown == 0:
                    xDist = player.x - entity.x
                    yDist = player.y - entity.y
                    dist = math.sqrt(xDist ** 2 + yDist ** 2)

                    if dist < 0.5:
                        player.cooldown = hit_cooldown
                        player.health -= 10


def clear_all_bullet_bits() -> None:
    for i, b in enumerate(bullets):
        left_bound_x = math.floor(b.x - 0.25)
        right_bound_x = math.ceil(b.x + 0.25)
        top_bound_y = math.floor(b.y - 0.25)
        bottom_bound_y = math.ceil(b.y + 0.25)

        for y in range(top_bound_y, bottom_bound_y):
            for x in range(left_bound_x, right_bound_x):
                if 0 <= y < len(world) and 0 <= x < len(world[y]):
                    if world[y][x] < 1:
                        bulletBits = -world[y][x]
                        bulletBits &= ~(1 << (i + bullet_offset))
                        world[y][x] = -bulletBits


def write_bullet_bits(i: int) -> None:
    b = bullets[i]
    left_bound_x = math.floor(b.x - 0.25)
    right_bound_x = math.ceil(b.x + 0.25)
    top_bound_y = math.floor(b.y - 0.25)
    bottom_bound_y = math.ceil(b.y + 0.25)

    for y in range(top_bound_y, bottom_bound_y):
        for x in range(left_bound_x, right_bound_x):
            if 0 <= y < len(world) and 0 <= x < len(world[y]):
                if world[y][x] < 1:
                    bulletBits = -world[y][x]
                    bulletBits |= 1 << (i + bullet_offset)
                    world[y][x] = -bulletBits


def clear_enemy_bits(i: int) -> None:
    e = enemies[i]
    if e is None:
        return

    left_bound_x = math.floor(e.x - 0.25)
    right_bound_x = math.ceil(e.x + 0.25)
    top_bound_y = math.floor(e.y - 0.25)
    bottom_bound_y = math.ceil(e.y + 0.25)

    for y in range(top_bound_y, bottom_bound_y):
        for x in range(left_bound_x, right_bound_x):
            if 0 <= y < len(world) and 0 <= x < len(world[y]):
                if world[y][x] < 1:
                    tile_bits = -world[y][x]
                    tile_bits &= ~(1 << (i + enemy_offset))
                    world[y][x] = -tile_bits


def write_enemy_bits(i: int) -> None:
    e = enemies[i]
    if e is None:
        return

    left_bound_x = math.floor(e.x - 0.25)
    right_bound_x = math.ceil(e.x + 0.25)
    top_bound_y = math.floor(e.y - 0.25)
    bottom_bound_y = math.ceil(e.y + 0.25)

    for y in range(top_bound_y, bottom_bound_y):
        for x in range(left_bound_x, right_bound_x):
            if i < enemy_max and 0 <= y < len(world) and 0 <= x < len(world[y]):
                if world[y][x] < 1:
                    tileBits = -world[y][x]
                    tileBits |= 1 << (i + enemy_offset)
                    world[y][x] = -tileBits


def check_bullet_collision(index: int) -> bool:
    b = bullets[index]

    left_bound_x = math.floor(b.x - 0.125)
    right_bound_x = math.ceil(b.x + 0.125)

    top_bound_y = math.floor(b.y - 0.125)
    bottom_bound_y = math.ceil(b.y + 0.125)

    for y in range(top_bound_y, bottom_bound_y):
        for x in range(left_bound_x, right_bound_x):
            if 0 <= y < len(world) and 0 <= x < len(world[y]):
                if world[y][x] > 0:
                    return True

                if world[y][x] < 0:
                    tile_bits = -world[y][x]
                    enemy_bits = tile_bits >> enemy_offset

                    for i in range(enemy_max):
                        if enemy_bits == 0:
                            break

                        if (enemy_bits & 1) == 0:
                            enemy_bits >>= 1
                            continue

                        enemy_bits >>= 1

                        if i < len(enemies) and (e := enemies[i]) is not None:
                            x_dist = e.x - b.x
                            y_dist = e.y - b.y
                            dist = math.sqrt(x_dist ** 2 + y_dist ** 2)

                            if dist < 0.375:
                                clear_enemy_bits(i)
                                enemies[i] = None
                                return True
    return False


def render() -> None:
    screen.fill((0, 0, 0))
    width, height = screen.get_size()

    # Render 1D view
    max_res = 450
    resolution = max(1, int(max_res / (10 / render_quality)))
    pixel_width = width / resolution

    for i in range(resolution):
        currentDir = (math.pi / 2) * (i / resolution - 0.5) + player.direction
        color = cast_ray(player.x, player.y, currentDir)

        startPos = int(round(i * pixel_width))
        endPos = int(round((i + 1) * pixel_width))
        pygame.draw.rect(screen, color, (startPos, 0,
                         endPos - startPos, height))
        
    # Draw damage overlay
    if player.cooldown > 0:
        overlay = pygame.Surface((width, height))
        overlay.set_alpha(128)
        overlay.fill((int(player.cooldown / hit_cooldown * 255), 0, 0))
        screen.blit(overlay, (0, 0))

    # Draw health bar when damaged
    if player.cooldown > 0:
        max_res = 450
        resolution = max(1, int(max_res / (10 / render_quality)))
        pixel_width = width / resolution
        health_bar_width = int((player.health / 100) * resolution) * pixel_width
        pygame.draw.rect(screen, (0, 192, 0), (0, 0, health_bar_width, height))

    # Render 2D minimap if enabled
    if show_2d:
        minimap_width, minimap_height = minimap.get_size()
        c_x = minimap_width // 2
        c_y = minimap_height // 2

        minimap.fill((0, 0, 0))

        # Draw world tiles centered on player
        for y in range(len(world)):
            for x in range(len(world[y])):
                if world[y][x] > 0:
                    tile_x = int((x - player.x) * 32 + c_x)
                    tile_y = int((y - player.y) * 32 + c_y)

                    if -32 <= tile_x <= minimap_width and -32 <= tile_y <= minimap_height:
                        pygame.draw.rect(minimap, (255, 255, 0),
                                         (tile_x, tile_y, 32, 32), 1)

                        if world[y][x] == 2:
                            pygame.draw.rect(minimap, tuple(
                                portal_color), (tile_x, tile_y, 32, 32))

        # Draw bullets
        for b in bullets:
            bullet_x = int((b.x - player.x) * 32 + c_x)
            bullet_y = int((b.y - player.y) * 32 + c_y)
            pygame.draw.circle(minimap, (255, 255, 0), (bullet_x, bullet_y), 4)

        # Draw player (always in center)
        pygame.draw.circle(minimap, (255, 0, 255), (c_x, c_y), 8)

        # Draw player eyes
        left_eye_ang = player.direction - math.pi / 5
        left_eye_x = c_x + math.cos(left_eye_ang) * 6
        left_eye_y = c_y + math.sin(left_eye_ang) * 6
        pygame.draw.circle(minimap, (255, 255, 255),
                           (int(left_eye_x), int(left_eye_y)), 3)

        right_eye_ang = player.direction + math.pi / 5
        right_eye_x = c_x + math.cos(right_eye_ang) * 6
        right_eye_y = c_y + math.sin(right_eye_ang) * 6
        pygame.draw.circle(minimap, (255, 255, 255),
                           (int(right_eye_x), int(right_eye_y)), 3)

        # Draw pupils
        left_pupil_ang = player.direction - math.pi / 6
        left_pupil_x = c_x + math.cos(left_pupil_ang) * 7.5
        left_pupil_y = c_y + math.sin(left_pupil_ang) * 7.5
        pygame.draw.circle(minimap, (0, 0, 0),
                           (int(left_pupil_x), int(left_pupil_y)), 1.5)

        right_pupil_ang = player.direction + math.pi / 6
        right_pupil_x = c_x + math.cos(right_pupil_ang) * 7.5
        right_pupil_y = c_y + math.sin(right_pupil_ang) * 7.5
        pygame.draw.circle(minimap, (0, 0, 0),
                           (int(right_pupil_x), int(right_pupil_y)), 1.5)

        # Draw enemies
        for e in enemies:
            if e is None:
                continue
            enemy_x = int((e.x - player.x) * 32 + c_x)
            enemy_y = int((e.y - player.y) * 32 + c_y)
            pygame.draw.circle(minimap, (255, 0, 0), (enemy_x, enemy_y), 8)

        screen.blit(minimap, (width - minimap_width - 10, 10))

    # Draw player info HUD
    large_font = pygame.font.SysFont(FONT_NAME, 32, True)
    info_y = 10
    line_height = 30
    hud_color = (255, 255, 0) if tex_index in (0, 3, 6) else (255, 255, 255)

    # Level info
    level_text = large_font.render(f"Level: {level}", True, hud_color)
    screen.blit(level_text, (10, info_y))
    info_y += line_height

    # Health info
    health_text = large_font.render(
        f"Health: {player.health}/100", True, hud_color)
    screen.blit(health_text, (10, info_y))
    info_y += line_height + 10

    # Controls info
    controls_font = pygame.font.SysFont(FONT_NAME, 24)
    controls = [
        "Controls:",
        "W/↑ = Forward",
        "S/↓ = Backward",
        "A/D = Strafe",
        "←/→ = Turn",
        "SPACE = Shoot"
    ]
    for line in controls:
        controls_text = controls_font.render(line, True, hud_color)
        screen.blit(controls_text, (10, info_y))
        info_y += 22


# Game loop
step_st = 30
while running:
    dt = clock.tick(60)
    tr = dt / step_st

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys["forward"] = True
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys["backward"] = True
            elif event.key == pygame.K_a:
                keys["left"] = True
            elif event.key == pygame.K_d:
                keys["right"] = True
            elif event.key == pygame.K_LEFT:
                keys["turn_left"] = True
            elif event.key == pygame.K_RIGHT:
                keys["turn_right"] = True
            elif event.key == pygame.K_SPACE:
                keys["shoot"] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                keys["forward"] = False
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                keys["backward"] = False
            elif event.key == pygame.K_a:
                keys["left"] = False
            elif event.key == pygame.K_d:
                keys["right"] = False
            elif event.key == pygame.K_LEFT:
                keys["turn_left"] = False
            elif event.key == pygame.K_RIGHT:
                keys["turn_right"] = False
            elif event.key == pygame.K_SPACE:
                keys["shoot"] = False

    # Update player rotation
    if keys["turn_right"]:
        player.ang_vel += ang_acc * tr
    elif keys["turn_left"]:
        player.ang_vel -= ang_acc * tr
    player.ang_vel *= (1 - ang_fric * tr)
    player.direction += player.ang_vel * tr

    # Calculate direction components
    x_comp = math.cos(player.direction)
    y_comp = math.sin(player.direction)

    # Handle movement
    if keys["forward"]:
        player.x_vel += x_comp * acc * tr
        player.y_vel += y_comp * acc * tr
    elif keys["backward"]:
        player.x_vel -= x_comp * acc / 2 * tr
        player.y_vel -= y_comp * acc / 2 * tr

    xCompPer = math.cos(player.direction - math.pi / 2)
    yCompPer = math.sin(player.direction - math.pi / 2)
    if keys["left"]:
        player.x_vel += xCompPer * acc * tr
        player.y_vel += yCompPer * acc * tr
    elif keys["right"]:
        player.x_vel -= xCompPer * acc * tr
        player.y_vel -= yCompPer * acc * tr

    # Handle shooting
    if keys["shoot"] and len(bullets) < bullet_max:
        keys["shoot"] = False
        bullets.append(Bullet(
            x=player.x,
            y=player.y,
            x_vel=x_comp * bullet_speed,
            y_vel=y_comp * bullet_speed,
            type=bullet_type
        ))

    # Apply friction
    player.x_vel *= (1 - fric * tr)
    player.y_vel *= (1 - fric * tr)

    # Update player position with collision detection
    rvx = abs(player.x_vel * tr)
    rvy = abs(player.y_vel * tr)
    x_dir = 1 if player.x_vel > 0 else -1
    y_dir = 1 if player.y_vel > 0 else -1

    while rvx > 0 or rvy > 0:
        if rvx > 1:
            player.x += x_dir
            rvx -= 1
        else:
            player.x += x_dir * rvx
            rvx = 0
        check_collision(player, True)

        if rvy > 1:
            player.y += y_dir
            rvy -= 1
        else:
            player.y += y_dir * rvy
            rvy = 0
        check_collision(player, False)

    # Update damage cooldown
    if player.cooldown > 0:
        player.cooldown = max(0, player.cooldown - dt)

    # Update bullets
    clear_all_bullet_bits()
    num_bullets = len(bullets)
    i = 0
    while i < len(bullets):
        b = bullets[i]
        if b is None:
            i += 1
            continue

        rvx = abs(b.x_vel * tr)
        rvy = abs(b.y_vel * tr)
        x_dir = 1 if b.x_vel > 0 else -1
        y_dir = 1 if b.y_vel > 0 else -1

        bullet_removed = False
        while rvx > 0 or rvy > 0 and not bullet_removed:
            if rvx > 1:
                b.x += x_dir
                rvx -= 1
            else:
                b.x += x_dir * rvx
                rvx = 0

            if check_bullet_collision(i):
                bullets.pop(i)
                bullet_removed = True
                break

            if rvy > 1:
                b.y += y_dir
                rvy -= 1
            else:
                b.y += y_dir * rvy
                rvy = 0

            if check_bullet_collision(i):
                bullets.pop(i)
                bullet_removed = True
                break

        if not bullet_removed and i < len(bullets):
            write_bullet_bits(i)
            i += 1

    # Update enemies
    for i in range(len(enemies)):
        e = enemies[i]
        if e is None:
            continue

        clear_enemy_bits(i)

        x_dist = player.x - e.x
        y_dist = player.y - e.y
        dist = math.sqrt(x_dist ** 2 + y_dist ** 2)

        if dist > 0:
            x_comp = x_dist / dist
            y_comp = y_dist / dist

            e.x_vel += x_comp * acc * tr
            e.y_vel += y_comp * acc * tr

        e.x_vel *= (1 - fric * tr)
        e.y_vel *= (1 - fric * tr)

        rvx = abs(e.x_vel * tr / 3)
        rvy = abs(e.y_vel * tr / 3)
        x_dir = 1 if e.x_vel > 0 else -1
        y_dir = 1 if e.y_vel > 0 else -1

        while rvx > 0 or rvy > 0:
            if rvx > 1:
                e.x += x_dir
                rvx -= 1
            else:
                e.x += x_dir * rvx
                rvx = 0
            check_collision(e, True)

            if rvy > 1:
                e.y += y_dir
                rvy -= 1
            else:
                e.y += y_dir * rvy
                rvy = 0
            check_collision(e, False)

        write_enemy_bits(i)

    # Update portal color animation
    portal_anim_speed = 5 * tr

    brightness = portal_color[0]
    if brighten_portal:
        brightness += portal_anim_speed
        if brightness > 255:
            brightness = 255
            brighten_portal = False
    else:
        brightness -= portal_anim_speed
        if brightness < 0:
            brightness = 0
            brighten_portal = True

    portal_color[0] = int(brightness)
    portal_color[1] = int(brightness)
    portal_color[2] = int(brightness)

    # Render game
    render()
    pygame.display.flip()

    # Check for game over
    if player.health <= 0:
        game_dialog.msg_box(f"You reached Level {level}. Press OK to exit.", 
                "Game Over", ["OK"])
        running = False

pygame.quit()
