# Copyright (C) 2021 Biren Patel
# MIT License
# Lightweight and minimal preprocessor to allow for debugging toggle switches.
# The preprocessor is only valid for lox source executed from script.

class Preprocessor():
    def __init__(self):
        """\
        @flags: all pragma switches (defaulted to off mode)
        """
        self.flags = {"tok_debug": False, "parse_debug": False}

    def scan(self, p_src):
        """\
        seek and eliminate #pragma statements. OFF statements take precedence
        over ON statements of the same type, regardless of order of occurence
        within a lox script. #pragma statements may be placed anywhere. Syntax
        errors on #pragma are carried on to the lox tokenizer which may result
        in untold doom and chaos.
        """
        if p_src.find("#pragma tok_debug on") >= 0:
            self.flags["tok_debug"] = True
            p_src = p_src.replace("#pragma tok_debug on", " ")

        if p_src.find("pragma tok_debug off") >= 0:
            self.flags["tok_debug"] = False
            p_src = p_src.replace("#pragma tok_debug off", " ")

        if p_src.find("pragma parse_debug on") >= 0:
            self.flags["parse_debug"] = True
            p_src = p_src.replace("#pragma parse_debug on", " ")

        if p_src.find("pragma parse_debug off") >= 0:
            self.flags["parse_debug"] = False
            p_src = p_src.replace("#pragma parse_debug off", " ")

        return (p_src, self.flags)
