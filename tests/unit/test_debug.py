import pytest
import src.lib.debug


_MSG_HDR_CUSTOM_ = 'Test Header'
_MSG_HDR_DEFAULT_ = ' [DEBUG'

_TEXT_STRING_ = 'This is just a test!'

_DATA_SET_ = [1,2,'three',5,4]
_DATA_SET_AS_PP_STRING_ = "[1, 2, 'three', 5, 4]"

# NOTE: PP seems to sort DICT output in alphanum order
_DATA_DICT_ = {'one':1, 'two':2, 'three':3, 'four':4, 'five':5}
_DATA_DICT_AS_PP_STRING_ = "{'five': 5, 'four': 4, 'one': 1, 'three': 3, 'two': 2}"


def test_debug_msg_missing_required():
    with pytest.raises(TypeError) as excinfo:
        src.lib.debug.debug_msg()
        
    exMsg = excinfo.value.args[0]
    assert exMsg == "debug_msg() missing 1 required positional argument: 'data'"    
    

def test_debug_msg_w_data(capsys):
    expectedHdr = _MSG_HDR_DEFAULT_ + '] '
    
    src.lib.debug.debug_msg(_TEXT_STRING_)
    out, err = capsys.readouterr()
    assert expectedHdr in out
    assert _TEXT_STRING_ in out
    assert err == ''
    
    src.lib.debug.debug_msg(_DATA_SET_)
    out, err = capsys.readouterr()
    assert expectedHdr in out
    assert _DATA_SET_AS_PP_STRING_ in out
    assert err == ''

    src.lib.debug.debug_msg(_DATA_DICT_)
    out, err = capsys.readouterr()
    assert expectedHdr in out
    assert _DATA_DICT_AS_PP_STRING_ in out
    assert err == ''
    
    
def test_debug_msg_w_custom_header(capsys):
    expectedHdr = _MSG_HDR_DEFAULT_ + src.lib.debug._SPACER_ + _MSG_HDR_CUSTOM_ + '] '
    
    src.lib.debug.debug_msg(_DATA_SET_, _MSG_HDR_CUSTOM_)
    out, err = capsys.readouterr()
    assert expectedHdr in out
    assert _DATA_SET_AS_PP_STRING_ in out
    assert err == ''

    
def test_debug_msg_w_custom_message(capsys):
    expectedHdr = _MSG_HDR_DEFAULT_ + src.lib.debug._SPACER_ + _MSG_HDR_CUSTOM_ + '] '
    
    src.lib.debug.debug_msg(_DATA_SET_, _MSG_HDR_CUSTOM_, _TEXT_STRING_)
    out, err = capsys.readouterr()
    assert expectedHdr in out
    assert _DATA_SET_AS_PP_STRING_ in out
    assert _TEXT_STRING_ in out
    assert err == ''
