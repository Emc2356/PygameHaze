__author__ = "emc235"
__version__ = "0.2.1"
__name__ = "PygameHelper"


# import the base classes
from PygameHelper.Classes import Button
from PygameHelper.Classes import SimpleText
from PygameHelper.Classes import MultiLineText
from PygameHelper.Classes import InputField
from PygameHelper.Classes import InputFieldNumbers
from PygameHelper.Classes import InputFieldLetters
from PygameHelper.Classes import Particle
from PygameHelper.Classes import Animation

# the managers for the widgets/tools
from PygameHelper.Classes import ButtonManager
from PygameHelper.Classes import TextManager
from PygameHelper.Classes import ParticleManager
from PygameHelper.Classes import AnimationManager
from PygameHelper.Classes import InputFieldManager

# classes files
from PygameHelper.Classes import animation
from PygameHelper.Classes import button
from PygameHelper.Classes import input_field
from PygameHelper.Classes import managers
from PygameHelper.Classes import particle
from PygameHelper.Classes import text

# general imports that can be used by the user with general use
# in their projects
from PygameHelper.constants import *
from PygameHelper.exceptions import *
from PygameHelper.utils import *

print(f"PygameHelper {__version__}")
