
""" A collection of commands
"""

import os
import json
import pint
import re
from colorama import Fore, Back, Style
from sympy import sympify
from sympy.solvers import solve


UNIT_REGISTRY = pint.UnitRegistry()
ERROR_TEMPLATE = (Fore.RED + '\n --- \n ' + Fore.LIGHTRED_EX + '{}\n {}\n\n' +
                  Fore.LIGHTGREEN_EX + ' {}' + Fore.RED + '\n ---\n' +
                  Fore.RESET)

def convertUnit(inputString):
    """ Converts the unit.
    """
    quantity, originalUnit, _, destinationUnit = inputString.split(' ')

    try:
        print(' {:,.2f}'.format(
            UNIT_REGISTRY.Quantity(
                int(quantity), originalUnit).to(destinationUnit)))

    except pint.errors.UndefinedUnitError:
        print(ERROR_TEMPLATE
              .format('Invalid Unit',
                      '"{}" contains invalid units',
                      'Please input units that are valid.')
              .format(inputString))

    except pint.errors.DimensionalityError:
        print(ERROR_TEMPLATE
              .format('Units In Different Category',
                      'The units "{}" and "{}" are not the same type',
                      'Please input units that are the same type')
              .format(originalUnit, destinationUnit))


def calculate(inputString):
    """ Calculates the input.
    """

    try:
        # Checks if the input string is an algebraic equation.
        if re.search(r'=', inputString):

            # The sympy solvers only accepts equation that equals to "zero".
            # Thats why the "equal" sign is replaced with the "minus" sign.
            equation = sympify(inputString.replace(' = ', ' - '))

            result = solve(equation, list(equation.free_symbols)[0])[0]
        else:
            result = sympify(inputString)

        print(' {:,.2f}'.format(int(result)))
    except TypeError:
        print(ERROR_TEMPLATE.format('Division by Zero',
                                    'You can\'t divide by zero.',
                                    'Remove the number 0'))
    except (SyntaxError, IndexError):
        print(ERROR_TEMPLATE.format('Invalid Syntax',
                                    '"{}" contains invalid syntax.'.
                                    format(inputString),
                                    'Use a correct syntax.'))


def openFile(inputString):
    """ Opens a file or folder.
    """
    _, bookmarkName = inputString.split(' ')

    try:
        os.system('start "" "' + FILE_BOOKMARKS[bookmarkName] + '"')
    except KeyError:
        print(ERROR_TEMPLATE.format(
            'Bookmark Doesn\'t Exist',
            'The bookmark "{}" doesn\'t exist.'.format(bookmarkName),
            'You can add the bookmark in the "bookmark.json"'
            ))


def readFile(path):
    fileObject = open(path, "r")
    fileContent = fileObject.read()
    fileObject.close()
    return fileContent


FILE_BOOKMARKS = json.loads(readFile('bookmarks.json'))
