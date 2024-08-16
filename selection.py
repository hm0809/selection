import pygame
import random
import math
import time

pygame.init()

WIDTH, HEIGHT = 1680, 890
PADDING = 50  #Padding around the simulation box
screen = pygame.display.set_mode((WIDTH + PADDING * 2, HEIGHT + PADDING * 2))
pygame.display.set_caption("Creature Simulation")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (50, 50, 50)

font = pygame.font.SysFont(None, 21)
font2 = pygame.font.SysFont(None, 14)

#Can toggle, so all of to start
damage_quartiles = {
    "top_left": 0,
    "top_right": 0,
    "bottom_left": 0,
    "bottom_right": 0,
}

food_density = {
    "x": 0,
    "y": 0,
    "spread": 0

}

#Damage amount, adjusting for frame rate of 60
damage_value = 30 / 60

class Creature:
    def __init__(self, health=None, speed=None, direction_bias_x=None, direction_bias_y=None):
        self.radius = 12
        self.x = random.randint(self.radius, WIDTH - self.radius) + PADDING
        self.y = random.randint(self.radius, HEIGHT - self.radius) + PADDING

        #Properties of creature, random initially, then inherited in future generations.
        self.health = health if health is not None else random.uniform(0.75, 1.25) * 100
        self.initial_health = self.health  #Store initial health
        self.speed = speed if speed is not None else random.uniform(1.5, 3.2) * 2
        self.direction_bias_x = direction_bias_x if direction_bias_x is not None else random.uniform(-0.3, 0.3)
        self.direction_bias_y = direction_bias_y if direction_bias_y is not None else random.uniform(-0.3, 0.3)
        self.radius = max(1, ((self.health - 90) / 100) + 5)

        #Random initial direction
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

    def move(self):
        #Apply random movements but with the randomly or inherited direction bias
        self.dx += self.direction_bias_x + random.uniform(-0.1, 0.1)
        self.dy += self.direction_bias_y + random.uniform(-0.1, 0.1)

        #Preventing speed from increasing too much
        magnitude = math.sqrt(self.dx**2 + self.dy**2)
        self.dx = (self.dx / magnitude) * self.speed
        self.dy = (self.dy / magnitude) * self.speed

        #Update position and make sure dont go through wall
        new_x = self.x + self.dx
        new_y = self.y + self.dy

        if new_x <= self.radius + PADDING or new_x >= WIDTH + PADDING - self.radius:
            self.dx = -self.dx

        if new_y <= self.radius + PADDING or new_y >= HEIGHT + PADDING - self.radius:
            self.dy = -self.dy


        self.x += self.dx
        self.y += self.dy

        #Damage urself
        self.apply_damage()

    def apply_damage(self):

        if self.x < WIDTH / 2 + PADDING and self.y < HEIGHT / 2 + PADDING:
            self.health -= damage_quartiles["top_left"]
        elif self.x >= WIDTH / 2 + PADDING and self.y < HEIGHT / 2 + PADDING:
            self.health -= damage_quartiles["top_right"]
        elif self.x < WIDTH / 2 + PADDING and self.y >= HEIGHT / 2 + PADDING:
            self.health -= damage_quartiles["bottom_left"]
        elif self.x >= WIDTH / 2 + PADDING and self.y >= HEIGHT / 2 + PADDING:
            self.health -= damage_quartiles["bottom_right"]

        self.radius = max(1, ((self.health - 1) / 90) * 7 + 10)

        health_clamped = max(0, min(self.health, 100))

        #Gradient for health
        green_value = int((health_clamped / 100) * 255)
        red_value = 255 - green_value
        self.color = (red_value, green_value, 0)

        

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        """" Commented out, could be a useful debugging tool though, as it shows all the properties of individual creatures
        text = font2.render(
            f"h: {int(self.health)} s: {round(self.speed, 2)} bx: {round(self.direction_bias_x, 2)} by: {round(self.direction_bias_y, 2)}",
            True,
            WHITE,
        )
        screen.blit(text, (self.x - self.radius, self.y - self.radius - 20)) 
        """

class Food:
    def __init__(self):
        pass
#Calculate average values on call, so it doesn't happen 60*8 times every generation lmao
def calculate_averages(creatures, calculate, mutations):
    if creatures and calculate:
        avg_health = sum([creature.initial_health for creature in creatures]) / len(creatures)
        avg_speed = sum([creature.speed for creature in creatures]) / len(creatures)
        avg_bias_x = sum([creature.direction_bias_x for creature in creatures]) / len(creatures)
        avg_bias_y = sum([creature.direction_bias_y for creature in creatures]) / len(creatures)
        alive = len(creatures)
    return [avg_health, avg_speed, avg_bias_x, avg_bias_y, alive, mutations]


def display_averages(creatures, screen, avg_list, write_to_file):
    avg_health = avg_list[0]
    avg_speed = avg_list[1]
    avg_bias_x = avg_list[2]
    avg_bias_y = avg_list[3]
    alive = avg_list[4]
    mutations = avg_list[5]
    
    if creatures:
        avg_text = font.render(
            f"Avg Health: {round(avg_health, 2)}  Avg Speed: {round(avg_speed, 2)}  Avg Bias X: {round(avg_bias_x, 2)}  Avg Bias Y: {round(avg_bias_y, 2)}  Alive: {alive} Mutations: {mutations}",
            True,
            WHITE,
        )
    
        screen.blit(avg_text, (PADDING, HEIGHT + PADDING + 10))
    if write_to_file:
        with open("generation_values.txt", "a") as file:
            file.write(
                f"Health: {round(avg_health, 2)}, Speed: {round(avg_speed, 2)}, BX: {round(avg_bias_x, 2)}, BY: {round(avg_bias_y, 2)}, Alive: {round(len(creatures))}\n"
            )


