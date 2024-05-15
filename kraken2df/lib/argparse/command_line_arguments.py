# Project     : kraken2df
# File Name   : command_line_arguments.py
# Description : CLI argument handling.
# Author      : Todd N. Wylie
# Email       : twylie@wustl.edu
# Created     : Mon May 13 09:49:36 CDT 2024
# Copyright   : Copyright (C) 2024 by T.N. Wylie. All rights reserved.

import argparse
import pathlib
from typing_extensions import Self

VERSION = '1.0'
WRITE_DIR = 'kraken2df'


class CommandLineArguments:
    """Command line interface argument handling."""

    def __init__(self: Self) -> None:
        """Construct the class."""
        self.__arguments = self.__collect_cli_arguments()
        self.__eval_cli_arguments()
        self.mpa_path = pathlib.Path(self.args().mpa)
        self.outdir_path = pathlib.Path(self.args().outdir)
        self.write_dir_path = self.outdir_path / WRITE_DIR
        self.sample_id = self.args().id
        return

    def args(self: Self) -> argparse.Namespace:
        """Returns the defined arguments for the object."""
        return self.__arguments

    def __collect_cli_arguments(self: Self) -> argparse.Namespace:
        """Collects the CLI arguments for the object."""
        parser = argparse.ArgumentParser(
            description='Description here.',
            prog='kraken2df.py',
            add_help=False
        )

        # OPTIONAL

        parser.add_argument(
            '-h',
            '--help',
            action='help',
            help='Display the extended usage statement.'
        )

        parser.add_argument(
            '--version',
            action='version',
            version=VERSION,
            help='Display the software version number.'
        )

        # REQUIRED

        required_group = parser.add_argument_group('required')

        required_group.add_argument(
            '--mpa',
            metavar='FILE',
            action='store',
            help='File path to the source Kraken2 MPA report.',
            required=True,
        )

        required_group.add_argument(
            '--outdir',
            metavar='DIR',
            action='store',
            help='Existing directory path to write report files.',
            required=True
        )

        required_group.add_argument(
            '--id',
            metavar='STR',
            action='store',
            help='Sample id used for labeling reports.',
            required=True
        )

        return parser.parse_args()

    def __eval_cli_arguments(self) -> None:
        """Evaluate CLI arguments and handle exceptions."""
        args = self.args()

        mpa_path = pathlib.Path(args.mpa)
        if mpa_path.is_file() is False:
            raise FileNotFoundError(
                'File is missing.',
                mpa_path.as_posix()
            )

        outdir_path = pathlib.Path(args.outdir)
        if outdir_path.exists() is False:
            raise NotADirectoryError(
                'Directory does not exist.',
                outdir_path.as_posix()
            )

        # The kraken2df report directory should not already exist, it
        # will be written during report generation.

        write_dir_path = outdir_path / WRITE_DIR
        if write_dir_path.is_dir() is True:
            raise IsADirectoryError(
                'Directory already exists.',
                write_dir_path.as_posix()
            )

        return

# __END__
