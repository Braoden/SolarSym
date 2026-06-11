# Panda3D Solar System Simulator

A realistic 3D solar system simulation built with Panda3D, featuring accurate physics-based gravity calculations and orbital mechanics using real-world values. Watch planets orbit the sun, select celestial objects to inspect, and explore the solar system from various perspectives.

## Features

- **Complete Solar System**: Includes the Sun, all 8 planets, and Earth's Moon
- **Interactive Camera**: 
  - Orbit around objects with mouse
  - Pan with keyboard (WASD, QE)
  - Smooth transitions when selecting objects
- **Time Scale**: Adjust dynamically how fast the simulation runs
- **Object Selection**: Click on any celestial body to select and view information
- **Dynamic & Interactable Minimap**: A display of the Sun's and planets' positions. Click on an object on the minimap to select it

## Requirements

- Python 3.7 or higher
- [Panda3D](https://www.panda3d.org/) 1.10.0 or higher

## Usage

To install the requirements and run the simulation, simply run the "run.bat" file

### Controls

- **Mouse Right-Click + Drag**: Rotate camera around target
- **W / S**: Zoom in / Zoom out (or move forward/backward when no object selected)
- **A / D**: Pan left / Pan right
- **Q / E**: Pan up / Pan down
- **Left-Click**: Select an object (works on minimap as well)

### Camera Behavior

- When no object is selected: Free camera movement with panning and zooming
- When an object is selected: Camera smoothly follows the selected object

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
├── menu.py           # For UI features
├── slider.py         # Dynamic slider to adjust simulation speed
├── nav.py            # Minimap implementation
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
   *increased to 50 past the asteroid belt*
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
