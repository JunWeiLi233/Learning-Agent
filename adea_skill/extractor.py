"""Design System Extractor - Documents extracted design systems."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


@dataclass
class ColorPalette:
    """Extracted color palette."""
    primary: str = ""
    secondary: str = ""
    accent: str = ""
    background: str = ""
    surface: str = ""
    text: str = ""
    text_secondary: str = ""
    border: str = ""
    custom: Dict[str, str] = field(default_factory=dict)


@dataclass
class TypographySystem:
    """Extracted typography system."""
    font_family: str = ""
    font_families: List[str] = field(default_factory=list)
    base_size: str = "16px"
    scale_ratio: float = 1.25
    weights: Dict[str, str] = field(default_factory=dict)
    sizes: Dict[str, str] = field(default_factory=dict)


@dataclass
class SpacingSystem:
    """Extracted spacing system."""
    base_unit: str = "8px"
    scale: List[str] = field(default_factory=list)
    padding: Dict[str, str] = field(default_factory=dict)
    margin: Dict[str, str] = field(default_factory=dict)
    gap: str = "8px"


@dataclass
class ComponentSpec:
    """Specification for a reusable component."""
    name: str
    selector: str
    description: str = ""
    variants: List[str] = field(default_factory=list)
    props: Dict[str, str] = field(default_factory=dict)
    styles: Dict[str, str] = field(default_factory=dict)
    html_structure: str = ""


@dataclass
class DesignSystem:
    """Complete extracted design system."""
    name: str
    url: str
    extracted_at: str = ""
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: TypographySystem = field(default_factory=TypographySystem)
    spacing: SpacingSystem = field(default_factory=SpacingSystem)
    components: List[ComponentSpec] = field(default_factory=list)
    layout_patterns: Dict[str, Any] = field(default_factory=dict)
    animations: Dict[str, Any] = field(default_factory=dict)
    responsive_breakpoints: Dict[str, str] = field(default_factory=dict)


class DesignSystemExtractor:
    """
    Extracts and documents design systems from analyzed data.

    Outputs structured Markdown documentation as the immutable source of truth.
    """

    def __init__(self):
        self._system: Optional[DesignSystem] = None

    def extract(self, design_data: Dict[str, Any]) -> DesignSystem:
        """
        Extract design system from analyzed data.

        Args:
            design_data: Data from DesignAnalyzer

        Returns:
            Complete DesignSystem
        """
        system = DesignSystem(
            name=design_data.get("name", "Extracted Design"),
            url=design_data.get("url", ""),
            extracted_at=datetime.now().isoformat(),
        )

        # Extract colors
        system.colors = self._extract_colors(design_data)

        # Extract typography
        system.typography = self._extract_typography(design_data)

        # Extract spacing
        system.spacing = self._extract_spacing(design_data)

        # Extract components
        system.components = self._extract_components(design_data)

        # Extract layout patterns
        system.layout_patterns = design_data.get("layout", {})

        # Set responsive breakpoints
        system.responsive_breakpoints = {
            "mobile": "320px",
            "tablet": "768px",
            "desktop": "1024px",
            "wide": "1440px",
        }

        self._system = system
        return system

    def write_documentation(self, system: DesignSystem, output_path: Path):
        """
        Write design system documentation to Markdown file.

        Args:
            system: DesignSystem to document
            output_path: Path to write the .md file
        """
        content = self._generate_markdown(system)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    def _extract_colors(self, data: Dict[str, Any]) -> ColorPalette:
        """Extract color palette from design data."""
        # Colors may be in "raw" or at top level
        raw = data.get("raw", data)
        colors = raw.get("colors", {})
        text_colors = colors.get("textColors", [])
        bg_colors = colors.get("backgroundColors", [])

        palette = ColorPalette()

        # Map extracted colors to palette roles
        if text_colors:
            palette.text = text_colors[0] if text_colors else ""
            palette.text_secondary = text_colors[1] if len(text_colors) > 1 else ""

        if bg_colors:
            palette.background = bg_colors[0] if bg_colors else ""
            palette.surface = bg_colors[1] if len(bg_colors) > 1 else ""

        # Extract additional custom colors
        for i, color in enumerate(text_colors[2:], start=1):
            palette.custom[f"text-{i}"] = color

        for i, color in enumerate(bg_colors[2:], start=1):
            palette.custom[f"surface-{i}"] = color

        return palette

    def _extract_typography(self, data: Dict[str, Any]) -> TypographySystem:
        """Extract typography system from design data."""
        raw = data.get("raw", data)
        typo = raw.get("typography", {})

        system = TypographySystem(
            font_family=typo.get("primaryFont", ""),
            base_size="17px",
        )

        # Parse font sizes
        font_sizes = typo.get("fontSizes", {})
        for size, count in sorted(font_sizes.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                system.sizes[f"size-{len(system.sizes) + 1}"] = size

        # Parse font weights
        font_weights = typo.get("fontWeights", {})
        weight_map = {
            "100": "Thin",
            "200": "Extra Light",
            "300": "Light",
            "400": "Regular",
            "500": "Medium",
            "600": "Semi Bold",
            "700": "Bold",
            "800": "Extra Bold",
            "900": "Black",
        }
        for weight, count in font_weights.items():
            if count > 0 and weight in weight_map:
                system.weights[weight_map[weight]] = weight

        return system

    def _extract_spacing(self, data: Dict[str, Any]) -> SpacingSystem:
        """Extract spacing system from design data."""
        raw = data.get("raw", data)
        spacing = raw.get("spacing", {})

        system = SpacingSystem(
            base_unit="8px",
            scale=[
                "4px", "8px", "12px", "16px", "20px",
                "24px", "32px", "40px", "48px", "64px",
            ],
        )

        # Extract common padding patterns
        paddings = spacing.get("commonPaddings", {})
        for pattern, count in sorted(paddings.items(), key=lambda x: x[1], reverse=True):
            if count > 1:
                system.padding[f"pattern-{len(system.padding) + 1}"] = pattern

        return system

    def _extract_components(self, data: Dict[str, Any]) -> List[ComponentSpec]:
        """Extract component specifications."""
        components = []
        raw = data.get("raw", data)
        raw_components = raw.get("components", data.get("components", []))

        for comp in raw_components:
            spec = ComponentSpec(
                name=comp.get("name", "Unknown Component"),
                selector=comp.get("selector", ""),
                styles=comp.get("styles", {}),
            )
            components.append(spec)

        return components

    def _generate_markdown(self, system: DesignSystem) -> str:
        """Generate Markdown documentation for the design system."""
        md = f"""# Design System: {system.name}

