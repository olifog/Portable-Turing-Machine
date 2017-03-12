# Portable-Turing-Machine
This is the Github repository for the Portable Python Turing Machine. Here you can find source code, package information, syntax tips and more.

Kivy installation (required for the GUI): https://kivy.org/docs/installation/installation.html

Directory help:
  - Historical          = Old versions of the programs.
  - otm                 = The actual Turing Machine simulator!
  - otmg                = The graphical user interface for the simulator, built with Kivy. See below for Kivy installation.
  - otmp                = The Turing Machine programs that the Turing Machine runs.


Syntax for programs:
  - Each line should contain one tuple of the form '<current state> <current symbol> <new symbol> <direction> <new state>'.
  - You can use any number or word for <current state> and <new state>, eg. 10, a, state1. State labels are case-sensitive.
  - You can use any character for <current symbol> and <new symbol>, or '_' to represent blank (space). Symbols are case-sensitive.
  - <direction> should be 'l', 'r' or '*', denoting 'move left', 'move right' or 'do not move', respectively.
  - Anything after a ';' is a comment and is ignored.
  - The machine halts when it reaches any state starting with 'halt', eg. halt, halt-accept.
Also:
  - '*' can be used as a wildcard in <current symbol> or <current state> to match any character or state.
  - '*' can be used in <new symbol> or <new state> to mean 'no change'.
