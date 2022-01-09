__author__ = "emc2356"
__version__ = "0.3.6"
__name__ = "PygameHazel"


# import the base classes
from PygameHazel.Classes import Button
from PygameHazel.Classes import InputField
from PygameHazel.Classes import InputFieldNumbers
from PygameHazel.Classes import InputFieldLetters
from PygameHazel.Classes import Particle
from PygameHazel.Classes import Animation
from PygameHazel.Classes import SpriteSheet
from PygameHazel.Classes import Font
from PygameHazel.Classes import Cloth
from PygameHazel.Classes import Point
from PygameHazel.Classes import Connection
from PygameHazel.Classes import QuadTree

# the managers for some classes
from PygameHazel.Classes import ButtonManager
from PygameHazel.Classes import ParticleManager
from PygameHazel.Classes import AnimationManager
from PygameHazel.Classes import InputFieldManager


# constants and functions that are useful with PygameHazel
from PygameHazel.exceptions import PygameHazelException as error
from PygameHazel.constants import *
from PygameHazel.utils import *
from PygameHazel.types import *

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

        from PygameHazel.utils.formulas import build_numba_formulas
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

        from PygameHazel.utils.draw import build_draw_numba
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


print(f"PygameHazel {__version__}")

del sys
