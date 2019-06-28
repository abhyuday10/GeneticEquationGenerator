import random
import numpy

table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']
chromosomeLength = 10
crossRate = 0.7
mutationRate = 0.005
POOL_SIZE = 40
target = 55


class Chromosome():
    def __init__(self, genes):
        self.code = ""
        self.fitness = None
        self.formula = None
        self.result = None
        for gene in genes:
            self.code += str(gene)

    def set_self_formula(self):
        split_length = len(self.code) // chromosomeLength
        split_binary = [self.code[i:i + split_length] for i in range(0, len(self.code), split_length)]
        equation = ""
        for item in split_binary:
            try:
                equation += str(parse_to_chr(item))
            except:
                continue

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
        if new_equation[-1:] in operator:
            self.formula = new_equation[:-1]
        elif len(new_equation)==0:
            self.formula=None
        else:
            self.formula = new_equation

    def set_self_result(self):
        if not self.formula == None:
            try:
                self.result = eval(self.formula)
            except:
                self.result = None

    def set_self_fitness(self):
        if target == self.result:
            self.fitness = 9999
        elif self.result==None:
            self.fitness=0
        else:
            self.fitness = 1 / abs(target - self.result)


def parse_to_chr(binarycharacter):
    if binarycharacter == "1110" or binarycharacter == "1111":
        return None
    return table[int(binarycharacter, 2)]


def parse_to_binary(stringchr):
    return str(bin(table.index(stringchr))[2:].zfill(4))


def generate_population():
    pool = []
    for chrom in range(POOL_SIZE):
        genes = []
        for gene in range(chromosomeLength):
            genes.append(parse_to_binary(random.choice(table)))
        pool.append(Chromosome(genes))
    return pool


def main():
    # Generate Population
    population = generate_population()

    # Check for solution
    generation = 0
    solution_found = False

    while (not solution_found):
        # Test Population: formula, result, fitness
        for chromosome in population:
            chromosome.set_self_formula()
            chromosome.set_self_result()
            chromosome.set_self_fitness()

            print(chromosome.fitness)

        # for debugging
        solution_found = True


main()
