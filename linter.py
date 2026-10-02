import re
from bisect import bisect_right
from functools import lru_cache
from itertools import accumulate

import sublime
from SublimeLinter import lint
from SublimeLinter.lint import LintMatch
from SublimeLinter.lint.linter import VirtualView


@lru_cache(maxsize=1)
def line_offsets(code):
    """Return the lines of code and the offsets of the start of each line.

    The offsets are returned as a tuple of two lists: the offsets in
    UTF-8 encoded bytes and the offsets in characters.
    """
    lines = code.splitlines(keepends=True)
    byte_starts = list(accumulate(
        (len(line.encode('utf-8')) for line in lines),
        initial=0,
    ))
    char_starts = list(accumulate((len(line) for line in lines), initial=0))
    return lines, byte_starts, char_starts


def char_offset(code, byte_offset):
    """Convert an offset in UTF-8 encoded bytes into a character offset.

    clang-format reports the offset and length of each replacement in
    bytes, whereas VirtualView.rowcol expects characters. Offsets that
    fall inside a multi-byte character are rounded down to the start of
    that character.
    """
    lines, byte_starts, char_starts = line_offsets(code)
    if not lines:
        return 0

    byte_offset = max(byte_offset, 0)
    row = min(bisect_right(byte_starts, byte_offset) - 1, len(lines) - 1)
    line = lines[row].encode('utf-8')[:byte_offset - byte_starts[row]]
    return char_starts[row] + len(line.decode('utf-8', 'ignore'))


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
            code = vv.substr(sublime.Region(0, vv.size()))
            start = char_offset(code, m['offset'])
            end = char_offset(code, m['offset'] + m['length'])
            line, col = vv.rowcol(start)
            return line, col, col + end - start

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
