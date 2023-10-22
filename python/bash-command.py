from enum import Enum
from typing import Union, Optional


class WordDescFlag(Enum):
    W_HASDOLLAR = 1 << 0          # dollar sign present
    W_QUOTED = 1 << 1             # some form of quote character is present
    W_ASSIGNMENT = 1 << 2        # this word is a variable assignment
    W_SPLITSPACE = 1 << 3        # split this word on " " regardless of IFS
    # do not perform word splitting on this word because IFS is empty string
    W_NOSPLIT = 1 << 4
    W_NOGLOB = 1 << 5            # do not perform globbing on this word
    # don't split word except for $@ expansion (using spaces) because context does not allow it
    W_NOSPLIT2 = 1 << 6
    W_TILDEEXP = 1 << 7          # tilde expand this assignment word
    W_DOLLARAT = 1 << 8          # UNUSED - $@ and its special handling
    W_ARRAYREF = 1 << 9          # word is a valid array reference
    W_NOCOMSUB = 1 << 10         # don't perform command substitution on this word
    W_ASSIGNRHS = 1 << 11        # word is rhs of an assignment statement
    W_NOTILDE = 1 << 12          # don't perform tilde expansion on this word
    W_NOASSNTILDE = 1 << 13      # don't do tilde expansion like an assignment statement
    W_EXPANDRHS = 1 << 14        # expanding word in ${paramOPword}
    W_COMPASSIGN = 1 << 15       # compound assignment
    W_ASSNBLTIN = 1 << 16        # word is a builtin command that takes assignments
    W_ASSIGNARG = 1 << 17        # word is assignment argument to command
    W_HASQUOTEDNULL = 1 << 18    # word contains a quoted null character
    W_DQUOTE = 1 << 19           # UNUSED - word should be treated as if double-quoted
    W_NOPROCSUB = 1 << 20        # don't perform process substitution
    W_SAWQUOTEDNULL = 1 << 21    # word contained a quoted null that was removed
    W_ASSIGNASSOC = 1 << 22      # word looks like associative array assignment
    W_ASSIGNARRAY = 1 << 23      # word looks like a compound indexed array assignment
    W_ARRAYIND = 1 << 24         # word is an array index being expanded
    # word is a global assignment to declare (declare/typeset -g)
    W_ASSNGLOBAL = 1 << 25
    W_NOBRACE = 1 << 26          # don't perform brace expansion
    W_COMPLETE = 1 << 27         # word is being expanded for completion
    W_CHKLOCAL = 1 << 28         # check for local vars on assignment
    # force assignments to be to local variables, non-fatal on assignment errors
    W_FORCELOCAL = 1 << 29

    def to_json(self) -> str:
        if self == WordDescFlag.W_HASDOLLAR:
            return "has_dollar"
        elif self == WordDescFlag.W_QUOTED:
            return "quoted"
        elif self == WordDescFlag.W_ASSIGNMENT:
            return "assignment"
        elif self == WordDescFlag.W_SPLITSPACE:
            return "split_space"
        elif self == WordDescFlag.W_NOSPLIT:
            return "no_split"
        elif self == WordDescFlag.W_NOGLOB:
            return "no_glob"
        elif self == WordDescFlag.W_NOSPLIT2:
            return "no_split2"
        elif self == WordDescFlag.W_TILDEEXP:
            return "tilde_exp"
        elif self == WordDescFlag.W_DOLLARAT:
            return "dollar_at"
        elif self == WordDescFlag.W_ARRAYREF:
            return "array_ref"
        elif self == WordDescFlag.W_NOCOMSUB:
            return "no_comsub"
        elif self == WordDescFlag.W_ASSIGNRHS:
            return "assign_rhs"
        elif self == WordDescFlag.W_NOTILDE:
            return "no_tilde"
        elif self == WordDescFlag.W_NOASSNTILDE:
            return "no_assign_tilde"
        elif self == WordDescFlag.W_EXPANDRHS:
            return "expand_rhs"
        elif self == WordDescFlag.W_COMPASSIGN:
            return "comp_assign"
        elif self == WordDescFlag.W_ASSNBLTIN:
            return "assign_builtin"
        elif self == WordDescFlag.W_ASSIGNARG:
            return "assign_arg"
        elif self == WordDescFlag.W_HASQUOTEDNULL:
            return "has_quoted_null"
        elif self == WordDescFlag.W_DQUOTE:
            return "dquote"
        elif self == WordDescFlag.W_NOPROCSUB:
            return "no_procsub"
        elif self == WordDescFlag.W_SAWQUOTEDNULL:
            return "saw_quoted_null"
        elif self == WordDescFlag.W_ASSIGNASSOC:
            return "assign_assoc"
        elif self == WordDescFlag.W_ASSIGNARRAY:
            return "assign_array"
        elif self == WordDescFlag.W_ARRAYIND:
            return "array_index"
        elif self == WordDescFlag.W_ASSNGLOBAL:
            return "assign_global"
        elif self == WordDescFlag.W_NOBRACE:
            return "no_brace"
        elif self == WordDescFlag.W_COMPLETE:
            return "complete"
        elif self == WordDescFlag.W_CHKLOCAL:
            return "check_local"
        elif self == WordDescFlag.W_FORCELOCAL:
            return "force_local"
        else:
            raise Exception('invalid word description flag')


