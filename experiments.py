from tqdm import tqdm
import numpy as np
import multiprocessing
import threading
from typing_extensions import DefaultDict
from simulations import *



def base_experiment(reduction_sim, runs, minimum):
  # num_threads = multiprocessing.cpu_count()
  times = np.zeros_like(pops)
  convergence = np.zeros_like(pops)

  for i in tqdm(range(len(pops))):
      for j in range(len(pops[i])):
          sigma = stds[i][j]
          p0_size = int(pops[i][j])
          global tt
          global c
          tt = 0
          c = 0
          lck = threading.Lock()

          def thread_fn():
            global tt
            global c
            pop_avg, _, _, t = reduction_sim(p0_size, sigma) #linear_population_fixed_std(search_range, dim, p0_size, keep_n_linear, sigma, parabola)
            lck.acquire()
            c += (minimum - np.mean(pop_avg[-5:]))**2
            tt += t
            lck.release()
          
          worker_threads = [threading.Thread(target= thread_fn, args=()) for it in range(runs)]

          for t in worker_threads:
            # print("running thread ", t)
            t.start()

          for t in worker_threads:
            t.join()

          times[i, j] = tt/runs
          convergence[i, j] = float(c/runs)
  return times, convergence

def geom_population_g_search(geom_test_vals, runs, dim):
    search_range = (-100, 100)
    output_times = DefaultDict(lambda : [])
    output_errors = DefaultDict(lambda : [])
    for g in geom_test_vals:
      keep_n_geom = lambda pop: int(max(1, len(pop) //g))
      for n, fn in func_list.items():
        reduction_sim = lambda p0_size, sigma: geom_population_fixed_std(search_range, dim, p0_size, keep_n_geom, sigma, fn)
        minimum = min_list[n]
        times, convergence = base_experiment(reduction_sim, runs, minimum)
        output_times[n] += [np.mean(times)]
        output_errors[n] += [np.mean(convergence)]
        print(f"g: {g}\tfunc: {n}\t {np.mean(times)}, {np.mean(convergence)}")
    return output_times, output_errors, geom_test_vals

def linear_population_b_search(linear_test_vals, runs, dim):
    search_range = (-100, 100)
    output_times = DefaultDict(lambda : [])
    output_errors = DefaultDict(lambda : [])
    for b in linear_test_vals:
      keep_n_linear = lambda pop: max(1, (len(pop)-b)//2)
      for n, fn in func_list.items():
        reduction_sim = lambda p0_size, sigma: linear_population_fixed_std(search_range, dim, p0_size, keep_n_linear, sigma, fn)
        minimum = min_list[n]
        times, convergence = base_experiment(reduction_sim, runs, minimum)
        output_times[n] += [np.mean(times)]
        output_errors[n] += [np.mean(convergence)]
        print(f"g: {b}\tfunc: {n}\t {np.mean(times)}, {np.mean(convergence)}")
    return output_times, output_errors, linear_test_vals

def geom_std_g_search(geom_test_vals, runs, dim):
    search_range = (-100, 100)
    output_times = DefaultDict(lambda : [])
    output_errors = DefaultDict(lambda : [])
    for g in geom_test_vals:
      for n, fn in func_list.items():
        reduction_sim = lambda p0_size, sigma: fixed_population_geom_std(search_range, dim, p0_size, sigma, g, fn)
        minimum = min_list[n]
        times, convergence = experiment(reduction_sim, runs, minimum)
        output_times[n] += [np.mean(times)]
        output_errors[n] += [np.mean(convergence)]
        print(f"g: {g}\tfunc: {n}\t {np.mean(times)}, {np.mean(convergence)}")
    return output_times, output_errors, geom_test_vals

def linear_std_g_search(linear_test_vals, runs, dim):
    search_range = (-100, 100)
    output_times = DefaultDict(lambda : [])
    output_errors = DefaultDict(lambda : [])
    for b in linear_test_vals:
      for n, fn in func_list.items():
        reduction_sim = lambda p0_size, sigma: fixed_population_linear_std(search_range, dim, p0_size, sigma, b, fn)
        minimum = min_list[n]
        times, convergence = experiment(reduction_sim, runs, minimum)
        output_times[n] += [np.mean(times)]
        output_errors[n] += [np.mean(convergence)]
        print(f"g: {b}\tfunc: {n}\t {np.mean(times)}, {np.mean(convergence)}")
    return output_times, output_errors, linear_test_vals