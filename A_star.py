import heapq
import time
GoalState = [0, 1, 2, 3, 4, 5, 6, 7, 8]

##class for the graph node
class Node:
    ## Function that calculate the heuristic and it takes a boolean to check whether to work
    ## with manhattan distance or euclidean distance
    def calculate_heuristics(self, state, manhattan_or_euclidean):
        heuristic = 0
        for i in range(len(state)):
            if state[i] != i and state[i] != 0:
                if manhattan_or_euclidean:
                    # h = abs(currentcell:x - goal:x) + abs(currentcell:y - goal:y)
                    #Manhattan distance = 𝑎𝑏𝑠(𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑐𝑒𝑙𝑙.𝑥−𝑔𝑜𝑎𝑙.𝑥)+𝑎𝑏𝑠(𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑐𝑒𝑙𝑙.𝑦−𝑔𝑜𝑎𝑙.𝑦)
                    heuristic += abs(state[i] % 3 - i % 3) + abs(state[i] // 3 - i // 3)
                else:
                    #Euclidean distance = 𝑠𝑞𝑟𝑡((𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑐𝑒𝑙𝑙.𝑥−𝑔𝑜𝑎𝑙.𝑥)^2+ 𝑠𝑞𝑟𝑡((𝑐𝑢𝑟𝑟𝑒𝑛𝑡 𝑐𝑒𝑙𝑙.𝑦−𝑔𝑜𝑎𝑙.𝑦)^2)
                    heuristic += ((state[i] % 3 - i % 3) ** 2 + (state[i] // 3 - i // 3) ** 2) ** 0.5
        return heuristic
    #costructor for the Node class
    def __init__(self, state, parent,movement, manhattan_or_euclidean):
        # Contains the state of the node, [list of the state of the board at this node]
        self.state = state
        # Contains the node that generated this node
        self.parent = parent
        self.movement = movement
        if self.parent is not None:
            self.g = parent.g + 1
        else:
            self.g = 0

        self.h = self.calculate_heuristics(state, manhattan_or_euclidean)
        self.f = self.g + self.h
        if self.state:
            self.map = ''.join(str(e) for e in self.state)

    def __lt__(self, other):
        return self.f < other.f

## function to check if the goal is reached
def goal_test(check_state):
    return check_state.state == GoalState

##functino used to compute the neighbours of a given state
def get_neighbours(parent_state, manhattan_or_euclidean):
    state = parent_state.state
    zero_position = state.index(0)

    neighbours = []
    motions = []

    if zero_position % 3 != 0:
        motions.append('l')
    if zero_position % 3 != 2:
        motions.append('r')
    if zero_position // 3 != 0:
        motions.append('u')
    if zero_position // 3 != 2:
        motions.append('d')

    for motion in motions:

        new_state = state[:]
        if motion == 'l':
            new_state[zero_position], new_state[zero_position - 1] = new_state[zero_position - 1], new_state[
                zero_position]
        elif motion == 'r':
            new_state[zero_position], new_state[zero_position + 1] = new_state[zero_position + 1], new_state[
                zero_position]
        elif motion == 'u':
            new_state[zero_position], new_state[zero_position - 3] = new_state[zero_position - 3], new_state[
                zero_position]
        elif motion == 'd':
            new_state[zero_position], new_state[zero_position + 3] = new_state[zero_position + 3], new_state[
                zero_position]
        neighbours.append(Node(new_state, parent_state,motion, manhattan_or_euclidean))

    return neighbours

## function used to check the solvability of the puzzle
## by counting the number of inversions if it is even then it
## is solvable else it is not
def is_solvable(state):
    inv_count = 0
    state_arr = state[:]
    state_arr.remove(0)
    n = len(state_arr)
    for i in range(n):
        for j in range(i + 1, n):
            if state_arr[i] > state_arr[j]:
                inv_count += 1

    if inv_count % 2 == 0:
        return True
    else:
        return False

### main function for the A star algorithm
def a_star(start_state, manhattan_or_euclidean):
    global max_depth
    max_depth = 0
    if not is_solvable(start_state):
        return False, Node([], None," ", manhattan_or_euclidean)
    frontier = []
    start_node = Node(start_state, None," ",manhattan_or_euclidean)
    if not is_solvable(start_state):
        return False, start_node,[]
    heapq.heappush(frontier, start_node)
    explored = set()
    in_frontier = set()
    in_frontier.add(start_node.map)
    if not is_solvable(start_state):
        return False, start_node, explored
    while len(frontier) != 0:

        popped_state = heapq.heappop(frontier)
        if popped_state.g > max_depth:
            max_depth = popped_state.g
        in_frontier.remove(popped_state.map)
        explored.add(popped_state.map)
        if goal_test(popped_state):
            return True, popped_state, explored
        neighbours = get_neighbours(popped_state, manhattan_or_euclidean)
        for neighbour in neighbours:
            if not (neighbour.map in explored.union(in_frontier)):
                heapq.heappush(frontier, neighbour)
                in_frontier.add(neighbour.map)
            elif neighbour.map in in_frontier:

                index = 0
                j = 0
                for i in frontier:
                    if i.map == neighbour.map:
                        index = j
                        break
                    j += 1
                frontier[index], frontier[0] = frontier[0], frontier[index]
                test = heapq.heappop(frontier)
                heapq.heapify(frontier)
                heapq.heappush(frontier, neighbour)

## function used to set the start state
def setStartState(start):
    global start_state
    start_state = start


# stuff to run always here such as class/def
def main():
    manhattan_or_euclidean = True
    t0 = time.time()
    result, returned_goal_state ,explored = a_star(start_state, manhattan_or_euclidean)
    t1 = time.time()- t0

    cost = returned_goal_state.f
    global movements
    movements = []
    heuristic_used = "Manhattan distance" if manhattan_or_euclidean else "Euclidean distance"
    print("Using",heuristic_used,"is more admissible")
    print("Cost to the goal = ",cost)
    if result == False:
        print("The puzzle has no solution")
        movements= None
    elif result == True and returned_goal_state.parent is None:
        print("the start state is the goal")
        movements = [None]
    else:

        path = []
        state = returned_goal_state
        while state.parent is not None:
            path.append(state.state)
            state = state.parent
        path.reverse()
        movements= []
        state = returned_goal_state
        while state.parent is not None:
            movements.append(state.movement)
            state = state.parent

    print("The search depth= ", max_depth)
    print("Number of expanded nodes= ", len(explored))
    print("Running time = ",t1," seconds")