class WordDesc:
    word: str
    flags: list[WordDescFlag]

    def __init__(self, word: str, flags: int):
        self.word = word
        self.flags = flags

    def to_json(self) -> dict[str, Union(int, str)]:
        return {
            'word': self.word,
            'flags': [x.to_json() for x in self.flags]
        }


class RedirecteeUnion:
    # use only if R_DUPLICATING_INPUT or R_DUPLICATING_OUTPUT
    dest: Optional[int]
    # use otherwise
    word: Optional[WordDesc]

    def __init__(self, dest: Optional[int], word: Optional[WordDesc]):
        self.dest = dest
        self.word = word

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        if self.dest is not None:
            return {
                'dest': self.dest
            }
        elif self.word is not None:
            return {
                'word': self.word.to_json()
            }
        else:
            raise Exception('invalid redirectee')


class CommandFlag(Enum):
    """
    represents command flags present in several command types
    """
    CMD_WANT_SUBSHELL = 1 << 0  # user wants subshell
    CMD_FORCE_SUBSHELL = 1 << 1  # shell needs to force subshell
    CMD_INVERT_RETURN = 1 << 2  # invert the exit value
    CMD_IGNORE_RETURN = 1 << 3  # ignore the exit value
    CMD_NO_FUNCTIONS = 1 << 4  # ignore functions during command lookup
    CMD_INHIBIT_EXPANSION = 1 << 5  # do not expand command words
    CMD_NO_FORK = 1 << 6  # do not fork, just call execv
    CMD_TIME_PIPELINE = 1 << 7  # time the pipeline
    CMD_TIME_POSIX = 1 << 8  # time -p was specified
    CMD_AMPERSAND = 1 << 9  # command &
    CMD_STDIN_REDIRECTED = 1 << 10  # async command needs implicit </dev/null
    CMD_COMMAND_BUILTIN = 1 << 11  # command executed by 'command' builtin
    CMD_COPROC_SHELL = 1 << 12  # coprocess shell
    CMD_LASTPIPE = 1 << 13  # last command in pipeline
    CMD_STD_PATH = 1 << 14  # use default PATH for command lookup
    CMD_TRY_OPTIMIZING = 1 << 15  # try to optimize simple command

    def to_json(self) -> str:
        if self == CommandFlag.CMD_WANT_SUBSHELL:
            return "want_subshell"
        elif self == CommandFlag.CMD_FORCE_SUBSHELL:
            return "force_subshell"
        elif self == CommandFlag.CMD_INVERT_RETURN:
            return "invert_return"
        elif self == CommandFlag.CMD_IGNORE_RETURN:
            return "ignore_return"
        elif self == CommandFlag.CMD_NO_FUNCTIONS:
            return "no_functions"
        elif self == CommandFlag.CMD_INHIBIT_EXPANSION:
            return "inhibit_expansion"
        elif self == CommandFlag.CMD_NO_FORK:
            return "no_fork"
        elif self == CommandFlag.CMD_TIME_PIPELINE:
            return "time_pipeline"
        elif self == CommandFlag.CMD_TIME_POSIX:
            return "time_posix"
        elif self == CommandFlag.CMD_AMPERSAND:
            return "ampersand"
        elif self == CommandFlag.CMD_STDIN_REDIRECTED:
            return "stdin_redirected"
        elif self == CommandFlag.CMD_COMMAND_BUILTIN:
            return "command_builtin"
        elif self == CommandFlag.CMD_COPROC_SHELL:
            return "coproc_shell"
        elif self == CommandFlag.CMD_LASTPIPE:
            return "last_pipe"
        elif self == CommandFlag.CMD_STD_PATH:
            return "std_path"
        elif self == CommandFlag.CMD_TRY_OPTIMIZING:
            return "try_optimizing"
        else:
            raise Exception('invalid command flag')


