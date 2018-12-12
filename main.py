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
    "a": attack_weakest_enemy_planet,
    "b": spread_to_weakest_neutral_planet
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
    __slots__ = ["genome", "_fitness"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None

    # Update this individual's estimate of its fitness.
    # This can be expensive so we do it once and then cache the result.



    def calculate_fitness(self):

        tree = self.genome
        tree_string = get_node_string(tree)
        #print("Tree was turned into: ", tree_string)
        with open("behavior_tree_bot/tree.txt", "w") as file:
            file.write(tree_string)
        results = run.run_test()
        #print("Results: ", results)
        self._fitness = 1 + results['wins']

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
                    for node in current_node.child_nodes:
                        tree_to_list(tree_list, node)


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
        random_node = random.choice(tree_as_list)
        other_node = random.choice(other_as_list)


        random_node_parent = random_node.parent_node
        other_node_parent = other_node.parent_node

        random_node_index = random_node_parent.child_nodes.index(random_node)
        other_node_index = other_node_parent.child_nodes.index(other_node)

        #print("Removing : " + str(random_node) + " from " + str(random_node_parent))
        random_node_parent.child_nodes.remove(random_node)
        random_node_parent.child_nodes.insert(random_node_index, other_node)

        other_node_parent.child_nodes.remove(other_node)
        other_node_parent.child_nodes.insert(other_node_index, random_node)


        #print("Generated new genome1 : " + new_genome1.tree_to_string())
        #print("Generated new genome2 : " + new_genome2.tree_to_string())

        #####################################################################
        ##                            TODO                             
        ##  We should implement either single or two point crossover here.
        ##
        ##  -Damen
        #####################################################################


        return (Individual_Grid(new_genome1),Individual_Grid(new_genome2))

    # Turn the genome into a level string (easy for this genome)
    def to_tree(self):
        return self.genome

    # These both start with every floor tile filled with Xs
    # STUDENT Feel free to change these
    @classmethod
    def empty_individual(cls):
        
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
        

        #root = Selector(name = 'High Level Ordering of Strategies')
        return cls(root)

    @classmethod
    def random_individual(cls):
        root = Selector(name='High Level Ordering of Strategies')
        g = generate_tree(root)

        #print("test")


        return cls(g)

def generate_tree(root):
    num_children = random.randint(2, 4)
    while True:
        new_class = random.choice(list(node_dict.items()))

        if new_class[1] == Selector:
            if random.randint(0, 10) < 8:
                continue;
            new_node = Selector(name = "Selector")
            new_node.child_nodes = []
            new_root = generate_tree(new_node)
            new_root.parent_node = root
            root.child_nodes.append(new_root)

        elif new_class[1] == Sequence:            
            if random.randint(0, 10) < 8:
                continue;
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

    sorted_pop = sorted(population, key=lambda p: p.fitness())

    continuing_pop = sorted_pop[len(sorted_pop)//2:]

    print("Highest successor had fitness: " + str(continuing_pop[-1].fitness()))
    return continuing_pop


def ga():
    # STUDENT Feel free to play with this parameter
    pop_limit = 128

    # Code to parallelize some computations
    batches = os.cpu_count()
    if pop_limit % batches != 0:
        print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
    batch_size = int(math.ceil(pop_limit / batches))

    with mpool.Pool(processes=os.cpu_count()) as pool:
        init_time = time.time()

        # STUDENT (Optional) change population initialization
        population = [Individual.random_individual() if random.random() < 0.8
                      else Individual.empty_individual()
                      for _g in range(pop_limit)]

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
                stop_condition = (generation > 5)
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
    print("Tree looks like: " + final_gen[0].to_tree().tree_to_string())



    now = time.strftime("%m_%d_%H_%M_%S")

    # STUDENT You can change this if you want to blast out the whole generation, or ten random samples, or...

    # DAMEN: For now, we wont be blasting out anything. Because we don't know what we need to blast out yet. If you guys
    # find any need to blast things out, feel free to uncomment this and blast them out here

    #for k in range(0, 10):
    #    with open("levels/" + now + "_" + str(k) + ".txt", 'w') as f:
    #        for row in final_gen[k].to_level():
    #            f.write("".join(row) + "\n")
