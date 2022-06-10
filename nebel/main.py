#!/usr/bin/env python3
"""
Nebel is a Python command-line tool to automate certain routine tasks
associated with creating and managing _modular documentation_.

For example, you can use Nebel to create an instance of
an assembly, procedure, concept, or reference file.
"""

from __future__ import absolute_import, print_function

__author__ = "ajonsson"
__version__ = "3.0.0"
__license__ = "MIT"

import argparse
import logging
import os
import sys

import nebel.context
import nebel.factory
from nebel import Tasks
from nebel.commands import add_module_arguments


def process_run():
    # MAIN CODE - PROGRAM STARTS HERE!
    # --------------------------------

    # Basic initialization
    if not os.path.exists('nebel.cfg'):
        print('WARN: No nebel.cfg file found in this directory.')
        sys.exit()
    context = nebel.context.NebelContext()
    context.initializeFromFile('nebel.cfg')
    this_script_path = os.path.dirname(os.path.abspath(__file__))
    context.templatePath = os.path.abspath(os.path.join(this_script_path, '..', 'template'))
    context.moduleFactory = nebel.factory.ModuleFactory(context)
    tasks = Tasks(context)

    # Create the top-level parser
    parser = argparse.ArgumentParser(prog='nebel')
    parser.add_argument('-v', '--version', action='version', version='Nebel 3.0.x (dev release)')
    subparsers = parser.add_subparsers()

    # Create the sub-parser for the 'assembly' command
    assembly_parser = subparsers.add_parser('assembly', help='Generate an assembly')
    add_module_arguments(assembly_parser)
    assembly_parser.set_defaults(func=tasks.create_assembly)

    # Create the sub-parser for the 'procedure' command
    procedure_parser = subparsers.add_parser('procedure', help='Generate a procedure module')
    add_module_arguments(procedure_parser)
    procedure_parser.set_defaults(func=tasks.create_procedure)

    # Create the sub-parser for the 'concept' command
    concept_parser = subparsers.add_parser('concept', help='Generate a concept module')
    add_module_arguments(concept_parser)
    concept_parser.set_defaults(func=tasks.create_concept)

    # Create the sub-parser for the 'reference' command
    reference_parser = subparsers.add_parser('reference', help='Generate a reference module')
    add_module_arguments(reference_parser)
    reference_parser.set_defaults(func=tasks.create_reference)

    # Create the sub-parser for the 'create-from' command
    create_parser = subparsers.add_parser('create-from',
                                          help='Create multiple assemblies/modules from a CSV file, or an assembly file')
    create_parser.add_argument('FROM_FILE',
                               help='Can be either a comma-separated values (CSV) file (ending with .csv), or an assembly file (starting with {}/ and ending with .adoc)'.format(
                                   context.ASSEMBLIES_DIR))
    create_parser.set_defaults(func=tasks.create_from)

    # Create the sub-parser for the 'split' command
    split_parser = subparsers.add_parser('split',
                                         help='Split an annotated AsciiDoc file into multiple assemblies and modules')
    split_parser.add_argument('FROM_FILE',
                              help='Annotated AsciiDoc file (ending with .adoc, including optional wildcard braces, {})')
    split_parser.add_argument('--legacybasedir',
                              help='Base directory for annotated file content. Subdirectories of this directory are used as default categories.')
    split_parser.add_argument('--category-prefix',
                              help='When splitting an annotated file, add this prefix to default categories.')
    split_parser.add_argument('-a', '--attribute-files', help='Specify a comma-separated list of attribute files')
    split_parser.add_argument('--conditions',
                              help='Define a comma-separated list of condition attributes, for resolving ifdef and ifndef directives')
    split_parser.add_argument('--timestamp', help='Generate a timestamp in the generated module and assembly files',
                              action='store_true')
    split_parser.set_defaults(func=tasks.adoc_split)

    # Create the sub-parser for the 'book' command
    book_parser = subparsers.add_parser('book', help='Create and manage book directories')
    book_parser.add_argument('BOOK_DIR', help='The book directory')
    book_parser.add_argument('--create', help='Create a new book directory', action='store_true')
    book_parser.add_argument('-c', '--category-list',
                             help='Comma-separated list of categories to add to book (enclose in quotes)')
    book_parser.set_defaults(func=tasks.book)

    # Create the sub-parser for the 'mv' command
    book_parser = subparsers.add_parser('mv',
                                        help='Move (or rename) module or assembly files. You can optionally use a single instance of braces for globbing/substituting. For example, to change a file prefix from p_ to proc_ you could enter: nebel mv p_{}.adoc proc_{}.adoc')
    book_parser.add_argument('FROM_FILE', help='File origin. Optionally use {} for globbing.')
    book_parser.add_argument('TO_FILE', help='File destination. Optionally use {} to substitute captured glob content')
    book_parser.set_defaults(func=tasks.mv)

    # Create the sub-parser for the 'update' command
    update_parser = subparsers.add_parser('update', help='Update metadata in modules and assemblies')
    update_parser.add_argument('--fix-includes', help='Fix erroneous include directives in assemblies',
                               action='store_true')
    update_parser.add_argument('--fix-links', help='Fix erroneous cross-reference links', action='store_true')
    update_parser.add_argument('-p', '--parent-assemblies',
                               help='Update ParentAssemblies property in modules and assemblies', action='store_true')
    update_parser.add_argument('--generate-ids', help='Generate missing IDs for headings', action='store_true')
    update_parser.add_argument('--id-prefix', help='Customize ID prefix for IDs generated using --generate-ids')
    update_parser.add_argument('--add-contexts',
                               help='Add _{context} to IDs and add boilerplate around include directives',
                               action='store_true')
    update_parser.add_argument('--hash-contexts',
                               help='Use together with --add-contexts if you want contexts to contain hashes instead of literal IDs',
                               action='store_true')
    update_parser.add_argument('-c', '--category-list',
                               help='Apply update only to this comma-separated list of categories (enclose in quotes)')
    update_parser.add_argument('-b', '--book', help='Apply update only to the specified book')
    update_parser.add_argument('-a', '--attribute-files', help='Specify a comma-separated list of attribute files')
    update_parser.add_argument('FILE',
                               help='File to update OR you can omit this argument and use --book or --category-list instead',
                               nargs='?')
    update_parser.set_defaults(func=tasks.update)

    # Create the sub-parser for the 'orphan' command
    orphan_parser = subparsers.add_parser('orphan', help='Search for orphaned module and assembly files')
    orphan_parser.add_argument('-c', '--category-list',
                               help='Filter for orphan files belonging to this comma-separated list of categories')
    orphan_parser.add_argument('-a', '--attribute-files', help='Specify a comma-separated list of attribute files')
    orphan_parser.set_defaults(func=tasks.orphan_search)

    # Create the sub-parser for the 'toc' command
    toc_parser = subparsers.add_parser('toc', help='List TOC for assembly or book')
    toc_parser.add_argument('ASSEMBLY_OR_BOOK_FILE',
                            help='Path to the assembly or book file whose table of contents you want to list')
    toc_parser.set_defaults(func=tasks.toc)

    # Create the sub-parser for the 'atom' command
    atom_parser = subparsers.add_parser('atom', help='Open a module or an assembly using the atom editor')
    atom_parser.add_argument('FILE', help='Pathname of the assembly or module file to edit')
    atom_parser.add_argument('-p', '--parent', help='Open the parent assembly of the specified assembly or module',
                             action='store_true')
    atom_parser.add_argument('-s', '--siblings', help='Open the siblings of the specified assembly or module',
                             action='store_true')
    atom_parser.add_argument('-c', '--children', help='Open the children of the specified assembly',
                             action='store_true')
    atom_parser.set_defaults(func=tasks.atom)

    # Create the sub-parser for the 'csv' command
    csv_parser = subparsers.add_parser('csv', help='Generate CSV of metadata for assembly or book')
    csv_parser.add_argument('ASSEMBLY_OR_BOOK_FILE',
                            help='Path to the assembly or book file whose metadata you want to generate as a CSV file')
    csv_parser.add_argument('-c', '--cols', help='Specify a comma-separated list of column headers')
    csv_parser.set_defaults(func=tasks.csv)

    # Now, parse the args and call the relevant sub-command
    args = parser.parse_args()
    args.func(args)


def main(args):
    """ Main entry point of the app """
    logging.info("Starting Nebel")
    logging.info("with arguments: ", args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

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
