"""
Contained within this file is the primary interface
"""

import utils
import types

loaded_commands: list[utils.Command] = [] # Contains every command currently defined
current_environment = None

class Func:
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

    def _tag_toggle_singline(args: list[str]) -> int:
        global current_environment




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
    
    def _dss_cmd_first_pass():
        Define.define(
            Func._new_alias,
            "alias",
            """
            Defines a new alias.

            Arguments: <name> <value>
            """
        )

    def _dss_cmd_second_pass():
        Define.define(
            Func._debug_out,
            "out",
            """
            Returns its argument back to the standard out
            
            Arguments: <message>
            """
        )

        Define.define(
            Func._del_alias,
            "del_alias",
            """
            Deletes an alias, if it exists.

            Arguments: <alias>
            """
        )

        Define.define(
            Func._del_all_aliases,
            "delall",
            """
            Deletes every alias in the env.

            Arguments: None
            """
        )

class Key:
    """
    Contains various constants
    """

    MULTILINE_DELIM = "\n"
    SINGLE_DELIM = ";"

    COMMENT_IDENTIFIER = "#"
    DEREF = "$"

    ERROR_COMMAND_FAILED_TO_INTERPRET = "Execution failure: internal command error"
    ERROR_INVALID_DELETION = "Execution failure: invalid deletion. Unknown alias: %s"
    WARNING_FLOATING_ALIAS = "Warning: alias \"%s\" is floating (never accessed)"

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
        
        print(msg)
    
    def _warn(msg: str, line: int = 0):
        if line > 0:
            print("Warning on line", line)
        
        print(msg)

    def _interpret_error_catch(cmd: str, line: int = 0):
        """
        Attempts to run `cmd`, and will output errors if present.

        This is how commands should be run
        """
        formatted = cmd.strip()
        command_res = Interpret._run_command(formatted)

        if command_res == 1:
            Interpret._error(Key.ERROR_COMMAND_FAILED_TO_INTERPRET, line)

    def _script_interpret(inp: str, delim: str = Key.MULTILINE_DELIM):
        """
        Handles multiple lines of Deep Seashell script.
        """

        lines = inp.split(delim)

        line_num = 0
        for line in lines:
            line_num += 1
            if Interpret._should_ignore(line) == True:
                continue
            
            Interpret._interpret_error_catch(line, line_num)

    def source(path: str):
        global loaded_commands

        try:
            file = open(path, "r")
            read = file.read()

            loaded_commands.clear()
            
            Define._dss_cmd_first_pass()
            Interpret._script_interpret(read)

            loaded_commands.clear()

            read = current_environment._reformat_script(read)

            Define._dss_cmd_second_pass()
            Interpret._script_interpret(read)
        except FileExistsError:
            return #Muahahahahahahahah

def init():
    global current_environment
    current_environment = Environment()

if __name__ == "__main__":
    init()
    Interpret.source("test.dss")
    Interpret.source("additional_test.dss")