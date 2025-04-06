"""
Contained within this file is the primary interface
"""

import utils
import types

loaded_commands: list[utils.Command] = [] # Contains every command currently defined

class Func:
    """
    Contains the functionality for each command.

    Each function requires the type: func(args: list[str]) -> int
    """
    def debug_out(args: list[str]) -> int:
        print("DebugOut")
        utils.print_list_as_string(args)

class Define:
    """
    Functions for command defining; actually binds functionality to words and arguments
    """

    def define(fn: types.FunctionType, keyword: str, description: str):
        new_command: utils.Command = utils.Command([fn], keyword, description)
        Interpret.loaded_commands.append(new_command)
    
    def define_all():
        Define.define(
            Func.debug_out,
            "out",
            """
            Returns its argument back to the standard out
            
            Arguments: <message>
            """
        )

class Key:
    """
    Contains various constants
    """

    COMMENT_IDENTIFIER = ";"

    ERROR_COMMAND_FAILED_TO_INTERPRET = "Command failed to interpret: internal command error"

class Interpret:
    """
    Pipeline for the interpretation of commands
    """

    def should_ignore(cmd: str):
        formatted = cmd.strip()
        identifier = formatted[0]

        if identifier != Key.COMMENT_IDENTIFIER:
            return False
        
        return True
    
    def run_command(cmd: str):
        global loaded_commands

        """
        The underlying interpretation command. This will run the command; however, it
        does no error handling.

        This *will* run commands directly, but `interpret_error_catch` should be used
        when possible.
        """
        res = 0

        for command in loaded_commands:
            command_res = command.attempt_interpret(cmd)

            if command_res == 2:
                res = 1
        
        return res
    
    def error(msg: str, line: int):
        if line > 0:
            print("Error on line", line)
        
        print(msg)

    def interpret_error_catch(cmd: str, line: int = 0):
        """
        Attempts to run `cmd`, and will output errors if present.

        This is how commands should be run
        """
        formatted = cmd.strip()
        command_res = Interpret.run_command(formatted)

        if command_res == 1:
            Interpret.error(Key.ERROR_COMMAND_FAILED_TO_INTERPRET, line)

    def script_interpret(inp: str):
        """
        Handles multiple lines of Deep Seashell script.
        """

        lines = inp.splitlines()

        line_num = 0
        for line in lines:
            line_num += 1
            if Interpret.should_ignore(line) == True:
                continue
            
            Interpret.interpret_error_catch(line, line_num)

if __name__ == "__main__":
    file = open("test.dss", "r")

    Interpret.script_interpret(file.read())