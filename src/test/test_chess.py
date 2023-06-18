from src.main.python.chess.game_rules import GameRules

def test_positionInBound():
    assert GameRules.is_in_bounds((0,0)) == True
    assert GameRules.is_in_bounds((0,11)) == False
    
def test_parsingTuple():
    assert GameRules.parse_tuple_position((0,0)) == "a8"
    
def test_parsingString():
    assert GameRules.parse_str_position("a8") == (0,0)
    
    
# cd chess_game
# python -m pytest src/test/