# Panda3D Solar System Simulator

A realistic 3D solar system simulation built with Panda3D, featuring accurate physics-based gravity calculations and orbital mechanics. Watch planets orbit the sun, select celestial objects to inspect, and explore the solar system from various perspectives.

## Features

### Current Features
- **Realistic Physics**: N-body gravitational simulation with accurate mass and orbital calculations
- **Complete Solar System**: Includes the Sun, all 8 planets, and Earth's Moon
- **Orbital Mechanics**: Planets automatically calculate their orbital positions and velocities based on orbital periods
- **Interactive Camera**: 
  - Orbit around objects with mouse
  - Pan with keyboard (WASD, QE)
  - Smooth transitions when selecting objects
- **Object Selection**: Click on any celestial body to select and view information
- **Visual Trails**: Motion trails show the orbital paths of planets and moons
- **3D Models**: High-quality GLB models for all celestial bodies
- **Skybox**: Immersive backdrop for the simulation

### Technical Details
- Uses real-world physical constants and formulas
- Accurate planetary masses, radii, and orbital periods
- Configurable time scale for speeding up or slowing down simulation
- Custom scaling system for rendering large distances efficiently
- Collision detection for object selection

## Requirements

- Python 3.7 or higher
- [Panda3D](https://www.panda3d.org/) 1.10.0 or higher

### Quick Install

```bash
pip install -r requirements.txt
```

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or install manually:
   ```bash
   pip install panda3d
   ```
3. Ensure all model files are in the `models/` directory:
   - `backdrop.glb`
   - `sun8.glb`
   - `mercury2.glb`
   - `venus.glb`
   - `earth2.glb`
   - `moon.glb`
   - `mars.glb`
   - `jupiter2.glb`
   - `saturn8.glb`
   - `uranus2.glb`
   - `neptune.glb`

## Usage

Run the simulation:
```bash
python main.py
```

### Controls

- **Mouse Right-Click + Drag**: Rotate camera around target (yaw/pitch)
- **W / S**: Zoom in / Zoom out (or move forward/backward when no object selected)
- **A / D**: Pan left / Pan right
- **Q / E**: Pan up / Pan down
- **Left-Click**: Select a celestial object
- **Close Button**: Deselect the current object (appears in UI when object is selected)

### Camera Behavior

- When no object is selected: Free camera movement with panning and zooming
- When an object is selected: Camera smoothly follows the selected object at an appropriate distance

## Project Structure

```
panda3d/
├── main.py           # Main application entry point and physics update loop
├── objects.py        # Base class for all celestial objects (abstract)
├── star.py           # Star implementation (Sun)
├── planet.py         # Planet implementation
├── moon.py           # Moon implementation
├── camera.py         # Camera control system
├── select.py         # Object selection system (ray casting)
├── trail.py          # Motion trail rendering for orbits
├── requirements.txt  # Python dependencies
├── .gitignore        # Git ignore rules
├── LICENSE           # License file
├── README.md         # This file
└── models/           # 3D model files (GLB format)
    ├── backdrop.glb
    ├── sun8.glb
    ├── mercury2.glb
    ├── venus.glb
    ├── earth2.glb
    ├── moon.glb
    ├── mars.glb
    ├── jupiter2.glb
    ├── saturn8.glb
    ├── uranus2.glb
    └── neptune.glb
```

## Implementation Details

### Scaling System
The simulation uses real world values with multiple scales to handle astronomical distances:
- `dimension_scale`: 1e-6 (converts meters to renderable units)
- `distance_scale`: 5 (additional distance compression for visual purposes only) 
   *changed to 50 past the asteroid belt*
- `size_scale`: 3 (increases the sizes of objects for visual purposes only)
- `time_scale`: 1e5 (speeds up simulation time)

### Physics System
- Gravity is calculated using Newton's law of universal gravitation: F = G × (m₁ × m₂) / r²
- Velocity-Verlet integration for position and velocity updates
- All objects interact gravitationally with each other (N-body simulation)

## Notes

- The time scale affects physics accuracy: larger values result in less accurate integration due to frame rate
- Poor performance will cause miscalculations in physics values
- Trails purposely delayed to optimize and prevent lag 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Built with [Panda3D](https://www.panda3d.org/)
- 3D models are made using [Blender](https://www.blender.org/)
   - Textures are from [NASA](https://www.nasa.gov/) and [SSS](https://www.solarsystemscope.com/textures/)
