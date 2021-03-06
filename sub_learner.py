import random
import sys
import sub_visualizer as v
from typing import Dict, List, Tuple
# Size X x Y x D/P x K 

def genf_j(S: Tuple, K: int, winCount: Dict, loseCount: Dict):
    '''
    This is f_J, the win ratio per action in each state.
    '''
    X, Y, D = S
    f = {}
    for J in range(0,K+1):
        wc, lc = winCount.get(str((X,Y,D,J))), loseCount.get(str((X,Y,D,J)))
        wc = 0 if wc == None else wc # If the entry doesn't exist, consider it 0
        lc = 0 if lc == None else lc
        denom = wc + lc
        f[J] = wc/denom if denom != 0 else 0.5
    return f

def getMaxf_J(K: int, f: Dict):
    '''
    This is B, the optimal move index of a state given f.
    '''
    valB = 0
    B = 0
    for J in range(0,K+1):
        if f[J] >= valB: # Decided to make it >= instead of to make it more exploratory.
            B = J
            valB = f[J]
    return B

def sumOver_f_J_notB(B: int, f: Dict):
    '''
    This is sum of all f_J where J is not B, otherwise known as g.
    '''
    total = 0
    for J in f:
        if J != B: total += f[J] 
    return total

def sumSeenInTrajectory(S: List, K: int, wc: Dict, lc: Dict):
    '''
    This is T, all the times we've seen this move in history.
    '''
    total = 0
    X, Y, D = S
    for J in range(0,K+1):
        wc_S = wc.get(str((X,Y,D,J)))
        lc_S = lc.get(str((X,Y,D,J)))
        wc_S = 0 if wc_S == None else wc_S
        lc_S = 0 if lc_S == None else wc_S
        total += wc_S + lc_S
    return total

def pB(T, f, B, M, K):
    '''
    Probability of choosing optimal move index B.
    S: state (X, Y, D)
    f: Win Ratio 
    M: explore-exploit hyperparameter
    B: index of 'optimal' move
    K: # cards that can be drawn
    '''
    numer = T*f[B] + M
    denom = T*f[B] + (K + 1) * M
    return numer / denom

def pJ(pB, T, f, J, M, g, K):
    '''
    Probability of choosing nonoptimal move index J.
    '''
    oneMinuspB = 1 - pB
    numer = T*f[J] + M
    denom = g * T + K * M 
    return oneMinuspB * numer / denom

def stoch(K, B, probB, T, f, M, g):
    '''
    Adds stochasticity to results of actions. 
    Next state given action is stochastically determined here.
    '''
    cdf = []
    sanity = 0
    for J in range(0,K+1):
        add = 0
        if J == B: 
            add = probB
            val = probB + cdf[J-1] if J != 0 else probB
            cdf.append(val)
        else: 
            add = pJ(probB, T, f, J, M, g, K)
            val = add + cdf[J-1] if J != 0 else add
            cdf.append(val)
        sanity += add
    if sanity < 0.97 or sanity - 0.03 > 0.98: print("Total is weird.",sanity) 
    x = random.randint(0,999) / 1000 # Uniformly distributed between 0 and 1. 
    for i in range(0,K+1):
        if x <= cdf[i]: 
            return i
    return K

def populateTerms(settings, S, winCount, loseCount):
    N, L, U, K, M, NGAMES = settings
    X, Y, D = S 
    f = genf_j(S, K, winCount, loseCount)
    B = getMaxf_J(K, f)
    g = sumOver_f_J_notB(B, f)
    T = sumSeenInTrajectory(S, K, winCount, loseCount)
    return (N, L, U, K, M, X, Y, D, f, B, g, T)

def draw_card(N): 
    card_drawn = random.randint(1,N)
    return card_drawn

def take_turn(X, Y, D, N, T, f, B, M, K, g): 
    '''
    Uses combination of above to decide next move.
    '''
    probB = pB(T, f, B, M, K)
    outcome = stoch(K, B, probB, T, f, M, g)
    total = 0
    for draw in range(0, outcome):
        d = draw_card(N)
        total += d
    new_state = (X + total, Y, outcome)
    # if_pass = True if B == 0 else False
    if_pass = True if total == 0 else False
    return new_state, if_pass

def update(winnerMoves, loserMoves, wc, lc):
    for move in winnerMoves:
        wc[str(move)] = wc[str(move)] + 1 if str(move) in wc else 1
    for move in loserMoves:
        lc[str(move)] = lc[str(move)] + 1 if str(move) in lc else 1
    return wc, lc

def other(player):
    return -player + 1  

def run_trial(wc, lc, policy, settings):
    trajectory = [[],[]]
    assert len(settings) == 6
    N = settings[0]
    L = settings[1]
    U = settings[2]
    K = settings[3]
    S =(0, 0, 1) # Random initial draw state, should approximate away
    X, Y, D = S
    endgame = False
    player = 0
    while endgame == False:  
        X0, Y0, D0 = X, Y, D
        f = genf_j((X, Y, D),K,wc,lc)
        B = getMaxf_J(K, f)
        T = sumSeenInTrajectory((X,Y,D),K,wc,lc)
        g = sumOver_f_J_notB(B, f)
        policy[str((X, Y, D))] = B
        (X, Y, D), if_pass = take_turn(X, Y, D, N, T, f, B, M, K, g)
        if player == 0: trajectory[0].append([(X0,Y0,D0,D)])
        else: trajectory[1].append((X0,Y0,D0,D))
        if if_pass and D0 == 0: # Both players have passed, Y being the first one.
            endgame = True 
            if X > Y and X <= U:
                wc, lc = update(trajectory[player],trajectory[other(player)], wc, lc)
            else: 
                wc, lc = update(trajectory[other(player)],trajectory[player], wc, lc)
        elif X >= L and X <= U: 
            endgame = True 
            wc, lc = update(trajectory[player],trajectory[other(player)], wc, lc)
        elif X > U:
            endgame = True 
            wc, lc = update(trajectory[other(player)],trajectory[player], wc, lc)
        player = other(player)
        X, Y = Y, X
    return policy, wc, lc

def run(N,L,U,K,M,NGAMES):
    policy = {}
    wc = {}
    lc = {}
    settings = N,L,U,K,M,NGAMES
    for n in range(0, NGAMES):
        if n % 1000 == 0: print("Working... Trial",n)
        policy, wc, lc = run_trial(wc, lc, policy, settings)
    print("Done!")
    return policy, wc, lc
N = int(sys.argv[1]) 
L = int(sys.argv[2])
U = int(sys.argv[3])
K = int(sys.argv[4])
M = float(sys.argv[5])
NGAMES = int(sys.argv[6])
policy, wc, lc = run(N,L,U,K,M,NGAMES)
print('\nInput:',N, L, U, K, M,'\n')
v.printPolicyGrid(policy,K,L, True)
print('\n')
v.printProbabilityGrid(policy, wc, lc,L, True)