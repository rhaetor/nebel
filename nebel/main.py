#!/usr/bin/env python3
"""
Nebel is a Python command-line tool to automate certain routine tasks
associated with creating and managing _modular documentation_.

For example, you can use Nebel to create an instance of
an assembly, procedure, concept, or reference file.
"""

__author__ = "ajonsson"
__version__ = "3.0.0"
__license__ = "MIT"

import argparse
import logging


def main(args):
    """ Main entry point of the app """
    logging.info("Starting Nebel")
    logging.info("with arguments: ", *args)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # Required positional argument
    parser.add_argument("arg", help="Required positional argument")

    # Optional argument flag which defaults to False
    parser.add_argument("-f", "--flag", action="store_true", default=False)

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-n", "--name", action="store", dest="name")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    args = parser.parse_args()
    main(args)
