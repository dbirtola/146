import sys, logging, random
sys.path.insert(0, '../')
from planet_wars import issue_order

def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

    
def min_ships_from_my_strongest_planet_to_weakest_enemy(state):

    # (1) Targets come from the pool of enemies.
    target_planets = [planet for planet in state.enemy_planets() \
                      if not any(fleet.destination_planet == planet.ID \
                                 for fleet in state.my_fleets())]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(target_planets, key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send the necessary number of ships from my strongest planet to the weakest enemy planet.
        required_ships = weakest_planet.num_ships + \
                         state.distance(strongest_planet.ID, weakest_planet.ID) * \
                         weakest_planet.growth_rate + 1
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships)


def twice_min_ships_from_my_strongest_planet_to_weakest_enemy(state):

    # (1) Targets come from the pool of enemies.
    target_planets = [planet for planet in state.enemy_planets() \
                      if not any(fleet.destination_planet == planet.ID \
                                 for fleet in state.my_fleets())]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(target_planets, key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send the necessary number of ships from my strongest planet to the weakest enemy planet.
        required_ships = weakest_planet.num_ships + \
                         state.distance(strongest_planet.ID, weakest_planet.ID) * \
                         weakest_planet.growth_rate + 1
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships * 2)


def half_ships_from_my_strongest_planet_to_weakest_enemy(state):

    # (1) Targets come from the pool of enemies.
    target_planets = [planet for planet in state.enemy_planets() \
                      if not any(fleet.destination_planet == planet.ID \
                                 for fleet in state.my_fleets())]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(target_planets, key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the available ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def strongest_planet_spreads_to_weakest_neutral_planet(state):

    # (1) Targets come from the pool of neutral planets.
    target_planets = [planet for planet in state.neutral_planets() \
                      if not any(fleet.destination_planet == planet.ID \
                                 for fleet in state.my_fleets())]

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = min(target_planets, key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send the necessary number of ships from my strongest planet to the weakest enemy planet.
        required_ships = weakest_planet.num_ships + 1
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, required_ships * 1.5)


def min_ships_from_strongest_planet_to_nearest_enemy(state):
    checker = False

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Find enemy planet closest to my strongest planet (that I can actually take over).
    targets = sorted(state.enemy_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not targets:
        return False

    # Find nearest target I can actually hit
    for target in targets:
        if target.num_ships < strongest_planet.num_ships:
            checker = True
            break

    if not checker:
        return False
    else:
        # Send the necessary number of ships from my strongest planet.
        required_ships = target.num_ships + state.distance(strongest_planet.ID, target.ID) * \
                         target.growth_rate + 1
        return issue_order(state, strongest_planet.ID, target.ID, required_ships)


def min_ships_from_strongest_planet_to_nearest_neutral(state):

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Find neutral planet closest to my strongest planet (that I can actually take over).
    targets = sorted(state.neutral_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not targets:
        return False

    for target in targets:
        if target.num_ships < strongest_planet.num_ships:
            break

    if not target:
        return False
    else:
        # Send the necessary number of ships from my strongest planet.
        required_ships = target.num_ships + state.distance(strongest_planet.ID, target.ID) * \
                         target.growth_rate + 1
        return issue_order(state, strongest_planet.ID, target.ID, required_ships)


def min_ships_from_strongest_planet_to_nearest_any(state):
    checker = False

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Sort potential targets by distance.
    targets = sorted(state.not_my_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not targets:
        return False

    # Find nearest target I can actually hit
    for target in targets:
        if target.num_ships < strongest_planet.num_ships:
            checker = True
            break

    if not checker:
        return False
    else:
        # Send the necessary number of ships from my strongest planet.
        required_ships = target.num_ships + state.distance(strongest_planet.ID, target.ID) * \
                         target.growth_rate + 1
        return issue_order(state, strongest_planet.ID, target.ID, required_ships)


def twice_min_ships_from_strongest_planet_to_nearest_enemy(state):
    checker = False

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Find enemy planet closest to my strongest planet (that I can actually take over).
    targets = sorted(state.enemy_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not targets:
        return False

    # Find nearest target I can actually hit
    for target in targets:
        if target.num_ships < strongest_planet.num_ships:
            checker = True
            break

    if not checker:
        return False
    else:
        # Send the necessary number of ships from my strongest planet.
        required_ships = target.num_ships + state.distance(strongest_planet.ID, target.ID) * \
                         target.growth_rate + 1
        return issue_order(state, strongest_planet.ID, target.ID, required_ships * 2)


def twice_min_ships_from_strongest_planet_to_nearest_neutral(state):

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Find neutral planet closest to my strongest planet (that I can actually take over).
    targets = sorted(state.neutral_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not targets:
        return False

    for target in targets:
        if target.num_ships < strongest_planet.num_ships:
            break

    if not target:
        return False
    else:
        # Send the necessary number of ships from my strongest planet.
        required_ships = target.num_ships + state.distance(strongest_planet.ID, target.ID) * \
                         target.growth_rate + 1
        return issue_order(state, strongest_planet.ID, target.ID, required_ships * 2)


def twice_min_ships_from_strongest_planet_to_nearest_any(state):
    checker = False

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Sort potential targets by distance.
    targets = sorted(state.not_my_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not targets:
        return False

    # Find nearest target I can actually hit
    for target in targets:
        if target.num_ships < strongest_planet.num_ships:
            checker = True
            break

    if not checker:
        return False
    else:
        # Send the necessary number of ships from my strongest planet.
        required_ships = target.num_ships + state.distance(strongest_planet.ID, target.ID) * \
                         target.growth_rate + 1
        return issue_order(state, strongest_planet.ID, target.ID, required_ships * 2)


def reinforce_my_weakest_planet(state):

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # Find my weakest planet.
    weakest_planet = min(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        return False
    else:
        # Send half the strongest planet's ships to the weakest planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


def strongest_planet_reinforces_weakest_neighbor(state):
    count = 0

    # Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet:
        return False

    # Sort my planets as neighbors
    neighbors = sorted(state.my_planets(), key=lambda p: state.distance(p.ID, strongest_planet.ID), reverse=False)

    if not neighbors:
        return False

    # Find weakest of closest 5 neighbors
    weakest = neighbors[0]
    for neighbor in neighbors:
        count += 1
        if neighbor.num_ships < weakest.num_ships:
            weakest = neighbor
        if count == 5:
            break

    return issue_order(state, strongest_planet.ID, weakest.ID, strongest_planet.num_ships / 2)


def min_attack_random_enemy_from_nearest_planet(state):

    # Pick a random enemy.
    target = random.choice(state.enemy_planets())

    if not target:
        return False

    # Find my nearest planet (that can actually take the enemy)
    mine = sorted(state.my_planets(), key=lambda P: state.distance(P.ID, target.ID), reverse=False)

    if not mine:
        return False

    attacker = mine[0]
    for planet in mine:
        if planet.num_ships > target.num_ships:
            attacker = planet
            break

    required_ships = target.num_ships + state.distance(attacker.ID, target.ID) * \
                     target.growth_rate + 1
    return issue_order(state, attacker.ID, target.ID, required_ships)


def half_attack_random_enemy_from_nearest_planet(state):
    # Pick a random enemy.
    target = random.choice(state.enemy_planets())

    if not target:
        return False

    # Find my nearest planet (that can actually take the enemy)
    mine = sorted(state.my_planets(), key=lambda P: state.distance(P.ID, target.ID), reverse=False)

    if not mine:
        return False

    attacker = mine[0]
    for planet in mine:
        if planet.num_ships > target.num_ships:
            attacker = planet
            break

    return issue_order(state, attacker.ID, target.ID, attacker.num_ships / 2)


def min_attack_random_enemy_from_random_planet(state):

    # Pick a random enemy.
    target = random.choice(state.enemy_planets())

    if not target:
        return False

    # Pick a random planet of mine (that can actually take the enemy)
    while True:
        attacker = random.choice(state.my_planets())
        if attacker.num_ships > target.num_ships:
            break

    required_ships = target.num_ships + state.distance(attacker.ID, target.ID) * \
                     target.growth_rate + 1
    return issue_order(state, attacker.ID, target.ID, required_ships)


def half_attack_random_enemy_from_random_planet(state):

    # Pick a random enemy.
    target = random.choice(state.enemy_planets())

    if not target:
        return False

    # Pick a random planet of mine (that can actually take the enemy)
    while True:
        attacker = random.choice(state.my_planets())
        if attacker.num_ships > target.num_ships:
            break

    return issue_order(state, attacker.ID, target.ID, attacker.num_ships / 2)


def min_attack_weakest_enemy_from_nearest_planet(state):

    # Find the weakest enemy planet.
    target = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not target:
        return False

    mine = sorted(state.my_planets(), key=lambda p: state.distance(p.ID, target.ID), reverse=False)

    if not mine:
        return False

    attacker = mine[0]
    for my_planet in mine:
        if my_planet.num_ships > target.num_ships:
            attacker = my_planet
            break

    required_ships = target.num_ships + state.distance(attacker.ID, target.ID) * \
                     target.growth_rate + 1
    return issue_order(state, attacker.ID, target.ID, required_ships)


def half_attack_weakest_enemy_from_nearest_planet(state):
    # Find the weakest enemy planet.
    target = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not target:
        return False

    # Find nearest planet that can take it
    mine = sorted(state.my_planets(), key=lambda p: state.distance(p.ID, target.ID), reverse=False)

    if not mine:
        return False

    attacker = mine[0]
    for my_planet in mine:
        if my_planet.num_ships > target.num_ships:
            attacker = my_planet
            break

    return issue_order(state, attacker.ID, target.ID, attacker.num_ships / 2)


def half_attack_strongest_enemy_from_strongest_planet(state):

    # Find strongest enemy
    target = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # Find my strongest planet
    attacker = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not target or not attacker:
        return False

    return issue_order(state, attacker.ID, target.ID, attacker.num_ships / 2)


def min_attack_strongest_enemy_from_strongest_planet(state):
    # Find strongest enemy
    target = max(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    # Find my strongest planet
    attacker = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    if not target or not attacker:
        return False

    if attacker.num_ships < target.num_ships:
        required_ships = attacker.num_ships
    else:
        required_ships = target.num_ships + state.distance(attacker.ID, target.ID) * \
                         target.growth_rate + 1

    return issue_order(state, attacker.ID, target.ID, required_ships)
