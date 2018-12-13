import sys, logging
sys.path.insert(0, '../')
from planet_wars import issue_order

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

