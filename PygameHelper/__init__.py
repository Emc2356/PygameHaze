"""
__________                                     ___ ___         .__
\______   \___.__. _________    _____   ____  /   |   \   ____ |  | ______   ___________
 |     ___<   |  |/ ___\__  \  /     \_/ __ \/    ~    \_/ __ \|  | \____ \_/ __ \_  __ \
 |    |    \___  / /_/  > __ \|  Y Y  \  ___/\    Y    /\  ___/|  |_|  |_> >  ___/|  | \/
 |____|    / ____\___  (____  /__|_|  /\___  >\___|_  /  \___  >____/   __/ \___  >__|
           \/   /_____/     \/      \/     \/       \/       \/     |__|        \/
"""


__author__ = "emc235"
__version__ = "0.1.1"


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
