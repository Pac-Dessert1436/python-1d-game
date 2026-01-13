# 1D-Game: Python Port

![](screenshot.png)

## Description
This is a Python port of the 1D-Game, a unique first-person game experienced from the perspective of a 2D life form. Your goal is to survive through procedurally generated levels, navigating pathways, avoiding enemies, and finding the exit portal.

[The original JavaScript version](https://github.com/mashpoe/1D-Game) was created by Mashpoe. This Python implementation maintains the core gameplay mechanics while providing a clean, well-structured codebase.

**Warning:** This game contains flashing colors that may be unsuitable for individuals with photosensitive epilepsy, especially when using certain texture settings.

## Features

- **1D Perspective Rendering**: Experience the world through a custom ray-casting system that simulates vision from a 2D entity's viewpoint, delivering a truly unique visual experience
- **Procedural Level Generation**: Each level is dynamically and randomly generated with distinct pathways, enemy spawn points, and environmental layouts
- **Enemy AI**: Navigate procedurally generated levels while evading hostile entities with basic pathfinding behavior
- **Refined Enemy Visual Identity**: Enemy colors in the 1D view are precisely calibrated to RGB value (255, 0, 192), eliminating visual overlap with the player's color scheme for clearer distinction
- **Weapon System**: Defend yourself against hostiles by firing bullets at enemies within your field of view
- **Multiple Texture Packs**: Customize your visual experience with a selection of distinct thematic texture packs
- **2D Minimap**: Optional minimap overlay to enhance spatial awareness and navigation
- **Responsive Controls**: Enjoy smooth, fluid movement (forward/backward/strafing) and rotation mechanics for precise navigation

## Installation

### Prerequisites
- Python 3.8 or higher
- Pygame (pygame-ce recommended)

### Setup
1. Clone or download this repository, and navigate to the project directory:
   ```bash
   git clone https://github.com/Pac-Dessert1436/python-1d-game.git
   cd python-1d-game
   ```
2. Install the required dependencies:
   ```bash
   pip install pygame-ce
   ```
3. Run the game:
   ```bash
   python __main__.py
   ```

## Controls

### Movement
- **W / Up Arrow**: Move forward
- **S / Down Arrow**: Move backward
- **A**: Strafe left
- **D**: Strafe right
- **Left Arrow**: Rotate counterclockwise
- **Right Arrow**: Rotate clockwise

### Actions
- **Space**: Shoot a bullet

### Options
- **Enter**: Confirm selections in dialogs
- **Esc**: Exit dialogs or quit the game

## Gameplay

1. **Core Objective**: Locate and reach the white exit portal to progress to the next increasingly challenging level
2. **Navigation**: Utilize the unique 1D perspective for immersive exploration, or enable the optional 2D minimap for enhanced spatial orientation
3. **Combat Mechanics**: Engage hostile entities by shooting bullets when they appear within your 1D field of view
4. **Enemy Threat**: Each enemy attack inflicts a consistent 10 HP of damage – avoid direct contact and prioritize evasion or elimination
5. **Health Recovery**: Collect green health power-ups (marked by a green plus sign on the minimap) to restore 15 HP and sustain your survival
6. **Progressive Difficulty**: Each subsequent level ramps up the challenge with increased enemy spawn rates and more complex level geometry

## Project Structure

```
python-1d-game/
├── __main__.py          # Main game entry point and core logic
├── essentials.py        # Game data structures and utilities
├── game_dialog.py       # UI dialog system
├── screenshot.png       # Gameplay screenshot
├── LICENSE              # BSD 3-Clause License file
└── README.md            # This file
```

## Technical Details

- **Rendering**: Uses a custom ray-casting algorithm to generate the 1D perspective view
- **Physics**: Implements basic movement physics with acceleration, friction, and collision detection
- **AI**: Enemies navigate using simple pathfinding algorithms
- **Textures**: Supports 7 different texture packs for visual variety
- **Performance**: Optimized rendering with adjustable quality settings

## License

This project is licensed under the BSD 3-Clause License. See the [LICENSE](LICENSE) file for full details.

## Attribution

- **Original Concept & JavaScript Implementation**: [Mashpoe](https://github.com/mashpoe/1D-Game)
- **Python Port**: Pac-Dessert1436

## Disclaimer

This software is provided "as is" and without any express or implied warranties, including, without limitation, the implied warranties of merchantability and fitness for a particular purpose.

The names of the original author or contributors may not be used to endorse or promote products derived from this software without specific prior written permission.