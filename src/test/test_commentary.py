from src.main.python.commentary.commentator import getComment

def test_getCommentReturnsNonEmptyString():
    assert len(getComment(None,0)) > 0