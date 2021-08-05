__author__ = "emc235"
__version__ = "0.2.1"


# import the base classes
from .Classes import Button
from .Classes import SimpleText
from .Classes import MultiLineText
from .Classes import InputField
from .Classes import InputFieldNumbers
from .Classes import InputFieldLetters
from .Classes import Particle
from .Classes import Animation

# the managers for the widgets/tools
from .Classes import ButtonManager
from .Classes import TextManager
from .Classes import ParticleManager
from .Classes import AnimationManager

# general imports that can be used by the user with general use
# in their projects
from .constants import *
from .exceptions import *
from .utils import *

print(f"PygameHelper {__version__}")
