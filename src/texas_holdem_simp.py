import numpy as np  



class Texas_Holdem_Simp:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        
        actions = ['fold', 'call', 'raise', 'all_in']
        self.deck = [
            ('J', 'hearts'),
            ('Q', 'hearts'),
            ('K', 'hearts'),
            ('J', 'spades'),
            ('Q', 'spades'),
            ('K', 'spades')
        ]

        self.p1 = 6
        self.p2 = 5
        self.t1 = 4
        self.t2 = 3
        self.chips = 1+ 2*3
        self.bet = 3
        self.pot = 1+ 2*3
        self.rounds = 3
        
        self.S = np.arange(self.p1*self.p2*self.t1*self.t2*self.chips*self.bet*self.pot*self.rounds)
        self.A = np.arange(4)

    def to_factor(self, s):
        return list(np.array(np.meshgrid(
                range(len(self.deck)), 
                range(len(self.deck)), 
                range(len(self.deck)), 
                range(len(self.deck)), 
                range(self.chips), 
                range(self.bet), 
                range(self.pot), 
                range(self.rounds)
            )).T.reshape(-1,8)[s])
    def to_tabular(self, s):
        x = np.array(np.meshgrid(
                range(len(self.deck)), 
                range(len(self.deck)), 
                range(len(self.deck)), 
                range(len(self.deck)), 
                range(self.chips), 
                range(self.bet), 
                range(self.pot), 
                range(self.rounds)
            )).T.reshape(-1,8)
        return np.where(np.all(x == s, axis=1))[0][0]

    def evaluate_winner(self, p1,p2,t1,t2):
        p1_game = [p1, t1, t2]
        p2_game = [p2, t1, t2]
        
        # Flush
        if ( (0 in p1_game and 1 in p1_game and 2 in p1_game) 
         or  (3 in p1_game and 4 in p1_game and 5 in p1_game)
        ): 
            return True
        
        if ( (0 in p2_game and 1 in p2_game and 2 in p2_game) 
         or  (3 in p2_game and 4 in p2_game and 5 in p2_game)
        ): 
            return False
        
        # Seq
        if (  (0 in p1_game and 1 in p1_game and 5 in p1_game) 
            or  (0 in p1_game and 4 in p1_game and 2 in p1_game)
            or  (3 in p1_game and 1 in p1_game and 5 in p1_game)
            or  (3 in p1_game and 4 in p1_game and 2 in p1_game)
        ):
            return True
        if (  (0 in p2_game and 1 in p2_game and 5 in p2_game) 
            or  (0 in p2_game and 4 in p2_game and 2 in p2_game)
            or  (3 in p2_game and 1 in p2_game and 5 in p2_game)
            or  (3 in p2_game and 4 in p2_game and 2 in p2_game)
        ):
            return False

        # Pair
        if (  (0 in p1_game and 3 in p1_game) 
            or  (1 in p1_game and 4 in p1_game)
            or  (2 in p1_game and 5 in p1_game)
        ):
            return True
        if (  (0 in p2_game and 3 in p2_game) 
            or  (1 in p2_game and 4 in p2_game)
            or  (2 in p2_game and 5 in p2_game)
        ):
            return False
        
        

    def T(self, s,a,s_):
        """
        fold: 
            round r: (a, b, c, d, x, y, z, r) -> ([0..5], [0..4], 0, 0, x-1, 1, 2, 0) : 1/(6*5) pra todo a e b 

        call: 
            round 0: (a, b, 0, 0, x, y, z, 0) -> (a, b,[0..3], 0, x-y, y, z+(2*y), 1) : 1/4 pra todo c
            round 1: (a, b, c, 0, x, y, z, 1) -> (a, b, c, [0..2], x-y, y, z+(2*y), 2) : 1/3 pra todo d
            round 2: (a, b, c, d, x, y, z, 2) -> (a, b, c, d, (z|x-z), 1, 0, 0) : 1

        raise: 
            round 0: (a, b, 0, 0, x, y, z, 0) -> (a, b,[0..3], x-y-1, y+1, z+2*(y+1), 1) : 1/4 pra todo c
            round 1: (a, b, c, 0, x, y, z, 1) -> (a, b, c, [0..2], x-y-1, y+1, z+2(y+1), 2) : 1/3 pra todo d
            round 2: (a, b, c, d, x, y, z, 2) -> (a, b, c, d, (z|x-z), 1, 0, 0) : 1

        all_in: 
            round r: (a, b, c, d, x, y, z, r) -> (a, b, c, d, (z|x-z), 1, 0, 0) : 1
        """
        fs = self.to_factor(s)
        fs_ = self.to_factor(s_)    

        lBound = lambda v: v if v>=0 else 0
        uBound = lambda v, b=6: v if v<=b else b
        
        if a == 0: # fold
            if lBound(fs[4]-1) > 0:
                next_s = {
                    (p1, p2, 0, 0, lBound(fs[4]-1), 1, 2, 0): 1/(self.p1*self.p2)
                    for p1,_ in enumerate(self.deck)
                    for p2,_ in enumerate(self.deck)
                    if p1 != p2
                }
            else: next_s = {(0, 0, 0, 0, 0, 0, 0, 0): 1}    
        if a == 1: # call
            r = fs[-1]
            chips = lBound(fs[4]-fs[5])
            pot = uBound(fs[6]+2*fs[5], self.pot)
            if fs[-1] in (0,1): # round 0 or 1
                next_s = {
                    (fs[0], fs[1], (t if r==0 else fs[2]), (t if r==1 else 0), chips, fs[5], pot, r+1)
                    : 1/(self.t1 if r==0 else self.t2)
                    for t,_ in enumerate(self.deck)
                    if len({fs[0], fs[1]}| ({t} if r==0 else fs[2]) |({t} if r==1 else set())) == (3 if r==0 else 4)
                }
            if fs[-1] == 2: # round 2
                v = uBound(fs[4]+fs[-2], self.pot) if self.evaluate_winner(fs[0], fs[1], fs[2], fs[3]) else lBound(fs[4])
                if 0 < v > self.chips:
                    next_s = {
                        (p1, p2, 0, 0, lBound(fs[4]-1), 1, 2, 0): 1/(self.p1*self.p2)
                        for p1,_ in enumerate(self.deck)
                        for p2,_ in enumerate(self.deck)
                        if p1 != p2
                    }
                else:
                    next_s = {
                        (0, 0, 0, 0, v, 0, 0, 0)
                        : 1
                    }         
        if a == 2: # raise
            v = 1 if fs[4]>0 and (self.chips-1-fs[4])>0 else 0
            if fs[-1] == 0: # round 0
                next_s = {
                    (fs[0], fs[1], t1, 0, lBound(fs[4]-uBound(fs[5]+v,self.bet)), uBound(fs[5]+v,self.bet), uBound(fs[6]+2*uBound(fs[5]+v,self.bet), self.pot), 1)
                    : 1/self.t1
                    for t1,_ in enumerate(self.deck)
                    if len({fs[0], fs[1], t1})==3
                }
            if fs[-1] == 1: # round 1
                next_s = {
                    (fs[0], fs[1], fs[2], t2, lBound(fs[4]-uBound(fs[5]+v,self.bet)), uBound(fs[5]+v,self.bet), uBound(fs[6]+2*uBound(fs[5]+v,self.bet), self.pot), 2)
                    : 1/self.t2
                    for t2,_ in enumerate(self.deck)
                    if len({fs[0], fs[1], fs[2], t2})==4
                }
            if fs[-1] == 2: # round 2
                v = uBound(fs[4]+fs[-2], self.pot) if self.evaluate_winner(fs[0], fs[1], fs[2], fs[3]) else lBound(fs[4])
                if 0 < v > self.chips:
                    next_s = {
                        (p1, p2, 0, 0, lBound(fs[4]-1), 1, 2, 0): 1/(self.p1*self.p2)
                        for p1,_ in enumerate(self.deck)
                        for p2,_ in enumerate(self.deck)
                        if p1 != p2
                    }
                else:
                    next_s = {
                        (0, 0, 0, 0, v, 0, 0, 0)
                        : 1
                    }
        if a == 3: # all_in
            next_s = {
                (0, 0, 0, 0, self.chips if self.evaluate_winner(fs[0], fs[1], fs[2], fs[3]) else 0, 0, 0, 0): 1
            }

        i = tuple(fs_)
        return next_s[i] if i in next_s else 0
    


    def R(self, s,a,s_):
        fs_ = self.to_factor(s_)
        return int(fs_[4]==0)*-1

    def plot(self, label=None, mask=None):
        pass

