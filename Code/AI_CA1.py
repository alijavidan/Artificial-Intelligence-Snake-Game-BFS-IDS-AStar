from copy import deepcopy
from collections import OrderedDict 
import collections

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = [] 
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:        
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)

boardSize = (5, 5)

class Node:
  def __init__(self, state, action, cost, parent):
    self.state = state
    self.action = action
    self.cost = cost
    self.parent = parent

  # def __eq__(self, other):
  #   if self.state.snake.head == other.state.snake.head:
  #     if self.state.snake.body == other.state.snake.body:
  #       if self.state.seeds == other.state.seeds:
  #         return True

  #   return False

  # def __hash__(self):
  #   return hash((self.state))


class State:
   def __init__(self):
     self.snake = None
     self.seeds = None
   def __init__(self, snake, seeds):
     self.snake = snake
     self.seeds = seeds

class Snake:
   def __init__(self):
     self.head = (0, 0)
     self.body = []

def LEFT(cordinate):
  if cordinate-1 < 1:
    return boardSize[0]
  else:
    return cordinate-1

def RIGHT(cordinate):
  if cordinate+1 > boardSize[0]:
    return 1
  else:
    return cordinate+1

def UP(cordinate):
  if cordinate-1 < 1:
    return boardSize[1]
  else:
    return cordinate-1

def DOWN(cordinate):
  if cordinate+1 > boardSize[1]:
    return 1
  else:
    return cordinate+1

def evaluatePossibleActions(node):
  possibleActions = ['R', 'L', 'U', 'D']

  if RIGHT(node.state.snake.head[0]) in [body[0] for body in node.state.snake.body]:
    possibleActions.remove('R')
  if LEFT(node.state.snake.head[0]) in [body[0] for body in node.state.snake.body]:
    possibleActions.remove('L')
  if UP(node.state.snake.head[1]) in [body[0] for body in node.state.snake.body]:
    possibleActions.remove('U')
  if DOWN(node.state.snake.head[1]) in [body[0] for body in node.state.snake.body]:
    possibleActions.remove('D')

  return possibleActions

def ifGoal(node):
  for seed in node.state.seeds:
    if seed[1] > 0:
      return False

  return True

def bfs(initial_state):
  initial_node = Node(initial_state, None, 0, None)
  if ifGoal(initial_node):
    return

  frontier = OrderedSet()
  frontier.add(initial_node)
  explored = set()

  while True:
    if len(frontier) == 0:
      raise Exception("Failure")
    current_node = frontier.pop(last=False)
    explored.add(current_node)

    for action in evaluatePossibleActions(current_node):
      #yek khane dar jahate harekat be mar azafe mishavad
      #agar dooneiy khorde nashode akharin khaneye mar hazf mishavad, dar gehyre in soorat baghi mimanad
      #akharin iteme list dome mar ast
      new_state = deepcopy(current_node.state)
      new_state.snake.body.insert(0, current_node.state.snake.head) #heade ghabli be sare body ezafe mishavad
      if action == 'R':
        new_state.snake.head = (RIGHT(new_state.snake.head[0]), new_state.snake.head[1])
      elif action == 'L':
        new_state.snake.head = (LEFT(new_state.snake.head[0]), new_state.snake.head[1])
      elif action == 'U':
        new_state.snake.head = (new_state.snake.head[0], UP(new_state.snake.head[1]))
      elif action == 'D':
        new_state.snake.head = (new_state.snake.head[0], DOWN(new_state.snake.head[1]))

      for seed in new_state.seeds:
        if (seed[0] == new_state.snake.head) and (seed[1]>0):
          body.pop(-1)
          seed = (seed[0], seed[1]-1)

      child_node = Node(new_state, action, 0, current_node)
      if child_node not in explored and child_node not in frontier:
        if ifGoal(child_node):
          return
        frontier.add(child_node)


#Main
initial_state = State(
  Snake(),
  [([3, 1], 1), ([3, 2,], 1), ([1, 4], 2), ([4, 3], 1)]
)

bfs(initial_state)

#IDS
# // Returns true if target is reachable from
# // src within max_depth
# bool IDDFS(src, target, max_depth)
#     for limit from 0 to max_depth
#        if DLS(src, target, limit) == true
#            return true
#     return false   

# bool DLS(src, target, limit)
#     if (src == target)
#         return true;

#     // If reached the maximum depth, 
#     // stop recursing.
#     if (limit <= 0)
#         return false;   

#     foreach adjacent i of src
#         if DLS(i, target, limit?1)             
#             return true

#     return false

# // A*
# // Initialize both open and closed list
# let the openList equal empty list of nodes, genrated
# let the closedList equal empty list of nodes, expanded 
# // Add the start node
# put the startNode on the openList (leave it's f at zero)
# // Loop until you find the end
# while the openList is not empty
#     // Get the current node
#     let the currentNode equal the node with the least f value
#     remove the currentNode from the openList
#     add the currentNode to the closedList
#     // Found the goal
#     if currentNode is the goal
#         Congratz! You've found the end! Backtrack to get path
#     // Generate children
#     let the children of the currentNode equal the adjacent nodes
    
#     for each child in the children
#         // Child is on the closedList
#         if child is in the closedList
#             continue to beginning of for loop
#         // Create the f, g, and h values
#         child.g = currentNode.g + distance between child and current
#         child.h = distance from child to end
#         child.f = child.g + child.h
#         // Child is already in openList
#         if child.position is in the openList's nodes positions
#             if the child.g is higher than the openList node's g
#                 continue to beginning of for loop
#         // Add the child to the openList
#         add the child to the openList