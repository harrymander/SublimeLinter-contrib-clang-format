import re

from SublimeLinter import lint


class ClangFormat(lint.Linter):
    cmd = 'clang-format --dry-run --style=file ${args} ${file}'
    default_type = lint.WARNING
    defaults = {
        'selector': 'source.c - source.c++'
    }

    error_stream = lint.STREAM_STDERR
    multiline = True
    re_flags = re.MULTILINE
    regex = (
        r'^.*?:(?P<line>\d+):(?P<col>\d+): '  # line and column number
        r'(?:(?P<error>error)|(?P<warning>warning)): '  # 'error' or 'warning'
        r'(?P<message>.*?)'  # message
        r'\n.*\n.*$'  # two extra lines to ignore
    )
