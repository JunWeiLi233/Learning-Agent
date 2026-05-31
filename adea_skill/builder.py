"""UI Builder - Generates HTML/CSS from analyzed design data."""

from pathlib import Path
from typing import Dict, Any, List, Optional
import html
import json


class UIBuilder:
    """
    Builds UI implementations from extracted design data.

    Supports multiple frameworks:
    - html: Pure HTML/CSS
    - react: React components
    - vue: Vue components
    - svelte: Svelte components
    """

    def __init__(self, framework: str = "html", output_dir: str = "./output"):
        self.framework = framework
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build(self, design_data: Dict[str, Any]) -> str:
        """
        Build UI from design data.

        Args:
            design_data: Analyzed design data from DesignAnalyzer

        Returns:
            Generated HTML/CSS string
        """
        if self.framework == "html":
            return self._build_html(design_data)
        elif self.framework == "react":
            return self._build_react(design_data)
        elif self.framework == "vue":
            return self._build_vue(design_data)
        elif self.framework == "svelte":
            return self._build_svelte(design_data)
        else:
            raise ValueError(f"Unsupported framework: {self.framework}")

    def write_output(self, content: str, filename: str = "index.html"):
        """Write generated output to file."""
        output_path = self.output_dir / filename
        output_path.write_text(content, encoding="utf-8")
        return output_path

    def _build_html(self, data: Dict[str, Any]) -> str:
        """Build pure HTML/CSS implementation."""
        tokens = data.get("tokens", [])
        components = data.get("components", [])

        # Extract colors
        colors = self._extract_colors(tokens)
        typography = self._extract_typography(tokens)
        spacing = self._extract_spacing(tokens)

        # Generate CSS custom properties
        css_vars = self._generate_css_variables(colors, typography, spacing)

        # Generate component styles
        component_css = self._generate_component_styles(components)

        # Generate HTML structure
        html_structure = self._generate_html_structure(data)

        # Detect Apple-style from URL
        raw = data.get("raw", data)
        url = raw.get("url", "")
        is_apple = "apple.com" in url.lower() if url else False

        if is_apple:
            apple_css = self._generate_apple_css()
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Apple Design Clone</title>
    <style>
        :root {{
            {css_vars}
            /* Apple-specific tokens */
            --apple-nav-bg: rgba(29, 29, 31, 0.8);
            --apple-nav-height: 44px;
            --apple-dark-bg: rgb(22, 22, 23);
            --apple-light-bg: rgb(255, 255, 255);
            --apple-text-dark: rgb(29, 29, 31);
            --apple-text-light: rgb(245, 245, 247);
            --apple-link-blue: rgb(0, 113, 227);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: "SF Pro Text", "SF Pro Icons", "Helvetica Neue", Helvetica, Arial, sans-serif;
            font-size: 17px;
            color: var(--apple-text-dark);
            background-color: var(--apple-light-bg);
            line-height: 1.5;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }}

        {apple_css}

        {component_css}
    </style>
</head>
<body>
    {html_structure}
