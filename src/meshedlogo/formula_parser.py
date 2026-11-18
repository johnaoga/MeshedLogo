"""
Formula Parser Module
Advanced parsing for mathematical formulas with LaTeX support
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional


@dataclass
class FormulaToken:
    """Represents a parsed formula token with rendering metadata"""
    text: str
    token_type: str  # 'char', 'superscript', 'subscript', 'fraction_num', 'fraction_denom', 'fraction_bar'
    scale: float = 1.0
    y_offset: float = 0.0  # Vertical offset as fraction of character height


class FormulaParser:
    """Parse mathematical formulas with LaTeX-style notation"""
    
    def __init__(self):
        # LaTeX command to Unicode symbol mapping
        self.latex_symbols = {
            'theta': 'θ', 'Theta': 'Θ',
            'pi': 'π', 'Pi': 'Π',
            'alpha': 'α', 'Alpha': 'Α',
            'beta': 'β', 'Beta': 'Β',
            'gamma': 'γ', 'Gamma': 'Γ',
            'delta': 'δ', 'Delta': 'Δ',
            'epsilon': 'ε', 'Epsilon': 'Ε',
            'lambda': 'λ', 'Lambda': 'Λ',
            'mu': 'μ', 'Mu': 'Μ',
            'sigma': 'σ', 'Sigma': 'Σ',
            'omega': 'ω', 'Omega': 'Ω',
            'phi': 'φ', 'Phi': 'Φ',
            'psi': 'ψ', 'Psi': 'Ψ',
            'int': '∫',
            'sum': '∑',
            'prod': '∏',
            'sqrt': '√',
            'infty': '∞',
            'pm': '±',
            'times': '×',
            'cdot': '·',
            'leq': '≤',
            'geq': '≥',
            'neq': '≠',
            'approx': '≈',
        }
    
    def parse(self, formula: str) -> List[FormulaToken]:
        """
        Parse a formula string into tokens with rendering metadata.
        
        Supports:
        - x^2, x^{2}, x^(2) - superscripts
        - x_1, x_{1}, x_(1) - subscripts
        - \\frac{a}{b} - fractions with horizontal bar
        - \\theta, \\pi, etc. - Greek letters
        - i, x, etc. - case-sensitive variables
        
        Args:
            formula: Formula string to parse
            
        Returns:
            List of FormulaToken objects
        """
        tokens = []
        i = 0
        
        while i < len(formula):
            # Check for \frac{numerator}{denominator}
            if formula[i:].startswith('\\frac{'):
                frac_tokens, chars_consumed = self._parse_fraction(formula[i:])
                tokens.extend(frac_tokens)
                i += chars_consumed
                continue
            
            # Check for LaTeX commands (\theta, \pi, etc.)
            if formula[i] == '\\':
                latex_cmd, chars_consumed = self._parse_latex_command(formula[i:])
                if latex_cmd:
                    tokens.append(FormulaToken(
                        text=latex_cmd,
                        token_type='char',
                        scale=1.0,
                        y_offset=0.0
                    ))
                    i += chars_consumed
                    continue
                else:
                    # Not a recognized command, skip the backslash
                    i += 1
                    continue
            
            # Check for superscript (^)
            if formula[i] == '^':
                # Find the superscript content
                content, chars_consumed = self._extract_grouped_content(formula[i+1:])
                if content:
                    # Parse content recursively (could be nested)
                    sub_tokens = self.parse(content)
                    for token in sub_tokens:
                        tokens.append(FormulaToken(
                            text=token.text,
                            token_type='superscript',
                            scale=0.6,
                            y_offset=-0.4  # Move up
                        ))
                    i += 1 + chars_consumed
                    continue
                else:
                    # No valid superscript, treat ^ as regular character
                    tokens.append(FormulaToken(text='^', token_type='char'))
                    i += 1
                    continue
            
            # Check for subscript (_)
            if formula[i] == '_':
                # Find the subscript content
                content, chars_consumed = self._extract_grouped_content(formula[i+1:])
                if content:
                    # Parse content recursively
                    sub_tokens = self.parse(content)
                    for token in sub_tokens:
                        tokens.append(FormulaToken(
                            text=token.text,
                            token_type='subscript',
                            scale=0.6,
                            y_offset=0.3  # Move down
                        ))
                    i += 1 + chars_consumed
                    continue
                else:
                    # No valid subscript, treat _ as regular character
                    tokens.append(FormulaToken(text='_', token_type='char'))
                    i += 1
                    continue
            
            # Skip whitespace
            if formula[i].isspace():
                i += 1
                continue
            
            # Regular character (case-sensitive)
            tokens.append(FormulaToken(
                text=formula[i],
                token_type='char',
                scale=1.0,
                y_offset=0.0
            ))
            i += 1
        
        return tokens
    
    def _parse_fraction(self, text: str) -> Tuple[List[FormulaToken], int]:
        """
        Parse \\frac{numerator}{denominator} into tokens.
        
        Returns:
            (tokens, chars_consumed)
        """
        if not text.startswith('\\frac{'):
            return [], 0
        
        i = 6  # Skip '\\frac{'
        
        # Extract numerator
        numerator, num_len = self._extract_braced_content(text[i:])
        if numerator is None:
            return [], 0
        i += num_len
        
        # Expect '{' for denominator
        if i >= len(text) or text[i] != '{':
            return [], 0
        i += 1
        
        # Extract denominator
        denominator, denom_len = self._extract_braced_content(text[i:])
        if denominator is None:
            return [], 0
        i += denom_len
        
        # Create tokens for fraction
        tokens = []
        
        # Numerator tokens (scaled and positioned above)
        num_tokens = self.parse(numerator)
        for token in num_tokens:
            tokens.append(FormulaToken(
                text=token.text,
                token_type='fraction_num',
                scale=0.7,
                y_offset=-0.5  # Position above the line
            ))
        
        # Fraction bar
        tokens.append(FormulaToken(
            text='─',  # Horizontal line character
            token_type='fraction_bar',
            scale=1.0,
            y_offset=0.0
        ))
        
        # Denominator tokens (scaled and positioned below)
        denom_tokens = self.parse(denominator)
        for token in denom_tokens:
            tokens.append(FormulaToken(
                text=token.text,
                token_type='fraction_denom',
                scale=0.7,
                y_offset=0.5  # Position below the line
            ))
        
        return tokens, i
    
    def _parse_latex_command(self, text: str) -> Tuple[Optional[str], int]:
        """
        Parse a LaTeX command like \\theta, \\pi, etc.
        
        Returns:
            (symbol or None, chars_consumed)
        """
        if not text.startswith('\\'):
            return None, 0
        
        i = 1
        cmd_name = ''
        while i < len(text) and text[i].isalpha():
            cmd_name += text[i]
            i += 1
        
        if cmd_name in self.latex_symbols:
            return self.latex_symbols[cmd_name], i
        
        return None, 0
    
    def _extract_grouped_content(self, text: str) -> Tuple[Optional[str], int]:
        """
        Extract content from {}, (), or single character.
        
        Returns:
            (content, chars_consumed)
        """
        if not text:
            return None, 0
        
        # Check for braces {}
        if text[0] == '{':
            return self._extract_braced_content(text)
        
        # Check for parentheses ()
        if text[0] == '(':
            content, length = self._extract_parenthesized_content(text)
            return content, length
        
        # Single character
        return text[0], 1
    
    def _extract_braced_content(self, text: str) -> Tuple[Optional[str], int]:
        """
        Extract content from {...}.
        
        Returns:
            (content, chars_consumed including braces)
        """
        if not text or text[0] != '{':
            return None, 0
        
        i = 1
        depth = 1
        content = ''
        
        while i < len(text) and depth > 0:
            if text[i] == '{':
                depth += 1
                content += text[i]
            elif text[i] == '}':
                depth -= 1
                if depth > 0:
                    content += text[i]
            else:
                content += text[i]
            i += 1
        
        if depth == 0:
            return content, i
        else:
            return None, 0
    
    def _extract_parenthesized_content(self, text: str) -> Tuple[Optional[str], int]:
        """
        Extract content from (...).
        
        Returns:
            (content, chars_consumed including parentheses)
        """
        if not text or text[0] != '(':
            return None, 0
        
        i = 1
        depth = 1
        content = ''
        
        while i < len(text) and depth > 0:
            if text[i] == '(':
                depth += 1
                content += text[i]
            elif text[i] == ')':
                depth -= 1
                if depth > 0:
                    content += text[i]
            else:
                content += text[i]
            i += 1
        
        if depth == 0:
            return content, i
        else:
            return None, 0