class CommandType(Enum):
    """
    a command type enum
    """
    CM_FOR = 0  # for loop
    CM_CASE = 1  # switch case
    CM_WHILE = 2  # while loop
    CM_IF = 3  # if statement
    CM_SELECT = 4  # select statement
    CM_SIMPLE = 5  # simple command
    CM_CONNECTION = 6  # probably connectors like &,||, &&, ;
    CM_FUNCTION_DEF = 7  # function definition
    CM_UNTIL = 8  # until loop
    CM_GROUP = 9  # probably a command grouping via { } or ( )
    CM_ARITH = 10  # arithmetic expression, probably using $(( ))
    CM_COND = 11  # conditional expression, probably using [[ ]]
    CM_ARITH_FOR = 12  # probably for loop using (( ))
    CM_SUBSHELL = 13  # subshell via ( )
    CM_COPROC = 14  # coprocess

    def to_json(self) -> dict[str, str]:
        if self == CommandType.CM_FOR:
            return "for"
        elif self == CommandType.CM_CASE:
            return "case"
        elif self == CommandType.CM_WHILE:
            return "while"
        elif self == CommandType.CM_IF:
            return "if"
        elif self == CommandType.CM_SELECT:
            return "select"
        elif self == CommandType.CM_SIMPLE:
            return "simple"
        elif self == CommandType.CM_CONNECTION:
            return "connection"
        elif self == CommandType.CM_FUNCTION_DEF:
            return "function_def"
        elif self == CommandType.CM_UNTIL:
            return "until"
        elif self == CommandType.CM_GROUP:
            return "group"
        elif self == CommandType.CM_ARITH:
            return "arithmetic"
        elif self == CommandType.CM_COND:
            return "conditional"
        elif self == CommandType.CM_ARITH_FOR:
            return "arithmetic_for"
        elif self == CommandType.CM_SUBSHELL:
            return "subshell"
        elif self == CommandType.CM_COPROC:
            return "coproc"
        else:
            raise Exception('invalid command type')


