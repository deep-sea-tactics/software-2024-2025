import types

def args_list_to_string(inp: list[str]):
    res: str = ""

    for string in inp:
        res += string
        res += ' '
    
    return res

def print_args_list_as_string(inp: list[str]):
    print(args_list_to_string(inp))

class Delegate:
    """
    Adds delegation functionality to Python
    """

    def __init__(self, connected: list[types.FunctionType] = []):
        self.connected: list[types.FunctionType] = connected

    def call(self, args: list[str] = []):
        """
        Call all the functions connected to this delegate
        """
        res = 0

        for function in self.connected:
            func_result = function(args)

            if func_result == 0:
                continue
            
            res = func_result
        
        return res
    
    def connect(self, function: types.FunctionType):
        """
        Connect a function to this delegate.

        Note that the function must follow the format

        `func(args: list[str]) -> int`
        """

        self.connected.append(function)
    
    def mass_connect(self, functions: list[types.FunctionType]):
        """
        Connect functions to this delegate en masse
        """

        for function in functions:
            self.connect(function)

    def disconnect(self, function: types.FunctionType) -> int:
        """
        Disconnect a function, if it has already been connected

        0: Successful disconnect
        1: ValueError
        """

        try:
            self.connected.remove(function)
            return 0
        except ValueError:
            return 1

class Command:
    def __init__(self, functions: list[types.FunctionType], keyword: str, description: str):
        self.keyword = keyword
        self.description = description
        self.delegate = Delegate(functions)

    def attempt_interpret(self, inp: str):
        """
        (Inefficiently) Attempt to run this command, given a string input by the user

        2: Command errored
        1: Failed to interpret
        0: Command successful
        """

        words = inp.split()

        if words[0].lower() != self.keyword.lower():
            return 1
        
        del words[0] # The first token is not an argument, it's an identifier
        
        res = self.delegate.call(words)
        
        # This is stupid
        if res != 0:
            return 2
    
    def help(self):
        print(self.description)