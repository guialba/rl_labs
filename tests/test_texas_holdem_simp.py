import math
from src.texas_holdem_simp import Texas_Holdem_Simp

env = Texas_Holdem_Simp()

#round 0
s = env.to_tabular([0,1,0,0,2,1,2,0])

s_ = env.to_tabular([0,1,0,0,1,1,2,0])
def test_fold_0(): 
    acum = 0
    for i in range(6):
        for j in range(6):
            s_ = env.to_tabular([i,j,0,0,1,1,2,0])
            p = env.T(s, 0, s_)
            acum += p
            # print(i,p)
    assert (math.isclose(acum, 1., rel_tol=1e-9))

def test_call_0(): 
    acum = 0
    for i in range(6):
        s_ = env.to_tabular([0,1,i,0,1,1,4,1])
        p = env.T(s, 1, s_)
        acum += p
        # print(i,p)
    assert (math.isclose(acum, 1., rel_tol=1e-9))

def test_raise_0(): 
    acum = 0
    for i in range(6):
        s_ = env.to_tabular([0,1,i,0,0,2,6,1])
        p = env.T(s, 2, s_)
        acum += p
        # print(i,p)
    assert (math.isclose(acum, 1., rel_tol=1e-9))


def test_allin_0(): 
    acum = 0
    for i in range(7):
        s_ = env.to_tabular([0,0,0,0,i,0,0,0])
        p = env.T(s, 3, s_)
        acum += p
        # print(i,p)
    assert (math.isclose(acum, 1., rel_tol=1e-9))

#round 1
# def test_002(): assert (env.T(0,0,5) == 1) and (env.R(0,0,5) == -1)

#round 2
# def test_003(): assert (env.T(0,0,5) == 1) and (env.R(0,0,5) == -1)
