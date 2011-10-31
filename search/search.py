# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util



class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]


class Node:
    def __init__(self, state, parent, action, stepcost):
        self.state  = state
        self.parent = parent
        self.action = action
        if parent==None:
            self.cost = stepcost
        else:
            self.cost = parent.cost + stepcost

    def __str__(self):
        return "State: " + str(self.state) + "\n" + \
               "Parent: " + str(self.parent.state) + "\n" + \
               "Action: " + str(self.action) + "\n" + \
               "Cost: " + str(self.cost)

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getCost(self):
        return self.cost

    def pathFromStart(self):
        stateList = []
        actionList = []
        currNode = self
        while currNode.getAction() is not None:
            #print stateList
            #print actionList
            stateList.append(currNode.getState())
            actionList.append(currNode.getAction())
            currNode = currNode.parent
        actionList.reverse()
        return actionList




def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first
  [2nd Edition: p 75, 3rd Edition: p 87]
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm 
  [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """

  #Queue - BFS
  s = util.Stack()
  explored = []
  startNode = Node(problem.getStartState(), None, None, 0)
  s.push(startNode)
  actionslist = []

  while (not s.isEmpty()):
      currNode = s.pop()
      explored.append(currNode.getState())
      if problem.isGoalState(currNode.getState()):
          print "done"
          return currNode.pathFromStart()
      else:
          successors = problem.getSuccessors(currNode.getState())
          for item in successors:
              state = item[0]
              action = item[1]
              stepcost = item[2]
              if state not in explored:
                  s.push( Node(state, currNode, action, stepcost) )
  util.raiseNotDefined()

def breadthFirstSearch(problem):
  """
  Search the shallowest nodes in the search tree first.
  [2nd Edition: p 73, 3rd Edition: p 82]
  """
  s = util.Queue()
  explored = []
  startNode = Node(problem.getStartState(), None, None, 0)
  s.push(startNode)
  actionslist = []

  while (not s.isEmpty()):
  #for i in range(3):
      currNode = s.pop()
      #explored[currNode.getState()] = 1
      explored.append(currNode.getState())
      #print "Currnode", currNode.getState()
      if problem.isGoalState(currNode.getState()):
          print "done"
          return currNode.pathFromStart()
      else:
          successors = problem.getSuccessors(currNode.getState())
          for item in successors:
              state = item[0]
              action = item[1]
              stepcost = item[2]
              if state not in explored:
                  s.push( Node(state, currNode, action, stepcost) )
  util.raiseNotDefined()
      

class NodeUCS:
    def __init__(self, state, parent, action):
        self.state  = state
        self.parent = parent
        self.action = action
        if parent==None:
            self.actionsToReachNode = []
        else:
            t = parent.actionsToReachNode[:]
            t.append(action)
            self.actionsToReachNode = t

    def __str__(self):
        return "State: " + str(self.state) + "\n" + \
               "Parent: " + str(self.parent.state) + "\n" + \
               "Action: " + str(self.action) + "\n" + \
               "Cost: " + str(self.cost)

    def getState(self):
        return self.state

    def getParent(self):
        return self.parent

    def getAction(self):
        return self.action

    def getActionsToReachNode(self):
        return self.actionsToReachNode



def uniformCostSearch(problem):
  "Search the node of least total cost first. "

  s = util.PriorityQueue()
  explored = []
  startNode = NodeUCS(problem.getStartState(), None, None)
  s.push(startNode, problem.getCostOfActions(startNode.actionsToReachNode))

  while (not s.isEmpty()):
  #for i in range(3):
      currNode = s.pop()
      explored.append(currNode.getState())
      if problem.isGoalState(currNode.getState()):
          print "done"
          return currNode.getActionsToReachNode()
      else:
          successors = problem.getSuccessors(currNode.getState())
          for item in successors:
              state = item[0]
              action = item[1]
              if state not in explored:
                  n = NodeUCS(state, currNode, action)
                  #print "Action sequence: ", n.getActionsToReachNode()
                  #util.pause()
                  s.push( n, problem.getCostOfActions(n.getActionsToReachNode() ))
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"

  s = util.PriorityQueue()
  explored = []
  startNode = NodeUCS(problem.getStartState(), None, None)
  s.push(startNode, problem.getCostOfActions(startNode.actionsToReachNode) + heuristic(startNode.getState(),problem))

  while (not s.isEmpty()):
  #for i in range(3):
      currNode = s.pop()
      explored.append(currNode.getState())
      if problem.isGoalState(currNode.getState()):
          print "done"
          return currNode.getActionsToReachNode()
      else:
          successors = problem.getSuccessors(currNode.getState())
          for item in successors:
              state = item[0]
              action = item[1]
              if state not in explored:
                  n = NodeUCS(state, currNode, action)
                  #print "Action sequence: ", n.getActionsToReachNode()
                  #util.pause()
                  s.push( n, problem.getCostOfActions(n.getActionsToReachNode() ) + heuristic(n.getState(),problem))
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
