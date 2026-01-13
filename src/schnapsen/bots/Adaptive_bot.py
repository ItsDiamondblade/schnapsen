
from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import RegularMove, TrumpExchange
from schnapsen.deck import Card, Suit, Rank
from typing import cast

class AdaptiveBot(Bot):
    """
    
    """

    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        pass