class RInstruction(Enum):
    """
    a redirection instruction enum
    """
    R_OUTPUT_DIRECTION = 0  # >foo
    R_INPUT_DIRECTION = 1  # <foo
    R_INPUTA_DIRECTION = 2  # foo & makes this
    R_APPENDING_TO = 3  # >>foo
    R_READING_UNTIL = 4  # << foo
    R_READING_STRING = 5  # <<< foo
    R_DUPLICATING_INPUT = 6  # 1<&2
    R_DUPLICATING_OUTPUT = 7  # 1>&2
    R_DEBLANK_READING_UNTIL = 8  # <<-foo
    R_CLOSE_THIS = 9  # <&-
    R_ERR_AND_OUT = 10  # command &>filename
    R_INPUT_OUTPUT = 11  # <>foo
    R_OUTPUT_FORCE = 12  # >| foo
    R_DUPLICATING_INPUT_WORD = 13  # 1<&$foo
    R_DUPLICATING_OUTPUT_WORD = 14  # 1>&$foo
    R_MOVE_INPUT = 15  # 1<&2-
    R_MOVE_OUTPUT = 16  # 1>&2-
    R_MOVE_INPUT_WORD = 17  # 1<&$foo-
    R_MOVE_OUTPUT_WORD = 18  # 1>&$foo-
    R_APPEND_ERR_AND_OUT = 19  # &>> filename

    # converts redirection type actual bash redirection string
    def to_json(self) -> str:
        if self == RInstruction.R_OUTPUT_DIRECTION:
            return '>'
        elif self == RInstruction.R_INPUT_DIRECTION:
            return '<'
        elif self == RInstruction.R_INPUTA_DIRECTION:
            return '&'  # ?
        elif self == RInstruction.R_APPENDING_TO:
            return '>>'
        elif self == RInstruction.R_READING_UNTIL:
            return '<<'
        elif self == RInstruction.R_READING_STRING:
            return '<<<'
        elif self == RInstruction.R_DUPLICATING_INPUT:
            return '<&'
        elif self == RInstruction.R_DUPLICATING_OUTPUT:
            return '>&'
        elif self == RInstruction.R_DEBLANK_READING_UNTIL:
            return '<<-'
        elif self == RInstruction.R_CLOSE_THIS:
            return '<&-'
        elif self == RInstruction.R_ERR_AND_OUT:
            return '&>'
        elif self == RInstruction.R_INPUT_OUTPUT:
            return '<>'
        elif self == RInstruction.R_OUTPUT_FORCE:
            return '>|'
        elif self == RInstruction.R_DUPLICATING_INPUT_WORD:
            return '<&$'  # todo figure out if $ is needed
        elif self == RInstruction.R_DUPLICATING_OUTPUT_WORD:
            return '>&$'  # todo figure out if $ is needed
        elif self == RInstruction.R_MOVE_INPUT:
            return '<&-'
        elif self == RInstruction.R_MOVE_OUTPUT:
            return '>&-'
        elif self == RInstruction.R_MOVE_INPUT_WORD:
            return '<&$-'  # todo figure out if $ is needed
        elif self == RInstruction.R_MOVE_OUTPUT_WORD:
            return '>&$-'  # todo figure out if $ is needed
        elif self == RInstruction.R_APPEND_ERR_AND_OUT:
            return '&>>'
        else:
            raise Exception('invalid redirect instruction')


class CondTypeEnum(Enum):
    """
    a conditional expression type enum
    """
    COND_AND = 0
    COND_OR = 1
    COND_UNARY = 2
    COND_BINARY = 3
    COND_TERM = 4
    COND_EXPR = 5

    def to_json(self) -> str:
        if self == CondTypeEnum.COND_AND:
            return 'and'
        elif self == CondTypeEnum.COND_OR:
            return 'or'
        elif self == CondTypeEnum.COND_UNARY:
            return 'unary'
        elif self == CondTypeEnum.COND_BINARY:
            return 'binary'
        elif self == CondTypeEnum.COND_TERM:
            return 'term'
        elif self == CondTypeEnum.COND_EXPR:
            return 'expression'


class Redirect:
    """
    describes a redirection such as >, >>, <, <<
    """
    redirector: RedirecteeUnion  # the thing being redirected
    rflags: int  # not sure what this is
    flags: int  # flag value for open?
    instruction: RInstruction  # the type of redirection
    redirectee: RedirecteeUnion  # the thing being redirected to
    here_doc_eof: str  # the word that appeared in the << operator?

    def __init__(
            self,
            redirector: RedirecteeUnion,
            rflags: int,
            flags: int,
            instruction: RInstruction,
            redirectee: RedirecteeUnion,
            here_doc_eof: str):
        self.redirector = redirector
        self.rflags = rflags
        self.flags = flags
        self.instruction = instruction
        self.redirectee = redirectee
        self.here_doc_eof = here_doc_eof

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'redirector': self.redirector.to_json(),
            'rflags': self.rflags,
            'flags': self.flags,
            'instruction': self.instruction.to_json(),
            'redirectee': self.redirectee.to_json(),
            'here_doc_eof': self.here_doc_eof
        }


