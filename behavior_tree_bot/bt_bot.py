#!/usr/bin/env python
#

"""
// There is already a basic strategy in place here. You can use it as a
// starting point, or you can throw it out entirely and replace it with your
// own.
"""
import logging, traceback, sys, os, inspect
logging.basicConfig(filename=__file__[:-3] +'.log', filemode='w', level=logging.DEBUG)
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check

from planet_wars import PlanetWars, finish_turn

node_dict = {
    "-": Selector,
    "_": Sequence,
    "A": if_neutral_planet_available,
    "B": have_largest_fleet,
    "C": still_targets_left,
    "D": currently_attacking_all_planets,
    "a": attack_weakest_enemy_planet,
    "b": spread_to_weakest_neutral_planet,
    "c": min_ships_from_my_strongest_planet_to_weakest_enemy,
    "d": twice_min_ships_from_my_strongest_planet_to_weakest_enemy,
    "e": half_ships_from_my_strongest_planet_to_weakest_enemy,
    "f": strongest_planet_spreads_to_weakest_neutral_planet,
    #"g": min_ships_from_strongest_planet_to_nearest_enemy,
    "h": min_ships_from_strongest_planet_to_nearest_neutral,
    "i": min_ships_from_strongest_planet_to_nearest_any,
    "j": twice_min_ships_from_strongest_planet_to_nearest_enemy,
    "k": twice_min_ships_from_strongest_planet_to_nearest_neutral,
    "l": twice_min_ships_from_strongest_planet_to_nearest_any,
    "m": reinforce_my_weakest_planet,
    "n": strongest_planet_reinforces_weakest_neighbor,
    "o": min_attack_random_enemy_from_nearest_planet,
    "p": half_attack_random_enemy_from_nearest_planet,
    "q": min_attack_random_enemy_from_random_planet,
    "r": half_attack_random_enemy_from_random_planet,
    "s": min_attack_weakest_enemy_from_nearest_planet,
    "t": half_attack_weakest_enemy_from_nearest_planet,
    "u": half_attack_strongest_enemy_from_strongest_planet,
    "v": min_attack_strongest_enemy_from_strongest_planet
}


def parse_tree(tree_string):

    root = Selector(name="Root")

    #Current node has the current selector or sequence that we are processing
    current_node = root

    for char in tree_string:
        if char == "-":
            #Selector
            new_node = Selector(name="Selector")
            new_node.parent_node = current_node
            new_node.child_nodes = []
            current_node.child_nodes.append(new_node)

        elif char == "_":
            #Sequence
            new_node = Sequence(name="Sequence")
            new_node.parent_node = current_node
            new_node.child_nodes = []
            current_node.child_nodes.append(new_node)

        elif char == "[":
            #Start children
            current_node = current_node.child_nodes[-1]

        elif char == "]":
            #End children
            current_node = current_node.parent_node

        elif char.isupper():
            #Check
            new_node = Check(node_dict[char])
            new_node.parent_node = current_node
            current_node.child_nodes.append(new_node)

        elif char.islower():                   
            #Action
            new_node = Action(node_dict[char])
            new_node.parent_node = current_node
            current_node.child_nodes.append(new_node)  
    logging.info('\n Decoded tree as: ' + root.tree_to_string())

    return root   

# You have to improve this tree or create an entire new one that is capable
# of winning against all the 5 opponent bots
def setup_behavior_tree():

    #logging.info('\n' + root.tree_to_string())
    file = open('behavior_tree_bot/tree.txt')
    root = parse_tree(file.readline())
    #logging.info('\n Decoded tree as: ' + root2.tree_to_string())



    """
    # Top-down construction of behavior tree
    root = Selector(name='High Level Ordering of Strategies')
    
    offensive_plan = Sequence(name='Offensive Strategy')
    largest_fleet_check = Check(have_largest_fleet)
    attack = Action(attack_weakest_enemy_planet)
    offensive_plan.child_nodes = [largest_fleet_check, attack]

    spread_sequence = Sequence(name='Spread Strategy')
    neutral_planet_check = Check(if_neutral_planet_available)
    spread_action = Action(spread_to_weakest_neutral_planet)
    spread_sequence.child_nodes = [neutral_planet_check, spread_action]

    root.child_nodes = [offensive_plan, spread_sequence, attack.copy()]
	"""



    return root

# You don't need to change this function
def do_turn(state):
    behavior_tree.execute(planet_wars)

if __name__ == '__main__':
    logging.basicConfig(filename=__file__[:-3] + '.log', filemode='w', level=logging.DEBUG)

	
    behavior_tree = setup_behavior_tree()

    try:
        map_data = ''
        while True:
            current_line = input()
            if len(current_line) >= 2 and current_line.startswith("go"):
                planet_wars = PlanetWars(map_data)
                do_turn(planet_wars)
                finish_turn()
                map_data = ''
            else:
                map_data += current_line + '\n'

    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
    except Exception:
        traceback.print_exc(file=sys.stdout)
        logging.exception("Error in bot.")
