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


