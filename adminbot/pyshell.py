#!/usr/bin/env python3

import sys
from code import InteractiveConsole
import codecs


class FileCacher:
    """Object with a file-like API storing text which is returned when flushing"""

    def __init__(self):
        self.out = []

    def reset(self):
        self.out = []

    def write(self, line):
        self.out.append(line)

    def flush(self):
        output = '\n'.join(self.out)
        self.reset()
        return output


class CatchOutput:
    """Context manager to catch the output"""

    def __init__(self, cache):
        self.cache = cache

    def __enter__(self):
        self.stdout = sys.stdout
        sys.stdout = self.cache

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.stdout
        return False  # Do not suppress exceptions


class Shell(InteractiveConsole):
    """Wrapper around Python that can filter input/output to the shell"""

    def __init__(self, echo=False, escaped_input=True):
        self.cache = FileCacher()
        self.echo = echo
        self.escaped_input = escaped_input
        InteractiveConsole.__init__(self)
        return

    def write(self, data):
        # Always write to our buffer
        self.cache.write(data)

    # Display added error messages
    def showsyntaxerror(self, filename=None):
        self.write("Syntax Error!")
        InteractiveConsole.showsyntaxerror(self)

    def showtraceback(self):
        self.write("Error occured!")
        InteractiveConsole.showtraceback(self)

    def push(self, line):
        if self.escaped_input:
            line = codecs.decode(line, 'unicode_escape')
        if self.echo:
            print("In: %s \n" % line)

        with CatchOutput(self.cache):
            InteractiveConsole.push(self, line)

        output = self.cache.flush()

        if self.echo:
            print("Out: %s \n" % output)
        return output

    def interact(self):
        InteractiveConsole.interact(self, "")

if __name__ == '__main__':
    sh = Shell(echo=True)
    sh.interact()
