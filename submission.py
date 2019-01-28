#!/usr/bin/python3

# CS-E4800 AI, Programming assignment round 4: Sudoku solver.
# Fill in the code sections marked with "TODO"

import math
from expr import And, Or, Not, Implies, Equivalent # Logical operators
from expr import Var # Var(name, [some, params]) -> a variable "name(some,params)"

# value(x,y,v) represents a number v at position (x,y).
def value(x,y,v):   
    return Var("value", [x,y,v])
    
def value_exists(x, y, n):
    # Returns a list of logic formulas that together implement the rule
    # "There must exist a value (between 1 and n) at position (x,y)"
    return [Or([value(x,y,v) for v in range(1,n+1)])]
    
def unique_value(x, y, n):
    formulas = []
    # TODO: return a list of logic formulas that together implement the rule
    # "There can be at most one value at position (x,y)".
    for v1 in range (1,n):
        for v2 in range (v1+1,n+1):
            formulas.append(Or([Not(value(x,y,v1)), Not(value(x,y,v2))]))
    return formulas
        
def same_row(x0, y0, x1, y1):
    # TODO: return True if and only if 
    #(x0,y0) and (x1,y1) are on the same row
    return y0==y1
    
def same_col(x0, y0, x1, y1):
    # TODO: return True if and only if 
    #(x0,y0) and (x1,y1) are on the same column
    return x0==x1

def same_box(x0, y0, x1, y1, k):
    # TODO: return True if and only if 
    #(x0,y0) and (x1,y1) are in the same k*k box
    return (((x1-1)//k) == ((x0-1)//k)) and (((y1-1)//k) == ((y0-1)//k))

def require_different_values(x0, y0, x1, y1, n):
    formulas = []
    # TODO: return a list of logic formulas that together implement the rule 
    # "The values of cells (x0,y0) and (x1,y1) must be different"
    for v in range (1,n+1):
        formulas.append(Or([Not(value(x0,y0,v)), Not(value(x1,y1,v))]))
    return formulas

# Complete the above TODOs to finish the sudoku solver,
# or write your own solver from scratch.
def sudoku_solver(n=9):
    formulas = []
    # k: the size of the boxes the n*n sudoku grid is divided into
    k = int(math.sqrt(n))
    
    for x in range(1,n+1):
        for y in range(1,n+1):
            formulas += value_exists(x,y,n)
            formulas += unique_value(x,y,n)
            
    for x0 in range(1,n+1):
        for y0 in range(1,n+1):
            for x1 in range(x0,n+1):
                for y1 in range(1,n+1):
                    if x0 == x1 and y0 >= y1:
                        continue
                    if (same_row(x0,y0,x1,y1) or 
                        same_col(x0,y0,x1,y1) or 
                        same_box(x0,y0,x1,y1,k)):
                        formulas += require_different_values(x0,y0,x1,y1,n)
        
                    
    return formulas    
    

def clue(x,y,v):   
    return Var("clue", [x,y,v])
   
def origvalue(x,y,v):
    return Var("origvalue", [x,y,v])
    
def alternative_solution_finder(n=9):
    formulas = []
    # TODO: Return a list of formulas that, given 
    #   a sudoku puzzle defined by clue(x,y,v) atoms and
    #   a solution to the puzzle defined by origvalue(x,y,v) atoms,
    # finds a different solution to the sudoku expressed using value(x,y,v) atoms.
    # You can assume that clue(x,y,v) -> origvalue(x,y,v) holds true.
    k = int(math.sqrt(n))
    
    for x in range(1,n+1):
        for y in range(1,n+1):
            formulas += value_exists(x,y,n)
            formulas += unique_value(x,y,n)
            
    for x0 in range(1,n+1):
        for y0 in range(1,n+1):
            for x1 in range(x0,n+1):
                for y1 in range(1,n+1):
                    if x0 == x1 and y0 >= y1:
                        continue
                    if (same_row(x0,y0,x1,y1) or 
                        same_col(x0,y0,x1,y1) or 
                        same_box(x0,y0,x1,y1,k)):
                        formulas += require_different_values(x0,y0,x1,y1,n)
    disjunc = []

    for x in range(1,n+1):
        for y in range(1,n+1):
            for v in range (1,n+1): 
                disjunc.append((x,y,v))
                formulas.append(Implies(clue(x,y,v), value(x,y,v)))
    formulas += [Or([Not(Equivalent(origvalue(x,y,v), value(x,y,v))) for x,y,v in disjunc])]
    return formulas