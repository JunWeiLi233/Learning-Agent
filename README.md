# Autonomous Design Engineering & Adaptation Skill (ADEA)

An advanced AI agent capability that enables autonomous analysis, replication, optimization, and standardization of web user interfaces through an iterative, self-correcting feedback loop.

---

## Why This?

Current AI agents suffer from "template fatigue." While many tools grant agents the capability to spin up clean, modern UI components, they almost always resort to the same predictable, generic templates. Designers and developers don't want cookie-cutter layouts—they need highly customized, novel design components.

**ADEA solves this by teaching agents how to "learn" rather than just generate.** Instead of serving up predefined templates, this skill allows an AI agent to target specific, specialized design elements out in the wild—whether it is a highly unique atomic component (like an innovative, custom-animated button) or the entire design language of a complex web platform. The agent absorbs the design principles behind the code, masters it, and builds a completely customized implementation tailored directly to your project.

---

## Overview

The **Autonomous Design Engineering & Adaptation (ADEA)** skill empowers AI agents to look at an existing website design, reverse-engineer its technical implementation, and rebuild it flawlessly.

Unlike traditional code-generation tools that blindly copy structures, ADEA forces the agent to truly **"learn"** the underlying design language. The agent extracts design systems, documents them for long-term reusability, and generates creative optimizations tailored to your specific project needs.

```
       [ Input UI / Design ]
                 │
                 ▼
     ┌───────────────────────┐
     │ 1. Research & Build   │◄───────┐ (If Build Fails)
     └───────────┬───────────┘        │
                 │ (Success)          │
                 ▼                    │
     ┌───────────────────────┐        │
 ┌──>│ 2. Visual QA Loop     ├────────┘
 │   └───────────┬───────────┘
 │               │ (Matches Exactly)
 │               ▼
 │   ┌───────────────────────┐
 │   │ 3. Extract & Document │ ──► [ design-system.md ]
 │   └───────────┬───────────┘
 │               │
 │               ▼
 └───│ 4. Creative Evolution │ ──► [ Optimized Project Variant ]
     └───────────────────────┘
```

---

## Architecture & Workflow

### Phase 1: Research & Iterative Execution
The agent breaks down the targeted interface into structured, executable technical components.
1. **Feasibility Research:** The agent deeply analyzes the target design, identifying framework-specific patterns, layout methodologies (CSS Grid, Flexbox, custom components), and structural behaviors.
2. **Mock Trial & Execution:** It attempts a prototype build in an isolated sandbox environment.
3. **Failure Recovery Loop:** If the compilation, rendering, or syntax fails, the agent intercepts the stack trace, pivots to an alternative technical approach, and restarts the build.

### Phase 2: Visual Quality Assurance (QA)
Once a functional build is established, the agent triggers a strict visual verification loop.
* **Computer Vision Comparison:** The agent evaluates the rendered mockup side-by-side with the original reference asset or live page.
* **Refinement Loop:** If structural alignment, sizing, responsiveness, or typography deviations are detected, the agent returns to the code generation layer to refine the output.
* **Validation:** This loop executes recursively until the generated interface matches the original design specification pixel-for-pixel.

### Phase 3: Standardization & Design System Extraction
To guarantee repeatability and ensure the design can be implemented again and again, the agent codifies its success.
* **Design Token Extraction:** The agent extracts design primitives including typography hierarchies, color systems, spacing matrices, component scales, and motion behaviors.
* **Standardized Documentation:** It writes this design language into a structured **Markdown file** (`design-system.md`). This acts as an immutable source of truth for future prompt engineering, UI scaffolding, or engineering handoffs.

### Phase 4: Creative Optimization
The defining capability of the ADEA skill is that **it does not just copy; it innovates.**

Upon achieving 100% fidelity with the original layout, the skill instructs the agent to conceptualize alternative solutions tailored specifically for your target environment.

1. **Ideation:** The agent brainstorms distinct stylistic, performance, accessibility, or UX enhancements (e.g., refactoring elements for a faster DOM footprint or introducing modern component variations).
2. **Algorithmic Evaluation:** The agent rates these newly conceived variants against the primary constraints of your current codebase.
3. **Selection & Application:** The absolute best approach is automatically selected and implemented as the final solution.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/JunWeiLi233/Learning-Agent.git
cd Learning-Agent

# Install dependencies (if any)
pip install -r requirements.txt
```

---

## Usage

### Basic Usage

```python
from adea_skill import ADEAEngine, ADEAConfig

# Configure ADEA
config = ADEAConfig(
    target_url="https://www.apple.com/",
    output_dir="./adea_output",
    sandbox_dir="./adea_sandbox",
    max_retries=3,
    qa_threshold=0.95,
    enable_optimization=True,
    framework="html",  # html, react, vue, svelte
)

# Initialize and run engine
engine = ADEAEngine(config)
result = engine.execute()

# Check results
if result.success:
    print(f"Design system: {result.design_system_path}")
    print(f"Output: {result.output_path}")
    print(f"QA Score: {result.qa_score:.2%}")
    print(f"Iterations: {result.iterations}")
```

### Running the Example

```bash
python example_usage.py
```

---

## Output Artifacts

Upon a successful workflow run, the agent outputs:

### 1. Design System Documentation (`design-system.md`)

```markdown
# Design System: Apple.com

## Color Palette
| Token | Value | Usage |
|-------|-------|-------|
| `--text-color` | `rgb(29, 29, 31)` | Primary text |
| `--bg-color` | `rgb(255, 255, 255)` | Page background |

## Typography
| Token | Size | Usage |
|-------|------|-------|
| `--size-1` | 40px | Headings |
| `--size-2` | 17px | Body text |

## Components
- Navigation bar with backdrop blur
- Hero sections with CTA buttons
- Feature grid layout
- Responsive footer
```

### 2. Generated HTML Implementation

Pixel-perfect HTML/CSS that matches the target design, including:
- Extracted color palette as CSS custom properties
- Typography system with proper font stacks
- Spacing system with consistent scales
- Responsive breakpoints
- Component styles matching original patterns

### 3. Optimization Recommendations

Performance, accessibility, UX, and styling improvements with impact scores.

---

## Supported Frameworks

| Framework | Status | Description |
|-----------|--------|-------------|
| HTML/CSS | Complete | Pure HTML with CSS custom properties |
| React | In Progress | React components with CSS modules |
| Vue | Planned | Vue single-file components |
| Svelte | Planned | Svelte components |

---

## Use Cases

* **Autonomous Migration:** Porting legacy web pages to new UI libraries while optimizing the modern codebase layout.
* **Design-to-Code Pipelines:** Feeding raw visuals to agents and allowing them to self-correct until reaching exact production standards.
* **Competitor UI Auditing:** Automatically extracting, analyzing, and improving upon high-performing UI patterns across the web.

---

## Architecture

```
adea_skill/
├── __init__.py         # Package exports
├── core.py            # Main ADEAEngine orchestrator
├── analyzer.py        # DesignAnalyzer - extracts design tokens
├── builder.py         # UIBuilder - generates HTML/CSS
├── qa.py              # VisualQA - compares outputs
├── extractor.py       # DesignSystemExtractor - documents patterns
└── optimizer.py       # CreativeOptimizer - generates improvements
```

---

## License

MIT License - See LICENSE file for details.



