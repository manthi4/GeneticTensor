from abc import ABC, abstractmethod
import time
import numpy as np
from tqdm import tqdm


class model(ABC):
    @abstractmethod
    def eval(task):
        #return y
        pass
    @abstractmethod
    def spawn():
        return children
        pass
    @abstractmethod
    def params():
        pass
    
def spawner(p):
    ans = []
    for thing in p:
        ans += thing.spawn()
    ans = np.array(ans)
    return ans

def selector_10(p, scores):
#     print(scores)
    ii = np.argsort(scores)[:10]
    return p[ii]
 


def matched_spawner(p):
    ans = []
    l = len(p)
#     print(l)
    for thing in p:
        mate_i = np.random.randint(l)
        ans += thing.spawn(p[mate_i])
    ans = np.array(ans)
    return ans

def experiment(spawner, eval_input, selector, p0, max_generations = 10, stopCriteria = None):
    p = np.array(p0)
    generation_scores = []
    generation_params = []
    generation_ctime = []
    for i in range(max_generations):
        t0 = time.time()
        if stopCriteria:
            break
        scores = [m.eval(eval_input)[0] for m in p]
        generation_scores += [scores]
        generation_params += [[m.params() for m in p]]
        p = selector(p, scores)
#         print(p)
        p = spawner(p)
        t1 = time.time()
        generation_ctime += [t1-t0]
    return generation_scores, generation_params, generation_ctime

def light_experiment(spawner, eval_input, selector, p0, max_generations = 10, stopCriteria = None):
    p = np.array(p0)
    generation_losses = []
    generation_acc = []
    generation_ctime = []
    for i in tqdm(range(max_generations)):
        t0 = time.time()
        if stopCriteria:
            break
        scores = [m.eval(eval_input) for m in p]
        losses = [s[0] for s in scores]
        acces = [s[1] for s in scores]
        
        generation_losses += [losses]
        generation_acc += [acces]
        
        p = selector(p, losses)
        p = spawner(p)
        t1 = time.time()
        generation_ctime += [t1-t0]
    return generation_losses, generation_acc, generation_ctime