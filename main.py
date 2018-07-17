
""" Main script.
"""

import sys
import os
import re

from colorama import Fore, Back, Style
import commands


COMMAND_REGEX_MAPPING = [
    {   # Example strings: "17 km to cm","21 C to F", "ffffff hex to bin",
        # 21 km/s to m/s".
        'regex': r'[\w]+\s[\w,/]+\sto+\s[\w,/]+',
        'action': commands.convertUnit
    },
    {   # Example strings: "1 + 2, "1 + b = 3", "a + 1 = 3".
        'regex': r'[+\-\*\/=]\s?[\d\w]+',
        'action': commands.calculate
    },
    {
        'regex': r'f \w+',
        'action': commands.openFile
    }
]


class Assistant():
    """Assistant class"""

    def __init__(self):
        print(Style.RESET_ALL)  # Needed in order for colorama to work.

    def requestInput(self, text=' ' + Fore.LIGHTRED_EX + '> ' + Fore.RESET):
        """ Prompts the user for input.
        """
        userResponse = input(text)
        return userResponse

    def ask(self):
        """ Requests the input, and processes it.
        """
        self.process(self.requestInput())

    def process(self, commandString):
        """ Processes the command string.
        """
        for x in COMMAND_REGEX_MAPPING:
            if re.search(x['regex'], commandString):
                x['action'](commandString)
                break

    def clear(self):
        """ Clears the terminal.
        """
        os.system('cls')

    def setTitle(self, title):
        """ Sets the title for the terminal.
        """
        os.system('title ' + title)

    def greet(self):
        """ Prints the greeting message.
        """
        print('\n {}Hello, I\'m {}Japa{}.\n Ready to help.\n'
              .format(Fore.LIGHTGREEN_EX,
                      Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX))


def start(firstCommand=''):
    """ Starts the assistant.
    """
    assistant = Assistant()
    assistant.clear()
    assistant.setTitle('JAPA (Just A Personal Assistant) - By Lutfi')
    assistant.greet()

    if firstCommand:
        print(' ' + Fore.LIGHTRED_EX + '> ' + Fore.RESET + firstCommand)
        assistant.process(firstCommand)
        print('')

    while True:
        assistant.ask()
        print('')


if len(sys.argv) > 1:
    sys.argv.pop(0)
    start(' '.join(sys.argv))
else:
    start()
