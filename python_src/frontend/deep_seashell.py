"""
Contained within this file is the primary interface
"""

import utils

class Func:
    """
    Contains the functionality for each command.

    Each function requires the type: func(args: list[str]) -> int
    """
    pass

class Define:
    """
    Functions for command defining; actually binds functionality to words and arguments
    """
    pass

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

    loaded_commands: list[utils.Command]

    def should_ignore(cmd: str):
        formatted = cmd.strip()
        identifier = formatted[0]

        if identifier != Key.COMMENT_IDENTIFIER:
            return False
        
        return True
    
    def run_command(cmd: str):
        """
        The underlying interpretation command. This will run the command; however, it
        does no error handling.

        This *will* run commands directly, but `interpret_error_catch` should be used
        when possible.
        """
        res = 0

        for command in Interpret.loaded_commands:
            command_res = command.attempt_interpret(cmd)

            if command_res == 2:
                res = 1
        
        return res
    
    def error(msg: str, line: int):
        if line > -1:
            print("Error on line", line)
        
        print(msg)

    def interpret_error_catch(cmd: str, line: int = -1):
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

            