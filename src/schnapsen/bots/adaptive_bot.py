from schnapsen.game import Bot, Move, PlayerPerspective
from schnapsen.game import RegularMove, TrumpExchange, SchnapsenTrickScorer, Marriage
from schnapsen.deck import Card, Suit, Rank
from typing import Optional

class AdaptiveBot(Bot):
    """
    This bot has two strategies, one two hold on to high-value cards,
    and another to get rid of low-value cards. Which strategy is chosen
    depends on the percentage of high-value cards currently in the bot's hand.
    This percentage is set using the threshold variable.
    Args:
        threshold (float): Treshold of percentage of cards as to what strategy the bot employs (between 0 and 1), defaults to 0.5
        name (Optional[str]): The optional name of this bot
    """

    def __init__(self, threshold: float, name: Optional[str] = None) -> None:
        super().__init__(name)
        self.threshold = threshold if (threshold > 0 and threshold < 1) else 0.5
        self.aggressive_moves = 0
        self.defensive_moves = 0

    def aggressive(self, valid_moves: list[Move], trumps: list[RegularMove], trump_suit: Suit, marriage_moves: list[Marriage]) -> Move: # plays high-value cards first
        regular_non_trump_moves = [move for move in valid_moves if move.is_regular_move() and move.cards[0].suit != trump_suit]
        # play trump marriages first, as they give 40 points
        for move in marriage_moves:
            if move.suit == trump_suit:
                return move
        
        # else play marriages
        if marriage_moves:
            return marriage_moves[0]
        
        # else play trump exchanges
        for move in valid_moves:
            if move.is_trump_exchange():
                return move
        
        # else play highest scoring trumps
        if trumps:
            return max(trumps, key=lambda move: (SchnapsenTrickScorer.rank_to_points(self, move.cards[0].rank)))
    
        # else play the highest scoring move
        return max(regular_non_trump_moves, key=lambda move: (SchnapsenTrickScorer.rank_to_points(self, move.cards[0].rank)))

    def defensive(self, valid_moves: list[Move], trumps: list[RegularMove], trump_suit: Suit,marriage_moves: list[Marriage]) -> Move: # preserve high-value cards
        regular_non_trump_moves = [move for move in valid_moves if move.is_regular_move() and move.cards[0].suit != trump_suit]
        # play lowest scoring regular move
        if regular_non_trump_moves:
            return min(regular_non_trump_moves, key=lambda move: (SchnapsenTrickScorer.rank_to_points(self, move.cards[0].rank)))
    
        # hold on to marriages for as long as possible
        if marriage_moves:
            return marriage_moves[0]
    
        # hold on to trumps for as long as possible
        if trumps:
            return trumps[0]

    def get_move(self, perspective: PlayerPerspective, leader_move: Move | None) -> Move:
        valid_regular_moves: list[RegularMove] = [move.as_regular_move() for move in perspective.valid_moves() if move.is_regular_move()]
        valid_moves: list[Move] = [move for move in perspective.valid_moves()]

        trump_suit: Suit = perspective.get_trump_suit()
        trumps: list[RegularMove] = [move for move in valid_regular_moves if move.card.suit == trump_suit]
        marriage_moves: list[Marriage] = [move.as_marriage() for move in perspective.valid_moves() if move.is_marriage()]

        high_value_ranks = [Rank.ACE, Rank.TEN]
        # low_value_ranks = [Rank.KING, Rank.QUEEN, Rank.JACK]

        high_value_moves: list[Move] = []
        low_value_moves: list[Move] = []
        for move in perspective.valid_moves():
            if move.is_regular_move():
                card = move.cards[0]
                if card.rank in high_value_ranks:
                    high_value_moves.append(move)
                # elif card.rank in low_value_ranks:
                #     low_value_moves.append(move)
            elif move.is_trump_exchange():
                high_value_moves.append(move)
            elif move.is_marriage():
                high_value_moves.append(move)

        if len(high_value_moves) / len(perspective.get_hand()) >= self.threshold: # lots of high-value cards - want to preserve them
            print(f"{len(high_value_moves) / len(perspective.get_hand())} >= {self.threshold}")
            self.defensive_moves += 1
            return self.defensive(valid_moves, trumps, trump_suit, marriage_moves)
        else: # lots of low-value cards - want to expend them
            self.aggressive_moves += 1
            return self.aggressive(valid_moves, trumps, trump_suit, marriage_moves)