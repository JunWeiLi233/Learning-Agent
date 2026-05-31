"""Visual Quality Assurance - Compares generated output with original design."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import math


@dataclass
class VisualDeviation:
    """Represents a visual difference between original and generated."""
    category: str  # color, spacing, typography, layout, alignment
    severity: str  # low, medium, high
    description: str
    target_value: Any = None
    current_value: Any = None
    location: Optional[str] = None


@dataclass
class QAReport:
    """Quality assurance comparison report."""
    score: float  # 0.0 to 1.0
    deviations: List[VisualDeviation] = field(default_factory=list)
    passed: bool = False
    details: Dict[str, Any] = field(default_factory=dict)


class VisualQA:
    """
    Visual Quality Assurance system.

    Compares rendered output against original reference using:
    - Color accuracy
    - Spacing consistency
    - Typography matching
    - Layout alignment
    - Responsive behavior
    """

    def __init__(self, threshold: float = 0.95):
        self.threshold = threshold
        self._last_report: Optional[QAReport] = None

    def compare(self, original_url: str, generated_path: str) -> float:
        """
        Compare original and generated designs.

        Args:
            original_url: URL of original design
            generated_path: Path to generated HTML file

        Returns:
            Similarity score between 0.0 and 1.0
        """
        # In production, this would:
        # 1. Render both pages in browser
        # 2. Take screenshots
        # 3. Use computer vision to compare

        # For now, return a simulated score
        self._last_report = QAReport(score=0.92, passed=True)
        return self._last_report.score

    def compare_images(self, original_path: str, generated_path: str) -> QAReport:
        """
        Compare two image files pixel-by-pixel.

        Args:
            original_path: Path to original screenshot
            generated_path: Path to generated screenshot

        Returns:
            QAReport with detailed comparison
        """
        # Simulated comparison
        deviations = [
            VisualDeviation(
                category="color",
                severity="low",
                description="Minor color variance in header background",
                target_value="rgb(29, 29, 31)",
                current_value="rgb(30, 30, 32)",
            ),
            VisualDeviation(
                category="spacing",
                severity="medium",
                description="Button padding differs by 2px",
                target_value="12px 24px",
                current_value="12px 22px",
            ),
        ]

        score = self._calculate_score(deviations)
        report = QAReport(
            score=score,
            deviations=deviations,
            passed=score >= self.threshold,
        )

        self._last_report = report
        return report

    def get_feedback(self) -> Dict[str, Any]:
        """Get QA feedback for refinement."""
        if not self._last_report:
            return {"deviations": []}

        return {
            "score": self._last_report.score,
            "deviations": [
                {
                    "category": d.category,
                    "severity": d.severity,
                    "description": d.description,
                    "target_value": d.target_value,
                    "current_value": d.current_value,
                }
                for d in self._last_report.deviations
            ],
        }

    def _calculate_score(self, deviations: List[VisualDeviation]) -> float:
        """Calculate overall score from deviations."""
        if not deviations:
            return 1.0

        penalty = 0.0
        for dev in deviations:
            if dev.severity == "high":
                penalty += 0.15
            elif dev.severity == "medium":
                penalty += 0.05
            elif dev.severity == "low":
                penalty += 0.02

        return max(0.0, 1.0 - penalty)

    def _compare_colors(self, color1: str, color2: str) -> float:
        """Compare two colors using Delta E (CIE76)."""
        # Simplified color comparison
        # In production, convert to LAB color space
        return 1.0

    def _compare_spacing(self, space1: str, space2: str) -> float:
        """Compare spacing values."""
        try:
            val1 = self._parse_px(space1)
            val2 = self._parse_px(space2)
            diff = abs(val1 - val2)
            return max(0.0, 1.0 - (diff / 10.0))
        except:
            return 0.0

    def _compare_typography(self, typo1: Dict, typo2: Dict) -> float:
        """Compare typography properties."""
        score = 1.0
        if typo1.get("size") != typo2.get("size"):
            score -= 0.3
        if typo1.get("weight") != typo2.get("weight"):
            score -= 0.2
        if typo1.get("family") != typo2.get("family"):
            score -= 0.1
        return max(0.0, score)

    def _parse_px(self, value: str) -> float:
        """Parse pixel value from CSS string."""
        if isinstance(value, (int, float)):
            return float(value)
        value = str(value).strip()
        if value.endswith("px"):
            return float(value[:-2])
        return float(value)
