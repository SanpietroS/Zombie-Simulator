"""
CPS310 - 2026 Fall - Assignment #1
Zombie Simulator

Group Members:
1. Sean Sanpietro

"""

import random
import math
import time


WIDTH = 18
HEIGHT = 8

STARTING_HUMANS = 13
STARTING_ZOMBIES = 2

MAX_ROUNDS = 100

HUMAN_REPRODUCTION_CHANCE = 0.08
ZOMBIE_DEATH_CHANCE = 0.02

HUMAN_MOVE_DISTANCE = 1
ZOMBIE_MOVE_DISTANCE = 1

# -----------------------------
# CREATE PEOPLE
# -----------------------------

humans = []
zombies = []

for i in range(STARTING_HUMANS):
    humans.append([
        random.randint(0, WIDTH - 1),
        random.randint(0, HEIGHT - 1)
    ])

for i in range(STARTING_ZOMBIES):
    zombies.append([
        random.randint(0, WIDTH - 1),
        random.randint(0, HEIGHT - 1)
    ])

# -----------------------------
# DISPLAY THE MAP
# -----------------------------

def display_map():
    grid = []

    for y in range(HEIGHT):
        row = []
        for x in range(WIDTH):
            row.append(".")
        grid.append(row)

    for x, y in humans:
        grid[y][x] = "H"

    for x, y in zombies:
        grid[y][x] = "Z"

    print()
    for row in grid:
        print("".join(row))

    print()
    print("Humans:", len(humans))
    print("Zombies:", len(zombies))


# -----------------------------
# MOVE HUMANS
# -----------------------------

def move_humans():
    for human in humans:
        x = human[0]
        y = human[1]

        # Humans move randomly.
        direction = random.randint(1, 4)

        if direction == 1:
            x += HUMAN_MOVE_DISTANCE
        elif direction == 2:
            x -= HUMAN_MOVE_DISTANCE
        elif direction == 3:
            y += HUMAN_MOVE_DISTANCE
        else:
            y -= HUMAN_MOVE_DISTANCE

        # Keep humans inside the map.
        x = max(0, min(WIDTH - 1, x))
        y = max(0, min(HEIGHT - 1, y))

        human[0] = x
        human[1] = y


# -----------------------------
# FIND NEAREST HUMAN
# -----------------------------

def find_nearest_human(zombie):
    if len(humans) == 0:
        return None

    closest_human = humans[0]
    closest_distance = math.dist(zombie, closest_human)

    for human in humans:
        distance = math.dist(zombie, human)

        if distance < closest_distance:
            closest_distance = distance
            closest_human = human

    return closest_human


# -----------------------------
# MOVE ZOMBIES
# -----------------------------

def move_zombies():
    for zombie in zombies:
        target = find_nearest_human(zombie)

        if target is None:
            return

        # Zombies move toward the nearest human.
        if zombie[0] < target[0]:
            zombie[0] += ZOMBIE_MOVE_DISTANCE
        elif zombie[0] > target[0]:
            zombie[0] -= ZOMBIE_MOVE_DISTANCE

        if zombie[1] < target[1]:
            zombie[1] += ZOMBIE_MOVE_DISTANCE
        elif zombie[1] > target[1]:
            zombie[1] -= ZOMBIE_MOVE_DISTANCE


# -----------------------------
 # Infected Humans 
    # -----------------------------

def infect_humans():
    infected = []

    for human in humans[:]:
        for zombie in zombies:
            if human[0] == zombie[0] and human[1] == zombie[1]:
                infected.append(human)
                break

    for human in infected:
        if human in humans:
            humans.remove(human)
            zombies.append(human)



# -----------------------------
# HUMAN REPRODUCTION
# -----------------------------

def reproduce_humans():
    new_humans = []

    if len(humans) < 2:
        return

    for i in range(len(humans)):
        for j in range(i + 1, len(humans)):
            human1 = humans[i]
            human2 = humans[j]

            distance = math.dist(human1, human2)

            # Two nearby humans can create a new human.
            if distance <= 2 and random.random() < HUMAN_REPRODUCTION_CHANCE:
                new_x = (human1[0] + human2[0]) // 2
                new_y = (human1[1] + human2[1]) // 2

                new_humans.append([new_x, new_y])

    humans.extend(new_humans)


# -----------------------------
# ZOMBIE DEATH
# -----------------------------

def zombie_death():
    remaining_zombies = []

    for zombie in zombies:
        if random.random() > ZOMBIE_DEATH_CHANCE:
            remaining_zombies.append(zombie)

    zombies.clear()
    zombies.extend(remaining_zombies)


# -----------------------------
# MAIN SIMULATION
# -----------------------------

print("===================================")
print("       ZOMBIE SIMULATOR")
print("===================================")

for round_number in range(1, MAX_ROUNDS + 1):

    print("\n===================================")
    print("ROUND", round_number)
    print("===================================")

    # Humans move first.
    move_humans()

    # Zombies chase humans.
    move_zombies()

    # Humans that meet zombies become zombies.
    infect_humans()

    # Nearby humans may reproduce.
    reproduce_humans()

    # A small number of zombies may disappear.
    zombie_death()

    display_map()

    # End the simulation if there are no humans.
    if len(humans) == 0:
        print("All humans have been infected!")
        print("The zombies win!")
        break

    # End the simulation if there are no zombies.
    if len(zombies) == 0:
        print("There are no zombies left!")
        print("The humans survive!")
        break

    # Pause so the simulation can be watched.
    time.sleep(0.5)

else:
    print("\nThe simulation reached the maximum number of rounds.")
    print("Final Humans:", len(humans))
    print("Final Zombies:", len(zombies))
