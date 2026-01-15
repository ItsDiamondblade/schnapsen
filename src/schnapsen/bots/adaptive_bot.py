
from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import RegularMove, TrumpExchange
from schnapsen.deck import Card, Suit, Rank
from typing import Optional

class AdaptiveBot(Bot):
    """
    
    """

    def __init__(self, threshold: float, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.threshold = threshold if (threshold > 0 and threshold < 1) else 0.5

    def aggressive(self): # get rid of low-value cards
        pass

    def defensive(self): # preserve high-value cards
        pass

    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        valid_regular_moves: list[RegularMove] = [move.as_regular_move() for move in perspective.valid_moves() if move.is_regular_move()]

        high_value_ranks = [Rank.ACE, Rank.TEN]
        low_value_ranks = [Rank.KING, Rank.QUEEN, Rank.JACK]

        # play trump suits first
        trump_suit = perspective.get_trump_suit()
        trumps: list[RegularMove] = [move for move in valid_regular_moves if move.card.suit == trump_suit]
        if trumps:
            return trumps[0]

        high_value_moves = []
        low_value_moves = []
        total_moves = 0
        for move in valid_regular_moves:
            card = move.cards[0]
            if card.rank in high_value_ranks:
                high_value_moves.append(move)
                total_moves += 1
            elif card.rank in low_value_ranks:
                low_value_moves.append(move)
                total_moves += 1
        
        if len(high_value_moves) / total_moves >= self.threshold: # lots of high-value cards - want to preserve them
            return self.defensive()
        else: # lots of low-value cards - want to expend them
            return self.aggressive()
