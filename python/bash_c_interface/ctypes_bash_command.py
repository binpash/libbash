from ctypes import *


class word_desc(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n131
    """
    _fields_ = [
        ("word", c_char_p),
        ("flags", c_int)
    ]


class REDIRECTEE(Union):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n154
    """
    _fields_ = [
        ("dest", c_int),
        ("filename", POINTER(word_desc))
    ]


class redirect(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n161
    """
    _fields_ = [
        ("next", POINTER('redirect')),
        ("redirector", REDIRECTEE),
        ("rflags", c_int),
        ("flags", c_int),
        ("instruction", c_int),
        ("redirectee", REDIRECTEE),
        ("here_doc_eof", c_char_p)
    ]


class word_list(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n137
    """
    _fields_ = [
        ("next", POINTER('word_list')),
        ("word", POINTER(word_desc))
    ]


class for_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n259
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("name", POINTER(word_desc)),
        ("map_list", POINTER(word_list)),
        ("action", POINTER('command'))
    ]


class pattern_list(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n243
    """
    _fields_ = [
        ("next", POINTER('pattern_list')),
        ("patterns", POINTER(word_list)),
        ("action", POINTER('command')),
        ("flags", c_int)
    ]


class case_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n251
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("word", POINTER(word_desc)),
        ("clauses", POINTER(pattern_list))
    ]


class while_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n302
    """
    _fields_ = [
        ("flags", c_int),
        ("test", POINTER('command')),
        ("action", POINTER('command'))
    ]


class if_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n294
    """
    _fields_ = [
        ("flags", c_int),
        ("test", POINTER('command')),
        ("true_case", POINTER('command')),
        ("false_case", POINTER('command'))
    ]


class connection(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n229
    """
    _fields_ = [
        ("ignore", c_int),
        ("first", POINTER('command')),
        ("second", POINTER('command')),
        ("connector", c_int)
    ]


class simple_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n337
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("words", POINTER(word_list)),
        ("redirects", POINTER(redirect))
    ]


class function_def(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n346
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("name", POINTER(word_desc)),
        ("command", POINTER('command')),
        ("source_file", c_char_p)
    ]


class group_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n356
    """
    _fields_ = [
        ("ignore", c_int),
        ("command", POINTER('command'))
    ]


class select_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n282
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("name", POINTER(word_desc)),
        ("map_list", POINTER(word_list)),
        ("action", POINTER('command'))
    ]


class arith_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n364
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("exp", POINTER(word_list))
    ]


class cond_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n328
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("type", c_int),
        ("op", POINTER(word_desc)),
        ("left", POINTER('cond_com')),
        ("right", POINTER('cond_com')),
    ]


class arith_for_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n270
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("init", POINTER(word_list)),
        ("test", POINTER(word_list)),
        ("step", POINTER(word_list)),
        ("action", POINTER('command'))
    ]


class subshell_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n361
    """
    _fields_ = [
        ("flags", c_int),
        ("line", c_int),
        ("command", POINTER('command'))
    ]


class coproc_com(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n382
    """
    _fields_ = [
        ("flags", c_int),
        ("name", c_char_p),
        ("command", POINTER('command'))
    ]


class value(Union):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n202
    """
    _fields_ = [
        ("For", POINTER(for_com)),
        ("Case", POINTER(case_com)),
        ("While", POINTER(while_com)),
        ("If", POINTER(if_com)),
        ("Connection", POINTER(connection)),
        ("Simple", POINTER(simple_com)),
        ("Function_def", POINTER(function_def)),
        ("Group", POINTER(group_com)),
        ("Select", POINTER(select_com)),
        ("Arith", POINTER(arith_com)),
        ("Cond", POINTER(cond_com)),
        ("ArithFor", POINTER(arith_for_com)),
        ("Subshell", POINTER(subshell_com)),
        ("Coproc", POINTER(coproc_com)),
    ]


class command(Structure):
    """
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h#n197
    """
    _fields_ = [
        ("type", c_int),
        ("flags", c_int),
        ("line", c_int),
        ("redirects", POINTER(redirect))
        ("value", value)
    ]
