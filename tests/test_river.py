from src.river import River

env = River()

#s0
def test_005(): assert (env.T(0,0,5) == 1) and (env.R(0,0,5) == -1)
def test_010(): assert (env.T(0,1,0) == 1) and (env.R(0,1,0) == -1)
def test_021(): assert (env.T(0,2,1) == 1) and (env.R(0,2,1) == -1)
def test_030(): assert (env.T(0,3,0) == 1) and (env.R(0,3,0) == -1)

def test_024(): assert (env.T(0,2,4) == 0) and (env.R(0,2,4) == -1)
def test_006(): assert (env.T(0,0,6) == 0) and (env.R(0,0,6) == -1)
def test_000(): assert (env.T(0,0,0) == 0) and (env.R(0,0,0) == -1)

#river
def test_100(): assert (env.T(1,0,0) == .5) and (env.R(1,0,0) == -1)
def test_110(): assert (env.T(1,1,0) == .5) and (env.R(1,1,0) == -1)
def test_120(): assert (env.T(1,2,0) == .5) and (env.R(1,2,0) == -1)
def test_130(): assert (env.T(1,3,0) == 1) and (env.R(1,3,0) == -1)

def test_106(): assert (env.T(1,0,6) == .5) and (env.R(1,0,6) == -1)
def test_111(): assert (env.T(1,1,1) == 1) and (env.R(1,1,1) == -1)
def test_122(): assert (env.T(1,2,2) == .5) and (env.R(1,2,2) == -1)
def test_130(): assert (env.T(1,3,0) == 1) and (env.R(1,3,2) == -1)

def test_200(): assert (env.T(2,0,0) == .5) and (env.R(2,0,0) == -1)
def test_210(): assert (env.T(2,1,0) == .5) and (env.R(2,1,0) == -1)
def test_220(): assert (env.T(2,2,0) == .5) and (env.R(2,2,0) == -1)
def test_230(): assert (env.T(2,3,0) == .5) and (env.R(2,3,0) == -1)

def test_207(): assert (env.T(2,0,7) == .5) and (env.R(2,0,7) == -1)
def test_212(): assert (env.T(2,1,2) == 1) and (env.R(2,1,2) == -1)
def test_223(): assert (env.T(2,2,3) == .5) and (env.R(2,2,3) == -1)
def test_231(): assert (env.T(2,3,1) == .5) and (env.R(2,3,1) == -1)

#other
def test_808(): assert (env.T(8,0,8) == 1) and (env.R(8,0,8) == -1)
def test_813(): assert (env.T(8,1,3) == 1) and (env.R(8,1,3) == -1)
def test_829(): assert (env.T(8,2,9) == 1) and (env.R(8,2,9) == -1)
def test_837(): assert (env.T(8,3,7) == 1) and (env.R(8,3,7) == -1)

def test_839(): assert (env.T(8,3,9) == 0) and (env.R(8,3,9) == -1)


#G
def test_914(): assert (env.T(9,1,4) == 1) and (env.R(9,1,4) == 0)
def test_324(): assert (env.T(3,2,4) == .5) and (env.R(3,2,4) == 0)
def test_224(): assert (env.T(2,2,4) == 0) and (env.R(2,2,4) == -1)
def test_404(): assert (env.T(4,0,4) == 0) and (env.R(4,0,4) == -1)
