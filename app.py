import json
import random

FILE_NAME = 'states.txt'

class Rule:

    def __init__(self,state,adjacent):
        if state < adjacent:
            state, adjacent = adjacent, state

        self.state = state
        self.adjacent = adjacent

    def __repr__(self):
        return f'<Rule {self.state}, {self.adjacent}>'

    def __eq__(self, other):
        return self.state == other.state and self.adjacent == self.adjacent

    def __hash__(self):
        return hash(self.state) * 397 ^ hash(self.adjacent)


class DataProblemError(Exception):
    pass

class Data:

    def __init__(self,filename):
        self.filename = filename

    def get_states(self):
        states_ = {}
        with open(self.filename, 'r') as file:
            for line in file.readlines():
                state = line.rstrip().split(',')
                adjacent = state[1].split(';')
                states_[state[0]] = adjacent

        #json.dumps(states, indent=4)
        return states_

    def checking_data_sanity(self):

        states_ = self.get_states()
        added_rules = {}
        for state, adjacents in states_.items():
            for adjacent in adjacents:
                if adjacent == '':
                    continue
                rule = Rule(state,adjacent)
                if rule in added_rules:
                    added_rules[rule] += 1
                else:
                    added_rules[rule] = 1

        for key,value in added_rules.items():
            try:
                if value != 2:
                    for rule, val in added_rules.items():
                        print(rule.state,rule.adjacent,val)
                    print(key,value)
                    print(key.state < key.adjacent)
                    rule = Rule(key.state,key.adjacent)
                    print(rule)
                    raise DataProblemError("data problem, rule {0} is not bidirectional".format(key))
            except DataProblemError as e :
                return None

        return added_rules.keys()

    def max_length_adjacence(self):
        states = self.get_states()
        return max([len(adjacents)for state,adjacents in states.items()])








class graph_coloring:

    def __init__(self, colors_ , population, states_):
        self.colors = colors_
        self.geneset = population
        self.states = states_
        self.edges = {}

    def generate_parents(self):
        self.edges = {edge: self.colors[random.randint(0, len(self.colors) - 1)] for edge in self.geneset}


    def get_fitness(self):

        total = 0
        for state, adjacents in self.states.items():
            optimal = set()
            for adjacent in adjacents:
                if adjacent == '':
                    continue
                rule = Rule(state,adjacent)
                color = self.edges[rule]
                optimal.add(color)
            if len(optimal) == len(adjacents):
                total+=1

        return total

    def __repr__(self):
        return f'{self.edges}'

    def get_optimal(self):
        max_fitness = 0
        count = 100000
        while count >= 0:
            self.generate_parents()
            fitness = self.get_fitness()
            if fitness > max_fitness:
                max_fitness = fitness
                optimal = {fitness: self.edges}
            print('Edges : -> ',self.__repr__(),'\n')
            print('Fitness : -> ',fitness)

            if fitness == len(self.states):
                break
            count-=1
        print('Optimal solution that we could found in 1000 iteration ->  :',optimal)



if __name__ == '__main__':

    data = Data(FILE_NAME)
    colors = ["A", "B", "C", "D","E", "F", "G", "H","I","J","K","L", "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","&","#","!","+","-","@","$",")","=","`",",",";"] #17

    if data.max_length_adjacence() > len(colors): #colors_number >= max(len(adjacents))
        raise Exception('Limited Number of colors !!')

    geneset = data.checking_data_sanity()
    states = data.get_states()
   # print(json.dumps(states['ME'],indent=4))

    gc = graph_coloring(colors, geneset, states)
    gc.get_optimal()


