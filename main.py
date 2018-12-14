import copy
import heapq
import metrics
import multiprocessing.pool as mpool
import os
import random
import shutil
import time
import math
import run
from behavior_tree_bot.behaviors import *
from behavior_tree_bot.checks import *
from behavior_tree_bot.bt_nodes import Selector, Sequence, Action, Check



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


def get_node_string(node):
    node_string = ""

    if isinstance(node, Selector):
        node_string += "-["
        #code to add children values
        for child in node.child_nodes:
            node_string += get_node_string(child)
        node_string += "]"

        return node_string

    if isinstance(node, Sequence):
        node_string += "_["
        #code to add children values        
        for child in node.child_nodes:
            node_string += get_node_string(child)

        node_string += "]"
        return node_string

    if isinstance(node, Action):
        return next((symbol for symbol, n in node_dict.items() if n == node.action_function))

    if isinstance(node, Check):
        return next((symbol for symbol, n in node_dict.items() if n == node.check_function))




# The level as a grid of tiles

class Individual_Grid(object):
    __slots__ = ["genome", "_fitness", "_results"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None
        self._results = None

    # Update this individual's estimate of its fitness.
    # This can be expensive so we do it once and then cache the result.



    def calculate_fitness(self):

        tree = self.genome
        tree_string = get_node_string(tree)
        #print("Tree was turned into: ", tree_string)
        #input("GO ON?!")
        with open("behavior_tree_bot/tree.txt", "w") as file:
            file.write(tree_string)
        results = run.run_test()
        #print("Results: ", results)
        #self._fitness = 10 + results['wins'] - 2 * results['crashes'] - results['timed_out']

    
        
        self._fitness = 10 + 0.5 * results['easy_bot'] + 1.5* results['spread_bot'] + 1.7 *results['aggressive_bot'] + 0.8 * results['production_bot'] - 2 * results['crashes'] - results['timed_out'] + 0.5*results["unique_wins"]
        self._results = results

        #measurements = metrics.metrics(self.to_level())
        # Print out the possible measurements or look at the implementation of metrics.py for other keys:
        # print(measurements.keys())
        # Default fitness function: Just some arbitrary combination of a few criteria.  Is it good?  Who knows?
        # STUDENT Modify this, and possibly add more metrics.  You can replace this with whatever code you like.


        #####################################################################
        ##                            TODO                             
        ##  We need to think of a way to calculate fitness. The naive solution is to
        ##  literally just run the game and check our win rate. Unfortunately this would
        ##  take a lot of time. Keep an eye out for patterns that might give us a better
        ##  way to analyze trees success without actually running it. In the meantime,
        ##  this should probably just create the behavior tree from our genome and
        ##  run the planet wars program.
        ##
        ##  -Damen
        #####################################################################

        """
        coefficients = dict(
            meaningfulJumpVariance=0.5,
            negativeSpace=0.6,
            pathPercentage=0.5,
            emptyPercentage=0.6,
            linearity=-0.5,
            solvability=2.0
        )

        self._fitness = sum(map(lambda m: coefficients[m] * measurements[m],
                                coefficients))
        """
        return self

    # Return the cached fitness value or calculate it as needed.
    def fitness(self):
        if self._fitness is None:
            self.calculate_fitness()
        return self._fitness

    # Mutate a genome into a new genome.  Note that this is a _genome_, not an individual!
    def mutate(self, genome):
        # STUDENT implement a mutation operator, also consider not mutating this individual
        # STUDENT also consider weighting the different tile types so it's not uniformly random
        # STUDENT consider putting more constraints on this to prevent pipes in the air, etc




        #####################################################################
        ##                            TODO                             
        ##  For mutate, I'm thinking we start simple. Have a mutate rate of 5-15%
        ##  which 50/50 adds or removes a random node at a random point in the tree
        ##  we can come up with more clever solutions when that one works, or if whoever
        ##  is assigned this task already has a more clever solution in mind feel free to try it out.
        ##
        ##  -Damen
        #####################################################################



        left = 1
        right = width - 1
        for y in range(height):
            for x in range(left, right):
                pass
        return genome

    # Create zero or more children from self and other
    def generate_children(self, other):
        new_genome1 = copy.deepcopy(self.genome)
        new_genome2 = copy.deepcopy(other.genome)

        def tree_to_list(tree_list, node):

            current_node = node

            #Don't add the root, for now
            if current_node.parent_node != None:
            	tree_list.append(current_node)

            if(isinstance(node, Sequence) or isinstance(node, Selector)):

                if len(current_node.child_nodes) > 0:
                    for node2 in current_node.child_nodes:
                        tree_to_list(tree_list, node2)


        tree_as_list = []
        tree_to_list(tree_as_list, new_genome1)
        """
        print("\nGenerated tree list of self as: ")
        for node in tree_as_list:
            print(str(node))
        """
        other_as_list = []
        tree_to_list(other_as_list, new_genome2)
        """
        print("\nGenerated tree list of other as: ")
        for node in other_as_list:
            print(str(node))
        """

        #If either is empty, just return copies of themselves
        if(len(other_as_list) == 0 or len(tree_as_list) == 0):
        	return (Individual_Grid(new_genome1),Individual_Grid(new_genome2))


        random_node = random.choice(tree_as_list)
        other_node = random.choice(other_as_list)


        random_node_parent = random_node.parent_node
        other_node_parent = other_node.parent_node

        #print("Parents of nodes: " + str(random_node.parent_node) + ", " + str(other_node.parent_node))

        if random_node_parent != None:
            #Insert into the behavior tree
            random_node_index = random_node_parent.child_nodes.index(random_node)

            random_node_parent.child_nodes.remove(random_node)
            random_node_parent.child_nodes.insert(random_node_index, other_node)
            other_node.parent_node = random_node_parent
        


        if other_node_parent != None:
            #insert into other behavior tree
            other_node_index = other_node_parent.child_nodes.index(other_node)

            other_node_parent.child_nodes.remove(other_node)
            other_node_parent.child_nodes.insert(other_node_index, random_node)
            random_node.parent_node = other_node_parent


        if random_node_parent == None:
            new_genome2 = other_node
            new_genome2.parent_node = None
        if other_node_parent == None:
            new_genome1 = random_node
            new_genome1.parent_node = None
        #print("Generated new genome1 : " + new_genome1.tree_to_string())
        #print("Generated new genome2 : " + new_genome2.tree_to_string())

        #####################################################################
        ##                            TODO                             
        ##  We should implement either single or two point crossover here.
        ##
        ##  -Damen
        #####################################################################

        #print("Parents of nodes2: " + str(random_node.parent_node) + ", " + str(other_node.parent_node))

        return (Individual_Grid(new_genome1),Individual_Grid(new_genome2))

    # Turn the genome into a level string (easy for this genome)
    def to_tree(self):
        return self.genome

    # These both start with every floor tile filled with Xs
    # STUDENT Feel free to change these
    @classmethod
    def empty_individual(cls):
        """
        # Top-down construction of behavior tree
        root = Selector(name='High Level Ordering of Strategies')
        
        offensive_plan = Sequence(name='Offensive Strategy')
        largest_fleet_check = Check(have_largest_fleet)
        attack = Action(attack_weakest_enemy_planet)
        offensive_plan.child_nodes = [largest_fleet_check, attack]

        for node in offensive_plan.child_nodes:
            node.parent_node = offensive_plan

        spread_sequence = Sequence(name='Spread Strategy')
        neutral_planet_check = Check(if_neutral_planet_available)
        spread_action = Action(spread_to_weakest_neutral_planet)
        spread_sequence.child_nodes = [neutral_planet_check, spread_action]

        for node in spread_sequence.child_nodes:
            node.parent_node = spread_sequence

        root.child_nodes = [offensive_plan, spread_sequence, attack.copy()]

        for node in root.child_nodes:
            node.parent_node = root

        root.parent_node = None
        """

        root = Selector(name = 'High Level Ordering of Strategies')
        root.child_nodes = []
        #print("Starting with: " + root.tree_to_string())
        #input()
        root.parent_node = None
        return cls(root)

    @classmethod
    def random_individual(cls):
        root = Selector([], name='High Level Ordering of Strategies')
        root.parent_node = None

        #print("Starting with: " + root.tree_to_string())
        g = generate_tree(root)

        #print("test")

        #print("Generated random treE: " + g.tree_to_string())
        #input()
        #print("Created: " + g.tree_to_string())
        return cls(g)

def generate_tree(root):
    num_children = random.randint(2, 5)
    while True:

        is_composite = random.randint(0, 100) < 10
        if is_composite:
            new_class = ["-", Selector] if random.randint(0, 2) == 0 else ["_", Sequence]
        else:
            new_class = random.choice(list(node_dict.items()))

        if new_class[1] == Selector:

            new_node = Selector(name = "Selector")
            new_node.child_nodes = []
            new_root = generate_tree(new_node)
            new_root.parent_node = root
            root.child_nodes.append(new_root)

        elif new_class[1] == Sequence:            

            new_node = Sequence(name = "Sequence")
            new_node.child_nodes = []
            new_root = generate_tree(new_node)
            new_root.parent_node = root
            root.child_nodes.append(new_root)

        elif new_class[0].isupper():
            new_node = Check(new_class[1])
            new_node.parent_node = root
            root.child_nodes.append(new_node)

        elif new_class[0].islower():
            new_node = Action(new_class[1])
            new_node.parent_node = root
            root.child_nodes.append(new_node)

        if num_children > 0:
            num_children -= 1
        if num_children <= 0:
            break
    return root


def offset_by_upto(val, variance, min=None, max=None):
    val += random.normalvariate(0, variance**0.5)
    if min is not None and val < min:
        val = min
    if max is not None and val > max:
        val = max
    return int(val)


def clip(lo, val, hi):
    if val < lo:
        return lo
    if val > hi:
        return hi
    return val

# Inspired by https://www.researchgate.net/profile/Philippe_Pasquier/publication/220867545_Towards_a_Generic_Framework_for_Automated_Video_Game_Level_Creation/links/0912f510ac2bed57d1000000.pdf


Individual = Individual_Grid

def generate_successors(population):
    results = []
    # STUDENT Design and implement this
    # Hint: Call generate_children() on some individuals and fill up results.

    #####################################################################
    ##                            TODO                             
    ##  Generate some successors. This will need a working fitness function
    ##  to work properly.
    ##  -Damen
    #####################################################################
    """
    print("Before sort: ")
    for pop in population:
        print(pop.fitness())

    """

    sorted_pop = sorted(population, key=lambda p: p.fitness())

    """
    print("After sort: ")
    for pop in sorted_pop:
        print(pop.fitness())
	"""


    #input()
    continuing_pop = sorted_pop[len(sorted_pop)//2:]

    """
    print("After cuts: ")
    for pop in continuing_pop:
        print(pop.fitness())
    """
    new_children = []
    num_remaining = len(continuing_pop)



    #print("There are : " + str(num_remaining) + " successors")

    old_average_fitness = 0
    for pop in sorted_pop:
    	old_average_fitness += pop.fitness()
    old_average_fitness /= len(sorted_pop)


    #input()
    for i in range(0, num_remaining//2):
        c1, c2 = continuing_pop[random.randint(0, num_remaining-1)].generate_children(continuing_pop[random.randint(0, num_remaining-1)])
        new_children.append(c1)
        new_children.append(c2)




    print("\n\n\n ---- NEW GENERATION ---- \n\n")    
    print("Average fitness of last generation: " + str(old_average_fitness))
    print("Old generation fitnesses: ")
    for pop in sorted_pop:
    	print(str(pop.fitness()))


    print("Highest successor has fitness: " + str(continuing_pop[-1].fitness()))
    print("Highest successor had results: " + str(continuing_pop[-1]._results))
    continuing_pop.extend(new_children)
    #print("After children : " + str(len(continuing_pop)))
    #input()
    return continuing_pop


def ga():
    # STUDENT Feel free to play with this parameter
    pop_limit = 4

    # Code to parallelize some computations
    batches = os.cpu_count()


    batches = 1


    if pop_limit % batches != 0:
        print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
    batch_size = int(math.ceil(pop_limit / batches))



    with mpool.Pool(processes=os.cpu_count()) as pool:
        init_time = time.time()

        # STUDENT (Optional) change population initialization
        population = [Individual.random_individual() if random.random() < 0.8
                      else Individual.empty_individual()
                      for _g in range(pop_limit)]

        """
        print("\n\n Initial Population \n\n")

        for tree in population:
            print(tree.to_tree().tree_to_string())

        input()
        """

        # But leave this line alone; we have to reassign to population because we get a new population that has more cached stuff in it.
        population = pool.map(Individual.calculate_fitness,
                              population,
                              batch_size)
        init_done = time.time()
        print("Created and calculated initial population statistics in:", init_done - init_time, "seconds")
        generation = 0
        start = time.time()
        now = start
        print("Use ctrl-c to terminate this loop manually.")
        try:
            while True:                
                #input("\nReady for next gen?: \n")
                now = time.time()
                # Print out statistics
                if generation > 0:
                    #print("POPULATION: " + str(population))
                    #print("FITNESS: " + str(Individual.fitness))
                    best = max(population, key=Individual.fitness)
                    print("Generation:", str(generation))
                    print("Max fitness:", str(best.fitness()))
                    print("Average generation time:", (now - start) / generation)
                    print("Net time:", now - start)

                    #####################################################################
                    ##                            TODO                             
                    ##  Reconstruct the behavior tree of our best individual and use the
                    ##  behavior tree print function to write its output to a file
                    ##  -Damen
                    #####################################################################

                    #with open("levels/last.txt", 'w') as f:
                    #    for row in best.to_level():
                    #        f.write("".join(row) + "\n")




                generation += 1


                # STUDENT Determine stopping condition
                stop_condition = (generation > 4)
                if stop_condition:
                    break

                # STUDENT Also consider using FI-2POP as in the Sorenson & Pasquier paper
                gentime = time.time()
                next_population = generate_successors(population)
                gendone = time.time()
                print("Generated successors in:", gendone - gentime, "seconds")

                # Calculate fitness in batches in parallel
                next_population = pool.map(Individual.calculate_fitness,
                                           next_population,
                                           batch_size)
                popdone = time.time()
                print("Calculated fitnesses in:", popdone - gendone, "seconds")
                population = next_population


        except KeyboardInterrupt:
            pass

    return population


if __name__ == "__main__":


    #Remember, the extra selector being added when encoding/decoding may not be given a parent_node.
    #All nodes need to have a parent_node, and the root should have it set to None
    """
    p1 = Individual.empty_individual()
    p2 = Individual.empty_individual()

    c1, c2 = p1.generate_children(p2)

    print("Parent1: " + p1.to_tree().tree_to_string())
    print("Parent2: " + p2.to_tree().tree_to_string())

    print("Child1: " + c1.to_tree().tree_to_string())
    print("Child2: " + c2.to_tree().tree_to_string())

    print("Test: ", test_indiv.to_tree())

    print("Calculated fitness: ", test_indiv.fitness())
    input()
    """

    final_gen = sorted(ga(), key=Individual.fitness, reverse=True)
    best = final_gen[0]
    print("Best fitness: " + str(best.fitness()))
    print("Tree looks like: " + best.to_tree().tree_to_string())


    now = time.strftime("%m_%d_%H_%M_%S")


    tree_string = get_node_string(best.to_tree())


    print("--Testing against all 100 maps--")
    with open("behavior_tree_bot/tree.txt", "w") as file:
        file.write(tree_string)
    results_100 = run.run_test(False, True)
    print("--Finished test against all 100 maps--")

    best_win_percent = best._results["win_percentage"]
    best_win_percent_100 = results_100["win_percentage"]
    print("Results of best during generation were: [" + str(best_win_percent) + "] " + str(best._results))
    print("Results of best against all 100 maps: " + str(results_100))
    print("Fitness of best was: " + str(best.fitness()))
    print("Tree of best was: \n" + str(best.to_tree().tree_to_string()))
    

    
    #print("Tree was turned into: ", tree_string)
    #input("GO ON?!")
    with open("behavior_tree_bot/tree.txt", "w") as file:
        file.write(tree_string)

    
    #results = run.run_test(True)

    # STUDENT You can change this if you want to blast out the whole generation, or ten random samples, or...

    # DAMEN: For now, we wont be blasting out anything. Because we don't know what we need to blast out yet. If you guys
    # find any need to blast things out, feel free to uncomment this and blast them out here

    #for k in range(0, 10):
    #    with open("levels/" + now + "_" + str(k) + ".txt", 'w') as f:
    #        for row in final_gen[k].to_level():
    #            f.write("".join(row) + "\n")
