"""
Contained within this file is the primary interface
"""

import frontend.dss.utils as utils
import types
import os

class Tag: pass # See future definition

loaded_commands: list[utils.Command] = [] # Contains every command currently defined
loaded_tags: list[Tag] = []
current_environment = None

class DefaultCmd:
    """
    Contains the functionality for each command.

    Each function requires the type: func(args: list[str]) -> int
    """

    def _debug_out(args: list[str]) -> int:
        """
        Outputs to the console
        """
        utils.print_args_list_as_string(args)

        return 0
    
    def _new_alias(args: list[str]) -> int:
        global current_environment
        
        MIN_ARGS = 1
        if len(args) < MIN_ARGS: return 1
        
        additional_args = args.copy()
        del(additional_args[0])
        s_additional_args = utils.args_list_to_string(additional_args)

        current_environment._new_alias(Alias(args[0], s_additional_args))

        return 0

    def _del_alias(args: list[str]) -> int:
        global current_environment
        
        MIN_ARGS = 1
        if len(args) < MIN_ARGS: return 1

        current_environment._delete_alias(args[0])

        return 0
    
    def _del_all_aliases(args: list[str]) -> int:
        global current_environment

        if len(args) > 0: return 1

        current_environment._delete_all_aliases()
        
        return 0

    def _source(args: list[str]) -> int:
        MIN_ARGS = 1
        if len(args) < MIN_ARGS: return 1

        Interpret.source(args[0])

    def _tag_toggle_singleline(_args: list[str]) -> int:
        global current_environment
        
        current_environment.current_script_delim = Key.SINGLE_DELIM

        return 0

class Define:
    """
    Functions for command defining; actually binds functionality to words and arguments

    Note: use the define function, which requires a function that:
    accepts a list[str] as its sole argument
    returns an integer as a status of the command
    """

    def define(fn: types.FunctionType, keyword: str, description: str):
        """
        Each function requires the type: func(args: list[str]) -> int

        Returns an integer as a result of running the command
        """
        global loaded_commands

        new_command: utils.Command = utils.Command([fn], keyword, description)
        loaded_commands.append(new_command)

    def define_tag(fn: types.FunctionType, keyword: str, description: str):
        """
        Tags are fancy commands for modifying program variables.
        They are computed first before any other part of the DSS program.
        """
        global loaded_tags
        loaded_tags.append(Tag(Key.TAG_IDENTIFIER + keyword, utils.Delegate([fn])))

    def _dss_cmd_all_tags():
        Define.define_tag(
            DefaultCmd._tag_toggle_singleline,
            "singleline",
            """
            Toggles singleline and changes the delimiter used by the
            interpreter.

            Note: This is enabled by default when using a string stream
            """
        )
    
    additional_first_pass_commands: utils.Delegate = utils.Delegate([])
    def _dss_cmd_first_pass():
        Define.additional_first_pass_commands.call()

        Define.define(
            DefaultCmd._new_alias,
            "alias",
            """
            Defines a new alias.

            Arguments: <name> <value>
            """
        )

    additional_second_pass_commands: utils.Delegate = utils.Delegate([])
    def _dss_cmd_second_pass():
        Define.additional_second_pass_commands.call()

        Define.define(
            DefaultCmd._debug_out,
            "out",
            """
            Returns its argument back to the standard out
            
            Arguments: <message>
            """
        )

        Define.define(
            DefaultCmd._del_alias,
            "del_alias",
            """
            Deletes an alias, if it exists.

            Arguments: <alias>
            """
        )

        Define.define(
            DefaultCmd._del_all_aliases,
            "delall",
            """
            Deletes every alias in the env.

            Arguments: None
            """
        )

        Define.define(
            DefaultCmd._source,
            "src",
            """
            Run a DSS script.

            Arguments: <cwd relative path>
            """
        )
    
    def _define_all():
        Define._dss_cmd_first_pass()
        Define._dss_cmd_second_pass()
        Define._dss_cmd_all_tags()

class Key:
    """
    Contains various constants
    """

    MULTILINE_DELIM = "\n"
    SINGLE_DELIM = ";"

    DEFAULT_DELIM = MULTILINE_DELIM

    COMMENT_IDENTIFIER = "#"
    DEREF = "$"

    TAG_IDENTIFIER = "!#"

    ERROR = "error: %s"
    WARNING = "warning: %s"

    ERROR_COMMAND_FAILED_TO_INTERPRET = "internal command error"
    ERROR_INVALID_DELETION = "invalid deletion. Unknown alias: %s"
    ERROR_SCRIPT_NOT_FOUND = "(file-io) non-existent script (%s)"
    WARNING_FLOATING_ALIAS = "alias \"%s\" is floating (never accessed)"

    EXIT = "exit"
    HELP = "help"

    CMD_LINE = "dss$ "

