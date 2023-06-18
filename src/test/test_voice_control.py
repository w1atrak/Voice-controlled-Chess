from src.main.python.voice_control.s_recognition import stringNumbersToNumbers, cutSpaces

def test_stringNumbersToNumbers():
    assert stringNumbersToNumbers("jeden jeden trzy") == "1 1 3"
    
    
def test_stringNumbersToNumbers_noNumbers():
    assert stringNumbersToNumbers("hello world") == "hello world"
    
    
def test_cutSpaces():
    assert cutSpaces("2a a 2 2 a b 3 ") == "a2 a2 a2 b3 "