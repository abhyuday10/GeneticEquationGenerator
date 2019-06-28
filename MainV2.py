import random
import numpy


# From http://www.ai-junkie.com/ga/intro/gat3.html

class Chromosome():
    def __init__(self, nodes):
        self.nodes = nodes
        self.fitness = None
        self.code = ""
        self.value = None
        for node in nodes:
            self.code += str(node.code)

    def get_self_value(self):
        split_length = len(self.code) // chromosomeLength
        split_binary = [self.code[i:i + split_length] for i in range(0, len(self.code), split_length)]
        equation = ""
        for item in split_binary:
            equation += str(parse_to_chr(item))
        if "None" in equation:
            del self
            return
        corrected_equation = self.correct_equation(equation)
        if corrected_equation == None:
            return None

        # print("corrected equat: ",corrected_equation)
        try:
            value = eval(corrected_equation)
            self.value = value
            return value
        except:
            return None

    def correct_equation(self, equation):
        operand = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        operator = ['+', '-', '*', '/']
        new_equation = ""
        next = operand

        for index in range(len(equation)):
            if equation[index] in next:
                new_equation += equation[index]
                if next == operand:
                    next = operator
                elif next == operator:
                    next = operand
            self.trueEquation = equation
        if new_equation[-1:] in operator or len(new_equation) == 0:
            return None
        else:
            self.corrected_equation = new_equation
            return new_equation

    def calculate_fitness(self):
        value = self.get_self_value()
        if value == None:
            self.fitness = 0
        else:
            try:
                self.fitness = abs(1 / (target - value))
                # print(value)
            except:
                print("SUCCESS!!")
                print(self.trueEquation)
                self.fitness = 1
                return 1
                # print(self.fitness, "\n")


class Node():
    def __init__(self, code):
        self.code = code


def parse_to_binary(stringchr):
    return str(bin(table.index(stringchr))[2:].zfill(4))


def parse_to_chr(binarycharacter):
    if binarycharacter == "1110" or binarycharacter == "1111":
        return None
    return table[int(binarycharacter, 2)]


def generate_pool():
    pool = []
    for chrom in range(poolsize):
        nodes = []
        for node in range(chromosomeLength):
            nodes.append(Node(parse_to_binary(random.choice(table))))
        pool.append(Chromosome(nodes))
    return pool


def breed_two_chromosomes(first, second):
    firstList = list(first.code)
    secondList = list(second.code)

    # Cross DNA based on probability
    if random.random() <= crossRate:
        point = random.randint(0, len(firstList) - 1)
        if not point == len(firstList):
            # Not last one selected
            for i in range(point, len(firstList)):
                tmp = firstList[i]
                firstList[i] = secondList[i]
                secondList[i] = tmp
        # print("Breeding Occurred!!")

        # Check for mutation based on probability
        if random.uniform(0, 1) <= mutationRate:
            # print(len(firstList) - 1)
            # print(firstList)
            cellIndex = random.randint(0, len(firstList) - 1)
            if firstList[cellIndex] == "0":
                firstList[cellIndex] = "1"
            else:
                firstList[cellIndex] = "0"
            print("mutation Occurred!!")
            # print(firstList)
        if random.uniform(0, 1) <= mutationRate:
            cellIndex = random.randint(0, len(secondList) - 1)
            if secondList[cellIndex] == "0":
                secondList[cellIndex] = "1"
            else:
                secondList[cellIndex] = "0"
            print("mutation Occurred!!")

    first.code = "".join(firstList)
    second.code = "".join(secondList)
    return [first, second]


def calculate_pool_fitness(pool):
    totalFitness = 0
    for chromosome in pool:
        if chromosome.fitness:
            totalFitness += chromosome.fitness
    return totalFitness


def select_parent_from_pool(pool):
    poolFitness = calculate_pool_fitness(pool)
    probabilitiesForEach = []
    for chromosome in pool:

        if chromosome.fitness == None or chromosome.fitness == 0:
            probabilitiesForEach.append(0)
        else:
            probabilitiesForEach.append(chromosome.fitness / poolFitness)


            # print(chromosome.fitness)
    parent = numpy.random.choice(a=pool, p=probabilitiesForEach)
    return parent


table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']
chromosomeLength = 5
crossRate = 0.7
mutationRate = 0.005
poolsize = 40
target = 55


# Main GA function
def genetic_algorithm():
    newPool = []
    pool = generate_pool()
    while 1:

        while len(newPool) < poolsize:

            for chromosome in pool:
                if chromosome.calculate_fitness():
                    return 1

            # Remove bad ones
            for chromosome in pool:
                if chromosome.fitness == 0 or chromosome.fitness == None:
                    pool.remove(chromosome)

            # Breeding to get 2 child chromosomes
            poolFitness = calculate_pool_fitness(pool)

            # for thing in pool:
            #     print("Here: ",thing.fitness)

            childs = breed_two_chromosomes(select_parent_from_pool(pool),
                                           select_parent_from_pool(pool))

            # Add children to new pool
            newPool.append(childs[0])
            newPool.append(childs[1])
            # print(len(pool))
            # print(len(newPool))
        pool = newPool
        newPool = []
        # print(len(pool))
        # print(pool)
        print("total pool fitness: ", calculate_pool_fitness(pool) / poolsize)


genetic_algorithm()
