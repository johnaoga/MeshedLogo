"""
String Processor Module
Processes text strings and formulas, converting them to character images
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from lib.character_renderer import CharacterRenderer, CharacterImage


class RenderMode(Enum):
    """Rendering mode for strings"""
    SINGLE = "single"  # Render entire string as one image
    INDIVIDUAL = "individual"  # Render each character separately


@dataclass
class TextSegment:
    """Represents a segment of text or formula"""
    text: str
    is_formula: bool
    

@dataclass
class CharacterMetadata:
    """Metadata for character rendering"""
    char: str
    char_type: str  # 'regular', 'superscript', 'subscript', 'fraction_num', 'fraction_denom', 'fraction_bar'
    scale_factor: float = 1.0  # Relative scale (0.6 for super/subscripts)
    y_offset_factor: float = 0.0  # Vertical offset (-0.4 for superscript, 0.3 for subscript)
    

@dataclass
class ProcessedString:
    """Data class to hold processed string data"""
    original_text: str
    segments: List[TextSegment]  # List of text/formula segments
    characters: List[str]
    images: List[CharacterImage]
    metadata: List[CharacterMetadata]  # Positioning and styling info
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
    
    def process(self, text: str, mode: RenderMode = RenderMode.INDIVIDUAL,
                width: Optional[int] = None, height: Optional[int] = None,
                thickness: Optional[int] = None,
                save_dir: Optional[str] = None) -> ProcessedString:
        """
        Process a string and convert to character images.
        Supports mixed text and formulas using $ delimiters.
        
        Args:
            text: Input text with optional formulas in $...$ or $$...$$
            mode: Rendering mode (single or individual)
                  - For formulas: SINGLE renders whole formula as one image,
                                 INDIVIDUAL renders each symbol separately
            width: Image width for each character
            height: Image height for each character
            thickness: Stroke thickness
            save_dir: Optional directory to save all images
            
        Returns:
            ProcessedString object containing all character images
            
        Examples:
            - "HELLO" -> regular text, all characters rendered
            - "$e^{i\\theta}$" -> formula rendered based on mode
            - "m$e$sh" -> mixed: 'm', formula 'e', 'sh'
        """
        # Split text into text and formula segments
        segments = self._split_text_and_formulas(text)
        
        # Process each segment
        all_images = []
        all_characters = []
        all_metadata = []
        
        for segment in segments:
            if segment.is_formula:
                # Process as formula using FormulaParser
                if mode == RenderMode.SINGLE:
                    # Render entire formula as single image using matplotlib LaTeX
                    img = self.renderer.render_latex(
                        latex_formula=segment.text,
                        width=width,
                        height=height,
                        thickness=thickness
                    )
                    all_images.append(img)
                    all_characters.append(segment.text)
                    all_metadata.append(CharacterMetadata(
                        char=segment.text,
                        char_type='regular',
                        scale_factor=1.0,
                        y_offset_factor=0.0
                    ))
                else:
                    # INDIVIDUAL mode: Render each character separately
                    # For complex formulas, use SINGLE mode instead
                    for char in segment.text:
                        if not char.strip():  # Skip whitespace
                            continue
                        
                        img = self.renderer.render(
                            character=char,
                            width=width,
                            height=height,
                            thickness=thickness
                        )
                        all_images.append(img)
                        all_characters.append(char)
                        all_metadata.append(CharacterMetadata(
                            char=char,
                            char_type='regular',
                            scale_factor=1.0,
                            y_offset_factor=0.0
                        ))
            else:
                # Process as regular text (always character by character)
                for char in segment.text:
                    img = self.renderer.render(
                        character=char,
                        width=width,
                        height=height,
                        thickness=thickness
                    )
                    all_images.append(img)
                    all_characters.append(char)
                    all_metadata.append(CharacterMetadata(
                        char=char,
                        char_type='regular',
                        scale_factor=1.0,
                        y_offset_factor=0.0
                    ))
        
        # Determine if any formula was present
        has_formula = any(seg.is_formula for seg in segments)
        
        # Create ProcessedString object
        processed = ProcessedString(
            original_text=text,
            segments=segments,
            characters=all_characters,
            images=all_images,
            metadata=all_metadata,
            mode=mode,
            is_formula=has_formula
        )
        
        # Save if directory is provided
        if save_dir:
            processed.save_all(save_dir)
        
        return processed
    
    def process_formula(self, formula: str, width: Optional[int] = None,
                       height: Optional[int] = None, thickness: Optional[int] = None,
                       save_dir: Optional[str] = None) -> ProcessedString:
        """
        Process a mathematical formula with special handling.
        Formulas should be provided with $ delimiters or will be treated as formula by default.
        
        Args:
            formula: Mathematical formula string (e.g., "$e^{i\\theta}$" or "e^{i\\theta}")
            width: Image width for each character
            height: Image height for each character
            thickness: Stroke thickness
            save_dir: Optional directory to save all images
            
        Returns:
            ProcessedString object with formula components (rendered individually)
        """
        # Remove $ delimiters if present
        clean_formula = formula.strip()
        if clean_formula.startswith('$$') and clean_formula.endswith('$$'):
            clean_formula = clean_formula[2:-2]
        elif clean_formula.startswith('$') and clean_formula.endswith('$'):
            clean_formula = clean_formula[1:-1]
        
        # Render each character separately
        # For complex formulas with proper formatting, use SINGLE mode instead
        images = []
        characters = []
        metadata = []
        
        for char in clean_formula:
            if not char.strip():  # Skip whitespace
                continue
            
            img = self.renderer.render(
                character=char,
                width=width,
                height=height,
                thickness=thickness
            )
            images.append(img)
            characters.append(char)
            metadata.append(CharacterMetadata(
                char=char,
                char_type='regular',
                scale_factor=1.0,
                y_offset_factor=0.0
            ))
        
        # Create segment
        segment = TextSegment(text=clean_formula, is_formula=True)
        
        # Create ProcessedString object
        processed = ProcessedString(
            original_text=formula,
            segments=[segment],
            characters=characters,
            images=images,
            metadata=metadata,
            mode=RenderMode.INDIVIDUAL,
            is_formula=True
        )
        
        # Save if directory is provided
        if save_dir:
            processed.save_all(save_dir, prefix="formula")
        
        return processed
    
    def _split_text_and_formulas(self, text: str) -> List[TextSegment]:
        r"""
        Split text into segments of regular text and formulas.
        Formulas are enclosed in $ or $$. Escaped \$ is treated as literal $.
        
        Args:
            text: Input text with optional formula delimiters
            
        Returns:
            List of TextSegment objects
            
        Examples:
            - "HELLO" -> [TextSegment("HELLO", False)]
            - "$e$" -> [TextSegment("e", True)]
            - "m$e$sh" -> [TextSegment("m", False), TextSegment("e", True), TextSegment("sh", False)]
            - "price is \$5" -> [TextSegment("price is $5", False)]
        """
        segments = []
        current_text = ""
        i = 0
        
        while i < len(text):
            # Check for escaped $
            if i < len(text) - 1 and text[i:i+2] == '\\$':
                current_text += '$'
                i += 2
                continue
            
            # Check for $$ delimiter
            if i < len(text) - 1 and text[i:i+2] == '$$':
                # Save current text segment if any
                if current_text:
                    segments.append(TextSegment(text=current_text, is_formula=False))
                    current_text = ""
                
                # Find closing $$
                j = i + 2
                while j < len(text) - 1:
                    if text[j:j+2] == '$$':
                        formula_text = text[i+2:j]
                        segments.append(TextSegment(text=formula_text, is_formula=True))
                        i = j + 2
                        break
                    j += 1
                else:
                    # No closing $$, treat as literal
                    current_text += text[i]
                    i += 1
                continue
            
            # Check for single $ delimiter
            if text[i] == '$':
                # Save current text segment if any
                if current_text:
                    segments.append(TextSegment(text=current_text, is_formula=False))
                    current_text = ""
                
                # Find closing $
                j = i + 1
                while j < len(text):
                    if text[j] == '$' and (j == 0 or text[j-1] != '\\'):
                        formula_text = text[i+1:j]
                        segments.append(TextSegment(text=formula_text, is_formula=True))
                        i = j + 1
                        break
                    j += 1
                else:
                    # No closing $, treat as literal
                    current_text += text[i]
                    i += 1
                continue
            
            # Regular character
            current_text += text[i]
            i += 1
        
        # Add final text segment if any
        if current_text:
            segments.append(TextSegment(text=current_text, is_formula=False))
        
        # If no segments, return empty text segment
        if not segments:
            segments.append(TextSegment(text="", is_formula=False))
        
        return segments
    
    def _is_formula(self, text: str) -> bool:
        """
        Check if text contains formula patterns.
        Now primarily checks for $ delimiters.
        """
        # Check for formula delimiters
        if '$' in text and '\\$' not in text:
            return True
        
        # Check for common math symbols
        math_symbols = ['∫', '∑', '∏', '√', '∞', '±', '≈', '≠', '≤', '≥', 
                       '∂', '∇', '∈', '∉', '⊂', '⊃', '∪', '∩', 'θ', 'π', 
                       'α', 'β', 'γ', 'δ', 'ε', 'λ', 'μ', 'σ', 'ω', '\\int',
                       '\\sum', '\\prod', '\\sqrt']
        
        return any(symbol in text for symbol in math_symbols)
    
    def _parse_string(self, text: str, is_formula: bool) -> List[str]:
        """
        Parse string into individual characters or tokens.
        Note: This is now primarily used internally. Use process() instead.
        """
        if not is_formula:
            # Simple character split for plain text
            return list(text)
        else:
            # More sophisticated parsing for formulas
            return self._tokenize_formula(text)
    
    def _tokenize_formula(self, formula: str) -> List[str]:
        """
        Tokenize a formula into meaningful components.
        Handles LaTeX-style notation and special math symbols.
        """
        tokens = []
        i = 0
        
        while i < len(formula):
            char = formula[i]
            
            # Check for LaTeX commands (\command)
            if char == '\\':
                j = i + 1
                while j < len(formula) and formula[j].isalpha():
                    j += 1
                if j > i + 1:
                    tokens.append(formula[i:j])
                    i = j
                    continue
            
            # Check for braces {} (used for grouping in formulas)
            if char in ['{', '}']:
                # Skip braces, process content inside
                i += 1
                continue
            
            # Check for multi-character symbols
            if i < len(formula) - 1:
                two_char = formula[i:i+2]
                if two_char in ['==', '!=', '<=', '>=', '->', '<-', '=>']:
                    tokens.append(two_char)
                    i += 2
                    continue
            
            # Check for superscript notation (^ with parentheses)
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
            
            # Check for subscript notation (_ with parentheses)
            if char == '_' and i + 1 < len(formula):
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
