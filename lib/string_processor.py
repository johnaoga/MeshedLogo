"""
String Processor Module
Processes text strings and formulas, converting them to character images
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
import re
from lib.character_renderer import CharacterRenderer, CharacterImage


class RenderMode(Enum):
    """Rendering mode for strings"""
    SINGLE = "single"  # Render entire string as one image
    INDIVIDUAL = "individual"  # Render each character separately


@dataclass
class ProcessedString:
    """Data class to hold processed string data"""
    original_text: str
    characters: List[str]
    images: List[CharacterImage]
    mode: RenderMode
    is_formula: bool
    
    def save_all(self, output_dir: str, prefix: str = "char") -> List[str]:
        """
        Save all character images to files
        
        Args:
            output_dir: Directory to save images
            prefix: Filename prefix
            
        Returns:
            List of saved file paths
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        saved_paths = []
        for i, img in enumerate(self.images):
            char_safe = self.characters[i].replace('/', '_').replace('\\', '_')
            filepath = os.path.join(output_dir, f"{prefix}_{i}_{char_safe}.png")
            img.save(filepath)
            saved_paths.append(filepath)
        
        return saved_paths


class StringProcessor:
    """
    Processes text strings and mathematical formulas
    Converts them to character images using CharacterRenderer
    """
    
    def __init__(self, renderer: Optional[CharacterRenderer] = None):
        """
        Initialize the string processor
        
        Args:
            renderer: CharacterRenderer instance (creates default if None)
        """
        self.renderer = renderer or CharacterRenderer()
        self._formula_patterns = {
            'fraction': r'(\w+)/(\w+)',  # ME/IN
            'exponent': r'(\w+)\^(\([^)]+\)|[\w]+)',  # e^(iθ)
            'subscript': r'(\w+)_(\w+)',  # x_1
            'sqrt': r'√(\w+)',  # √x
            'integral': r'∫',
            'sum': r'∑',
            'product': r'∏',
        }
    
    def process(self, text: str, mode: RenderMode = RenderMode.INDIVIDUAL,
                width: Optional[int] = None, height: Optional[int] = None,
                thickness: Optional[int] = None,
                save_dir: Optional[str] = None) -> ProcessedString:
        """
        Process a string and convert to character images
        
        Args:
            text: Input text or formula
            mode: Rendering mode (single or individual)
            width: Image width for each character
            height: Image height for each character
            thickness: Stroke thickness
            save_dir: Optional directory to save all images
            
        Returns:
            ProcessedString object containing all character images
        """
        # Detect if it's a formula
        is_formula = self._is_formula(text)
        
        # Parse the string into characters/tokens
        characters = self._parse_string(text, is_formula)
        
        # Render each character
        images = []
        for char in characters:
            img = self.renderer.render(
                character=char,
                width=width,
                height=height,
                thickness=thickness
            )
            images.append(img)
        
        # Create ProcessedString object
        processed = ProcessedString(
            original_text=text,
            characters=characters,
            images=images,
            mode=mode,
            is_formula=is_formula
        )
        
        # Save if directory is provided
        if save_dir:
            processed.save_all(save_dir)
        
        return processed
    
    def process_formula(self, formula: str, width: Optional[int] = None,
                       height: Optional[int] = None, thickness: Optional[int] = None,
                       save_dir: Optional[str] = None) -> ProcessedString:
        """
        Process a mathematical formula with special handling
        
        Args:
            formula: Mathematical formula string
            width: Image width for each character
            height: Image height for each character
            thickness: Stroke thickness
            save_dir: Optional directory to save all images
            
        Returns:
            ProcessedString object with formula components
        """
        # Parse formula into components
        components = self._parse_formula(formula)
        
        # Render each component
        images = []
        characters = []
        
        for component in components:
            char_text = component['text']
            char_type = component['type']
            
            # Adjust size based on component type
            w = width or self.renderer.default_width
            h = height or self.renderer.default_height
            
            if char_type == 'superscript':
                w = int(w * 0.6)
                h = int(h * 0.6)
            elif char_type == 'subscript':
                w = int(w * 0.6)
                h = int(h * 0.6)
            
            img = self.renderer.render(
                character=char_text,
                width=w,
                height=h,
                thickness=thickness
            )
            images.append(img)
            characters.append(char_text)
        
        # Create ProcessedString object
        processed = ProcessedString(
            original_text=formula,
            characters=characters,
            images=images,
            mode=RenderMode.INDIVIDUAL,
            is_formula=True
        )
        
        # Save if directory is provided
        if save_dir:
            processed.save_all(save_dir, prefix="formula")
        
        return processed
    
    def _is_formula(self, text: str) -> bool:
        """Check if text contains formula patterns"""
        for pattern in self._formula_patterns.values():
            if re.search(pattern, text):
                return True
        
        # Check for common math symbols
        math_symbols = ['∫', '∑', '∏', '√', '∞', '±', '≈', '≠', '≤', '≥', 
                       '∂', '∇', '∈', '∉', '⊂', '⊃', '∪', '∩', 'θ', 'π', 
                       'α', 'β', 'γ', 'δ', 'ε', 'λ', 'μ', 'σ', 'ω']
        
        return any(symbol in text for symbol in math_symbols)
    
    def _parse_string(self, text: str, is_formula: bool) -> List[str]:
        """Parse string into individual characters or tokens"""
        if not is_formula:
            # Simple character split for plain text
            return list(text)
        else:
            # More sophisticated parsing for formulas
            return self._tokenize_formula(text)
    
    def _tokenize_formula(self, formula: str) -> List[str]:
        """Tokenize a formula into meaningful components"""
        tokens = []
        i = 0
        
        while i < len(formula):
            char = formula[i]
            
            # Check for multi-character symbols
            if i < len(formula) - 1:
                two_char = formula[i:i+2]
                if two_char in ['==', '!=', '<=', '>=', '->', '<-', '=>']:
                    tokens.append(two_char)
                    i += 2
                    continue
            
            # Check for superscript/subscript notation
            if char == '^' and i + 1 < len(formula):
                if formula[i + 1] == '(':
                    # Find matching parenthesis
                    j = i + 2
                    depth = 1
                    while j < len(formula) and depth > 0:
                        if formula[j] == '(':
                            depth += 1
                        elif formula[j] == ')':
                            depth -= 1
                        j += 1
                    tokens.append(formula[i:j])
                    i = j
                    continue
            
            # Single character
            if char.strip():  # Ignore whitespace
                tokens.append(char)
            
            i += 1
        
        return tokens
    
    def _parse_formula(self, formula: str) -> List[dict]:
        """
        Parse formula into components with type information
        
        Returns:
            List of dicts with 'text' and 'type' keys
        """
        components = []
        tokens = self._tokenize_formula(formula)
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if token.startswith('^'):
                # Superscript
                text = token[1:].strip('()')
                components.append({'text': text, 'type': 'superscript'})
            elif token.startswith('_'):
                # Subscript
                text = token[1:]
                components.append({'text': text, 'type': 'subscript'})
            elif token == '/':
                # Fraction bar
                components.append({'text': token, 'type': 'operator'})
            else:
                # Regular character
                components.append({'text': token, 'type': 'regular'})
            
            i += 1
        
        return components
