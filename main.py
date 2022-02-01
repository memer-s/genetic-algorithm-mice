import random
import numpy as np
#import time
import matplotlib.pyplot as plt

scatter_x = []
scatter_y = []

def create_generation(gene_size, nr_of_genes, generation_size):
    generations = []
    for _ in range(generation_size):
        temp2 = []
        for __ in range(gene_size): 
            temp2.append(random.randint(0, nr_of_genes-1))

        generations.append(temp2)

    return generations

def get_mouse_position(arr):
    array = []
    for gen in arr:
        coor = [0,0]
        for i in range(len(gen)):
            direction = gen[i]
            if direction == 1:
                coor[0] += 1
            elif direction == 2:
                coor[1] += 1
            elif direction == 3:
                coor[0] -= 1
            elif direction == 4:
                coor[1] -= 1 
        scatter_x.append(coor[0])
        scatter_y.append(coor[1])
        array.append(tuple(coor))

    return array

def fitness(mouse_positions, goal):
    array = []
    for pos in mouse_positions:
        poshypo = (((pos[0]-goal[0])**2)+((pos[1]-goal[1])**2))**0.5
        array.append(poshypo)

    return array
               
def crossover(generation):
    new_gen = []
    for i in range(int(len(generation)/2)):
        splicing_point = random.randint(0,len(generation))

        parent1 = generation[i*2]
        parent2 = generation[i*2+1]
        
        p1gene1 = parent1[:splicing_point]
        p1gene2 = parent1[splicing_point:]
        p2gene1 = parent2[:splicing_point]
        p2gene2 = parent2[splicing_point:]

        child1 = p1gene1 + p2gene2
        child2 = p2gene1 + p1gene2

        new_gen.append(child1)
        new_gen.append(child2)

    return new_gen

def mutation(generation, mutation_rate, generation_size):
    
    mutated = generation

    for i in range(len(mutated)):
        for j in range(len(mutated[i])):
            if random.randint(0,mutation_rate) == 0:
                mutated[i][j] = random.randint(0, generation_size)
    
    return mutated

def selection(genes_to_kill, goal):
    arr = []
    for _ in range(len(genes_to_kill)):
        sp1 = genes_to_kill[random.randint(0,len(genes_to_kill)-1)]
        sp2 = genes_to_kill[random.randint(0,len(genes_to_kill)-1)]
        
        mouse = get_mouse_position([sp1, sp2])
        fitnesss = fitness(mouse, goal)
        
        if fitnesss[0] < fitnesss[1]:
            arr.append(sp2)
        else:
            arr.append(sp1)
    
    return arr

def avarage(arr):
    length = len(arr)
    sum = 0
    for i in range(length):
        sum += arr[i]

    return sum/length

def main():
    goal = (2,8)

    generations = create_generation(100,100,100)
    print(generations)
    print(get_mouse_position(generations))
    print(fitness(generations, goal))
    print(crossover(generations))
    print(fitness(crossover(generations), goal))
    print(selection(generations, goal))
    gen = 0

    total_generations = 300

    gen_arr = []
    times = range(total_generations)


    for i in range(total_generations):
        generations = selection(generations, goal)
        generations = mutation(generations, 300, 4)
        generations = crossover(generations)
        if i % 10 == 0:
            print("Avarage fitness score for generation " + str(gen) + ": " + str(avarage(fitness(generations, goal))-5))
        gen_arr.append(avarage(fitness(generations, goal)))
        gen+=1
    
    plt.hist2d(scatter_x, scatter_y, bins=[np.arange(-10,10,1), np.arange(-10,10,1)])
    plt.show()
    
main()
