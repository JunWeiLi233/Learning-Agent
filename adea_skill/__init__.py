# ADEA - Autonomous Design Engineering & Adaptation Skill
# Enables AI agents to analyze, replicate, optimize, and standardize web UIs

from .core import ADEAEngine, ADEAConfig
from .analyzer import DesignAnalyzer
from .builder import UIBuilder
from .qa import VisualQA
from .extractor import DesignSystemExtractor
from .optimizer import CreativeOptimizer

__version__ = "1.0.0"
__all__ = [
    "ADEAEngine",
    "DesignAnalyzer",
    "UIBuilder",
    "VisualQA",
    "DesignSystemExtractor",
    "CreativeOptimizer",
]
