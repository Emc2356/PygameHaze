__author__ = "emc2356"
__version__ = "0.3.6"
__name__ = "PygameHaze"


# import the base classes
from PygameHaze.Classes import Button
from PygameHaze.Classes import InputField
from PygameHaze.Classes import InputFieldNumbers
from PygameHaze.Classes import InputFieldLetters
from PygameHaze.Classes import Particle
from PygameHaze.Classes import Animation
from PygameHaze.Classes import SpriteSheet
from PygameHaze.Classes import Font
from PygameHaze.Classes import Cloth
from PygameHaze.Classes import Point
from PygameHaze.Classes import Connection
from PygameHaze.Classes import QuadTree

# the managers for some classes
from PygameHaze.Classes import ButtonManager
from PygameHaze.Classes import ParticleManager


# constants and functions that are useful with PygameHaze
from PygameHaze.exceptions import PygameHazeException as error
from PygameHaze.constants import *
from PygameHaze.utils import *
from PygameHaze.types import *

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

        from PygameHaze.utils.formulas import build_numba_formulas
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

        from PygameHaze.utils.draw import build_draw_numba
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


print(f"PygameHaze {__version__}")

del sys
