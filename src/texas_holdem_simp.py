import numpy as np  
import itertools
import math

def points(game):
    flush = {'J♥', 'K♥', 'Q♥'}
    seq = 'JKQ'
    pairs = ('KKQ', 'JKK', 'KQQ', 'JQQ', 'JJK', 'JJQ')
    # Flush
    if set(game) == flush:
        return 1
    
    cards = ''.join(sorted([card[0] for card in game]))
    # sequence
    if cards == seq:
        return 2
    
    # pairs
    return (3 + pairs.index(cards))

class Texas_Holdem_Simp:
    def __init__(self, seed=None):
        if seed is not None:
            np.random.seed(seed)
        
        self.actions = ['fold', 'call']
        self.deck = ['J♥', 'J♠', 'Q♥', 'Q♠', 'K♥', 'K♠']
        # self.deck = ['J♥', 'J♠', 'Q♥', 'Q♠', 'K♥', 'K♠', 'A♥', 'A♠']

        self.cards = 4
        self.chips_per_player = 5
        self.rounds = 2
        
        self.aux = np.array(
            np.meshgrid( range(6), range(5), range(4), range(3), range(7), range(2), range(3), range(3) )
        ).T.reshape(-1,8)
        
        self.games = list(itertools.permutations(self.deck, self.cards))
        self.info = [tuple(i) for i in np.array(np.meshgrid( 
            range(self.chips_per_player*2), 
            range(self.chips_per_player), 
            range(self.rounds) 
        )).T.reshape(-1,3)]
        
        self.S = [(*g, *i) for g,i in list(itertools.product(self.games, self.info))]
        self.A = np.arange(4)
        self.possible_games = {g:points(g) for g in list(itertools.permutations(self.deck, 3))}
    
    def enum(self, s):
        return self.S.index(s)

    def factor(self, i):
        return self.S[i]
    
    def evaluate_game(self, s):
        p1,p2,t1,t2 = self.factor(s)[:4]
        p1_game = (p1,t1,t2)
        p2_game = (p2,t1,t2)

        points_p1 = self.possible_games[p1_game]
        points_p2 = self.possible_games[p2_game]

        return None if points_p1 == points_p2 else (points_p1 < points_p2)
        
    def T(self, s, a, s_):
        p1,p2,t1,_,chips,pot,r = self.factor(s)
        p1_,p2_,t1_,_,chips_,pot_,r_ = self.factor(s_)
        
        lBound = lambda v: v if v>=0 else 0
        uBound = lambda v, b=6: v if v<=b else b

        if chips in (6,0) and r==0:
            return 0

        prob_round_1 =  1/(math.factorial(len(self.deck) ) / math.factorial(len(self.deck)-3))
        prob_round_2 =  1/(math.factorial(len(self.deck)-3) / math.factorial(len(self.deck)-3 - 1))

        if a == 0: # fold
            next_s = ((r_ == 0) and (pot_ == 0) and (chips_ == lBound(chips-1)))
            return prob_round_1 if next_s else 0
        
        if a == 1: # call
            if r == 0:
                next_s = (
                    (r_ == r+1) and (pot_ == pot+1) and (chips_ == lBound(chips-1)) 
                    and (p1==p1_), (p2==p2_), (t1==t1_)
                )
                return prob_round_2 if next_s else 0
            else:
                win = self.evaluate_game(s)
                prize = ((pot+1)*2 if win else (0, ((pot+1)*2)//2)[win is None])
                next_s = (
                    (r_ == 0) and (pot_ == 0) and (chips_ == uBound(lBound(chips-1+prize)))
                )
                return prob_round_1 if next_s else 0
        
    def R(self, s,a=None,s_=None):
        fs = self.factor(s)
        return -int(fs[4:]==(0,0,0))

    def plot(self, s):
        fs = self.factor(s)
        print(fs)

