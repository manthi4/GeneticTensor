from tqdm import tqdm
import numpy as np
import multiprocessing
import threading




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

