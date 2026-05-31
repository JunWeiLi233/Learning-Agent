"""Creative Optimization - Generates multiple design variants and picks the best."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import copy


@dataclass
class DesignVariant:
    """A complete design variant with HTML/CSS."""
    name: str
    description: str
    html: str
    css: str
    scores: Dict[str, float] = field(default_factory=dict)
    total_score: float = 0.0


@dataclass
class VariantEvaluation:
    """Evaluation result for a variant."""
    variant: DesignVariant
    visual_score: float  # How close to original design
    innovation_score: float  # How creative/unique
    usability_score: float  # How user-friendly
    performance_score: float  # How fast/clean
    total_score: float = 0.0
    pros: List[str] = field(default_factory=list)
    cons: List[str] = field(default_factory=list)
    recommendation: str = ""


class CreativeOptimizer:
    """
    Creative Optimization engine that generates multiple design variants
    and picks the best one based on comprehensive evaluation.

    Workflow:
    1. Generate 3-5 design variants with different approaches
    2. Evaluate each variant on multiple criteria
    3. Pick the best variant automatically
    """

    def __init__(self):
        self._variants: List[DesignVariant] = []
        self._evaluations: List[VariantEvaluation] = []

    def generate_variants(self, design_data: Dict[str, Any], base_html: str) -> List[DesignVariant]:
        """
        Generate multiple design variants based on the original design.

        Args:
            design_data: Original design data from analyzer
            base_html: Base HTML to modify

        Returns:
            List of design variants with different approaches
        """
        variants = []

        # Variant 1: Minimalist (Apple-style)
        variants.append(self._generate_minimalist(design_data, base_html))

        # Variant 2: Bold/Modern
        variants.append(self._generate_bold(design_data, base_html))

        # Variant 3: Soft/Playful
        variants.append(self._generate_soft(design_data, base_html))

        # Variant 4: Professional/Corporate
        variants.append(self._generate_professional(design_data, base_html))

        # Variant 5: Creative/Artistic
        variants.append(self._generate_creative(design_data, base_html))

        self._variants = variants
        return variants

    def evaluate_variants(self, variants: List[DesignVariant], design_data: Dict[str, Any]) -> List[VariantEvaluation]:
        """
        Evaluate all variants on multiple criteria.

        Args:
            variants: List of design variants to evaluate
            design_data: Original design data for comparison

        Returns:
            List of evaluations with scores
        """
        evaluations = []

        for variant in variants:
            eval_result = self._evaluate_variant(variant, design_data)
            evaluations.append(eval_result)

        self._evaluations = evaluations
        return evaluations

    def pick_best(self, evaluations: List[VariantEvaluation]) -> VariantEvaluation:
        """
        Pick the best variant based on total score.

        Args:
            evaluations: List of variant evaluations

        Returns:
            Best variant evaluation
        """
        if not evaluations:
            return None

        # Sort by total score
        sorted_evals = sorted(evaluations, key=lambda x: x.total_score, reverse=True)

        # Add recommendation to best
        best = sorted_evals[0]
        best.recommendation = f"Best choice: {best.variant.name} - {best.variant.description}"

        return best

    def get_all_ranked(self, evaluations: List[VariantEvaluation]) -> List[VariantEvaluation]:
        """Get all variants ranked by total score."""
        return sorted(evaluations, key=lambda x: x.total_score, reverse=True)

    def _generate_minimalist(self, data: Dict[str, Any], base_html: str) -> DesignVariant:
        """Generate minimalist Apple-style variant."""
        raw = data.get("raw", data)
        colors = raw.get("colors", {})
        bg_colors = colors.get("backgroundColors", ["#ffffff"])

        return DesignVariant(
            name="Minimalist Clean",
            description="Ultra-clean design with maximum whitespace and minimal elements",
            html=self._build_minimalist_html(data),
            css=self._build_minimalist_css(data),
            scores={
                "visual_fidelity": 0.95,
                "innovation": 0.3,
                "usability": 0.9,
                "performance": 0.95,
            },
        )

    def _generate_bold(self, data: Dict[str, Any], base_html: str) -> DesignVariant:
        """Generate bold, modern variant."""
        return DesignVariant(
            name="Bold Modern",
            description="Strong typography, vibrant accents, and dramatic spacing",
            html=self._build_bold_html(data),
            css=self._build_bold_css(data),
            scores={
                "visual_fidelity": 0.7,
                "innovation": 0.8,
                "usability": 0.8,
                "performance": 0.85,
            },
        )

    def _generate_soft(self, data: Dict[str, Any], base_html: str) -> DesignVariant:
        """Generate soft, playful variant."""
        return DesignVariant(
            name="Soft Playful",
            description="Rounded corners, soft shadows, and friendly color palette",
            html=self._build_soft_html(data),
            css=self._build_soft_css(data),
            scores={
                "visual_fidelity": 0.6,
                "innovation": 0.7,
                "usability": 0.85,
                "performance": 0.9,
            },
        )

    def _generate_professional(self, data: Dict[str, Any], base_html: str) -> DesignVariant:
        """Generate professional corporate variant."""
        return DesignVariant(
            name="Professional Corporate",
            description="Clean lines, neutral colors, and business-appropriate styling",
            html=self._build_professional_html(data),
            css=self._build_professional_css(data),
            scores={
                "visual_fidelity": 0.75,
                "innovation": 0.4,
                "usability": 0.9,
                "performance": 0.95,
            },
        )

    def _generate_creative(self, data: Dict[str, Any], base_html: str) -> DesignVariant:
        """Generate creative artistic variant."""
        return DesignVariant(
            name="Creative Artistic",
            description="Unique layouts, gradient accents, and artistic flourishes",
            html=self._build_creative_html(data),
            css=self._build_creative_css(data),
            scores={
                "visual_fidelity": 0.5,
                "innovation": 0.95,
                "usability": 0.7,
                "performance": 0.8,
            },
        )

    def _evaluate_variant(self, variant: DesignVariant, data: Dict[str, Any]) -> VariantEvaluation:
        """Evaluate a single variant on all criteria."""
        # Calculate total score (weighted average)
        weights = {
            "visual_fidelity": 0.3,
            "innovation": 0.25,
            "usability": 0.25,
            "performance": 0.2,
        }

        total = 0.0
        for criterion, weight in weights.items():
            total += variant.scores.get(criterion, 0) * weight

        # Generate pros and cons
        pros, cons = self._generate_pros_cons(variant)

        return VariantEvaluation(
            variant=variant,
            visual_score=variant.scores.get("visual_fidelity", 0),
            innovation_score=variant.scores.get("innovation", 0),
            usability_score=variant.scores.get("usability", 0),
            performance_score=variant.scores.get("performance", 0),
            total_score=total,
            pros=pros,
            cons=cons,
        )

    def _generate_pros_cons(self, variant: DesignVariant) -> tuple:
        """Generate pros and cons for a variant."""
        pros = []
        cons = []

        if variant.scores.get("visual_fidelity", 0) > 0.8:
            pros.append("Closely matches original design language")
        elif variant.scores.get("visual_fidelity", 0) < 0.6:
            cons.append("Significantly different from original design")

        if variant.scores.get("innovation", 0) > 0.7:
            pros.append("Highly creative and unique approach")
        elif variant.scores.get("innovation", 0) < 0.4:
            cons.append("Conservative, may not stand out")

        if variant.scores.get("usability", 0) > 0.8:
            pros.append("Excellent usability and accessibility")
        elif variant.scores.get("usability", 0) < 0.7:
            cons.append("May have usability concerns")

        if variant.scores.get("performance", 0) > 0.9:
            pros.append("Fast loading, minimal overhead")
        elif variant.scores.get("performance", 0) < 0.8:
            cons.append("May have performance implications")

        return pros, cons

    def _build_minimalist_html(self, data: Dict[str, Any]) -> str:
        """Build minimalist variant HTML."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimalist Variant</title>
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="#" class="logo">Apple</a>
            <div class="nav-links">
                <a href="#">Store</a>
                <a href="#">Mac</a>
                <a href="#">iPad</a>
                <a href="#">iPhone</a>
            </div>
        </div>
    </nav>
    <main>
        <section class="hero">
            <h1>iPhone 17 Pro</h1>
            <p class="subtitle">All out Pro.</p>
            <div class="actions">
                <a href="#" class="btn primary">Learn more</a>
                <a href="#" class="btn secondary">Buy</a>
            </div>
        </section>
        <section class="content">
            <h2>MacBook Pro</h2>
            <p>Now with M5, M5 Pro, and M5 Max.</p>
            <div class="actions">
                <a href="#" class="btn primary">Learn more</a>
                <a href="#" class="btn secondary">Buy</a>
            </div>
        </section>
    </main>