class ForCom:
    """
    a for command class
    """
    flags: int  # command flags
    line: int  # line number the command is on?
    name: WordDesc  # the variable name to get mapped over?
    map_list: list[WordDesc]  # the list of words to map over
    action: list['Command']  # the action to take for each word in the map list

    def __init__(
            self,
            flags: int,
            line: int,
            name: WordDesc,
            map_list: list[WordDesc],
            action: list['Command']):
        self.flags = flags
        self.line = line
        self.name = name
        self.map_list = map_list
        self.action = action

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'for',
            'flags': self.flags,
            'line': self.line,
            'name': self.name.to_json(),
            'map_list': [x.to_json() for x in self.map_list],
            'action': [x.to_json() for x in self.action]
        }


class Pattern:
    """
    represents a pattern in a case command
    """
    patterns: list[WordDesc]  # the list of patterns to match against
    action: 'Command'  # the action to take if the pattern matches
    flags: int  # not sure what flag type this is

    def __init__(self, patterns: list[WordDesc], action: 'Command', flags: int):
        self.patterns = patterns
        self.action = action
        self.flags = flags

    def to_json(self) -> dict[str, Union(int, dict, list)]:
        return {
            'patterns': [x.to_json() for x in self.patterns],
            'action': self.action.to_json(),
            'flags': self.flags
        }


class CaseCom:
    """
    a case command class
    """
    flags: int  # command flags
    line: int  # line number the command is on?
    word: WordDesc  # the thing to match against
    clauses: list[Pattern]  # the list of patterns to match against

    def __init__(self, flags: int, line: int, word: WordDesc, clauses: list[Pattern]):
        self.flags = flags
        self.line = line
        self.word = word
        self.clauses = clauses

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'case',
            'flags': self.flags,
            'line': self.line,
            'word': self.word.to_json(),
            'clauses': [x.to_json() for x in self.clauses]
        }


class WhileCom:
    """
    a while command class
    """
    flags: int  # command flags
    test: 'Command'  # the thing to test
    action: 'Command'  # the action to take while the test is true

    def __init__(self, flags: int, test: 'Command', action: 'Command'):
        self.flags = flags
        self.test = test
        self.action = action

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'while',
            'flags': self.flags,
            'test': self.test.to_json(),
            'action': self.action.to_json()
        }


class IfCom:
    """
    an if command class
    """
    flags: int  # command flags
    test: 'Command'  # the thing to test
    true_case: 'Command'  # the action to take if the test is true
    false_case: 'Command'  # the action to take if the test is false

    def __init__(self, flags: int, test: 'Command', true_case: 'Command', false_case: 'Command'):
        self.flags = flags
        self.test = test
        self.true_case = true_case
        self.false_case = false_case

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'if',
            'flags': self.flags,
            'test': self.test.to_json(),
            'true_case': self.true_case.to_json(),
            'false_case': self.false_case.to_json()
        }


class Connection:
    """
    represents connections
    """
    ignore: int  # unused but keep for consistency
    first: 'Command'  # the first command to run
    second: 'Command'  # the second command to run
    connector: int  # the connector to use?

    def __init__(self, ignore: int, first: 'Command', second: 'Command', connector: int):
        self.ignore = ignore
        self.first = first
        self.second = second
        self.connector = connector

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'connection',
            'first': self.first.to_json(),
            'second': self.second.to_json(),
            'connector': self.connector  # todo: figure out what this int means
        }


class SimpleCom:
    """
    a simple command class
    """
    flags: int  # command flags
    line: int  # line number the command is on
    words: list[WordDesc]  # program name, arguments, variable assignments, etc
    redirects: list[Redirect]  # redirections

    def __init__(self, flags: int, line: int, words: list[WordDesc], redirects: list[Redirect]):
        self.flags = flags
        self.line = line
        self.words = words
        self.redirects = redirects

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'simple',
            'flags': self.flags,
            'line': self.line,
            'words': [x.to_json() for x in self.words],
            'redirects': [x.to_json() for x in self.redirects]
        }


