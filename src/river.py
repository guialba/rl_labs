import numpy as np

class River:
    def __init__(self, 
                 width=5, 
                 height=2,
                 river = [1,2,3],
                 S0 = 0,
                 G = [4]
                ):
        
        self.width = width
        self.height = height

        self.S0 = S0
        self.river = river
        self.G = G

        self.S = np.arange(width*height)
        self.A = np.arange(4)

    def T(self, s,a,s_):
        if s in self.G: # Meta é um estado absorvedor, portanto a prob de sair é 0
            return 0 if s!=s_ else 1
        
        m=None
        allowed_move = False
        try:
            # contrói grid e ações
            sx,sy = np.meshgrid(np.arange(self.width),np.arange(self.height))
            grid = np.vstack([sx.ravel(), sy.ravel()])
            acts = np.array([[0,0,1,-1], [1,-1,0,0]])
            m = grid[:,s] + acts[:,a]
            
            # valida movimento
            allowed_move = all(m == grid[:,s_])
            # move_s = np.where((grid[0] == m[0]) & (grid[1] == m[1]))[0][0]
        except:
            return 0 

        if not allowed_move: # Movimento não permitido 
            if s_ == 0 and s in self.river: 
                return .5 
            else: # Movimento no grid
                if 0<=m[0]<self.width and 0<=m[1]<self.height:
                    return 0
                else: # Movimento para fora do grid matem a posição
                    return 0 if s!=s_ else 1
        else:
            if s_ == 0 and s in self.river:
                return 1
            else:
                return .5 if s in self.river else 1
                # return .5 if s in self.river or s_ in self.river else 1
    
    def R(self, s,a,s_):
        return int(self.T(s,a,s_)>0 and s_ in self.G)-1
