import src.main


def test_action_one_w_1_arg():
    """'action_one' should return 'foo'."""
    expected = src.main.action_one('foo')
    assert 'foo' == expected


def test_action_one_w_2_args():
    """'action_one' should return 'bar'."""
    expected = src.main.action_one('foo', 'bar')
    assert 'bar' == expected

    
def test_action_two_w_2_args():
    """'action_two' should return 5."""
    expected = src.main.action_two(2, 3)
    assert 5 == expected
    