class FunctionDef:
    """
    for function definitions
    """
    flags: int  # command flags
    line: int  # line number the command is on
    name: WordDesc  # the name of the function
    command: 'Command'  # the execution tree for the function
    source_file: Optional[str]  # the file the function was defined in, if any

    def __init__(self, flags: int, line: int, name: WordDesc, command: 'Command', source_file: Optional[str]):
        self.flags = flags
        self.line = line
        self.name = name
        self.command = command
        self.source_file = source_file

    def to_json(self) -> dict[str, Union(int, str, dict, None)]:
        return {
            'type': 'function_def',
            'flags': self.flags,
            'line': self.line,
            'name': self.name.to_json(),
            'command': self.command.to_json(),
            'source_file': self.source_file if self.source_file is not None else None
        }


class GroupCom:
    """
    group commands allow pipes and redirections to be applied to a group of commands
    """
    ignore: int  # is this used?
    command: 'Command'  # the command to run

    def __init__(self, ignore: int, command: 'Command'):
        self.ignore = ignore
        self.command = command

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'group',
            'command': self.command.to_json()
        }


class SelectCom:
    """
    the select command is like a for loop but with a menu
    """
    flags: int  # command flags
    line: int  # line number the command is on
    name: WordDesc  # the name of the variable?
    map_list: list[WordDesc]  # the list of words to map over
    action: 'Command'  # the action to take for each word in the map list, during execution name is bound to member of map_list

    def __init__(self, flags: int, line: int, name: WordDesc, map_list: list[WordDesc], action: 'Command'):
        self.flags = flags
        self.line = line
        self.name = name
        self.map_list = map_list
        self.action = action

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'select',
            'flags': self.flags,
            'line': self.line,
            'name': self.name.to_json(),
            'map_list': [x.to_json() for x in self.map_list],
            'action': self.action.to_json()
        }


class ArithCom:
    """
    arithmetic expression ((...))
    """
    flags: int  # not sure what flag type this is
    line: int  # line number the command is on
    exp: WordDesc  # the expression to evaluate

    def __init__(self, flags: int, line: int, exp: WordDesc):
        self.flags = flags
        self.line = line
        self.exp = exp

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'arithmetic',
            'flags': self.flags,
            'line': self.line,
            'exp': self.exp.to_json()
        }


class CondCom:
    """
    conditional expression [[...]]
    """
    flags: int  # unclear flag type
    line: int  # line number the command is on
    type: CondTypeEnum  # the type of conditional expression
    op: WordDesc  # unclear
    left: Optional['CondCom']  # the left side of the expression
    right: Optional['CondCom']  # the right side of the expression

    def __init__(
            self,
            flags: int,
            line: int,
            type: CondTypeEnum,
            op: WordDesc,
            left: Optional['Command'],
            right: Optional['Command']):
        self.flags = flags
        self.line = line
        self.type = type
        self.op = op
        self.left = left
        self.right = right

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'conditional',
            'flags': self.flags,
            'line': self.line,
            'cond_type': self.type.to_json(),
            'op': self.op.to_json(),
            'left': self.left.to_json() if self.left is not None else None,
            'right': self.right.to_json() if self.right is not None else None
        }


