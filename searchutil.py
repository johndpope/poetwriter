import heapq, collections, re, sys, time, os, random

############################################################
# Abstract interfaces for search problems and search algorithms.

class SearchProblem:
    # Return the start state.
    def startState(self): raise NotImplementedError("Override me")

    # Return whether |state| is a goal state or not.
    def isGoal(self, state): raise NotImplementedError("Override me")

    # Return a list of (action, newState, cost) tuples corresponding to edges
    # coming out of |state|.
    def succAndCost(self, state): raise NotImplementedError("Override me")

class SearchAlgorithm:
    # First, call solve on the desired SearchProblem |problem|.
    # Then it should set two things:
    # - self.actions: list of actions that takes one from the start state to a goal
    #                 state; if no action sequence exists, set it to None.
    # - self.totalCost: the sum of the costs along the path or None if no valid
    #                   action sequence exists.
    def solve(self, problem): raise NotImplementedError("Override me")

############################################################
# Uniform cost search algorithm (Dijkstra's algorithm).

class UniformCostSearch(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def solve(self, problem):
        # If a path exists, set |actions| and |totalCost| accordingly.
        # Otherwise, leave them as None.
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0
        self.solution = None

        # Initialize data structures
        frontier = PriorityQueue()  # Explored states are maintained by the frontier.
        backpointers = {}  # map state to (action, previous state)

        # Add the start state
        startState = problem.startState()
        frontier.update(startState, 0)

        while True:
            # Remove the state from the queue with the lowest pastCost
            # (priority).
            state, pastCost = frontier.removeMin()
            if state == None: break
            self.numStatesExplored += 1
            if self.verbose >= 2:
                print "Exploring %s with pastCost %s" % (state, pastCost)

            # Check if we've reached the goal; if so, extract solution
            if problem.isGoal(state):
                self.solution = state
                self.actions = []
                while state != startState:
                    action, prevState = backpointers[state]
                    self.actions.append(action)
                    state = prevState
                self.actions.reverse()
                self.totalCost = pastCost
                if self.verbose >= 1:
                    print "numStatesExplored = %d" % self.numStatesExplored
                    print "totalCost = %s" % self.totalCost
                    print "actions = %s" % self.actions
                return

            # Expand from |state| to new successor states,
            # updating the frontier with each newState.
            for action, newState, cost in problem.succAndCost(state):
                if self.verbose >= 3:
                    print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
                if frontier.update(newState, pastCost + cost):
                    # Found better way to go to |newState|, update backpointer.
                    backpointers[newState] = (action, state)
        if self.verbose >= 1:
            print "No path found"

#Change to be implemented iteratively if possible (not a big deal)
class DepthFirstSearch(SearchAlgorithm):
    def __init__(self, verbose=0):
        self.verbose = verbose

    def stats(self):
        if self.verbose >= 1:
            if self.solution:
                print "numStatesExplored = %d" % self.numStatesExplored
                print "totalCost = %s" % self.totalCost
                print "graphSize = %s" % self.size
                print "actions = %s" % self.actions
        return self.numStatesExplored

    def solve(self, problem):
        self.solution = None
        self.actions = None
        self.totalCost = None
        self.numStatesExplored = 0

        # A heuristic for the size of the graph, documents the number of possible
        # actions stemming from explored states. Gives the user an idea about
        # the determinicity of the n-gram system for the corpus
        self.size = 0

        # We are not interested in finding the best solution, but merely
        # finding a solution, so we don't need to do a complete traversal
        # of the graph. 
        # best = [float('inf'), None]
        def recurse(state, pastCost, history):
            if self.solution is None:
                self.numStatesExplored += 1
                # Base case
                if problem.isGoal(state):
                    self.solution = state
                    self.actions = []
                    for past_state in history:
                        self.actions.append(past_state[0])
                    self.totalCost = pastCost
                    if self.verbose >= 1:
                        print "numStatesExplored = %d" % self.numStatesExplored
                        print "totalCost = %s" % self.totalCost
                        print "graphSize = %s" % self.size
                        print "actions = %s" % self.actions
                    # Update the minimum cost path, not used here.
                    # if pastCost < best[0]:
                    #     best[0] = pastCost
                    #     best[1] = list(history)  # COPY
                    return
                # Recursive case
                successors = problem.succAndCost(state)
                self.size += len(successors)
                for action, newState, cost in successors:
                    if self.verbose >= 3:
                        print "  Action %s => %s with cost %s + %s" % (action, newState, pastCost, cost)
                    history.append((action, newState, cost))
                    recurse(newState, pastCost + cost, history)
                    history.pop()
        recurse(problem.startState(), 0, [])
        #return tuple(best) #unused functionality, returns immediately

#DP probably not useful for our problem, but here it is
def dynamicProgramming(problem):
    cache = {} # state -> (futureCost, best action, newState, cost)

    # Returns the future cost of state (minimum cost path to a goal).
    def recurse(state):
        # Base case
        if problem.isGoal(state):
            return 0
        # Recursive case
        if state not in cache:
            cache[state] = min( \
                (cost + recurse(newState), action, newState, cost) \
                for action, newState, cost in problem.succAndCost(state))
        return cache[state][0]
    totalCost = recurse(problem.startState())

    # Reconstruct the solution
    state = problem.startState()
    history = []
    while not problem.isGoal(state):
        futureCost, action, newState, cost = cache[state]
        history.append((action, newState, cost))
        state = newState

    return (totalCost, history)

# Data structure for supporting uniform cost search.
class PriorityQueue:
    def  __init__(self):
        self.DONE = -100000
        self.heap = []
        self.priorities = {}  # Map from state to priority

    # Insert |state| into the heap with priority |newPriority| if
    # |state| isn't in the heap or |newPriority| is smaller than the existing
    # priority.
    # Return whether the priority queue was updated.
    def update(self, state, newPriority):
        oldPriority = self.priorities.get(state)
        if oldPriority == None or newPriority < oldPriority:
            self.priorities[state] = newPriority
            heapq.heappush(self.heap, (newPriority, state))
            return True
        return False

    # Returns (state with minimum priority, priority)
    # or (None, None) if the priority queue is empty.
    def removeMin(self):
        while len(self.heap) > 0:
            priority, state = heapq.heappop(self.heap)
            if self.priorities[state] == self.DONE: continue  # Outdated priority, skip
            self.priorities[state] = self.DONE
            return (state, priority)
        return (None, None) # Nothing left...