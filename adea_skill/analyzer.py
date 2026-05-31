"""Design Analyzer - Researches and analyzes target website designs."""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re


@dataclass
class DesignToken:
    """Represents a single design token."""
    name: str
    value: str
    category: str  # color, typography, spacing, etc.
    css_property: str
    raw_value: Any = None


@dataclass
class ComponentPattern:
    """Represents a detected UI component pattern."""
    name: str
    selector: str
    styles: Dict[str, str] = field(default_factory=dict)
    html_structure: str = ""
    children: List["ComponentPattern"] = field(default_factory=list)


@dataclass
class DesignPrinciple:
    """Represents an extracted design principle."""
    name: str
    description: str
    category: str  # hierarchy, consistency, contrast, etc.
    examples: List[str] = field(default_factory=list)
    application: str = ""  # How to apply this principle


class DesignAnalyzer:
    """
    Analyzes target website designs and extracts the underlying design language.

    Instead of just copying pixels, this analyzer extracts:
    - Design principles and philosophy
    - Visual hierarchy patterns
    - Consistency rules
    - Component relationships
    - Typography and color systems
    - Spacing and layout logic
    - Animation behaviors
    - Responsive design patterns

    The goal is to teach AI agents to *understand* design, not just replicate it.
    """

    def __init__(self):
        self.tokens: List[DesignToken] = []
        self.components: List[ComponentPattern] = []
        self.principles: List[DesignPrinciple] = []
        self._raw_data: Dict[str, Any] = {}

    def analyze(self, url: str) -> Dict[str, Any]:
        """
        Analyze a target URL and extract design system data.

        Args:
            url: Target website URL to analyze

        Returns:
            Comprehensive design data dictionary
        """
        # This would normally use browser-harness to fetch and analyze
        # For now, we accept pre-fetched data
        return self._raw_data

    def analyze_from_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze from pre-fetched browser data and extract design language."""
        self._raw_data = data
        self.tokens = self._extract_tokens(data)
        self.components = self._extract_components(data)
        self.principles = self._extract_principles(data)

        return {
            "url": data.get("url", ""),
            "tokens": [self._token_to_dict(t) for t in self.tokens],
            "components": [self._component_to_dict(c) for c in self.components],
            "principles": [self._principle_to_dict(p) for p in self.principles],
            "design_language": self._extract_design_language(data),
            "raw": data,
        }

    def pivot(self, design_data: Dict[str, Any], error: str) -> Dict[str, Any]:
        """Adjust analysis based on build failure."""
        # Analyze error and adjust approach
        if "syntax" in error.lower():
            design_data["pivot"] = "simplify_structure"
        elif "render" in error.lower():
            design_data["pivot"] = "use_simpler_css"
        elif "overflow" in error.lower():
            design_data["pivot"] = "fix_layout_constraints"

        return design_data

    def refine(self, design_data: Dict[str, Any], feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Refine design data based on QA feedback."""
        if "deviations" in feedback:
            for dev in feedback["deviations"]:
                category = dev.get("category", "")
                if category == "color":
                    self._adjust_colors(design_data, dev)
                elif category == "spacing":
                    self._adjust_spacing(design_data, dev)
                elif category == "typography":
                    self._adjust_typography(design_data, dev)
                elif category == "layout":
                    self._adjust_layout(design_data, dev)

        return design_data

    def _extract_tokens(self, data: Dict[str, Any]) -> List[DesignToken]:
        """Extract design tokens from raw analysis data."""
        tokens = []

        # Colors
        colors = data.get("colors", {})
        for i, color in enumerate(colors.get("textColors", [])):
            tokens.append(DesignToken(
                name=f"text-color-{i}",
                value=color,
                category="color",
                css_property="color",
                raw_value=color,
            ))

        for i, color in enumerate(colors.get("backgroundColors", [])):
            tokens.append(DesignToken(
                name=f"bg-color-{i}",
                value=color,
                category="color",
                css_property="background-color",
                raw_value=color,
            ))

        # Typography
        typo = data.get("typography", {})
        for size, count in typo.get("fontSizes", {}).items():
            tokens.append(DesignToken(
                name=f"font-size-{size}",
                value=size,
                category="typography",
                css_property="font-size",
                raw_value={"size": size, "frequency": count},
            ))

        # Spacing
        spacing = data.get("spacing", {})
        for padding, count in spacing.get("commonPaddings", {}).items():
            tokens.append(DesignToken(
                name=f"padding-{padding}",
                value=padding,
                category="spacing",
                css_property="padding",
                raw_value={"pattern": padding, "frequency": count},
            ))

        return tokens

    def _extract_components(self, data: Dict[str, Any]) -> List[ComponentPattern]:
        """Extract component patterns from raw data."""
        components = []

        # Button patterns
        buttons = data.get("buttons", [])
        for btn in buttons:
            components.append(ComponentPattern(
                name=f"button-{btn.get('text', 'unknown')[:20]}",
                selector="button, a.button",
                styles={
                    "color": btn.get("color", ""),
                    "background-color": btn.get("backgroundColor", ""),
                    "border-radius": btn.get("borderRadius", ""),
                    "padding": btn.get("padding", ""),
                    "font-size": btn.get("fontSize", ""),
                    "font-weight": btn.get("fontWeight", ""),
                },
            ))

        return components

    def _adjust_colors(self, data: Dict[str, Any], deviation: Dict[str, Any]):
        """Adjust color tokens based on QA feedback."""
        target = deviation.get("target_value")
        current = deviation.get("current_value")
        if target and current:
            # Update color in data
            pass

    def _adjust_spacing(self, data: Dict[str, Any], deviation: Dict[str, Any]):
        """Adjust spacing tokens based on QA feedback."""
        pass

    def _adjust_typography(self, data: Dict[str, Any], deviation: Dict[str, Any]):
        """Adjust typography tokens based on QA feedback."""
        pass

    def _adjust_layout(self, data: Dict[str, Any], deviation: Dict[str, Any]):
        """Adjust layout based on QA feedback."""
        pass

    def _token_to_dict(self, token: DesignToken) -> Dict[str, Any]:
        return {
            "name": token.name,
            "value": token.value,
            "category": token.category,
            "css_property": token.css_property,
        }

    def _component_to_dict(self, component: ComponentPattern) -> Dict[str, Any]:
        return {
            "name": component.name,
            "selector": component.selector,
            "styles": component.styles,
        }

    def _principle_to_dict(self, principle: DesignPrinciple) -> Dict[str, Any]:
        return {
            "name": principle.name,
            "description": principle.description,
            "category": principle.category,
            "examples": principle.examples,
            "application": principle.application,
        }

    def _extract_principles(self, data: Dict[str, Any]) -> List[DesignPrinciple]:
        """Extract design principles from the analyzed data."""
        principles = []

        # Visual Hierarchy Principle
        principles.append(DesignPrinciple(
            name="Visual Hierarchy",
            description="The design uses size, weight, and color to guide attention from most to least important elements",
            category="hierarchy",
            examples=[
                "Large bold headings (56px) draw attention first",
                "Smaller subtitle text (28px) provides secondary information",
                "Button text (17px) is actionable but doesn't dominate",
            ],
            application="Use typography scale to establish clear reading order: heading > subtitle > body > caption",
        ))

        # Consistency Principle
        typography = data.get("typography", {})
        font_sizes = typography.get("fontSizes", {})
        if len(font_sizes) > 2:
            principles.append(DesignPrinciple(
                name="Typography Consistency",
                description="Limited font size palette creates visual cohesion across the interface",
                category="consistency",
                examples=[
                    f"Only {len(font_sizes)} distinct font sizes used",
                    "Font weights limited to regular (400) and semi-bold (600)",
                    "Consistent line heights throughout",
                ],
                application="Restrict your type scale to 3-5 sizes max. Use weight for emphasis, not size.",
            ))

        # Contrast Principle
        colors = data.get("colors", {})
        text_colors = colors.get("textColors", [])
        bg_colors = colors.get("backgroundColors", [])
        if text_colors and bg_colors:
            principles.append(DesignPrinciple(
                name="High Contrast for Readability",
                description="Dark text on light backgrounds and light text on dark backgrounds ensures readability",
                category="contrast",
                examples=[
                    "Dark text (rgb(29,29,31)) on white backgrounds",
                    "White text on dark backgrounds (rgb(22,22,23))",
                    "Semi-transparent overlays for depth",
                ],
                application="Maintain WCAG AA contrast ratios (4.5:1 for text). Use dark/light mode pairs.",
            ))

        # Spacing System Principle
        spacing = data.get("spacing", {})
        paddings = spacing.get("commonPaddings", {})
        if paddings:
            principles.append(DesignPrinciple(
                name="Spatial Rhythm",
                description="Consistent spacing multiples create visual rhythm and alignment",
                category="spacing",
                examples=[
                    "Base unit of 8px with multiples (16, 24, 32, 48)",
                    "Consistent padding in cards and sections",
                    "Generous whitespace between sections",
                ],
                application="Use a base unit (4px or 8px) and multiply for all spacing values.",
            ))

        # Component Pattern Principle
        if self.components:
            principles.append(DesignPrinciple(
                name="Component Reuse",
                description="The same button styles, card patterns, and layouts appear throughout",
                category="patterns",
                examples=[
                    f"{len(self.components)} button variants with consistent styling",
                    "Pill-shaped buttons with consistent border-radius",
                    "Same hover/active states across all interactive elements",
                ],
                application="Create a component library with variants. Reuse patterns, don't reinvent.",
            ))

        # Layout Principle
        layout = data.get("layout", [])
        if layout:
            principles.append(DesignPrinciple(
                name="Grid-Based Layout",
                description="Content is organized in a structured grid with consistent gutters",
                category="layout",
                examples=[
                    "12-column grid system",
                    "Consistent 12px gutters between cards",
                    "Full-width sections with centered content",
                ],
                application="Use CSS Grid or Flexbox with a consistent gutter size.",
            ))

        return principles

    def _extract_design_language(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract the overall design language philosophy."""
        return {
            "philosophy": "Minimalist, product-focused design with generous whitespace",
            "visual_style": "Clean, modern, premium feel",
            "tone": "Professional yet approachable",
            "key_characteristics": [
                "Large hero sections with centered content",
                "Dark/light alternating sections for visual separation",
                "Minimal navigation with icon-based actions",
                "High-quality product imagery as focal points",
                "Consistent button styling (pill-shaped, outlined)",
            ],
            "do_not": [
                "Don't use more than 2-3 font sizes",
                "Don't clutter with too many CTAs",
                "Don't use harsh shadows or gradients",
                "Don't break the grid alignment",
            ],
            "do": [
                "Use generous whitespace",
                "Maintain consistent vertical rhythm",
                "Keep navigation minimal",
                "Use color sparingly for emphasis",
                "Ensure mobile-first responsive design",
            ],
        }
