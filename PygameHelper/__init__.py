__author__ = "emc2356"
__version__ = "0.3.6"
__name__ = "PygameHelper"


# import the base classes
from PygameHelper.Classes import Button
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

# the managers for some classes
from PygameHelper.Classes import ButtonManager
from PygameHelper.Classes import ParticleManager
from PygameHelper.Classes import AnimationManager
from PygameHelper.Classes import InputFieldManager


# constants and functions that are useful with PygameHelper
from PygameHelper.exceptions import PygameHelperException as error
from PygameHelper.constants import *
from PygameHelper.utils import *
from PygameHelper.types import *

import sys


def init(debug: bool=False) -> int:
    """
    it initializes all of the optional modules
    :return: int
    """
    failed = 0

    if debug:
        try:
            import numba
            del numba
        except ImportError:
            debug = False
            print(f"[DEBUG] numba was no found so no module will be built")

    try:
        import numpy as np
    except ImportError:
        print("failed to import numpy, maybe it isn't installed?", file=sys.stderr)
        raise

    try:
        if debug:
            print("[DEBUG] building noise module")
        noise.init()
        if debug:
            print("[DEBUG] successfully built the perlin noise module")
    except Exception:
        failed += 1
        if debug:
            print("[DEBUG] failed to build the perlin noise module")
            import traceback
            print(traceback.format_exc(), file=sys.stderr)
    try:
        if debug:
            print("[DEBUG] building the formulas")

        from PygameHelper.utils.formulas import build_numba_formulas
        build_numba_formulas()

        if debug:
            print("[DEBUG] successfully built the formula module")
    except Exception:
        if debug:
            print("[DEBUG] failed to initialize the formula module", file=sys.stderr)
            import traceback
            print(traceback.format_exc(), file=sys.stderr)
        failed += 1

    try:
        if debug:
            print("[DEBUG] building the draw functions")

        from PygameHelper.utils.draw import build_draw_numba
        build_draw_numba()

        if debug:
            print("[DEBUG] successfully built the draw functions")
    except Exception:
        if debug:
            print("[DEBUG] failed to pre-build the draw functions", file=sys.stderr)
            import traceback
            print(traceback.format_exc(), file=sys.stderr)
        failed += 1

    return failed


print(f"PygameHelper {__version__}")

del sys
