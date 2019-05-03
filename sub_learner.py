from typing import Dict, List
# Size X x Y x D/P x K 

def genf_j(K: int, winCount: Dict, loseCount: Dict):
    '''
    This is f_J, the win ratio per draw in each state.
    '''
    f = {}
    for J in range(0,K+1):
        wc, lc = winCount.get(str(X,Y,D,J)), loseCount.get((X,Y,D,J))
        wc = 0 if wc == None else wc # If the entry doesn't exist, consider it 0
        lc = 0 if lc == None else lc
        denom = wc + lc
        denom = denom if denom != 0 else 0.5
        f[J] = wc/denom
    return f

def getMaxf_J(K: int, f: Dict):
    '''
    This is B.
    '''
    valB = 0
    B = 0
    for J in range(0,K+1):
        if f[J] > valB:
            B = J
            valB = f[J]
    return B

def sumOver_f_J_notB(B: int, f: Dict):
    '''
    This is sum of all f_J where J is not B, otherwise known as g.
    '''
    total = 0
    for J, f_J in enumerate(f):
        if J != B: total += f_J 
    return total

def sumSeenInTrajectory(S: List, K: int, winCount: Dict, loseCount: Dict):
    '''
    This is T.
    '''
    total = 0
    X, Y, D = *S
    for J in range(0,K+1):
        total += winCount[(X,Y,D,J)] + loseCount[(X,Y,D,J)]
    return total

def pB(T, f, B, M, K):
    '''
    S: state (X, Y, D)
    f: Win Ratio 
    M: explore-exploit hyperparameter
    '''
    numer = T[f[B]] + M
    denom = T[f[B]] + (K + 1) * M
    return numer / denom

def pJ(pB, T, f, J, M, g, K):
    '''
    Probability of choosing winning given choosing J.
    '''
    oneMinuspB = 1 - pB
    numer = T[f[J]] + M
    denom = g * T + K * M 
    return oneMinuspB * numer / denom

def montecarlo(K, B, probB, T, f, M, g):
    cdf = []
    for J in range(0,K):
        if J == B: 
            cdf += [-1] # Append a value to fill (no -1's should be left after the for loop is done).
            cdf[J] = probB + cdf[J-1] if J != 0 else probB
        elif J == 0:
            cdf += [-1]
            cdf[J] = 0
        else: 
            cdf += [-1]
            cdf[J] = pJ(probB, T, f, J, M, g, K) + cdf[J-1]
    x = random.randint(0,100) # Uniformly distributed between 0 and 1. 
    for i in range(0,K):
        if x < cdf[i]: 
            return i
    return cdf

def choose(winCount: Dict, loseCount: Dict, S: List, settings: List): 
    '''
    Uses combination of above to decide next move.
    '''
    assert len(S) == 3
    assert len(settings) == 4
    L, U, K, M = *settings
    X, Y, D = *S 
    f = genf_j(K, winCount, loseCount)
    B = getMaxf_J(K, f)
    g = sumOver_f_J_notB(B, f)
    T = sumSeenInTrajectory(S, K, winCount, loseCount)
    probB = pB(T, f, B, M) 
    montecarlo(K, B, probB, T, f, M, g)

def run_trial(winCount, loseCount, S, settings):
    assert len(S) == 3
    X, Y, D = *S
    outcome = choose(winCount, loseCount, S, settings)
    X += 0

def run():
    pass