def draw_quadrants(screen):
    #Draw quadrants with their respective damage status
    #Quadrants will be red if active and grey if inactive
    colors = {
        "top_left": RED if damage_quartiles["top_left"] > 0 else GREY,
        "top_right": RED if damage_quartiles["top_right"] > 0 else GREY,
        "bottom_left": RED if damage_quartiles["bottom_left"] > 0 else GREY,
        "bottom_right": RED if damage_quartiles["bottom_right"] > 0 else GREY,
    }
    pygame.draw.rect(screen, colors["top_left"], (PADDING, PADDING, WIDTH / 2, HEIGHT / 2))
    pygame.draw.rect(screen, colors["top_right"], (PADDING + WIDTH / 2, PADDING, WIDTH / 2, HEIGHT / 2))
    pygame.draw.rect(screen, colors["bottom_left"], (PADDING, PADDING + HEIGHT / 2, WIDTH / 2, HEIGHT / 2))
    pygame.draw.rect(screen, colors["bottom_right"], (PADDING + WIDTH / 2, PADDING + HEIGHT / 2, WIDTH / 2, HEIGHT / 2))


def toggle_damage(x, y):
    if x < WIDTH / 2 + PADDING and y < HEIGHT / 2 + PADDING:
        #TL
        damage_quartiles["top_left"] = damage_value if damage_quartiles["top_left"] == 0 else 0
    elif x >= WIDTH / 2 + PADDING and y < HEIGHT / 2 + PADDING:
        #TR
        damage_quartiles["top_right"] = damage_value if damage_quartiles["top_right"] == 0 else 0
    elif x < WIDTH / 2 + PADDING and y >= HEIGHT / 2 + PADDING:
        #BL
        damage_quartiles["bottom_left"] = damage_value if damage_quartiles["bottom_left"] == 0 else 0
    elif x >= WIDTH / 2 + PADDING and y >= HEIGHT / 2 + PADDING:
        #BR
        damage_quartiles["bottom_right"] = damage_value if damage_quartiles["bottom_right"] == 0 else 0

def main():
    MUTATION_RATE = 0.1
    global mutations
    mutations = 0
    with open("generation_values.txt", "a") as file:
        file.write("NEW SIM \n\n\n\n\n\n\n")
    clock = pygame.time.Clock()
    initial_population_size = 100
    creatures = [Creature() for _ in range(initial_population_size)]  

    start_time = time.time()
    generation = 1

    running = True
    avg_list = calculate_averages(creatures, True, mutations)

    display_averages(creatures, screen, avg_list, True)

    def mutate_trait(trait, trait_name):
        RELATIVE_STRENGTH = {
            "health": 0.2,
            "speed": 0.15,
            "direction_bias_x": 0.12,
            "direction_bias_y": 0.12 
        }
        if random.random() < MUTATION_RATE:
            #Apply mutation depending on strength and property
            mutation_strength = RELATIVE_STRENGTH[trait_name]
            mutation_factor = 1 + random.uniform(-mutation_strength, mutation_strength)
            global mutations
            mutations += 1
            return trait * mutation_factor
        return trait
    
    def reproduce(parent1, parent2):
        # Offspring inherits traits from parents with possible mutations
        health = mutate_trait(random.choice([parent1.initial_health, parent2.initial_health]), "health")
        speed = mutate_trait(random.choice([parent1.speed, parent2.speed]), "speed")
        direction_bias_x = mutate_trait(random.choice([parent1.direction_bias_x, parent2.direction_bias_x]), "direction_bias_x")
        direction_bias_y = mutate_trait(random.choice([parent1.direction_bias_y, parent2.direction_bias_y]), "direction_bias_y")

        return Creature(
            health=health,
            speed=speed,
            direction_bias_x=direction_bias_x,
            direction_bias_y=direction_bias_y
        )


    while running:
        screen.fill(BLACK)

        draw_quadrants(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Toggle quad
                x, y = event.pos
                toggle_damage(x, y)

        #Shows the timer for the next generation of creatures hehehhe
        elapsed_time = time.time() - start_time
        timer_text = font.render(f"Generation: {generation}  Time Left: {round(8 - elapsed_time, 1)}s", True, WHITE)
        screen.blit(timer_text, (WIDTH // 2, PADDING + 10))

        #Move and draw each creature
        for creature in creatures:
            creature.move()
            creature.draw(screen)

        #Dead gets deaded
        creatures = [creature for creature in creatures if creature.health > 0]

        #Averages
        avg_list[4] = len(creatures)
        display_averages(creatures, screen, avg_list, False)

        #End of generation logic
        if elapsed_time > 8:
            #Reproduce for new generation up to population size 
            creatures_temp = []
            for i in range(initial_population_size):
                parent1, parent2 = random.sample(creatures, 2)
                offspring = reproduce(parent1, parent2)
                creatures_temp.append(offspring)
            creatures = creatures_temp
            
            avg_list = calculate_averages(creatures, True, mutations)
            display_averages(creatures, screen, avg_list, True)

            generation += 1
            start_time = time.time()  #Reset da timerrrrr

        #To update the display
        pygame.display.flip()
        #FPS at 60, may change
        clock.tick(60) 

    pygame.quit()


if __name__ == "__main__":
    main()
