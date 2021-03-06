# Copyright (c) 2016-present, Facebook, Inc.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import io
import unittest

from unittest.mock import patch, mock_open, MagicMock

from ... import EnvironmentException  # noqa
from ... import commands  # noqa


def mock_arguments():
    arguments = MagicMock()

    arguments.debug = False
    arguments.sequential = False
    arguments.strict = False
    arguments.show_error_traces = False
    arguments.verbose = False
    arguments.logging_sections = None
    arguments.log_identifier = None
    arguments.current_directory = '.'
    arguments.original_directory = '/original/directory/'

    return arguments


def mock_configuration():
    configuration = MagicMock()
    configuration.source_directories = ['.']
    configuration.get_search_path = MagicMock()
    return configuration


class CommandTest(unittest.TestCase):
    def test_relative_path(self) -> None:
        arguments = mock_arguments()
        configuration = mock_configuration()

        self.assertEqual(
            commands.Command(
                arguments,
                configuration, [])._relative_path('/original/directory/path'),
            'path')
        self.assertEqual(
            commands.Command(
                arguments,
                configuration,
                [])._relative_path('/original/directory/'),
            '.')

    @patch('os.kill')
    def test_state(self, os_kill) -> None:
        arguments = mock_arguments()
        configuration = mock_configuration()

        with patch('builtins.open', mock_open()) as open:
            open.side_effect = [io.StringIO('1')]
            self.assertEqual(
                commands.Command(
                    arguments,
                    configuration,
                    source_directory='.')._state(),
                commands.command.State.RUNNING)

        with patch('builtins.open', mock_open()) as open:
            open.side_effect = [io.StringIO('derp')]
            self.assertEqual(
                commands.Command(
                    arguments,
                    configuration,
                    source_directory='.')._state(),
                commands.command.State.DEAD)