> Extracted from [{system.url}]({system.url})
> Generated: {system.extracted_at}

---

## Color Palette

### Primary Colors

| Token | Value | Usage |
|-------|-------|-------|
| `--text-color` | `{system.colors.text}` | Primary text |
| `--text-secondary` | `{system.colors.text_secondary}` | Secondary text |
| `--bg-color` | `{system.colors.background}` | Page background |
| `--surface` | `{system.colors.surface}` | Card/panel background |

### Custom Colors

| Token | Value |
|-------|-------|
"""
        for name, value in system.colors.custom.items():
            md += f"| `--{name}` | `{value}` |\n"

        md += f"""

---

## Typography

### Font Stack

```css
font-family: {system.typography.font_family};
```

### Font Scale

| Token | Size | Usage |
|-------|------|-------|
"""
        for name, size in system.typography.sizes.items():
            md += f"| `--{name}` | {size} | Body text |\n"

        md += f"""

### Font Weights

| Name | Value |
|------|-------|
"""
        for name, value in system.typography.weights.items():
            md += f"| {name} | {value} |\n"

        md += f"""

---

## Spacing

### Base Unit

```css
--spacing-base: {system.spacing.base_unit};
```

### Scale

```css
{chr(10).join(f"--spacing-{i + 1}: {size};" for i, size in enumerate(system.spacing.scale))}
```

### Common Patterns

| Pattern | Value |
|---------|-------|
"""
        for name, value in system.spacing.padding.items():
            md += f"| {name} | `{value}` |\n"

        md += f"""

---

## Responsive Breakpoints

| Name | Min Width |
|------|-----------|
"""
        for name, value in system.responsive_breakpoints.items():
            md += f"| {name} | {value} |\n"

        md += f"""

---

## Components

"""
        for comp in system.components:
            md += f"""### {comp.name}

**Selector:** `{comp.selector}`

**Styles:**
```css
{comp.selector} {{
{chr(10).join(f"  {prop}: {value};" for prop, value in comp.styles.items())}
}}
```

"""

        md += """---

## Usage Guidelines

1. **Color Tokens**: Use CSS custom properties for all colors to ensure consistency
2. **Typography**: Follow the type scale for hierarchy
3. **Spacing**: Use the spacing scale for consistent padding and margins
4. **Components**: Extend base components rather than creating new ones
5. **Responsive**: Test at all breakpoint widths

---

*This design system was auto-generated by ADEA (Autonomous Design Engineering & Adaptation)*
"""

        return md
