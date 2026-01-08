import pygame
from dataclasses import dataclass
from game_dialog import GameDialog


@dataclass
class Player:
    x: float
    y: float
    x_vel: float
    y_vel: float
    ang_vel: float
    type: int
    direction: float
    cooldown: float
    health: int


@dataclass
class Enemy:
    x: float
    y: float
    x_vel: float
    y_vel: float
    type: int
    dir: float
    state: float


@dataclass
class Bullet:
    x: float
    y: float
    x_vel: float
    y_vel: float
    type: int


@dataclass
class Pathway:
    x: float
    y: float
    dist: int


def get_texture_index(dialog: GameDialog) -> int:
    def validate_texture_index(value: str) -> bool:
        try:
            idx = int(value)
            return 0 <= idx <= 6
        except ValueError:
            return False

    prompt = """Welcome to Python 1D Game! 
Available textures:

[0] Gray Waves (3D)
[1] Blue-Green Waves
[2] Trippy
[3] Gray Stripes (3D)
[4] Yellow Stripes (3D)
[5] Solid Red
[6] Barcode (3D)

Enter texture index (0-6):"""

    result = dialog.input_box(prompt, "Select Texture",
                              "4", validate_texture_index)

    if result.ok and result.value:
        try:
            return int(result.value)
        except ValueError:
            return 4
    return 4


type Color = tuple[int, int, int]
type List2D[T] = list[list[T]]
    
pygame.init()
pygame.display.set_caption("Python 1D Game")
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
minimap = pygame.Surface((300, 150))
dt: float = 0
running: bool = True

# Minimap

FONT_NAME = "Lucida Console"
game_dialog = GameDialog(screen, FONT_NAME)
tex_index = get_texture_index(game_dialog)

# Textures (converted from JS objects to Python tuples)
textures: List2D[Color] = [
    [(255, 255, 255), (192, 192, 192), (128, 128, 128),
     (64, 64, 64), (128, 128, 128), (192, 192, 192)],
    [(0, 0, 255), (0, 64, 192), (0, 128, 128),
     (0, 192, 64), (0, 128, 128), (0, 64, 192)],
    [(255, 0, 0), (255, 128, 0), (255, 255, 0),
     (0, 255, 0), (0, 0, 255), (255, 0, 255)],
    [(255, 255, 255), (128, 128, 128)],
    [(255, 255, 0), (128, 128, 0)],
    [(128, 0, 0)],
    [(255, 255, 255), (255, 255, 255), (0, 0, 0), (255, 255, 255),
     (0, 0, 0), (0, 0, 0), (255, 255, 255), (0, 0, 0)],
]

enemy_eye_color: Color = (255, 255, 255)
enemy_body_color: Color = (255, 0, 255)

enemy_texture_1d: list[Color] = [
    enemy_body_color,
    enemy_body_color,
    enemy_eye_color,
    (0, 0, 0),
    enemy_eye_color,
    enemy_body_color
]

game_over_background: Color = (0, 0, 0)
game_over_foreground: Color = (255, 255, 255)

# Game state
player_type: int = 1
player = Player(
    x=1.5,
    y=1.5,
    x_vel=0.0,
    y_vel=0.0,
    ang_vel=0.0,
    type=player_type,
    direction=0.0,
    cooldown=0.0,
    health=100
)

acc: float = 0.005
fric: float = 0.03
ang_acc: float = 0.003
ang_fric: float = 0.05
hit_cooldown: float = 1500
bullet_speed: float = 0.1

tutorial_max_view_dist = 400 / 32
level_max_view_dist = 200 / 32
max_view_dist = tutorial_max_view_dist

world: List2D[int] = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

level = 0
enemy_type = 2
enemies: list[Enemy | None] = []
spawn_enemies = True

bullet_type = 3
bullets: list[Bullet] = []

bullet_offset = 0
bullet_max = 8
enemy_offset = bullet_offset + bullet_max
enemy_max = 16

enemies.append(
    Enemy(x=8, y=10, x_vel=0, y_vel=0, type=enemy_type, dir=0, state=0)
)

anaglyph = False
show_2d = True
render_quality = 10

portal_color: list[int] = [255, 255, 255]
brighten_portal = False

keys = {
    "forward": False,
    "backward": False,
    "left": False,
    "right": False,
    "turn_left": False,
    "turn_right": False,
    "shoot": False
}