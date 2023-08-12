import re

from SublimeLinter import lint


class ClangFormat(lint.Linter):
    name = 'clang-format'
    cmd = (
        'clang-format',
        '--dry-run',
        '--assume-filename=${file}',
        '${args}',
    )
    default_type = lint.WARNING
    defaults = {
        'selector': 'source.c,source.c++',
        '--fallback-style=': 'llvm',
        '--style=': 'file',
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
