import time
import random
import numpy as np


######### First some helper functions

def check_convergence(prev_n):
#     if fn([prev_5[0]]) == min(fn(prev_5)):
#     print(prev_n)
    for f in prev_n:
        if not np.array_equal(f, prev_n[0]):
            return False
    return True
    
keep_n_geom = lambda pop: max(1, len(pop) //4)

keep_n_linear = lambda pop: max(1, (len(pop)-5)//2)

def keep_n_fit(pop, pop_best):
    delta = 1
    if len(pop_best) > 2:
        delta = (pop_best[-1] -  pop_best[-2])/pop_best[-2]
        delta = abs(delta)
    return int(max(20, ((len(pop)*(1-delta))//2), (len(pop)//3)))


def fixed_population_fixed_std(search_range, dim, p0_size, sigma, fn, max_generations = 100):
    pop_mean = []
    pop_error = []
    pop_std = []
    pop_best = []
    t0 = time.time()
    population = np.array([[random.uniform(*search_range) for _ in range(dim)] for _ in range(p0_size)])
    for _ in range(max_generations):

        if len(pop_mean) > 10 and check_convergence(pop_best[-7:]):
            break

        keep = len(population)//2
        num_children = 1
        scored = [(fn(v), v) for v in population ]
        selected = sorted(scored)[:keep]
        population = np.array([v for s,v in selected])
        
        pop_mean += [np.mean(population[:, 0])]
        pop_std += [np.std(population[:, 0])]
        pop_error += [np.mean(np.abs(population[:, 0]))]
        pop_best += [population[0]]
            
        
        
#         print("selected: ",population.shape)
        newpop = []
        for p in population:
#             print(p)
            newpop += [np.random.normal(scale = sigma, size = p.size) +  p for _ in range(num_children)]
#         print(newpop)
        population = np.concatenate((population, newpop))
#         print("fin: ",population)
    t = time.time() - t0
    return pop_mean, pop_std, pop_error, t



def linear_population_fixed_std(search_range, dim, p0_size, keep_n, sigma, fn, max_generations = 100):
    pop_mean = []
    pop_error = []
    pop_std = []
    pop_best = []
    t0 = time.time()
    population = np.array([[random.uniform(*search_range) for _ in range(dim)] for _ in range(p0_size)])
    for _ in range(max_generations):
        if len(pop_mean) > 10 and check_convergence(pop_best[-7:]):
            break
        # if len(population) < 3:
        #     break
#         print("bark")
        keep = keep_n(population)
#         print("maki", keep)
        num_children = 1
        
        scored = [(fn(v), v) for v in population ]
        selected = sorted(scored)[:keep]
        population = np.array([v for s,v in selected])
        
        pop_mean += [np.mean(population[:, 0])]
        pop_std += [np.std(population[:, 0])]
        pop_error += [np.mean(np.abs(population[:, 0]))]
        pop_best += [population[0]]
        
#         print("selected: ",population.shape)
        newpop = []
        for p in population:
#             print(p)
            newpop += [np.random.normal(scale = sigma, size = p.size) +  p for _ in range(num_children)]
#         print(newpop)
        population = np.concatenate((population, newpop))
#         print("fin: ",population)
    t = time.time() - t0
    return pop_mean, pop_std, pop_error, t

def geom_population_fixed_std(search_range, dim, p0_size, keep_n, sigma, fn, max_generations = 100):
    pop_mean = []
    pop_error = []
    pop_std = []
    pop_best = []
    t0 = time.time()
    population = np.array([[random.uniform(*search_range) for _ in range(dim)] for _ in range(p0_size)])
    for _ in range(max_generations):
        if len(pop_mean) > 10 and check_convergence(pop_best[-7:]):
            break
        # if len(population) < 3:
        #     break

        keep = keep_n(population)
        num_children = 1
        
        scored = [(fn(v), v) for v in population ]
        selected = sorted(scored)[:keep]
        population = np.array([v for s,v in selected])
        
        pop_mean += [np.mean(population[:, 0])]
        pop_std += [np.std(population[:, 0])]
        pop_error += [np.mean(np.abs(population[:, 0]))]
        pop_best += [population[0]]
        
#         print("selected: ",population.shape)
        newpop = []
        for p in population:
#             print(p)
            newpop += [np.random.normal(scale = sigma, size = p.size) +  p for _ in range(num_children)]
#         print(newpop)
        population = np.concatenate((population, newpop))
#         print("fin: ",population)
    t = time.time() - t0
    return pop_mean, pop_std, pop_error, t


def fit_population_fixed_std(search_range, dim, p0_size, keep_n, sigma, fn, max_generations = 100):
    pop_mean = []
    pop_error = []
    pop_std = []
    pop_best = []
    t0 = time.time()
    population = np.array([[random.uniform(*search_range) for _ in range(dim)] for _ in range(p0_size)])
    for _ in range(max_generations):
        if len(pop_mean) > 10 and check_convergence(pop_best[-7:]):
            break
        # if len(population) < 3:
        #     break
#         print("bark")
#         print(len(population), len(pop_best))
        keep = keep_n(population, pop_best)
        print("maki", keep)
        num_children = 1
        
        scored = [(fn(v), v) for v in population ]
        selected = sorted(scored)[:keep]
        population = np.array([v for s,v in selected])
        
        pop_mean += [np.mean(population[:, 0])]
        pop_std += [np.std(population[:, 0])]
        pop_error += [np.mean(np.abs(population[:, 0]))]
        pop_best += [population[0]]
        
#         print("selected: ",population.shape)
        newpop = []
        for p in population:
#             print(p)
            newpop += [np.random.normal(scale = sigma, size = p.size) +  p for _ in range(num_children)]
#         print(newpop)
        population = np.concatenate((population, newpop))
#         print("fin: ",population)
    t = time.time() - t0
    return pop_mean, pop_std, pop_error, t


def fixed_population_linear_std(search_range, dim, p0_size, sigma, b, fn, max_generations = 100):
    pop_mean = []
    pop_error = []
    pop_std = []
    pop_best = []
    t0 = time.time()
    population = np.array([[random.uniform(*search_range) for _ in range(dim)] for _ in range(p0_size)])
    for _ in range(max_generations):
        if len(pop_mean) > 10 and check_convergence(pop_best[-7:]):
            break

        keep = len(population)//2
        num_children = 1
        sigma = sigma -b
        
        scored = [(fn(v), v) for v in population ]
        selected = sorted(scored)[:keep]
        population = np.array([v for s,v in selected])
        
        pop_mean += [np.mean(population[:, 0])]
        pop_std += [np.std(population[:, 0])]
        pop_error += [np.mean(np.abs(population[:, 0]))]
        pop_best += [population[0]]
        
#         print("selected: ",population.shape)
        newpop = []
        for p in population:
#             print(p)
            newpop += [np.random.normal(scale = sigma, size = p.size) +  p for _ in range(num_children)]
#         print(newpop)
        population = np.concatenate((population, newpop))
#         print("fin: ",population)
    t = time.time() - t0
    return pop_mean, pop_std, pop_error, t


def fixed_population_geom_std(search_range, dim, p0_size, sigma, g, fn, max_generations = 100):
    pop_mean = []
    pop_error = []
    pop_std = []
    pop_best = []
    t0 = time.time()
    population = np.array([[random.uniform(*search_range) for _ in range(dim)] for _ in range(p0_size)])
    for _ in range(max_generations):
        if len(pop_mean) > 10 and check_convergence(pop_best[-7:]):
            break

        keep = len(population)//2
        num_children = 1
        sigma = sigma*g
        
        scored = [(fn(v), v) for v in population ]
        selected = sorted(scored)[:keep]
        population = np.array([v for s,v in selected])
        
        pop_mean += [np.mean(population[:, 0])]
        pop_std += [np.std(population[:, 0])]
        pop_error += [np.mean(np.abs(population[:, 0]))]
        pop_best += [population[0]]
        
#         print("selected: ",population.shape)
        newpop = []
        for p in population:
#             print(p)
            newpop += [np.random.normal(scale = sigma, size = p.size) +  p for _ in range(num_children)]
#         print(newpop)
        population = np.concatenate((population, newpop))
#         print("fin: ",population)
    t = time.time() - t0
    return pop_mean, pop_std, pop_error, t