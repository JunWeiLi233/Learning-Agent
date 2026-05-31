"""Creative Optimization - Generates and evaluates design variants."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional
import random


@dataclass
class OptimizationVariant:
    """A proposed design optimization variant."""
    name: str
    description: str
    category: str  # performance, accessibility, ux, styling
    changes: Dict[str, Any] = field(default_factory=dict)
    estimated_impact: float = 0.0  # 0.0 to 1.0
    implementation_complexity: float = 0.0  # 0.0 to 1.0
    score: float = 0.0


@dataclass
class OptimizationResult:
    """Result of optimization evaluation."""
    variant: OptimizationVariant
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    recommendation: str = ""


class CreativeOptimizer:
    """
    Creative Optimization engine.

    After achieving pixel-perfect fidelity, generates alternative solutions:
    1. Brainstorm stylistic, performance, accessibility, or UX enhancements
    2. Evaluate variants against codebase constraints
    3. Select and implement the best approach
    """

    def __init__(self):
        self._variants: List[OptimizationVariant] = []

    def brainstorm(self, design_data: Dict[str, Any]) -> List[OptimizationVariant]:
        """
        Generate optimization variants based on design data.

        Args:
            design_data: Original design data

        Returns:
            List of proposed optimization variants
        """
        variants = []

        # Performance optimizations
        variants.append(OptimizationVariant(
            name="lazy-loading",
            description="Implement lazy loading for images and below-fold content",
            category="performance",
            changes={
                "images": "add loading='lazy' attribute",
                "below_fold": "use Intersection Observer",
            },
            estimated_impact=0.8,
            implementation_complexity=0.3,
        ))

        variants.append(OptimizationVariant(
            name="critical-css",
            description="Inline critical CSS and defer non-critical styles",
            category="performance",
            changes={
                "css": "extract above-fold styles",
                "fonts": "use font-display: swap",
            },
            estimated_impact=0.7,
            implementation_complexity=0.5,
        ))

        # Accessibility improvements
        variants.append(OptimizationVariant(
            name="aria-enhancement",
            description="Add comprehensive ARIA labels and roles",
            category="accessibility",
            changes={
                "navigation": "add aria-label='Main navigation'",
                "buttons": "add aria-describedby for context",
                "images": "ensure meaningful alt text",
            },
            estimated_impact=0.6,
            implementation_complexity=0.2,
        ))

        variants.append(OptimizationVariant(
            name="keyboard-navigation",
            description="Enhance keyboard navigation and focus states",
            category="accessibility",
            changes={
                "focus": "add visible focus indicators",
                "tab_order": "ensure logical tab sequence",
                "skip_links": "add skip-to-content link",
            },
            estimated_impact=0.5,
            implementation_complexity=0.3,
        ))

        # UX enhancements
        variants.append(OptimizationVariant(
            name="micro-interactions",
            description="Add subtle hover and transition effects",
            category="ux",
            changes={
                "buttons": "add hover scale(1.02) transition",
                "links": "add underline animation",
                "cards": "add lift shadow on hover",
            },
            estimated_impact=0.4,
            implementation_complexity=0.2,
        ))

        variants.append(OptimizationVariant(
            name="responsive-typography",
            description="Implement fluid typography with clamp()",
            category="ux",
            changes={
                "headings": "use clamp() for font sizes",
                "body": "scale text based on viewport",
            },
            estimated_impact=0.6,
            implementation_complexity=0.4,
        ))

        # Styling refinements
        variants.append(OptimizationVariant(
            name="dark-mode",
            description="Add dark mode support with CSS custom properties",
            category="styling",
            changes={
                "colors": "use CSS custom properties",
                "media_query": "@media (prefers-color-scheme: dark)",
            },
            estimated_impact=0.7,
            implementation_complexity=0.5,
        ))

        variants.append(OptimizationVariant(
            name="css-grid-layout",
            description="Modernize layout with CSS Grid",
            category="styling",
            changes={
                "layout": "replace flexbox with grid where appropriate",
                "responsive": "use grid-template-areas",
            },
            estimated_impact=0.5,
            implementation_complexity=0.4,
        ))

        self._variants = variants
        return variants

    def evaluate(self, variants: List[OptimizationVariant], design_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluate variants against constraints.

        Args:
            variants: List of variants to evaluate
            design_data: Original design data for context

        Returns:
            Evaluated variants with scores
        """
        evaluated = []

        for variant in variants:
            # Calculate composite score
            score = self._calculate_score(variant)

            # Generate pros/cons
            result = OptimizationResult(
                variant=variant,
                pros=self._get_pros(variant),
                cons=self._get_cons(variant),
                recommendation=self._get_recommendation(variant, score),
            )

            variant.score = score

            evaluated.append({
                "name": variant.name,
                "description": variant.description,
                "category": variant.category,
                "score": score,
                "pros": result.pros,
                "cons": result.cons,
                "recommendation": result.recommendation,
            })

        # Sort by score
        evaluated.sort(key=lambda x: x["score"], reverse=True)

        return evaluated

    def select_best(self, evaluated: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Select the best optimization variant."""
        if not evaluated:
            return None
        return evaluated[0]

    def apply(self, variant: Dict[str, Any], output_dir: Path):
        """Apply the selected optimization variant."""
        # In production, this would modify the generated code
        # For now, just log the selection
        print(f"[Optimizer] Applied: {variant.get('name', 'unknown')}")

    def _calculate_score(self, variant: OptimizationVariant) -> float:
        """Calculate composite score for a variant."""
        # Weight: impact * (1 - complexity * 0.5)
        impact_weight = 0.6
        complexity_penalty = 0.4

        score = (
            variant.estimated_impact * impact_weight +
            (1 - variant.implementation_complexity) * complexity_penalty
        )

        return min(1.0, max(0.0, score))

    def _get_pros(self, variant: OptimizationVariant) -> List[str]:
        """Get pros for a variant."""
        pros_map = {
            "lazy-loading": [
                "Reduces initial page load time",
                "Improves Core Web Vitals scores",
                "Bandwidth-friendly for mobile users",
            ],
            "critical-css": [
                "Faster First Contentful Paint",
                "Reduces render-blocking resources",
                "Improves perceived performance",
            ],
            "aria-enhancement": [
                "Better screen reader support",
                "Improved SEO semantics",
                "WCAG 2.1 compliance",
            ],
            "keyboard-navigation": [
                "Essential for motor-impaired users",
                "Power user efficiency",
                "Required for accessibility compliance",
            ],
            "micro-interactions": [
                "Enhances user engagement",
                "Provides visual feedback",
                "Modern, polished feel",
            ],
            "responsive-typography": [
                "Optimal reading at any viewport",
                "Reduces need for media queries",
                "Future-proof scaling",
            ],
            "dark-mode": [
                "Reduces eye strain in low light",
                "Battery savings on OLED",
                "User preference satisfaction",
            ],
            "css-grid-layout": [
                "More expressive layouts",
                "Better responsive behavior",
                "Cleaner markup structure",
            ],
        }
        return pros_map.get(variant.name, ["Generic improvement"])

    def _get_cons(self, variant: OptimizationVariant) -> List[str]:
        """Get cons for a variant."""
        cons_map = {
            "lazy-loading": [
                "May affect above-fold images",
                "Requires JavaScript enabled",
            ],
            "critical-css": [
                "Requires build tooling",
                "Manual maintenance needed",
            ],
            "aria-enhancement": [
                "Increased HTML verbosity",
                "Requires ARIA knowledge",
            ],
            "keyboard-navigation": [
                "Focus management complexity",
                "Custom component challenges",
            ],
            "micro-interactions": [
                "May distract some users",
                "Performance cost on low-end devices",
            ],
            "responsive-typography": [
                "Less precise control",
                "Browser support considerations",
            ],
            "dark-mode": [
                "Requires color system refactoring",
                "Image/color asset duplication",
            ],
            "css-grid-layout": [
                "Browser support (IE11 fallback)",
                "Learning curve for grid syntax",
            ],
        }
        return cons_map.get(variant.name, ["Potential trade-offs"])

    def _get_recommendation(self, variant: OptimizationVariant, score: float) -> str:
        """Get recommendation text for a variant."""
        if score >= 0.7:
            return f"Strongly recommended: {variant.name} provides high impact with manageable complexity."
        elif score >= 0.5:
            return f"Recommended: {variant.name} offers good value. Consider implementing."
        elif score >= 0.3:
            return f"Optional: {variant.name} has moderate impact. Implement if time permits."
        else:
            return f"Low priority: {variant.name} has limited impact relative to effort."
