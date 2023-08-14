from SublimeLinter import lint
from SublimeLinter.lint import LintMatch


class ClangFormat(lint.Linter):
    name = 'clang-format'
    cmd = (
        'clang-format',
        '--output-replacements-xml',
        '--assume-filename=${file}',
        '${args}',
    )
    default_type = lint.WARNING
    defaults = {
        'selector': 'source.c,source.c++',
        '--fallback-style=': 'llvm',
        '--style=': 'file',
    }

    error_stream = lint.STREAM_STDOUT
    regex = r"^<replacement offset='(?P<offset>\d+)' length='(?P<length>\d+)'"

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
