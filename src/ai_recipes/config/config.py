import os
from enum import Enum

ROOT_PATH = os.path.dirname(os.path.abspath(".\\pec-iagen\\"))
class PATH(Enum):
    """
    Enum class to define the paths for different resources.
    """
    BOOKS = ROOT_PATH + "\\knowledge\\books\\"
    ARTICLES = ROOT_PATH + "\\knowledge\\articles\\"

is_verbose = True