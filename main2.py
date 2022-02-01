import random
import numpy as np
#import time
import matplotlib.pyplot as plt

scatter_x = []
scatter_y = []

distances = []

def create_generation(gene_size, nr_of_genes, generation_size):
    generations = []
    for _ in range(generation_size):
        temp2 = []
        for __ in range(gene_size): 
            temp2.append(random.randint(0, nr_of_genes-1))
            distances.append(random.random());


        generations.append(temp2)

    return generations

def get_mouse_position(arr):
    array = []
    for gen in arr:
        coor = [0,0]
        for i in range(len(gen)):
            direction = gen[i]
            if direction == 1:
                coor[0] += distances[i]
            elif direction == 2:
                coor[1] += distances[i]
            elif direction == 3:
                coor[0] -= distances[i]
            elif direction == 4:
                coor[1] -= distances[i]

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
        splicing_point = random.randint(0, len(generation))

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
                distances[(i*len(mutated[0]))+j] = random.random();

    #for i in range(len(distances)):
    #    if random.randint(0,mutation_rate) == 0:
    
    return mutated

def selection(genes_to_kill, goal):
    arr = []
    for _ in range(len(genes_to_kill)):
        sp1 = genes_to_kill[random.randint(0,len(genes_to_kill)-1)]
        sp2 = genes_to_kill[random.randint(0,len(genes_to_kill)-1)]
        
        mouse = get_mouse_position([sp1, sp2])
        fitnesss = fitness(mouse, goal)
        
        # print(fitnesss[0],"<=",fitnesss[1])

        if fitnesss[0] >= fitnesss[1]:
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
    goal = (5,5)
    # ????????????????????????????????????????????????????
    # goal_hypo = (((goal[0]-1)**2)+((goal[1]-1)**2))**0.5
    goal_hypo = (((goal[0])**2)+((goal[1])**2))**0.5

    print(goal_hypo)

    generations = create_generation(100,100,75)

    #print(generations)
    #print(get_mouse_position(generations))
    #print(fitness(generations, goal))
    #print(crossover(generations))
    #print(fitness(crossover(generations), goal))
    #print(selection(generations, goal))

    input_string = input("[Number of generations,Number of generations per print]: ")

    try:
        input_string = input_string.split(",")
        if len(input_string) > 1:
            prints = int(input_string[1])
        else:
            prints = 25

    except:
        print("Error...")
        print("Use whole numbers / integers separated by a comma.")
        return

    total_generations = int(input_string[0])

    x_values = range(total_generations)
    gen_arr = []

    for i in range(total_generations):
        generations = selection(generations, goal)
        generations = mutation(generations, 100, 4)
        generations = crossover(generations)
        if i % prints == 0:
            print("Avarage fitness score for generation " + str(i) + ": " + str(avarage(fitness(generations, goal))))
        gen_arr.append(avarage(fitness(generations, goal)))
    
    with plt.style.context("dark_background"):
        fig, (ax1, ax2) = plt.subplots(2)
        fig.suptitle("Genetic algorithm")

        ax1.plot(x_values, gen_arr)
        ax1.plot([0,total_generations-1], [goal_hypo, goal_hypo], alpha=0.6, color="red")
        ax1.set_ylabel("Deviation from goal")

        #ax2.hist2d(scatter_x, scatter_y, bins=[np.arange(-12.5,12.5,0.2), np.arange(-10,10,0.2)])
        ax2.hist2d(scatter_x, scatter_y, bins=[np.arange(goal[0]-10,goal[0]+10,0.1), np.arange(goal[1]-10,goal[1]+10,0.1)])
        ax2.set_ylabel("Position density")
        plt.show()
    
main()
