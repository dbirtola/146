import copy
import heapq
import metrics
import multiprocessing.pool as mpool
import os
import random
import shutil
import time
import math


# The level as a grid of tiles


class Individual_Grid(object):
    __slots__ = ["genome", "_fitness"]

    def __init__(self, genome):
        self.genome = copy.deepcopy(genome)
        self._fitness = None

    # Update this individual's estimate of its fitness.
    # This can be expensive so we do it once and then cache the result.
    def calculate_fitness(self):
        measurements = metrics.metrics(self.to_level())
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
        new_genome = copy.deepcopy(self.genome)
        # Leaving first and last columns alone...
        # do crossover with other


        #####################################################################
        ##                            TODO                             
        ##  We should implement either single or two point crossover here.
        ##
        ##  -Damen
        #####################################################################


        left = 1
        right = width - 1
        for y in range(height):
            for x in range(left, right):
                # STUDENT Which one should you take?  Self, or other?  Why?
                # STUDENT consider putting more constraints on this to prevent pipes in the air, etc
                pass
        # do mutation; note we're returning a one-element tuple here
        return (Individual_Grid(new_genome),)

    # Turn the genome into a level string (easy for this genome)
    def to_level(self):
        return self.genome

    # These both start with every floor tile filled with Xs
    # STUDENT Feel free to change these
    @classmethod
    def empty_individual(cls):
        g = [["-" for col in range(width)] for row in range(height)]
        g[15][:] = ["X"] * width
        g[14][0] = "m"
        g[7][-1] = "v"
        for col in range(8, 14):
            g[col][-1] = "f"
        for col in range(14, 16):
            g[col][-1] = "X"
        return cls(g)

    @classmethod
    def random_individual(cls):
        # STUDENT consider putting more constraints on this to prevent pipes in the air, etc
        # STUDENT also consider weighting the different tile types so it's not uniformly random
        g = [random.choices(options, k=width) for row in range(height)]
        g[15][:] = ["X"] * width
        g[14][0] = "m"
        g[7][-1] = "v"
        g[8:14][-1] = ["f"] * 6
        g[14:16][-1] = ["X", "X"]
        return cls(g)


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


    return population


def ga():
    # STUDENT Feel free to play with this parameter
    pop_limit = 480

    # Code to parallelize some computations
    batches = os.cpu_count()
    if pop_limit % batches != 0:
        print("It's ideal if pop_limit divides evenly into " + str(batches) + " batches.")
    batch_size = int(math.ceil(pop_limit / batches))

    with mpool.Pool(processes=os.cpu_count()) as pool:
        init_time = time.time()

        # STUDENT (Optional) change population initialization
        population = [Individual.random_individual() if random.random() < 0.9
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
                stop_condition = (generation > 10)
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
    final_gen = sorted(ga(), key=Individual.fitness, reverse=True)
    best = final_gen[0]
    print("Best fitness: " + str(best.fitness()))
    now = time.strftime("%m_%d_%H_%M_%S")

    # STUDENT You can change this if you want to blast out the whole generation, or ten random samples, or...

    # DAMEN: For now, we wont be blasting out anything. Because we don't know what we need to blast out yet. If you guys
    # find any need to blast things out, feel free to uncomment this and blast them out here

    #for k in range(0, 10):
    #    with open("levels/" + now + "_" + str(k) + ".txt", 'w') as f:
    #        for row in final_gen[k].to_level():
    #            f.write("".join(row) + "\n")
