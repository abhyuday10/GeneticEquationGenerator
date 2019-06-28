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
            equation += parse_to_chr(item)
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
        if new_equation[-1:] in operator or len(new_equation) == 0:
            return None
        else:
            self.correct_equation = new_equation
            return new_equation

    def calculate_fitness(self):
        value = self.get_self_value()
        if value == None:
            self.fitness = 0
        else:
            try:
                self.fitness = abs(1 / (target - value))
                print(value)
            except:
                print("SUCCESS!!")
                print(self.correct_equation)
                self.fitness = 1
                return 1
        print(self.fitness, "\n")


class Node():
    def __init__(self, code):
        self.code = code


def parse_to_binary(stringchr):
    return str(bin(table.index(stringchr))[2:].zfill(4))


def parse_to_chr(binarycharacter):
    if binarycharacter == "1110" or binarycharacter == "1111":
        print("FIX THIS! ")
    return table[int(binarycharacter, 2)]


def generate_pool():
    pool = []
    for chrom in range(poolsize):
        nodes = []
        for node in range(chromosomeLength):
            nodes.append(Node(parse_to_binary(random.choice(table))))
        pool.append(Chromosome(nodes))
    return pool


table = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/']
chromosomeLength = 5
crossRate = 0.7
mutationRate = 0.001
poolsize = 40
target = 42


# Main GA function
def genetic_algorithm():
    pool = generate_pool()
    for chromosome in pool:
        if chromosome.calculate_fitness():
            break



genetic_algorithm()
