import re

from SublimeLinter import lint
from SublimeLinter.lint import LintMatch
from SublimeLinter.lint.linter import VirtualView


class ClangFormat(lint.Linter):
    name = 'clang-format'
    default_type = lint.WARNING
    defaults = {
        'selector': 'source.c,source.c++',
        '--fallback-style=': 'none',
        '--style=': 'file',
    }

    if hasattr(VirtualView, 'rowcol'):
        """
        Requires SublimeLinter >=4.23.0

        Use --output-replacements-xml to output the offset and length of each
        replacement. Then match the entire region to be replaced. Requires
        VirtualView.rowcol method.
        """
        cmd = (
            'clang-format',
            '--output-replacements-xml',
            '--assume-filename=${file}',
            '${args}',
        )

        error_stream = lint.STREAM_STDOUT
        regex = (
            r"^<replacement offset='(?P<offset>\d+)' length='(?P<length>\d+)'"
        )

        def reposition_match(self, line, col, m, vv):
            line, col = vv.rowcol(m['offset'])
            return line, col, col + m['length']

        def split_match(self, match):
            return LintMatch({
                'warning': 'warning',
                'message': 'Not formatted properly',
                'offset': int(match.group('offset')),
                'length': int(match.group('length')),
                'line': 1,
            })
    else:
        """
        Just match the first character of the error.
        """
        cmd = (
            'clang-format',
            '--dry-run',
            '--assume-filename=${file}',
            '${args}',
        )
        error_stream = lint.STREAM_STDERR
        multiline = True
        re_flags = re.MULTILINE
        regex = (
            r'^.*?:(?P<line>\d+):(?P<col>\d+): '  # line and column number
            r'(?:(?P<error>error)|(?P<warning>warning)): '  # 'error'/'warning'
            r'(?P<message>.*?)'  # message
            r'\n.*\n.*$'  # two extra lines to ignore
        )
