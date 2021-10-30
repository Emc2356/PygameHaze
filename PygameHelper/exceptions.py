# MIT License
#
# Copyright (c) 2021 Emc2356
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
exceptions for PygameHelper
"""


class PygameHelperException(Exception):
    """
    the base exception for the rest of the exception
    that are used for this package
    """
    def __init__(self, message: str):
        self.message = str(message)
        if not message.endswith("."):
            self.message += "."
        super().__init__(message)

    def __str__(self):
        return str(self.message)

    def __repr__(self):
        return repr(self.message)


class TextOfOutBounds(PygameHelperException):
    """
    the exception that is raised when the
    text that is passed is out of the given
    bounds.
    """
    pass


class InvalidAnchor(PygameHelperException):
    """
    the exception that is raised when the
    user provides a invalid anchor for a widget.
    """
    pass


class MissingRequiredArgument(PygameHelperException):
    """
    this exception is raised when a method is
    missing a required argument.
    """
    pass


class WordTooLong(PygameHelperException):
    """
    this is the exception that is going to be raised
    when the word to be splitted to multi-line text
    is too long and wont fit
    """
    pass


class NoLockedPoints(PygameHelperException):
    """
    this is the exception that is going to be raised
    when a cloth has no points that are locked so
    it will just drop until who knows how much
    """
    pass


class NoConnection(PygameHelperException):
    """
    this exception is going to be raised
    when a point in a cloth has no connection
    with another point
    """


class Notimplemented(PygameHelperException):
    """
    this exception exists cause the creator of
    PygameHelper is too board to implement
    a full thing then update it
    """


class ShapeError(PygameHelperException):
    """
    this exception is raised when an
    error from the user or from the inner code
    occurs
    """


class NoLocationFound(PygameHelperException):
    """
    this exception is raised when the user tries
    to pop a location with PygameHelper.utils.draw.Draw.pop
    and ne hasn't pushed any yet
    """


class UnrecognisedCharacter(PygameHelperException):
    """
    this exception is raised when in the Font.render
    was passed a character that is not recognised
    """


__all__ = [
    "TextOfOutBounds",
    "InvalidAnchor",
    "MissingRequiredArgument",
    "WordTooLong",
    "NoLockedPoints",
    "NoConnection",
    "Notimplemented",
    "ShapeError",
    "NoLocationFound",
    "UnrecognisedCharacter"
]
