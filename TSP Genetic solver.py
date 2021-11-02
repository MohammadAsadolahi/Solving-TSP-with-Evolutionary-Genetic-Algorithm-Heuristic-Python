#   Solving-TSP-with-Evolutionary-Genetic-Algorithm-Heuristic-Python
#   by mohammad asadolahi
#   Mohammad.E.Asadolahi@gmail.com
import math
import random
import matplotlib.pyplot as plt

class Draw:
    def DrawSolutionPlot(self, cities, path: list, info):
        if info != "":
            plt.title(f'Best Path untill Generation:{info}')
        x = []
        y = []
        for point in cities:
            x.append(cities[point]['x'])
            y.append(cities[point]['y'])
        plt.plot(x, y, 'co')
        for route in range(1, len(path)):
            source = path[route - 1]
            destination = path[route]
            plt.arrow(cities[source]['x'], cities[source]['y'], cities[destination]['x'] - cities[source]['x'] , cities[destination]['y'] - cities[source]['y'], color='r',
                      length_includes_head=True)
        plt.xlim(0, max(x) * 1.1)
        plt.ylim(0, max(y) * 1.1)
        plt.show()

class Chromosome:
    def __init__(self, solution,cost):
        self.solution = solution
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost


class GeneticSolver:
    def __init__(self, populationSize, generationCount, mutationRate, cities,citycCount):
        self.draw=Draw()
        self.populationSize = populationSize
        self.generationCount = generationCount
        self.mutationRate = mutationRate
        self.citycCount = citycCount
        self.cities=cities
        self.population = []
        self.elitePopulation = []
        self.generationAverage = []
        self.initialPopulation()
        # self.printPopulation()

    def drawChromosome(self,chromosome,generation):
        self.draw.DrawSolutionPlot(self.cities, chromosome.solution,
                                   f"{generation} with cost: {chromosome.cost}")

    def getDistance(self, city1: int, city2: int):
        return math.sqrt((self.cities[city1]['x'] - self.cities[city2]['x']) ** 2 + (self.cities[city1]['y'] - self.cities[city2]['y']) ** 2)

    def getRouteCost(self, route: list):
        totalRouteCost = 0
        for case in range(1, len(route)):
            source = route[case - 1]
            destination = route[case]
            totalRouteCost += self.getDistance(source,destination)
        return totalRouteCost

    def initialPopulation(self):
        index = 0
        while index < self.populationSize:
            solution = [i for i in range(1,self.citycCount+1)]
            while self.isSolutionExists(self.population, solution):
                random.shuffle(solution)
            self.population.append(Chromosome(solution,self.getRouteCost(solution)))
            index+=1
        self.population.sort(key=lambda route: route.cost)
        self.elitePopulation.append(self.population[0])
        self.generationAverage.append((sum(x.cost for x in self.population)) / self.populationSize)

    def isSolutionExists(self, population, route):
        for gene in population:
            if gene.solution == route:
                return True
        return False

    def printPopulation(self):
        for route in self.population:
            print(f"Route: {route.solution}   with Cost of: {route.cost}   ")

    def printElitePopulation(self):
        generation = 0
        print("******************************************************************************************")
        print(f"printing elite chromosomes of all generations")
        for chromosome in self.elitePopulation:
            print(
                f"elite chromosome of generation:{generation} is: {chromosome.solution} with count of {chromosome.cost} clasehs.")
            generation += 1
        print("******************************************************************************************")

    def applyMutation(self, population, chromosome):
        tmpChromosome = Chromosome(chromosome.solution[::],chromosome.cost)
        while self.isSolutionExists(population, tmpChromosome.solution):
            mutationIndex1 = random.randint(0, len(tmpChromosome.solution) - 1)
            mutationIndex2 = random.randint(0, len(tmpChromosome.solution) - 1)
            if(mutationIndex1!=mutationIndex2):
                temp=tmpChromosome.solution[mutationIndex1]
                tmpChromosome.solution[mutationIndex1]=tmpChromosome.solution[mutationIndex2]
                tmpChromosome.solution[mutationIndex2]=temp
        chromosome.solution = tmpChromosome.solution[::]
        chromosome.cost=self.getRouteCost(chromosome.solution)

    def crossOver(self,firstChromosome,secondChromosome):
        index=random.randint(0,len(firstChromosome.solution))
        firstRoute=firstChromosome.solution[0:index]+secondChromosome.solution[index:len(firstChromosome.solution)]
        secondRoute = secondChromosome.solution[0:index] + firstChromosome.solution[index:len(firstChromosome.solution)]
        firstChild=Chromosome(firstRoute,self.getRouteCost(firstRoute))
        secondChild = Chromosome(secondRoute, self.getRouteCost(secondRoute))
        if (self.mutationRate > random.random()):
            self.applyMutation(self.population, firstChild)
        if (self.mutationRate > random.random()):
            self.applyMutation(self.population, secondChild)
        return firstChild,secondChild

    def solve(self):
        self.lunchEvolution()
        plt.plot([x.cost for x in self.elitePopulation], label="Elites")
        plt.xlabel('x - Generations')
        plt.ylabel('y - Cost ')
        plt.title('Evolution of elite chromosomes')
        plt.show()
        plt.plot([x for x in self.generationAverage], label="Average Cost")
        plt.title('Averge Cost of each generatins')
        plt.xlabel('x - Generations')
        plt.ylabel('y - Cost ')
        plt.show()

    def lunchEvolution(self):
        generation = 0
        while generation < self.generationCount:
            newPopulation=self.population[::]
            for index in range(0,self.populationSize,2):
                firstChild,secondChild=self.crossOver(self.population[index],self.population[index+1])
                newPopulation.append(firstChild)
                newPopulation.append(secondChild)
            newPopulation.sort(key=lambda chromosome: chromosome.cost)
            self.population.clear()
            self.population = newPopulation[0:self.populationSize]
            self.elitePopulation.append(self.population[0])
            self.generationAverage.append((sum(x.cost for x in self.population)) / self.populationSize)
            generation += 1
            if ((generation + 1) % 200) == 0:
                self.drawChromosome(self.population[0],generation+1)


cities = {}
cityCount = 0
with open('./Cities List.txt') as f:
    for line in f.readlines():
        city = line.split(' ')
        cities[int(city[0])]={}
        cities[int(city[0])]['x']=int(city[1])
        cities[int(city[0])]['y']=int(city[2])
        cityCount += 1


# populationSize, generationCount, mutationRate in %, cities ,cityCount
geneticSolver = GeneticSolver(100,1000, 0.1,cities,cityCount)
geneticSolver.solve()