</body>
</html>"""
        else:
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Design</title>
    <style>
        :root {{
            {css_vars}
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: var(--font-family);
            font-size: var(--font-size-base);
            color: var(--text-color);
            background-color: var(--bg-color);
            line-height: 1.5;
        }}

        {component_css}
    </style>
</head>
<body>
    {html_structure}
</body>
</html>"""

    def _generate_apple_css(self) -> str:
        """Generate Apple-specific CSS styles."""
        return """
        /* Apple Navigation */
        .apple-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 44px;
            background: rgba(29, 29, 31, 0.8);
            backdrop-filter: saturate(180%) blur(20px);
            -webkit-backdrop-filter: saturate(180%) blur(20px);
            z-index: 9999;
        }

        .nav-content {
            max-width: 1024px;
            margin: 0 auto;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 22px;
        }

        .nav-logo {
            color: rgba(255, 255, 255, 0.8);
            display: flex;
            align-items: center;
        }

        .nav-logo:hover {
            color: rgba(255, 255, 255, 1);
        }

        .nav-links {
            display: flex;
            list-style: none;
            gap: 0;
            flex: 1;
            justify-content: center;
        }

        .nav-links li a {
            color: rgba(255, 255, 255, 0.8);
            text-decoration: none;
            font-size: 12px;
            padding: 0 10px;
            line-height: 44px;
            transition: color 0.3s ease;
        }

        .nav-links li a:hover {
            color: rgba(255, 255, 255, 1);
        }

        .nav-actions {
            display: flex;
            gap: 16px;
        }

        .nav-search,
        .nav-bag {
            background: none;
            border: none;
            color: rgba(255, 255, 255, 0.8);
            cursor: pointer;
            padding: 0;
            display: flex;
            align-items: center;
        }

        .nav-search:hover,
        .nav-bag:hover {
            color: rgba(255, 255, 255, 1);
        }

        /* Hero Sections */
        .hero {
            min-height: 580px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 12px 22px 84px;
            position: relative;
        }

        .hero-dark {
            background-color: rgb(22, 22, 23);
            color: var(--apple-text-light);
        }

        .hero-light {
            background-color: var(--apple-light-bg);
            color: var(--apple-text-dark);
        }

        .hero-content {
            position: relative;
            z-index: 2;
        }

        .hero-title {
            font-size: 56px;
            font-weight: 700;
            letter-spacing: -0.005em;
            margin-bottom: 6px;
        }

        .hero-subtitle {
            font-size: 28px;
            font-weight: 400;
            color: rgb(134, 134, 139);
            margin-bottom: 16px;
        }

        .hero-dark .hero-subtitle {
            color: rgb(134, 134, 139);
        }

        .hero-light .hero-subtitle {
            color: rgb(110, 110, 115);
        }

        .hero-actions {
            display: flex;
            gap: 12px;
            justify-content: center;
        }

        .hero-image {
            margin-top: 20px;
        }

        .hero-image img {
            max-width: 100%;
            height: auto;
        }

        /* Buttons */
        .btn {
            display: inline-block;
            padding: 12px 24px;
            border-radius: 980px;
            font-size: 17px;
            font-weight: 400;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .btn-primary {
            background-color: var(--apple-link-blue);
            color: white;
        }

        .btn-primary:hover {
            background-color: rgb(0, 102, 204);
        }

        .btn-secondary {
            background-color: transparent;
            color: var(--apple-link-blue);
            border: 1px solid var(--apple-link-blue);
        }

        .btn-secondary:hover {
            background-color: var(--apple-link-blue);
            color: white;
        }

        .btn-primary-dark {
            background-color: rgb(0, 113, 227);
            color: white;
        }

        .btn-primary-dark:hover {
            background-color: rgb(0, 102, 204);
        }

        .btn-secondary-dark {
            background-color: transparent;
            color: rgb(0, 113, 227);
            border: 1px solid rgb(0, 113, 227);
        }

        .btn-secondary-dark:hover {
            background-color: rgb(0, 113, 227);
            color: white;
        }

        /* Feature Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            padding: 12px;
            background-color: var(--apple-light-bg);
        }

        .feature-card {
            min-height: 580px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 40px 22px 84px;
        }

        .feature-card-light {
            background-color: var(--apple-light-bg);
        }

        .feature-card-dark {
            background-color: var(--apple-dark-bg);
            color: var(--apple-text-light);
        }

        .feature-content h3 {
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 6px;
        }

        .feature-tagline {
            font-size: 21px;
            color: rgb(110, 110, 115);
            margin-bottom: 16px;
        }

        .feature-card-dark .feature-tagline {
            color: rgb(134, 134, 139);
        }

        .feature-actions {
            display: flex;
            gap: 12px;
            justify-content: center;
        }

        /* Footer */
        .apple-footer {
            background-color: var(--apple-light-bg);
            border-top: 1px solid rgb(210, 210, 215);
            padding: 20px 0;
        }

        .footer-content {
            max-width: 980px;
            margin: 0 auto;
            padding: 0 22px;
        }

        .footer-legal {
            font-size: 12px;
            color: rgb(110, 110, 115);
            margin-bottom: 8px;
        }

        .footer-links {
            display: flex;
            flex-wrap: wrap;
            list-style: none;
            gap: 0;
        }

        .footer-links li a {
            font-size: 12px;
            color: rgb(110, 110, 115);
            text-decoration: none;
            padding: 0 10px;
            border-right: 1px solid rgb(210, 210, 215);
        }

        .footer-links li:last-child a {
            border-right: none;
        }

        .footer-links li a:hover {
            color: var(--apple-text-dark);
            text-decoration: underline;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }

            .hero-title {
                font-size: 40px;
            }

            .hero-subtitle {
                font-size: 21px;
            }

            .feature-grid {
                grid-template-columns: 1fr;
            }

            .feature-content h3 {
                font-size: 32px;
            }
        }"""

    def _build_react(self, data: Dict[str, Any]) -> str:
        """Build React component implementation."""
        tokens = data.get("tokens", [])
        colors = self._extract_colors(tokens)

        return f"""import React from 'react';
import './styles.css';

const GeneratedComponent = () => {{
  return (
    <div className="generated-component">
      <!-- Generated content -->
    </div>
  );
}};

export default GeneratedComponent;"""

    def _build_vue(self, data: Dict[str, Any]) -> str:
        """Build Vue component implementation."""
        return """<template>
  <div class="generated-component">
    <!-- Generated content -->
  </div>
</template>

<script>
export default {
  name: 'GeneratedComponent'
}
</script>

<style scoped>
/* Generated styles */
</style>"""

    def _build_svelte(self, data: Dict[str, Any]) -> str:
        """Build Svelte component implementation."""
        return """<script>
  // Generated logic
</script>

<div class="generated-component">
  <!-- Generated content -->
</div>

<style>
  /* Generated styles */
</style>"""

    def _extract_colors(self, tokens: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract color tokens."""
        colors = {}
        for token in tokens:
            if token.get("category") == "color":
                name = token.get("name", "")
                value = token.get("value", "")
                if "text" in name:
                    colors["text"] = value
                elif "bg" in name:
                    colors["background"] = value
        return colors

    def _extract_typography(self, tokens: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract typography tokens."""
        typo = {}
        for token in tokens:
            if token.get("category") == "typography":
                name = token.get("name", "")
                value = token.get("value", "")
                if "font-size" in name:
                    typo["size"] = value
        return typo

    def _extract_spacing(self, tokens: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract spacing tokens."""
        spacing = {}
        for token in tokens:
            if token.get("category") == "spacing":
                name = token.get("name", "")
                value = token.get("value", "")
                spacing[name] = value
        return spacing

    def _generate_css_variables(self, colors: Dict, typography: Dict, spacing: Dict) -> str:
        """Generate CSS custom properties."""
        vars = []

        # Colors
        if colors.get("text"):
            vars.append(f"  --text-color: {colors['text']};")
        if colors.get("background"):
            vars.append(f"  --bg-color: {colors['background']};")

        # Typography
        if typography.get("size"):
            vars.append(f"  --font-size-base: {typography['size']};")

        # Default values
        vars.append("  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;")
        vars.append("  --spacing-xs: 4px;")
        vars.append("  --spacing-sm: 8px;")
        vars.append("  --spacing-md: 16px;")
        vars.append("  --spacing-lg: 24px;")
        vars.append("  --spacing-xl: 32px;")

        return "\n".join(vars)

    def _generate_component_styles(self, components: List[Dict[str, Any]]) -> str:
        """Generate CSS for detected components."""
        styles = []

        for comp in components:
            selector = comp.get("selector", "")
            comp_styles = comp.get("styles", {})

            if selector and comp_styles:
                css_props = []
                for prop, value in comp_styles.items():
                    if value and value != "rgba(0, 0, 0, 0)":
                        css_props.append(f"    {prop}: {value};")

                if css_props:
                    styles.append(f"""{selector} {{
{chr(10).join(css_props)}
  }}""")

        return "\n\n".join(styles)

    def _generate_html_structure(self, data: Dict[str, Any]) -> str:
        """Generate HTML structure from design data."""
        raw = data.get("raw", data)
        url = raw.get("url", "")

        # Detect Apple-style patterns
        is_apple = "apple.com" in url.lower() if url else False

        if is_apple:
            return self._generate_apple_structure(raw)
        else:
            return self._generate_generic_structure(raw)

    def _generate_apple_structure(self, data: Dict[str, Any]) -> str:
        """Generate Apple-style HTML structure."""
        return """    <!-- Apple-style Navigation -->
    <nav class="apple-nav">
        <div class="nav-content">
            <a href="#" class="nav-logo">
                <svg viewBox="0 0 17 48" width="14" height="44">
                    <path d="M15.5 22.1c0-4.4 3.6-6.6 3.8-6.7-2.1-3-5.3-3.4-6.4-3.4-2.7-.3-5.3 1.6-6.7 1.6s-3.5-1.5-5.8-1.5c-3 0-5.7 1.7-7.3 4.4-3.2 5.4-.8 13.4 2.3 17.8 1.5 2.2 3.3 4.6 5.7 4.5 2.2-.1 3.1-1.4 5.7-1.4 2.6 0 3.4 1.4 5.7 1.4 2.4 0 4-2.2 5.4-4.4 1.7-2.6 2.4-5.1 2.4-5.2-.1-.1-4.7-1.8-4.7-7.5zM11.4 7.1c1.3-1.5 2.1-3.6 1.9-5.7-1.8.1-4 1.2-5.3 2.7-1.2 1.4-2.2 3.5-1.9 5.6 2 .2 4-1.1 5.3-2.6z" fill="currentColor"/>
                </svg>
            </a>
            <ul class="nav-links">
                <li><a href="#">Store</a></li>
                <li><a href="#">Mac</a></li>
                <li><a href="#">iPad</a></li>
                <li><a href="#">iPhone</a></li>
                <li><a href="#">Watch</a></li>
                <li><a href="#">AirPods</a></li>
                <li><a href="#">TV & Home</a></li>
                <li><a href="#">Entertainment</a></li>
                <li><a href="#">Accessories</a></li>
                <li><a href="#">Support</a></li>
            </ul>
            <div class="nav-actions">
                <button class="nav-search" aria-label="Search">
                    <svg width="15" height="44" viewBox="0 0 15 44">
                        <path d="M14.3 23.7c0-.8-.1-1.6-.2-2.3l-1.1.5c-.1.7-.5 1.3-1.1 1.8-.4.3-.6.5-.6.5s.3.3.9.5c.7.3 1.2.4 1.4.4-.2.5-.5 1-.9 1.4-.7.7-1.4 1.1-2.2 1.1-.6 0-1.1-.2-1.6-.5-.5-.4-.9-.9-1.2-1.5-.3-.6-.5-1.3-.5-2.1 0-.8.2-1.5.5-2.1.4-.6.8-1.1 1.4-1.5.6-.4 1.2-.6 1.8-.6.7 0 1.3.2 1.8.7.5.4.9 1 1.1 1.7.2.7.3 1.4.3 2.2v.4zM6.2 19.3c0 .6.1 1.2.4 1.7.3.5.7.9 1.2 1.2.5.3 1 .4 1.6.4.6 0 1.1-.1 1.6-.4.5-.3.9-.7 1.2-1.2.3-.5.4-1.1.4-1.7 0-.6-.1-1.2-.4-1.7-.3-.5-.7-.9-1.2-1.2-.5-.3-1-.4-1.6-.4-.6 0-1.1.1-1.6.4-.5.3-.9.7-1.2 1.2-.3.5-.4 1.1-.4 1.7zM4.5 23.7c0-1.3.3-2.4.9-3.3.6-.9 1.5-1.4 2.5-1.4 1 0 1.9.5 2.5 1.4.6.9.9 2 .9 3.3 0 1.3-.3 2.4-.9 3.3-.6.9-1.5 1.4-2.5 1.4-1 0-1.9-.5-2.5-1.4-.6-.9-.9-2-.9-3.3z" fill="currentColor"/>
                    </svg>
                </button>
                <button class="nav-bag" aria-label="Shopping Bag">
                    <svg width="14" height="44" viewBox="0 0 14 44">
                        <path d="M11.3 16.1h-1.5c-.1-.9-.4-1.7-.8-2.4-.5-.7-1.1-1.3-1.8-1.7-.7-.4-1.5-.6-2.3-.6-1.7 0-3.1.6-4.2 1.7C.7 14.2.1 15.7.1 17.5c0 1.7.6 3.2 1.7 4.3 1.1 1.1 2.5 1.7 4.2 1.7.8 0 1.6-.2 2.3-.6.7-.4 1.3-1 1.8-1.7.4-.7.7-1.5.8-2.4h1.5c.3 0 .5-.2.5-.5s-.2-.5-.5-.5zM5.4 20.8c-.8 0-1.5-.3-2.1-.8-.6-.6-.9-1.3-.9-2.1 0-.8.3-1.5.9-2.1.6-.6 1.3-.8 2.1-.8.8 0 1.5.3 2.1.8.6.6.9 1.3.9 2.1 0 .8-.3 1.5-.9 2.1-.6.6-1.3.8-2.1.8z" fill="currentColor"/>
                    </svg>
                </button>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero hero-dark">
        <div class="hero-content">
            <h1 class="hero-title">iPhone 17 Pro</h1>
            <p class="hero-subtitle">All out Pro.</p>
            <div class="hero-actions">
                <a href="#" class="btn btn-primary">Learn more</a>
                <a href="#" class="btn btn-secondary">Buy</a>
            </div>
        </div>
        <div class="hero-image">
            <img src="https://www.apple.com/v/iphone-17-pro/a/images/overview/hero/hero_endframe__bpjfx5sr0yqi_large.jpg" alt="iPhone 17 Pro" loading="lazy">
        </div>
    </section>

    <!-- Secondary Hero -->
    <section class="hero hero-light">
        <div class="hero-content">
            <h2 class="hero-title">MacBook Pro</h2>
            <p class="hero-subtitle">Now with M5, M5 Pro, and M5 Max.</p>
            <div class="hero-actions">
                <a href="#" class="btn btn-primary-dark">Learn more</a>
                <a href="#" class="btn btn-secondary-dark">Buy</a>
            </div>
        </div>
    </section>

    <!-- Feature Grid -->
    <section class="feature-grid">
        <div class="feature-card feature-card-light">
            <div class="feature-content">
                <h3>iPhone 17</h3>
                <p class="feature-tagline">Magichromatic.</p>
                <div class="feature-actions">
                    <a href="#" class="btn btn-primary-dark">Learn more</a>
                    <a href="#" class="btn btn-secondary-dark">Buy</a>
                </div>
            </div>
        </div>
        <div class="feature-card feature-card-light">
            <div class="feature-content">
                <h3>Apple Intelligence</h3>
                <p class="feature-tagline">AI for the rest of us.</p>
                <div class="feature-actions">
                    <a href="#" class="btn btn-primary-dark">Learn more</a>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer class="apple-footer">
        <div class="footer-content">
            <p class="footer-legal">Copyright &copy; 2024 Apple Inc. All rights reserved.</p>
            <ul class="footer-links">
                <li><a href="#">Privacy Policy</a></li>
                <li><a href="#">Terms of Use</a></li>
                <li><a href="#">Sales and Refunds</a></li>
                <li><a href="#">Legal</a></li>
                <li><a href="#">Site Map</a></li>
            </ul>
        </div>
    </footer>"""

    def _generate_generic_structure(self, data: Dict[str, Any]) -> str:
        """Generate generic HTML structure."""
        return """    <header class="header">
        <nav class="nav">
            <a href="#" class="nav-brand">Brand</a>
            <ul class="nav-links">
                <li><a href="#">Link 1</a></li>
                <li><a href="#">Link 2</a></li>
                <li><a href="#">Link 3</a></li>
            </ul>
        </nav>
    </header>

    <main class="main">
        <section class="hero">
            <h1>Hero Title</h1>
            <p>Hero description</p>
            <a href="#" class="btn btn-primary">Call to Action</a>
        </section>

        <section class="features">
            <div class="feature">
                <h3>Feature 1</h3>
                <p>Description</p>
            </div>
            <div class="feature">
                <h3>Feature 2</h3>
                <p>Description</p>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>&copy; 2024 Generated Design</p>
    </footer>"""