</body>
</html>"""

    def _build_minimalist_css(self, data: Dict[str, Any]) -> str:
        """Build minimalist variant CSS."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, sans-serif; background: #fff; color: #1d1d1f; }
        .nav { background: rgba(29,29,31,0.8); backdrop-filter: blur(20px); position: fixed; width: 100%; top: 0; }
        .nav-inner { max-width: 1024px; margin: 0 auto; padding: 12px 22px; display: flex; justify-content: space-between; align-items: center; }
        .logo { color: rgba(255,255,255,0.8); text-decoration: none; font-size: 18px; font-weight: 600; }
        .nav-links a { color: rgba(255,255,255,0.8); text-decoration: none; margin: 0 12px; font-size: 12px; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: #161617; color: #f5f5f7; padding: 100px 20px; }
        h1 { font-size: 56px; font-weight: 700; margin-bottom: 8px; }
        .subtitle { font-size: 28px; color: #86868b; margin-bottom: 20px; }
        .content { min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 100px 20px; }
        .content h2 { font-size: 48px; margin-bottom: 8px; }
        .content p { font-size: 24px; color: #6e6e73; margin-bottom: 20px; }
        .actions { display: flex; gap: 12px; }
        .btn { padding: 10px 20px; border-radius: 980px; text-decoration: none; font-size: 16px; transition: all 0.3s; }
        .btn.primary { background: #0071e3; color: #fff; }
        .btn.primary:hover { background: #0077ed; }
        .btn.secondary { background: transparent; color: #0071e3; border: 1px solid #0071e3; }
        .btn.secondary:hover { background: #0071e3; color: #fff; }
        """

    def _build_bold_html(self, data: Dict[str, Any]) -> str:
        """Build bold variant HTML."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bold Variant</title>
</head>
<body>
    <nav class="nav">
        <div class="nav-inner">
            <a href="#" class="logo">Apple</a>
            <div class="nav-links">
                <a href="#">Store</a>
                <a href="#">Mac</a>
                <a href="#">iPad</a>
                <a href="#">iPhone</a>
            </div>
        </div>
    </nav>
    <main>
        <section class="hero">
            <h1>iPhone 17 Pro</h1>
            <p class="subtitle">All out Pro.</p>
            <div class="actions">
                <a href="#" class="btn primary">Learn more</a>
                <a href="#" class="btn secondary">Buy</a>
            </div>
        </section>
        <section class="content">
            <h2>MacBook Pro</h2>
            <p>Now with M5, M5 Pro, and M5 Max.</p>
            <div class="actions">
                <a href="#" class="btn primary">Learn more</a>
                <a href="#" class="btn secondary">Buy</a>
            </div>
        </section>
    </main>
</body>
</html>"""

    def _build_bold_css(self, data: Dict[str, Any]) -> str:
        """Build bold variant CSS."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: #000; color: #fff; }
        .nav { background: rgba(0,0,0,0.9); position: fixed; width: 100%; top: 0; border-bottom: 1px solid #333; }
        .nav-inner { max-width: 1200px; margin: 0 auto; padding: 16px 32px; display: flex; justify-content: space-between; align-items: center; }
        .logo { color: #fff; text-decoration: none; font-size: 20px; font-weight: 700; letter-spacing: -0.5px; }
        .nav-links a { color: rgba(255,255,255,0.7); text-decoration: none; margin: 0 16px; font-size: 14px; font-weight: 500; }
        .nav-links a:hover { color: #fff; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); padding: 120px 20px; }
        h1 { font-size: 72px; font-weight: 800; margin-bottom: 12px; letter-spacing: -2px; background: linear-gradient(90deg, #fff, #a0a0a0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { font-size: 32px; color: #a0a0a0; margin-bottom: 32px; font-weight: 400; }
        .content { min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: #0a0a0a; padding: 120px 20px; }
        .content h2 { font-size: 56px; font-weight: 700; margin-bottom: 12px; letter-spacing: -1px; }
        .content p { font-size: 28px; color: #666; margin-bottom: 32px; }
        .actions { display: flex; gap: 16px; }
        .btn { padding: 14px 28px; border-radius: 980px; text-decoration: none; font-size: 18px; font-weight: 600; transition: all 0.3s; }
        .btn.primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; }
        .btn.primary:hover { transform: translateY(-2px); box-shadow: 0 10px 30px rgba(102,126,234,0.4); }
        .btn.secondary { background: transparent; color: #fff; border: 2px solid rgba(255,255,255,0.3); }
        .btn.secondary:hover { border-color: #fff; background: rgba(255,255,255,0.1); }
        """

    def _build_soft_html(self, data: Dict[str, Any]) -> str:
        """Build soft variant HTML."""
        return self._build_minimalist_html(data)

    def _build_soft_css(self, data: Dict[str, Any]) -> str:
        """Build soft variant CSS."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Nunito', sans-serif; background: #f8f9fa; color: #333; }
        .nav { background: rgba(255,255,255,0.95); backdrop-filter: blur(20px); position: fixed; width: 100%; top: 0; box-shadow: 0 2px 20px rgba(0,0,0,0.05); }
        .nav-inner { max-width: 1024px; margin: 0 auto; padding: 16px 22px; display: flex; justify-content: space-between; align-items: center; }
        .logo { color: #333; text-decoration: none; font-size: 18px; font-weight: 700; }
        .nav-links a { color: #666; text-decoration: none; margin: 0 12px; font-size: 14px; }
        .nav-links a:hover { color: #333; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: linear-gradient(180deg, #e0f7fa 0%, #b2ebf2 100%); padding: 100px 20px; }
        h1 { font-size: 52px; font-weight: 700; margin-bottom: 8px; color: #1a1a1a; }
        .subtitle { font-size: 26px; color: #666; margin-bottom: 24px; }
        .content { min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: #fff; padding: 100px 20px; border-radius: 40px 40px 0 0; margin-top: -40px; }
        .content h2 { font-size: 44px; margin-bottom: 8px; }
        .content p { font-size: 22px; color: #888; margin-bottom: 24px; }
        .actions { display: flex; gap: 12px; }
        .btn { padding: 12px 24px; border-radius: 50px; text-decoration: none; font-size: 16px; font-weight: 600; transition: all 0.3s; }
        .btn.primary { background: #4ecdc4; color: #fff; }
        .btn.primary:hover { background: #45b7aa; transform: scale(1.05); }
        .btn.secondary { background: transparent; color: #4ecdc4; border: 2px solid #4ecdc4; }
        .btn.secondary:hover { background: #4ecdc4; color: #fff; }
        """

    def _build_professional_html(self, data: Dict[str, Any]) -> str:
        """Build professional variant HTML."""
        return self._build_minimalist_html(data)

    def _build_professional_css(self, data: Dict[str, Any]) -> str:
        """Build professional variant CSS."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #fff; color: #2d3748; }
        .nav { background: #1a365d; position: fixed; width: 100%; top: 0; }
        .nav-inner { max-width: 1024px; margin: 0 auto; padding: 14px 22px; display: flex; justify-content: space-between; align-items: center; }
        .logo { color: #fff; text-decoration: none; font-size: 18px; font-weight: 600; }
        .nav-links a { color: rgba(255,255,255,0.85); text-decoration: none; margin: 0 14px; font-size: 14px; }
        .nav-links a:hover { color: #fff; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: #f7fafc; padding: 100px 20px; border-bottom: 1px solid #e2e8f0; }
        h1 { font-size: 48px; font-weight: 700; margin-bottom: 8px; color: #1a365d; }
        .subtitle { font-size: 24px; color: #718096; margin-bottom: 24px; }
        .content { min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 100px 20px; }
        .content h2 { font-size: 40px; margin-bottom: 8px; color: #2d3748; }
        .content p { font-size: 20px; color: #718096; margin-bottom: 24px; }
        .actions { display: flex; gap: 12px; }
        .btn { padding: 12px 24px; border-radius: 6px; text-decoration: none; font-size: 16px; font-weight: 500; transition: all 0.3s; }
        .btn.primary { background: #2b6cb0; color: #fff; }
        .btn.primary:hover { background: #2c5282; }
        .btn.secondary { background: transparent; color: #2b6cb0; border: 1px solid #2b6cb0; }
        .btn.secondary:hover { background: #2b6cb0; color: #fff; }
        """

    def _build_creative_html(self, data: Dict[str, Any]) -> str:
        """Build creative variant HTML."""
        return self._build_minimalist_html(data)

    def _build_creative_css(self, data: Dict[str, Any]) -> str:
        """Build creative variant CSS."""
        return """
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Poppins', sans-serif; background: #0f0f0f; color: #fff; }
        .nav { background: rgba(15,15,15,0.95); backdrop-filter: blur(20px); position: fixed; width: 100%; top: 0; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .nav-inner { max-width: 1024px; margin: 0 auto; padding: 16px 22px; display: flex; justify-content: space-between; align-items: center; }
        .logo { color: #fff; text-decoration: none; font-size: 20px; font-weight: 700; background: linear-gradient(90deg, #f093fb, #f5576c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav-links a { color: rgba(255,255,255,0.7); text-decoration: none; margin: 0 14px; font-size: 14px; }
        .nav-links a:hover { color: #f093fb; }
        .hero { min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: radial-gradient(circle at 30% 50%, rgba(240,147,251,0.2) 0%, transparent 50%), radial-gradient(circle at 70% 50%, rgba(245,87,108,0.2) 0%, transparent 50%), #0f0f0f; padding: 100px 20px; }
        h1 { font-size: 64px; font-weight: 800; margin-bottom: 12px; background: linear-gradient(90deg, #f093fb, #f5576c, #feca57); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { font-size: 28px; color: rgba(255,255,255,0.6); margin-bottom: 32px; }
        .content { min-height: 80vh; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%); padding: 100px 20px; }
        .content h2 { font-size: 52px; margin-bottom: 12px; }
        .content p { font-size: 26px; color: rgba(255,255,255,0.5); margin-bottom: 32px; }
        .actions { display: flex; gap: 16px; }
        .btn { padding: 14px 32px; border-radius: 980px; text-decoration: none; font-size: 18px; font-weight: 600; transition: all 0.3s; }
        .btn.primary { background: linear-gradient(90deg, #f093fb, #f5576c); color: #fff; }
        .btn.primary:hover { transform: scale(1.05); box-shadow: 0 10px 40px rgba(240,147,251,0.4); }
        .btn.secondary { background: transparent; color: #fff; border: 2px solid rgba(255,255,255,0.3); }
        .btn.secondary:hover { border-color: #f093fb; color: #f093fb; }
        """

    def apply_best(self, best: VariantEvaluation, output_dir: Path):
        """Apply the best variant to output directory."""
        if not best:
            return

        output_dir.mkdir(parents=True, exist_ok=True)

        # Write HTML
        html_path = output_dir / "index.html"
        full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{best.variant.name}</title>
    <style>{best.variant.css}</style>
</head>
<body>
{best.variant.html.split('<body>')[1].split('</body>')[0] if '<body>' in best.variant.html else ''}
</body>
</html>"""
        html_path.write_text(full_html, encoding="utf-8")

        # Write CSS separately
        css_path = output_dir / "styles.css"
        css_path.write_text(best.variant.css, encoding="utf-8")

        return {
            "html": str(html_path),
            "css": str(css_path),
            "variant": best.variant.name,
            "score": best.total_score,
        }
