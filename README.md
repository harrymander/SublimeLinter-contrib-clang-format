# SublimeLinter-contrib-clang-format

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [clang-format](https://clang.llvm.org/docs/ClangFormat.html). It will be used with files that have the `C` and `C++` syntaxes.

## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before installing this plugin, you must ensure that `clang-format` is installed on your system.

In order for `clang-format` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings

- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

By default, linting will only be enabled if a [`.clang-format` file](https://clang.llvm.org/docs/ClangFormatStyleOptions.html) is present in one of the parent directories of the file being processed. To override this behaviour, set the `style` or `fallback-style` options (see table below) to one of the preset styles: run `clang-format --help` for a list of the available presets.

| Setting | Description |
| :-------| :-----------|
| `style` | Formatting style. Default is `file`, which will use the `.clang-format` file in one of the parent directories of the file being linted. |
| `fallback-style` | Style to use if `style` is `file` and no `.clang-format` file can be found. Default is `none`, which disables linting if no `.clang-format` file is found. |

For example, to use GNU style, add the following to your Sublime Text settings or project settings:

```json
{
    "SublimeLinter.linters.clang-format.style": "GNU"
}
```
