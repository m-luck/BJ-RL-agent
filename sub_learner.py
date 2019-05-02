from typing import Dict, List
# Size X x Y x D/P x K 
winCount = {}
loseCount = {}
policy_a_given_s = {}
value_of_intention = {}

def genf_j(K: int, winCount: Dict, loseCount: Dict):
    '''
    This is f_J, the win ratio.
    '''
    f = {}
    for J in range(0,K+1):
        wc, ls = winCount[(X,Y,D,J)], loseCount[(X,Y,D,J)]
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
    This is sum of all f_J where J is not B.
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
    numer = T[fB] + M
    denom = T[fB] + (K + 1) * M
    return numer / denom

def pJ(pB):
    '''
    Probability of choosing J.
    '''
    oneMinuspB = 1 - pB
    numer = T[f[J]] + M
    denom = g * T + K * M 
    return oneMinuspB * numer / denom

def choose(S: List, settings: List): 
    '''
    Uses combination of above to decide next move.
    '''
    assert len(settings) == 4
    L, U, K, M = *settings
    X, Y, D = *S 
    f = genf_j(K, winCount, loseCount)
    B = getMaxf_J(K, f)
    g = sumOver_f_J_notB(B, f)
    T = sumSeenInTrajectory(S, K, winCount, loseCount)
    probB = pB(T, f, B, M) 
    probJ = pJ(probB, T, f, J, M, g, K)
    u0 = p0 
    for i in range(0,k):
        u[i] = u[i−1] + p[i]
    x = random.randint(0,100) # Uniformly distributed between 0 and 1. 
    for i in range(0,k):
        if x < u[i]: 
            return i

def update_policy():
    pass

def run_trial():
    pass
