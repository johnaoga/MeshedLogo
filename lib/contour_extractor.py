"""
Contour Extractor Module
Extracts contour and outline points from images
"""

from dataclasses import dataclass
from typing import List, Tuple, Optional
import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt


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
            filepath: Path to save points (supports .npy, .txt, .csv, .png)
            
        Returns:
            Saved file path
        """
        if filepath.endswith('.npy'):
            np.save(filepath, self.points)
        elif filepath.endswith('.csv'):
            np.savetxt(filepath, self.points, delimiter=',', 
                      header='x,y', comments='')
        elif filepath.endswith('.png'):
            # Visualize contour as PNG
            fig, ax = plt.subplots(1, 1, figsize=(10, 10), facecolor='white')
            ax.set_facecolor('white')
            ax.set_aspect('equal')
            
            # Plot the contour points
            if self.is_closed:
                # Close the contour by adding first point at end
                plot_points = np.vstack([self.points, self.points[0]])
                ax.plot(plot_points[:, 0], plot_points[:, 1], 
                       'b-', linewidth=2, label='Contour')
                ax.fill(plot_points[:, 0], plot_points[:, 1], 
                       'cyan', alpha=0.3)
            else:
                ax.plot(self.points[:, 0], self.points[:, 1], 
                       'b-', linewidth=2, label='Contour')
            
            # Plot points
            ax.scatter(self.points[:, 0], self.points[:, 1], 
                      c='red', s=20, zorder=5, label='Points')
            
            # Add grid and labels
            ax.grid(True, alpha=0.3)
            ax.legend(loc='upper right')
            ax.set_title(f'Contour Visualization ({self.num_points} points)')
            ax.set_xlabel('X coordinate')
            ax.set_ylabel('Y coordinate')
            
            # Set limits with padding
            if len(self.points) > 0:
                x_min, x_max = self.points[:, 0].min(), self.points[:, 0].max()
                y_min, y_max = self.points[:, 1].min(), self.points[:, 1].max()
                padding = 0.1 * max(x_max - x_min, y_max - y_min)
                ax.set_xlim(x_min - padding, x_max + padding)
                ax.set_ylim(y_min - padding, y_max + padding)
            
            # Invert y-axis to match image coordinates
            ax.invert_yaxis()
            
            plt.tight_layout()
            plt.savefig(filepath, dpi=150, bbox_inches='tight')
            plt.close(fig)
            print(f"Contour visualization saved to {filepath}")
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
    
    def extract_with_openings(self, image_input, threshold: int = 127,
                             simplify: bool = False, epsilon: float = 2.0) -> Tuple[Optional[ContourData], List[ContourData]]:
        """
        Extract largest contour and detect all holes INCLUDING openings
        
        Detects:
        - Traditional holes (like in 'A', 'O', 'B')
        - Openings/gaps connected to edges (like in 'C', 'U', 'H')
        
        Uses flood fill: fills the character + true holes, leaving openings as contours.
        
        Args:
            image_input: Image input (various formats supported)
            threshold: Threshold value for binarization
            simplify: Whether to simplify contours
            epsilon: Simplification tolerance
            
        Returns:
            Tuple of (largest_contour, list_of_all_holes_including_openings)
        """
        # Load and binarize image
        img_array = self._load_image(image_input)
        binary = self._binarize(img_array, threshold)
        
        # Find all traditional contours
        all_contours = self.extract(image_input, threshold, simplify, epsilon)
        if not all_contours:
            return None, []
        
        # Get largest contour (character boundary)
        largest_contour = max(all_contours, key=lambda c: c.num_points)
        
        # binary: 255 = character, 0 = background
        # Get convex hull of the contour - this fills ALL concave regions
        hull = cv2.convexHull(largest_contour.points.astype(np.int32))
        
        # Fill the convex hull
        filled_hull = np.zeros_like(binary)
        cv2.fillConvexPoly(filled_hull, hull, 255)
        
        # Now find gaps: background pixels that are INSIDE the convex hull
        # These are openings (like in 'C', 'U', 'H') or holes (like in 'A')
        gaps = (filled_hull == 255) & (binary == 0)
        
        # Find contours of all gaps
        gap_contours, _ = cv2.findContours(
            gaps.astype(np.uint8) * 255,
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        holes = []
        for contour in gap_contours:
            if len(contour) >= 3:
                points = contour.reshape(-1, 2)
                if simplify:
                    contour_reshaped = points.reshape(-1, 1, 2).astype(np.float32)
                    simplified = cv2.approxPolyDP(contour_reshaped, epsilon, True)
                    points = simplified.reshape(-1, 2)
                
                hole_data = ContourData(
                    points=points,
                    image_shape=binary.shape,
                    num_points=len(points),
                    is_closed=True
                )
                holes.append(hole_data)
        
        return largest_contour, holes
    
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
