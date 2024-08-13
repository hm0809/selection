#Natural Selection Simulation

This model simulates a population of creatures, represented as dots. They have various properties such as health, speed, and directional biases. Since they live on a 2d plane, they only have left/right and up/down; so we apply random directional biases and other properties to simulate heterogeneity in the first generation. The simulation introduces selection pressures, this requires the user to toggle one of the 4 quadrants of the 2d plane. This area will become "dangerous", it will remove their health and ultimately kill any creatures who have the directional bias to move toward it. Each generation lasts 8 seconds as a default, although values can be changed. As you would expect, the creatures who die likely had the genes that caused them to tend toward the dangerous quadrant, the ones that survived had directional biases away from the dangerous quadrant - hence the next generation is likely to aquire that favorable gene. Try for yourself, and have fun (:

#Mutation, Predatory Competion and Disease mechanics will be added soon

## Features

- **Randomized Creature Attributes**: Each creature is initialized with random health, speed, and directional biases.
- **Movement System**: Creatures move across the simulation area with a bias in both the X and Y directions.
- **Natural Selection**: Creatures reproduce after a set time period, with offspring inheriting attributes from their parents.
- **Interactive Quadrants**: Users can toggle damage in different quadrants of the simulation area by clicking, simulating environmental pressures.
- **Real-time Statistics**: The average health, speed, directional bias, and the number of living creatures are displayed and logged for each generation.

## Requirements

- Python 3.x
- Pygame
- `pip install pygame` or `py -m pip install pygam`e or `python -m pip install pygame`

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hm0809/selection.git
   cd selection
