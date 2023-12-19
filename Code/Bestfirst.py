import globalvariables as GV
import random
import copy
class Node:
        def __init__(self, state, heuristic):
            self.state = state
            self.cost = heuristic

        def __lt__(self, other):
            if isinstance(other, Node):
                return self.cost < other.cost
            return NotImplemented

def get_successor_states(state):  # return all children of initial state(node)
        n = len(state)
        children = []
        for i in range(n):
            if state[i] == 0:
                copy_state = copy.deepcopy(state)
                copy_state[i] = 1
                children.append(copy_state)
            elif state[i] == n - 1:
                copy_state = copy.deepcopy(state)
                copy_state[i] = n - 2
                children.append(copy_state)
            else:
                copy_state1 = copy.deepcopy(state)
                copy_state2 = copy.deepcopy(state)
                copy_state1[i] += 1
                copy_state2[i] -= 1
                children.append(copy_state1)
                children.append(copy_state2)
        return children

def heuristic_function(state):
        # Simple heuristic: counts conflicts in the same row, column, and diagonals.
        conflicts = 0
        n = len(state)
        for i in range(n):
            for j in range(i + 1, n):
                # if list=(item1,item2,item3,item4) and item1 = item2 then they are in the same column
                # for each item in list compare it with the all next items for example item1 with item2,item3,item4
                # and when i=1 compare item2 with item3,item4 and so on
                # and if they satisfay these conditions increase the conflict by one
                if state[i] == state[j] or \
                        state[i] - i == state[j] - j or \
                        state[i] + i == state[j] + j:
                    conflicts += 1
        return conflicts
def make_random_itial_state(n):  # Shffling the inithial places of queens
    initial_state = list(range(0, n))
    random.shuffle(initial_state)
    return initial_state