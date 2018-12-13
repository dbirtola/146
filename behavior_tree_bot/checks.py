def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def still_targets_left(state):
    if len(state.not_my_planets()) == 0:
        return False
    else:
        return True

def currently_attacking_all_planets(state):
    target_planets = [planet for planet in state.not_my_planets() \
                      if not any(fleet.destination_planet == planet.ID \
                                 for fleet in state.my_fleets())]

    if len(target_planets) == 0:
        return False
    else:
        return True


def have_more_planets_than_enemy(state):
    return len(state.my_planets()) > len(state.enemy_planets())


def have_majority_of_planets(state):
    return len(state.my_planets()) > len(state.not_my_planets())


def enemy_has_majority_of_planets(state):
    return len(state.enemy_planets()) > len(state.my_planets()) + len(state.neutral_planets())


def strongest_planet_close_to_weakest_enemy(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    weakest_enemy_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    return state.distance(strongest_planet.ID, weakest_enemy_planet.ID) < 7


def strongest_planet_almost_too_strong(state):
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    next_strongest = max(state.my_planets(), key=lambda t: t.num_ships and t != strongest_planet, default=None)

    diff = strongest_planet.num_ships - next_strongest.num_ships

    return diff > 100

