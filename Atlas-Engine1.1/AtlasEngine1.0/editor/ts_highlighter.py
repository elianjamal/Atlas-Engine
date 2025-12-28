#!/usr/bin/env python3
"""
AtlasEngine - T# Syntax Highlighter
Provides syntax highlighting for the T# scripting language
"""

import re

class TSHighlighter:
    """T# Syntax Highlighter"""
    
    # T# Language Keywords
    KEYWORDS = [
        'var', 'func', 'if', 'else', 'elif', 'while', 'for',
        'return', 'break', 'continue', 'true', 'false', 'null',
        'spawn', 'move', 'rotate', 'destroy', 'print', 'input'
    ]
    
    # Built-in types
    TYPES = [
        'int', 'float', 'string', 'bool', 'object', 'array'
    ]
    
    # Operators
    OPERATORS = [
        '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
        '&&', '||', '!', '&', '|', '^', '~', '<<', '>>'
    ]
    
    @staticmethod
    def get_token_patterns():
        """Get regex patterns for different token types"""
        return {
            'keyword': r'\b(' + '|'.join(TSHighlighter.KEYWORDS) + r')\b',
            'type': r'\b(' + '|'.join(TSHighlighter.TYPES) + r')\b',
            'string': r'["\'](?:[^"\'\\]|\\.)*["\']',
            'comment': r'//.*?$|/\*.*?\*/',
            'number': r'\b\d+\.?\d*\b',
            'function': r'\b(\w+)(?=\s*\()',
            'operator': r'[+\-*/%=<>!&|^~]+',
        }
    
    @staticmethod
    def tokenize(code: str) -> list:
        """Tokenize T# code"""
        tokens = []
        patterns = TSHighlighter.get_token_patterns()
        
        for token_type, pattern in patterns.items():
            for match in re.finditer(pattern, code, re.MULTILINE):
                tokens.append({
                    'type': token_type,
                    'value': match.group(0),
                    'start': match.start(),
                    'end': match.end()
                })
        
        # Sort by position
        tokens.sort(key=lambda x: x['start'])
        
        return tokens
    
    @staticmethod
    def validate_syntax(code: str) -> tuple:
        """Basic syntax validation"""
        errors = []
        
        # Check for matching braces
        brace_stack = []
        for i, char in enumerate(code):
            if char == '{':
                brace_stack.append((char, i))
            elif char == '}':
                if not brace_stack:
                    errors.append(f"Unmatched closing brace at position {i}")
                else:
                    brace_stack.pop()
        
        if brace_stack:
            errors.append(f"Unclosed braces: {len(brace_stack)}")
        
        # Check for matching parentheses
        paren_stack = []
        for i, char in enumerate(code):
            if char == '(':
                paren_stack.append((char, i))
            elif char == ')':
                if not paren_stack:
                    errors.append(f"Unmatched closing parenthesis at position {i}")
                else:
                    paren_stack.pop()
        
        if paren_stack:
            errors.append(f"Unclosed parentheses: {len(paren_stack)}")
        
        return len(errors) == 0, errors