class Tag:
    def __init__(self, key: str, delegate: utils.Delegate):
        self.key = key
        self.delegate = delegate

class Alias:
    """
    An alias is a constant variable that gets placed into the script wherever seen.
    """

    def __init__(self, key: str, value: str):
        self.key: str = key
        self.value: str = value

class Environment:
    """
    Stores variables and whatnot.
    """

    def __init__(self):
        self.aliases: list[Alias] = []
        self.current_script_delim = Key.MULTILINE_DELIM

    def _find_alias(self, key: str):
        for alias in self.aliases:
            if alias.key != key:
                continue
            
            return alias

        return None
    
    def _reformat_script(self, script: str):
        for alias in self.aliases:
            deref = (Key.DEREF + alias.key).strip()

            if (deref in script) == False:
                Interpret._warn(Key.WARNING_FLOATING_ALIAS % alias.key)
                continue

            script = script.replace(deref, str(alias.value))
        
        return script
    
    def _new_alias(self, alias: Alias):
        self.aliases.append(alias)
    
    def _delete_alias(self, alias_key: str):
        found = self._find_alias(alias_key)

        if found == None:
            Interpret._error(Key.ERROR_INVALID_DELETION % alias_key)
            return
        
        self.aliases.remove(found)
    
    def _delete_all_aliases(self):
        self.aliases.clear()

class Interpret:
    """
    Pipeline for the interpretation of commands
    """

    def _handle_tags(inp: str):
        global loaded_tags

        for tag in loaded_tags:
            if (tag.key in inp) == False:
                continue
            
            tag.delegate.call()

    def _should_ignore(cmd: str):
        formatted = cmd.strip()
        
        if formatted == '':
            return True

        identifier = formatted[0]

        if identifier != Key.COMMENT_IDENTIFIER:
            return False
        
        return True
    
    def _run_command(cmd: str):
        """
        The underlying interpretation command. This will run the command; however, it
        does no error handling.

        This *will* run commands directly, but `interpret_error_catch` should be used
        when possible.
        """
        global loaded_commands
        res = 0

        for command in loaded_commands:
            command_res = command.attempt_interpret(cmd)

            if command_res == 2:
                res = 1
        
        return res
    
    def _error(msg: str, line: int = 0):
        if line > 0:
            print("Error on line", line)
        
        print(Key.ERROR % msg)
    
    def _warn(msg: str, line: int = 0):
        if line > 0:
            print("Warning on line", line)
        
        print(Key.WARNING % msg)

    def _interpret_error_catch(cmd: str, line: int = 0):
        """
        Attempts to run `cmd`, and will output errors if present.

        This is how commands should be run
        """
        formatted = cmd.strip()
        command_res = Interpret._run_command(formatted)

        if command_res == 1:
            Interpret._error(Key.ERROR_COMMAND_FAILED_TO_INTERPRET, line)

    def _interpret_script(inp: str, delim: str = None):
        """
        Runs Deep Sea Shell script.
        """
        global current_environment

        lines = inp.split(delim or current_environment.current_script_delim)

        line_num = 0
        for line in lines:
            line_num += 1
            if Interpret._should_ignore(line) == True:
                continue
            
            Interpret._interpret_error_catch(line, line_num)

    def _cmd_pass(func: types.FunctionType, read: str):
        global loaded_commands

        loaded_commands.clear()
        func()

        Interpret._interpret_script(read)

    def run(inp: str):
        Define._dss_cmd_all_tags()
        Interpret._handle_tags(inp)

        Interpret._cmd_pass(Define._dss_cmd_first_pass, inp)
        inp = current_environment._reformat_script(inp)

        Interpret._cmd_pass(Define._dss_cmd_second_pass, inp)

        current_environment.current_script_delim = Key.DEFAULT_DELIM

    def source(path: str):
        """
        Run a DSS script

        `path` specifies the location of the file
        """

        global loaded_commands

        try:
            file = open(path, "r")
            read = file.read()
            
            Interpret.run(read)

        except FileNotFoundError:
            Interpret._error(Key.ERROR_SCRIPT_NOT_FOUND % path)
    
    def _input_loop():
        global loaded_commands

        while True:
            try:
                user_input = input(Key.CMD_LINE)

                if user_input == Key.EXIT: break
                if user_input == Key.HELP:
                    Define._define_all()
                    for cmd in loaded_commands:
                        cmd.help()

                current_environment.current_script_delim = Key.SINGLE_DELIM
                Interpret.run(user_input)
            except KeyboardInterrupt:
                break

def is_initialized():
    return (current_environment != None)

def init():
    global current_environment
    current_environment = Environment()

if __name__ == "__main__":
    init()
    #Interpret._input_loop()