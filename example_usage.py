#!/usr/bin/env python3
"""
ADEA Skill Usage Example

Demonstrates the Autonomous Design Engineering & Adaptation workflow
using apple.com as a study model.
"""

import json
from pathlib import Path

from adea_skill import ADEAEngine, ADEAConfig


def main():
    """Run ADEA workflow on apple.com."""

    # Configure ADEA
    config = ADEAConfig(
        target_url="https://www.apple.com/",
        output_dir="./adea_output",
        sandbox_dir="./adea_sandbox",
        max_retries=3,
        qa_threshold=0.95,
        enable_optimization=True,
        framework="html",
    )

    # Initialize engine
    engine = ADEAEngine(config)

    # Example: Analyze from pre-fetched data
    # (In production, this would use browser-harness to fetch live data)
    sample_data = {
        "url": "https://www.apple.com/",
        "colors": {
            "textColors": [
                "rgb(29, 29, 31)",
                "rgb(0, 0, 0)",
                "rgba(255, 255, 255, 0.92)",
                "rgba(255, 255, 255, 0.8)",
            ],
            "backgroundColors": [
                "rgb(255, 255, 255)",
                "rgb(22, 22, 23)",
                "rgba(29, 29, 31, 0.8)",
            ],
        },
        "typography": {
            "primaryFont": '"SF Pro Text", "SF Pro Icons", "Helvetica Neue", Helvetica, Arial, sans-serif',
            "fontSizes": {
                "40px": 2,
                "34px": 1,
                "24px": 23,
                "17px": 11,
                "12px": 65,
            },
            "fontWeights": {
                "400": 31,
                "600": 69,
            },
        },
        "spacing": {
            "commonPaddings": {
                "40px 22px 84px": 12,
                "0px 88px 0px 0px": 11,
                "0px 44px 0px 0px": 20,
                "32px 22px 80px": 1,
                "56px 0px": 1,
            },
            "commonMargins": {
                "0px 440.5px": 14,
                "-44px 0px 0px": 13,
                "44px 0px 0px": 13,
            },
        },
        "buttons": [
            {
                "text": "Learn more",
                "color": "rgb(232, 232, 237)",
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "borderRadius": "980px",
                "padding": "12px 24px",
                "fontSize": "17px",
                "fontWeight": "400",
                "border": "1px solid rgba(255, 255, 255, 0.8)",
            },
            {
                "text": "Buy",
                "color": "rgb(232, 232, 237)",
                "backgroundColor": "rgba(0, 0, 0, 0)",
                "borderRadius": "980px",
                "padding": "12px 24px",
                "fontSize": "17px",
                "fontWeight": "400",
                "border": "1px solid rgba(255, 255, 255, 0.8)",
            },
        ],
        "layout": [
            {
                "display": "grid",
                "gridTemplateColumns": "1905px",
                "gap": "12px",
            },
            {
                "display": "grid",
                "gridTemplateColumns": "934.5px 934.5px",
                "gap": "12px",
            },
        ],
    }

    # Analyze the data
    print("=" * 60)
    print("ADEA - Autonomous Design Engineering & Adaptation")
    print("=" * 60)
    print(f"\nTarget: {config.target_url}")
    print(f"Framework: {config.framework}")
    print()

    # Phase 1: Analysis
    print("[Phase 1] Analyzing design...")
    design_data = engine.analyzer.analyze_from_data(sample_data)
    print(f"  - Extracted {len(design_data['tokens'])} design tokens")
    print(f"  - Detected {len(design_data['components'])} component patterns")

    # Phase 2: Build
    print("\n[Phase 2] Building implementation...")
    html = engine.builder.build(design_data)
    output_path = engine.builder.write_output(html)
    print(f"  - Generated: {output_path}")

    # Phase 3: QA
    print("\n[Phase 3] Running visual QA...")
    score = engine.qa.compare(
        config.target_url,
        str(output_path)
    )
    print(f"  - QA Score: {score:.2%}")

    # Phase 4: Extract Design System
    print("\n[Phase 4] Extracting design system...")
    design_system = engine.extractor.extract(design_data)
    ds_path = engine.output_dir / "design-system.md"
    engine.extractor.write_documentation(design_system, ds_path)
    print(f"  - Design system: {ds_path}")

    # Phase 5: Generate Design Variants (optional)
    if config.enable_optimization:
        print("\n[Phase 5] Generating design variants...")
        base_html = engine.builder.build(design_data)
        variants = engine.optimizer.generate_variants(design_data, base_html)
        print(f"  - Generated {len(variants)} variants: {[v.name for v in variants]}")

        # Evaluate variants
        print("\n[Phase 6] Evaluating variants...")
        evaluations = engine.optimizer.evaluate_variants(variants, design_data)

        # Pick best
        best = engine.optimizer.pick_best(evaluations)
        if best:
            print(f"  - Best variant: {best.variant.name}")
            print(f"  - Total score: {best.total_score:.2f}")
            print(f"  - Pros: {', '.join(best.pros)}")
            print(f"  - Cons: {', '.join(best.cons)}")

            # Apply best variant
            result = engine.optimizer.apply_best(best, engine.sandbox_dir)
            if result:
                print(f"  - Applied to: {result['html']}")

        # Show all ranked
        print("\n  All variants ranked:")
        for i, eval in enumerate(engine.optimizer.get_all_ranked(evaluations), 1):
            print(f"  {i}. {eval.variant.name} - Score: {eval.total_score:.2f}")

    print("\n" + "=" * 60)
    print("Workflow complete!")
    print("=" * 60)

    # Show output structure
    print("\nGenerated files:")
    print(f"  - {output_path}")
    print(f"  - {ds_path}")

    return 0


if __name__ == "__main__":
    exit(main())
