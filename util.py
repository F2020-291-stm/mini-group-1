import heapq
from math import floor
import itertools
from functools import reduce

class PQ():
    def __init__(self):
        self.heap = []                   # list of entries arranged in a heap
        self.entry_finder = {}               # mapping of tasks to entries
        self.REMOVED = '<removed-task>'      # placeholder for a removed task
        self.counter = itertools.count()     # unique sequence count
        
    def add_task(self, task, priority=0):
        ''' Add a new task or update the priority of an existing task '''
        if task in self.entry_finder:
            self.remove_task(task)
        count = next(self.counter)
        entry = [-1 * priority, count, task]
        self.entry_finder[task] = entry
        heapq.heappush(self.heap, entry)
    
    def remove_task(self,task):
        '''Mark an existing task as REMOVED.  Raise KeyError if not found.'''
        entry = self.entry_finder.pop(task)
        entry[-1] = self.REMOVED

    def pop_task(self):
        '''Remove and return the lowest priority task. Raise KeyError if empty.'''
        while self.heap:
            priority, count, task = heapq.heappop(self.heap)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')
    
    def get_priority(self, task):
        '''returns the priority of a given task'''
        entry = self.entry_finder[task]
        return -1 * entry[0]
    
    def check_if_in_queue(self, post):
        for task in self.entry_finder.keys():
            if reduce(lambda x, y : x and y, map(lambda p, q: p == q,task,post), True):
                return True
        return False
    
    def is_empty(self):
        if not bool(self.entry_finder):
            return True
        else:
            return False