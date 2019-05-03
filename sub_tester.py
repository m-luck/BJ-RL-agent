import sub_learner as l
from typing import Dict, List

def test_winRatio(K, winCount, loseCount):
    res = l.genf_j(K, winCount, loseCount)
    print(res)
    return res

def test_bestMove():
    pass

def test_noBestMove():
    pass

def test_countSeen():
    pass

def test_pB():
    pass

def test_pJ(pB):
    pass

def test_montecarlo():
    pass

def test_choose():
    pass

def run_trial():
    pass

if __name__ == "__main__":
    # Test Conditions 1
    K = 2
    M = 4 
    S = [2,3,1]
    winCount = {}
    loseCount = {}

    test_winRatio(K, winCount, loseCount)