class ArithForCom:
    """
    a c-style for loop ((init; test; step)) action
    """
    flags: int  # unclear flag type
    line: int  # line number the command is on
    init: list[WordDesc]  # the initial values of the variables
    test: list[WordDesc]  # the test to perform
    step: list[WordDesc]  # the step to take
    action: 'Command'  # the action to take for each iteration

    def __init__(
            self,
            flags: int,
            line: int,
            init: list[WordDesc],
            test: list[WordDesc],
            step: list[WordDesc],
            action: 'Command'):
        self.flags = flags
        self.line = line
        self.init = init
        self.test = test
        self.step = step
        self.action = action

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': 'arithmetic_for',
            'flags': self.flags,
            'line': self.line,
            'init': [x.to_json() for x in self.init],
            'test': [x.to_json() for x in self.test],
            'step': [x.to_json() for x in self.step],
            'action': self.action.to_json()
        }

    def to_bash(self) -> str:
        """
        Converts the arithmetic for command to its Bash representation.
        """
        init = ""
        test = ""
        step = ""

        for word in self.init:
            init += word.word + ", "

        if len(init) > 0:
            init = init[:-2]

        for word in self.test:
            test += word.word + ", "

        if len(test) > 0:
            test = test[:-2]

        for word in self.step:
            step += word.word + ", "

        if len(step) > 0:
            step = step[:-2]

        return f"for (( {init}; {test}; {step})); do {self.action.to_bash()}; done"


class SubshellCom:
    """
    a subshell command
    """
    flags: int  # unclear flag type
    line: int  # line number the command is on
    command: 'Command'  # the command to run in the subshell

    def __init__(self, flags: int, line: int, command: 'Command'):
        self.flags = flags
        self.line = line
        self.command = command

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'subshell',
            'flags': self.flags,
            'line': self.line,
            'command': self.command.to_json()
        }

    def to_bash(self) -> str:
        """
        Converts the subshell command to its Bash representation.
        """
        return f"({self.command.to_bash()})"


class CoprocCom:
    """
    a coprocess command
    """
    flags: int  # unclear flag type
    name: WordDesc  # the name of the coprocess
    command: 'Command'  # the command to run in the coprocess

    def __init__(self, flags: int, name: WordDesc, command: 'Command'):
        self.flags = flags
        self.name = name
        self.command = command

    def to_json(self) -> dict[str, Union(int, str, dict)]:
        return {
            'type': 'coproc',
            'flags': self.flags,
            'name': self.name.to_json(),
            'command': self.command.to_json()
        }

    def to_bash(self) -> str:
        """
        Converts the coprocess command to its Bash representation.
        """
        return f"coproc {self.name.word} {self.command.to_bash()}"


class ValueUnion:
    """
    a union of all the possible command types
    exactly one of these will be non-null
    """
    for_com: Optional[ForCom]
    case_com: Optional[CaseCom]
    while_com: Optional[WhileCom]
    if_com: Optional[IfCom]
    connection: Optional[Connection]
    simple_com: Optional[SimpleCom]
    function_def: Optional[FunctionDef]
    group_com: Optional[GroupCom]
    select_com: Optional[SelectCom]
    arith_com: Optional[ArithCom]
    cond_com: Optional[CondCom]
    arith_for_com: Optional[ArithForCom]
    subshell_com: Optional[SubshellCom]
    coproc_com: Optional[CoprocCom]

    def __init__(
        self,
        command_type: CommandType,
        command: Union[
            ForCom,
            CaseCom,
            WhileCom,
            IfCom,
            Connection,
            SimpleCom,
            FunctionDef,
            GroupCom,
            SelectCom,
            ArithCom,
            CondCom,
            ArithForCom,
            SubshellCom,
            CoprocCom]):
        self.for_com = None
        self.case_com = None
        self.while_com = None
        self.if_com = None
        self.connection = None
        self.simple_com = None
        self.function_def = None
        self.group_com = None
        self.select_com = None
        self.arith_com = None
        self.cond_com = None
        self.arith_for_com = None
        self.subshell_com = None
        self.coproc_com = None

        if command_type == CommandType.CM_FOR:
            self.for_com = command
        elif command_type == CommandType.CM_CASE:
            self.case_com = command
        elif command_type == CommandType.CM_WHILE:
            self.while_com = command
        elif command_type == CommandType.CM_IF:
            self.if_com = command
        elif command_type == CommandType.CM_CONNECTION:
            self.connection = command
        elif command_type == CommandType.CM_SIMPLE:
            self.simple_com = command
        elif command_type == CommandType.CM_FUNCTION_DEF:
            self.function_def = command
        elif command_type == CommandType.CM_GROUP:
            self.group_com = command
        elif command_type == CommandType.CM_SELECT:
            self.select_com = command
        elif command_type == CommandType.CM_ARITH:
            self.arith_com = command
        elif command_type == CommandType.CM_COND:
            self.cond_com = command
        elif command_type == CommandType.CM_ARITH_FOR:
            self.arith_for_com = command
        elif command_type == CommandType.CM_SUBSHELL:
            self.subshell_com = command
        elif command_type == CommandType.CM_COPROC:
            self.coproc_com = command
        else:
            raise Exception('Unknown command type provided.')

    def to_json(self) -> dict[str, dict]:
        if self.for_com is not None:
            return self.for_com.to_json()
        elif self.case_com is not None:
            return self.case_com.to_json()
        elif self.while_com is not None:
            return self.while_com.to_json()
        elif self.if_com is not None:
            return self.if_com.to_json()
        elif self.connection is not None:
            return self.connection.to_json()
        elif self.simple_com is not None:
            return self.simple_com.to_json()
        elif self.function_def is not None:
            return self.function_def.to_json()
        elif self.group_com is not None:
            return self.group_com.to_json()
        elif self.select_com is not None:
            return self.select_com.to_json()
        elif self.arith_com is not None:
            return self.arith_com.to_json()
        elif self.cond_com is not None:
            return self.cond_com.to_json()
        elif self.arith_for_com is not None:
            return self.arith_for_com.to_json()
        elif self.subshell_com is not None:
            return self.subshell_com.to_json()
        elif self.coproc_com is not None:
            return self.coproc_com.to_json()
        else:
            raise Exception('invalid value union')


