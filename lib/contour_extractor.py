"""
Contour Extractor Module
Extracts contour and outline points from images
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from PIL import Image
import cv2


@dataclass
class ContourData:
    """Data class to hold contour extraction results"""
    points: np.ndarray  # Array of (x, y) coordinates
    image_shape: Tuple[int, int]
    num_points: int
    is_closed: bool = True
    hierarchy: Optional[np.ndarray] = None
    
    def save_points(self, filepath: str) -> str:
        """
        Save contour points to a file
        
        Args:
            filepath: Path to save points (supports .npy, .txt, .csv)
            
        Returns:
            Saved file path
        """
        if filepath.endswith('.npy'):
            np.save(filepath, self.points)
        elif filepath.endswith('.csv'):
            np.savetxt(filepath, self.points, delimiter=',', 
                      header='x,y', comments='')
        else:  # .txt or default
            np.savetxt(filepath, self.points, delimiter=' ')
        
        return filepath
    
    def get_bounding_box(self) -> Tuple[int, int, int, int]:
        """
        Get bounding box of contour
        
        Returns:
            Tuple of (x_min, y_min, x_max, y_max)
        """
        if len(self.points) == 0:
            return (0, 0, 0, 0)
        
        x_coords = self.points[:, 0]
        y_coords = self.points[:, 1]
        
        return (int(x_coords.min()), int(y_coords.min()),
                int(x_coords.max()), int(y_coords.max()))
    
    def simplify(self, epsilon: float = 2.0) -> 'ContourData':
        """
        Simplify contour using Douglas-Peucker algorithm
        
        Args:
            epsilon: Maximum distance from original contour
            
        Returns:
            New ContourData with simplified points
        """
        if len(self.points) < 3:
            return self
        
        # Reshape for cv2.approxPolyDP
        contour = self.points.reshape(-1, 1, 2).astype(np.float32)
        simplified = cv2.approxPolyDP(contour, epsilon, self.is_closed)
        simplified_points = simplified.reshape(-1, 2)
        
        return ContourData(
            points=simplified_points,
            image_shape=self.image_shape,
            num_points=len(simplified_points),
            is_closed=self.is_closed,
            hierarchy=self.hierarchy
        )


class ContourExtractor:
    """
    Extracts contours and outline points from images
    Supports various image formats and contour detection methods
    """
    
    def __init__(self, method: str = 'opencv'):
        """
        Initialize the contour extractor
        
        Args:
            method: Extraction method ('opencv', 'canny', 'threshold')
        """
        self.method = method
    
    def extract(self, image_input, threshold: int = 127,
                simplify: bool = False, epsilon: float = 2.0) -> List[ContourData]:
        """
        Extract contours from an image
        
        Args:
            image_input: Can be:
                - numpy array (binary or grayscale)
                - PIL Image
                - file path (string)
            threshold: Threshold value for binarization
            simplify: Whether to simplify contours
            epsilon: Simplification tolerance
            
        Returns:
            List of ContourData objects, one per detected contour
        """
        # Load/convert image to numpy array
        img_array = self._load_image(image_input)
        
        # Convert to binary if needed
        binary = self._binarize(img_array, threshold)
        
        # Extract contours based on method
        if self.method == 'opencv':
            contours_list = self._extract_opencv(binary)
        elif self.method == 'canny':
            contours_list = self._extract_canny(img_array, binary)
        else:  # threshold method
            contours_list = self._extract_opencv(binary)
        
        # Simplify if requested
        if simplify:
            contours_list = [c.simplify(epsilon) for c in contours_list]
        
        return contours_list
    
    def extract_largest(self, image_input, threshold: int = 127,
                       simplify: bool = False, epsilon: float = 2.0) -> Optional[ContourData]:
        """
        Extract only the largest contour from an image
        
        Args:
            image_input: Image input (various formats supported)
            threshold: Threshold value for binarization
            simplify: Whether to simplify contour
            epsilon: Simplification tolerance
            
        Returns:
            ContourData for largest contour, or None if no contours found
        """
        contours = self.extract(image_input, threshold, simplify, epsilon)
        
        if not contours:
            return None
        
        # Find largest by number of points
        largest = max(contours, key=lambda c: c.num_points)
        return largest
    
    def extract_outer_boundary(self, image_input, threshold: int = 127,
                              num_points: Optional[int] = None) -> Optional[ContourData]:
        """
        Extract outer boundary of image content
        
        Args:
            image_input: Image input
            threshold: Threshold value
            num_points: If specified, resample to this many points
            
        Returns:
            ContourData for outer boundary
        """
        # Load and binarize image
        img_array = self._load_image(image_input)
        binary = self._binarize(img_array, threshold)
        
        # Find contours with hierarchy
        contours, hierarchy = cv2.findContours(
            binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        if len(contours) == 0:
            return None
        
        # Find the outermost contour (parent = -1)
        if hierarchy is not None:
            for i, h in enumerate(hierarchy[0]):
                if h[3] == -1:  # No parent
                    contour_points = contours[i].reshape(-1, 2)
                    
                    # Resample if requested
                    if num_points is not None and len(contour_points) != num_points:
                        contour_points = self._resample_contour(contour_points, num_points)
                    
                    return ContourData(
                        points=contour_points,
                        image_shape=binary.shape,
                        num_points=len(contour_points),
                        is_closed=True,
                        hierarchy=h
                    )
        
        # Fallback: return largest contour
        return self.extract_largest(binary, threshold)
    
    def _load_image(self, image_input) -> np.ndarray:
        """Load image from various input types"""
        if isinstance(image_input, str):
            # File path
            img = Image.open(image_input)
            return np.array(img)
        elif isinstance(image_input, Image.Image):
            # PIL Image
            return np.array(image_input)
        elif isinstance(image_input, np.ndarray):
            # Already numpy array
            return image_input
        else:
            raise ValueError(f"Unsupported image input type: {type(image_input)}")
    
    def _binarize(self, img_array: np.ndarray, threshold: int) -> np.ndarray:
        """Convert image to binary"""
        # Convert to grayscale if needed
        if len(img_array.shape) == 3:
            img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            img_gray = img_array.copy()
        
        # Ensure the array is in 0-255 range
        if img_gray.max() <= 1.0:
            # If values are 0-1, scale to 0-255
            # CharacterRenderer produces 0=character, 1=background
            # OpenCV needs 255=character, 0=background, so invert after scaling
            img_gray = (img_gray * 255).astype(np.uint8)
            img_gray = cv2.bitwise_not(img_gray)  # Invert: now 255=character, 0=background
        else:
            img_gray = img_gray.astype(np.uint8)
            # For regular images, check if we need to invert
            # If background is brighter than foreground, invert
            if np.mean(img_gray) > 127:
                img_gray = cv2.bitwise_not(img_gray)
        
        # Apply threshold to ensure clean binary
        _, binary = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
        
        return binary.astype(np.uint8)
    
    def _extract_opencv(self, binary: np.ndarray) -> List[ContourData]:
        """Extract contours using OpenCV"""
        contours, hierarchy = cv2.findContours(
            binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        result = []
        for i, contour in enumerate(contours):
            points = contour.reshape(-1, 2)
            
            # Filter out very small contours
            if len(points) < 3:
                continue
            
            hier = hierarchy[0][i] if hierarchy is not None else None
            
            result.append(ContourData(
                points=points,
                image_shape=binary.shape,
                num_points=len(points),
                is_closed=True,
                hierarchy=hier
            ))
        
        return result
    
    def _extract_canny(self, img_array: np.ndarray, 
                       binary: np.ndarray) -> List[ContourData]:
        """Extract contours using Canny edge detection"""
        # Convert to grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        
        # Apply Canny edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours in edge image
        contours, hierarchy = cv2.findContours(
            edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        result = []
        for i, contour in enumerate(contours):
            points = contour.reshape(-1, 2)
            
            if len(points) < 3:
                continue
            
            hier = hierarchy[0][i] if hierarchy is not None else None
            
            result.append(ContourData(
                points=points,
                image_shape=edges.shape,
                num_points=len(points),
                is_closed=False,  # Canny edges may not be closed
                hierarchy=hier
            ))
        
        return result
    
    def _resample_contour(self, points: np.ndarray, num_points: int) -> np.ndarray:
        """Resample contour to have specific number of points"""
        if len(points) == num_points:
            return points
        
        # Calculate cumulative arc length
        distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
        cumulative = np.concatenate([[0], np.cumsum(distances)])
        
        # Create evenly spaced samples
        total_length = cumulative[-1]
        sample_points = np.linspace(0, total_length, num_points)
        
        # Interpolate x and y coordinates
        new_x = np.interp(sample_points, cumulative, points[:, 0])
        new_y = np.interp(sample_points, cumulative, points[:, 1])
        
        return np.column_stack([new_x, new_y])
