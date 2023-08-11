SublimeLinter-clang-format
==========================

[![Build Status](https://travis-ci.org/SublimeLinter/SublimeLinter-clang-format.svg?branch=master)](https://travis-ci.org/SublimeLinter/SublimeLinter-clang-format)

This linter plugin for [SublimeLinter](https://github.com/SublimeLinter/SublimeLinter) provides an interface to [clang-format](https://clang.llvm.org/docs/ClangFormat.html). It will be used with files that have the `C` and `C++` syntaxes.

## Installation

SublimeLinter must be installed in order to use this plugin. 

Please use [Package Control](https://packagecontrol.io) to install the linter plugin.

Before installing this plugin, you must ensure that `clang-format` is installed on your system.

In order for `clang-format` to be executed by SublimeLinter, you must ensure that its path is available to SublimeLinter. The docs cover [troubleshooting PATH configuration](http://sublimelinter.readthedocs.io/en/latest/troubleshooting.html#finding-a-linter-executable).

## Settings

- SublimeLinter settings: http://sublimelinter.readthedocs.org/en/latest/settings.html
- Linter settings: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html

Formatting style can be configured using a [`.clang-format` file](https://clang.llvm.org/docs/ClangFormatStyleOptions.html) or selecting one of the preset styles; see `clang-format --help` for the available preset styles.

|Setting        |Description                                                                                             |
|:--------------|:-------------------------------------------------------------------------------------------------------|
|style          |Formatting style. Default is `file`, which will use `.clang-format` file.                               |
|fallback-style |Style to use if no `.clang-format` file can be found and `fallback-style` is `file`. Default is `llvm`. |

For example, to use GNU style, add the following to your Sublime Text settings or project settings:

```json
{
    "SublimeLinter.linters.clang-format.style": "GNU"
}
```
