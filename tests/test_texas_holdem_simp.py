from src.texas_holdem_simp import Texas_Holdem_Simp

env = Texas_Holdem_Simp()

#round 0
s = env.to_tabular([0,1,0,0,2,1,2,0])

s_ = env.to_tabular([0,1,0,0,1,1,2,0])
def test_fold_0(): assert (env.T(s,0,s_) > 0) and (env.R(s,0,s_) == 0)

s_ = env.to_tabular([0,1,2,0,1,1,4,1])
def test_call_0(): assert (env.T(s,1,s_) > 0) and (env.R(s,1,s_) == 0)

s_ = env.to_tabular([0,1,2,0,1,1,4,1])
def test_raise_0(): assert (env.T(s,2,s_) > 0) and (env.R(s,2,s_) == 0)

s_ = env.to_tabular([0,1,2,0,1,1,4,1])
def test_allin_0(): assert (env.T(s,3,s_) > 0) and (env.R(s,3,s_) == 0)

#round 1
# def test_002(): assert (env.T(0,0,5) == 1) and (env.R(0,0,5) == -1)

#round 2
# def test_003(): assert (env.T(0,0,5) == 1) and (env.R(0,0,5) == -1)
