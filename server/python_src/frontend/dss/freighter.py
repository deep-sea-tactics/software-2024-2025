import os
import shutil
import deep_seashell as dss

NAVIGATE_DELIM = "/"
PACKAGES_DIR = "packages"
NAMESPACE = "freighter::"

def path_to_list(path: str) -> list[str]:
    return path.split(NAVIGATE_DELIM)

def format_dir_str(path: list[str]) -> str:
    res: str = ""
    
    for dir in path:
        if dir == "":
            continue

        res += dir
        res += NAVIGATE_DELIM
    
    res = res.removesuffix(NAVIGATE_DELIM)

    return res

def mkdir_if_nonexistent(path: str):
    if os.path.exists(path) == True:
        return
    
    if path == "":
        return
    
    os.mkdir(path)

def mkdir_R(full_path: list[str]):
    rdir: str = ""
    
    for dir in full_path:
        mkdir_if_nonexistent(rdir)
        rdir += dir
        rdir += NAVIGATE_DELIM
    
    mkdir_if_nonexistent(rdir)


def setup_packaging_system():
    mkdir_if_nonexistent(PACKAGES_DIR)

class File:
    """
    Reference to a file object.

    `filename` determines the actual name of the file (includes extension)

    `source` refers to the directory path of the file (for any dependencies). Not including the file.
    """

    def __init__(self, filename: str = "", source: list[str] = []):
        self.filename = filename
        self.source = source
    
    def from_relative_path(path: str):
        """
        An ideal way to initialize a `File` object
        """

        file = File()

        directories = path.split(NAVIGATE_DELIM)
        
        file.filename = directories.pop()
        file.source = directories

        return file
    
    def get_abs_relative_path(self):
        return format_dir_str(self.source) + NAVIGATE_DELIM + self.filename

class Key:
    SWN = "freighter:"
    MESSAGE_ADDED = SWN + " added %s to package \"%s\""
    MESSAGE_BUILDING = SWN + " building package \"%s\""
    MESSAGE_FINISHED = SWN + " finished building package \"%s\""
    MESSAGE_CLEARING = SWN + " clearing existing package \"%s\""

class Package:
    """
    A package containing code.

    `include` is a list of all the files in the package

    `name` is the name of the package
    """

    def __init__(self, name: str, include: list[File] = []):
        self.name = name
        self.include = include
    
    def add_file(self, path: str):
        new_file = File.from_relative_path(path)
        self.include.append(new_file)
    
    def dir(self) -> str:
        return format_dir_str([PACKAGES_DIR, self.name])

    def build(self):
        if os.path.exists(self.dir()):
            print(Key.MESSAGE_CLEARING % (self.name))
            shutil.rmtree(self.dir())
        
        mkdir_if_nonexistent(self.dir())
        print(Key.MESSAGE_BUILDING % (self.name))

        for file in self.include:
            filepath = format_dir_str([self.dir(), format_dir_str(file.source)])
            mkdir_R(path_to_list(filepath))
            
            print(Key.MESSAGE_ADDED % (file.get_abs_relative_path(), self.name))

            open(os.path.abspath(filepath) + NAVIGATE_DELIM + file.filename, "w+")
            shutil.copyfile(
                file.get_abs_relative_path(), 
                filepath + NAVIGATE_DELIM + file.filename
            )
        
        print(Key.MESSAGE_FINISHED % (self.name))

class DSS:
    loaded_packages: list[Package] = []

    def _find_package(pckg_name: str) -> Package | None:
        for pckg in DSS.loaded_packages:
            if pckg.name != pckg_name:
                continue

            return pckg
    
    def cmd_package(args: list[str]):
        MIN_ARGS = 1
        if len(args) < MIN_ARGS: return 1

        DSS.loaded_packages.append(Package(args[0]))
        return 0
    
    def cmd_package_add_file(args: list[str]):
        MIN_ARGS = 2
        if len(args) < MIN_ARGS: return 1

        package = DSS._find_package(args[0])
        if package == None: return 1

        package.add_file(args[1])

        return 0
    
    def cmd_package_build(args: list[str]):
        MIN_ARGS = 1
        if len(args) < MIN_ARGS: return 1

        package = DSS._find_package(args[0])
        if package == None: return 1

        package.build()

        return 0
    
    def define_all():
        dss.Define.define(
            DSS.cmd_package,
            NAMESPACE + "pckgdef",
            """
            Creates a freighter package

            Arguments: <name>
            """
        )

        dss.Define.define(
            DSS.cmd_package_add_file,
            NAMESPACE + "pckgfile",
            """
            Adds a file to the package

            Arguments: <name> <relative_file_path>
            """
        )

        dss.Define.define(
            DSS.cmd_package_build,
            NAMESPACE + "pckgbuild",
            """
            Builds the package

            Arguments: <name>
            """
        )

dss.Define.additional_second_pass_commands.connect(DSS.define_all)

if __name__ == "__main__":
    setup_packaging_system()

    pckg = Package("test")
    pckg.add_file("server/python_src/backend/networking/tx.py")
    pckg.build()
