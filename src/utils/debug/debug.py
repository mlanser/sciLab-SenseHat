import pprint

_MAXLEN_: int = 80
_LINE_CHAR_: str = '-'
_SPACER_: str = ' | '


def debug_msg(data, hdr=None, msg=None):
    divhdr = ' [DEBUG' + ((_SPACER_ + hdr + '] ') if hdr is not None else '] ')

    divmax = max(_MAXLEN_, len(divhdr))
    divline = ''.join([_LINE_CHAR_ * divmax])

    prefix = ''.join([_LINE_CHAR_ * int((divmax - len(divhdr)) / 2)])
    suffix = prefix + (_LINE_CHAR_ if len(divhdr) % 2 else '')

    print('\n{}{}{}'.format(prefix, divhdr, suffix))

    if msg is not None:
        print(msg)
        print('{}'.format(divline))

    _PP_ = pprint.PrettyPrinter(indent=4)
    _PP_.pprint(data)

    print('{}\n'.format(divline))
