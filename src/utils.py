from textwrap import wrap
import builtins
from pefile import PE, PEFormatError


def is_pe(data):
    try:
        pe = PE(data=data)
        if pe.is_exe():
            return 'exe'
        elif pe.is_dll():
            return 'dll'
    except PEFormatError:
        return None


def _print_body(*args):
    label, prob, ext, fname = args[:4]

    fname_len = fname.__len__()
    if fname_len > 24:
        fname = "{}...{}".format(fname[:13], fname[-8:])
    elif fname_len < 24:
        fname = fname.center(24)
    out = "    │ [{0}] {1:1.3f}  {2} {3} │".format(label, prob, ext, fname)
    builtins.print(out)


def _print_top():
    builtins.print("    ┌"+"─"*47+"┐")


def _print_bottom():
    builtins.print("    └"+"─"*47+"┘")


def _print_msg(*args):
    lines = wrap(args[0], width=45)
    _print_top()
    for line in lines:
        builtins.print("    │", line.ljust(45), "│")
    _print_bottom()


def print(*args, fmt=None):
    if not fmt:
        builtins.print(*args)
        return

    if fmt == 'body':
        return _print_body(*args)

    if fmt == 'msg':
        return _print_msg(*args)

    if fmt == 'top':
        return _print_top()

    if fmt == 'bottom':
        return _print_bottom()