class Command:
    """
    a mirror of the bash command struct defined here:
    https://git.savannah.gnu.org/cgit/bash.git/tree/command.h
    """
    type: CommandType  # command type
    flags: int  # command flags
    line: int  # line number the command is on
    redirects: list[Redirect]
    value: ValueUnion

    def to_json(self) -> dict[str, Union(int, str, dict, list)]:
        return {
            'type': self.type.to_json(),
            'flags': self.flags,
            'line': self.line,
            'redirects': [x.to_json() for x in self.redirects],
            'value': self.value.to_json()
        }

    def command_to_bash(self) -> str:
        """
        Recursively converts the command to its Bash representation.
        """
        bash_script = ""

        # First, handle the command type
        if self.type == CommandType.CM_FOR:
            bash_script += self.value.for_com.to_bash()
        elif self.type == CommandType.CM_CASE:
            bash_script += self.value.case_com.to_bash()
        elif self.type == CommandType.CM_WHILE:
            bash_script += self.value.while_com.to_bash()
        elif self.type == CommandType.CM_IF:
            bash_script += self.value.if_com.to_bash()
        elif self.type == CommandType.CM_CONNECTION:
            bash_script += self.value.connection.to_bash()
        elif self.type == CommandType.CM_SIMPLE:
            bash_script += self.value.simple_com.to_bash()
        elif self.type == CommandType.CM_FUNCTION_DEF:
            bash_script += self.value.function_def.to_bash()
        elif self.type == CommandType.CM_GROUP:
            bash_script += self.value.group_com.to_bash()
        elif self.type == CommandType.CM_SELECT:
            bash_script += self.value.select_com.to_bash()
        elif self.type == CommandType.CM_ARITH:
            bash_script += self.value.arith_com.to_bash()
        elif self.type == CommandType.CM_COND:
            bash_script += self.value.cond_com.to_bash()
        elif self.type == CommandType.CM_ARITH_FOR:
            bash_script += self.value.arith_for_com.to_bash()
        elif self.type == CommandType.CM_SUBSHELL:
            bash_script += self.value.subshell_com.to_bash()
        elif self.type == CommandType.CM_COPROC:
            bash_script += self.value.coproc_com.to_bash()
        else:
            raise Exception('Unknown command type encountered.')

        # Then, handle the redirects
        bash_script += " "
        for redirect in self.redirects:
            bash_script += redirect.to_bash() + " "

        return bash_script
