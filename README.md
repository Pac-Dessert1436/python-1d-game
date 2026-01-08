# 1D-Game: Python Port

![](screenshot.png)

## Description
This is a Python port of the 1D-Game, a unique first-person game experienced from the perspective of a 2D life form. Your goal is to survive through procedurally generated levels, navigating pathways, avoiding enemies, and finding the exit portal.

[The original JavaScript version](https://github.com/mashpoe/1D-Game) was created by Mashpoe. This Python implementation maintains the core gameplay mechanics while providing a clean, well-structured codebase.

**Warning:** This game contains flashing colors that may be unsuitable for individuals with photosensitive epilepsy, especially when using certain texture settings.

## Features

- **1D Perspective Rendering**: Experience the world through a unique ray-casting system that simulates vision from a 2D entity's viewpoint
- **Procedural Level Generation**: Each level is randomly generated with unique pathways and enemy placements
- **Enemy AI**: Navigate levels while avoiding hostile entities
- **Weapon System**: Shoot bullets to defend yourself
- **Multiple Texture Packs**: Choose from different visual themes
- **2D Minimap**: Optional minimap for spatial awareness
- **Responsive Controls**: Smooth movement and rotation mechanics

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

1. **Objective**: Find the white exit portal to advance to the next level
2. **Navigation**: Use the 1D perspective and optional minimap to explore the level
3. **Combat**: Shoot enemies when they appear in your field of view
4. **Health**: Avoid enemy attacks to maintain your health
5. **Progression**: Each level becomes progressively more challenging with increased enemy counts and complex pathways

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