__author__ = "emc2356"
__version__ = "0.3.6"
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
from PygameHelper.Classes import SpriteSheet
from PygameHelper.Classes import Font
from PygameHelper.Classes import Cloth
from PygameHelper.Classes import Point
from PygameHelper.Classes import Connection
from PygameHelper.Classes import QuadTree
from PygameHelper.Classes import Vector

# the managers for some classes
from PygameHelper.Classes import ButtonManager
from PygameHelper.Classes import TextManager
from PygameHelper.Classes import ParticleManager
from PygameHelper.Classes import AnimationManager
from PygameHelper.Classes import InputFieldManager

# instances
from PygameHelper.Classes import noise

# classes files
from PygameHelper.Classes import animation
from PygameHelper.Classes import button
from PygameHelper.Classes import input_field
from PygameHelper.Classes import managers
from PygameHelper.Classes import particle
from PygameHelper.Classes import text
from PygameHelper.Classes import font
from PygameHelper.Classes import spritesheet
from PygameHelper.Classes import cloth
from PygameHelper.Classes import quadtree
from PygameHelper.Classes import vector

# general imports that can be used by the user with general use
# in their projects
from PygameHelper.exceptions import PygameHelperException as error
from PygameHelper.constants import *
from PygameHelper.utils import *
from PygameHelper.types import *

print(f"PygameHelper {__version__}")
