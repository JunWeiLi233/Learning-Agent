"""ADEA Core Engine - Orchestrates the four-phase workflow."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List
import json
import time

from .analyzer import DesignAnalyzer
from .builder import UIBuilder
from .qa import VisualQA
from .extractor import DesignSystemExtractor
from .optimizer import CreativeOptimizer


@dataclass
class ADEAConfig:
    """Configuration for ADEA workflow."""
    target_url: str
    output_dir: str = "./adea_output"
    sandbox_dir: str = "./adea_sandbox"
    max_retries: int = 3
    qa_threshold: float = 0.95
    enable_optimization: bool = True
    framework: str = "html"  # html, react, vue, svelte


@dataclass
class ADEAResult:
    """Result of an ADEA workflow run."""
    success: bool
    target_url: str
    design_system_path: Optional[str] = None
    output_path: Optional[str] = None
    iterations: int = 0
    qa_score: float = 0.0
    optimizations: List[Dict[str, Any]] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class ADEAEngine:
    """
    Main engine for Autonomous Design Engineering & Adaptation.

    Orchestrates the four-phase pipeline:
    1. Research & Iterative Execution
    2. Visual Quality Assurance
    3. Standardization & Design System Extraction
    4. Creative Optimization
    """

    def __init__(self, config: ADEAConfig):
        self.config = config
        self.output_dir = Path(config.output_dir)
        self.sandbox_dir = Path(config.sandbox_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.sandbox_dir.mkdir(parents=True, exist_ok=True)

        self.analyzer = DesignAnalyzer()
        self.builder = UIBuilder(config.framework, config.sandbox_dir)
        self.qa = VisualQA()
        self.extractor = DesignSystemExtractor()
        self.optimizer = CreativeOptimizer()

    def execute(self) -> ADEAResult:
        """Execute the full ADEA workflow."""
        result = ADEAResult(success=False, target_url=self.config.target_url)

        try:
            # Phase 1: Research & Iterative Execution
            print(f"[ADEA] Phase 1: Analyzing {self.config.target_url}")
            design_data = self.analyzer.analyze(self.config.target_url)
            result.iterations = self._phase1_build_loop(design_data, result)

            # Phase 2: Visual Quality Assurance
            print("[ADEA] Phase 2: Visual QA")
            qa_score = self._phase2_qa_loop(design_data, result)
            result.qa_score = qa_score

            if qa_score < self.config.qa_threshold:
                result.errors.append(f"QA score {qa_score:.2f} below threshold {self.config.qa_threshold}")
                return result

            # Phase 3: Design System Extraction
            print("[ADEA] Phase 3: Extracting design system")
            design_system_path = self._phase3_extract(design_data)
            result.design_system_path = str(design_system_path)

            # Phase 4: Creative Optimization
            if self.config.enable_optimization:
                print("[ADEA] Phase 4: Creative optimization")
                optimizations = self._phase4_optimize(design_data)
                result.optimizations = optimizations

            result.success = True
            result.output_path = str(self.sandbox_dir / "index.html")
            print("[ADEA] Workflow complete!")

        except Exception as e:
            result.errors.append(str(e))
            print(f"[ADEA] Error: {e}")

        return result

    def _phase1_build_loop(self, design_data: Dict[str, Any], result: ADEAResult) -> int:
        """Phase 1: Build with failure recovery loop."""
        iterations = 0

        for attempt in range(self.config.max_retries):
            iterations += 1
            try:
                html = self.builder.build(design_data)
                self.builder.write_output(html)
                return iterations
            except Exception as e:
                print(f"[ADEA] Build attempt {attempt + 1} failed: {e}")
                if attempt < self.config.max_retries - 1:
                    design_data = self.analyzer.pivot(design_data, str(e))

        raise RuntimeError(f"Build failed after {self.config.max_retries} attempts")

    def _phase2_qa_loop(self, design_data: Dict[str, Any], result: ADEAResult) -> float:
        """Phase 2: Visual QA with refinement loop."""
        best_score = 0.0

        for i in range(5):
            score = self.qa.compare(
                self.config.target_url,
                str(self.sandbox_dir / "index.html")
            )

            if score > best_score:
                best_score = score

            if score >= self.config.qa_threshold:
                return score

            # Refine based on QA feedback
            feedback = self.qa.get_feedback()
            design_data = self.analyzer.refine(design_data, feedback)
            html = self.builder.build(design_data)
            self.builder.write_output(html)

        return best_score

    def _phase3_extract(self, design_data: Dict[str, Any]) -> Path:
        """Phase 3: Extract design system documentation."""
        design_system = self.extractor.extract(design_data)
        output_path = self.output_dir / "design-system.md"
        self.extractor.write_documentation(design_system, output_path)
        return output_path

    def _phase4_optimize(self, design_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Phase 4: Generate multiple design variants and pick the best."""
        # Get base HTML from builder
        base_html = self.builder.build(design_data)

        # Generate multiple design variants
        print("[ADEA] Generating design variants...")
        variants = self.optimizer.generate_variants(design_data, base_html)
        print(f"[ADEA] Generated {len(variants)} variants: {[v.name for v in variants]}")

        # Evaluate all variants
        print("[ADEA] Evaluating variants...")
        evaluations = self.optimizer.evaluate_variants(variants, design_data)

        # Pick the best variant
        best = self.optimizer.pick_best(evaluations)
        print(f"[ADEA] Best variant: {best.variant.name} (score: {best.total_score:.2f})")

        # Apply the best variant
        if best:
            result = self.optimizer.apply_best(best, self.sandbox_dir)
            if result:
                print(f"[ADEA] Applied variant to {result['html']}")

        # Return all ranked evaluations
        return self.optimizer.get_all_ranked(evaluations)
