#!/usr/bin/env python3
"""Theoretical Weighting Schemes for Materialist Indicators.

This module addresses the challenge of quantifying qualitative Marxist theory
by providing theoretically-grounded weighting schemes for different indicators.

Based on:
1. Marx's analysis of primary vs secondary contradictions
2. Historical materialism hierarchy of determining factors
3. Dialectical relationships between base and superstructure
"""

import logging
from dataclasses import dataclass
from enum import Enum

import numpy as np

from .materialist_ges_engine import ClassPosition, ConsciousnessType

# Module logger
logger = logging.getLogger(__name__)


class IndicatorWeight(Enum):
    """Theoretical importance of different indicators in materialist analysis."""

    PRIMARY = 1.0      # Base economic relations (most determining)
    SECONDARY = 0.7    # Social/political relations (important but derivative)
    TERTIARY = 0.4     # Cultural/ideological (influenced by base)
    CONTEXTUAL = 0.3   # Context-dependent significance


@dataclass
class TheoreticalWeights:
    """Theoretically-informed weights for materialist indicators."""

    # CLASS STRUCTURE WEIGHTS (Primary - determines everything else)
    exploitation_rate: float = 1.0           # Central to Marxist analysis
    class_distribution: float = 0.9          # Fundamental structure
    ownership_relations: float = 0.9         # Base economic relations

    # MATERIAL CONDITIONS (Primary - immediate life conditions)
    subsistence_security: float = 0.8        # Basic reproduction needs
    housing_security: float = 0.7           # Shelter is fundamental
    healthcare_access: float = 0.7          # Life and death matter

    # ALIENATION (Secondary - derivative of class relations)
    alienation_from_product: float = 0.8    # Structural under capitalism
    alienation_from_labor: float = 0.7      # Working conditions
    alienation_from_others: float = 0.6     # Social relations
    alienation_from_species: float = 0.5    # Human nature/creativity

    # CONSCIOUSNESS (Tertiary - emerges from material conditions)
    class_consciousness: float = 0.6        # Political awareness
    ideological_hegemony: float = 0.5       # Ruling class influence

    # HISTORICAL CONTEXT MODIFIERS
    crisis_period_multiplier: float = 1.5   # Crisis sharpens contradictions
    revolutionary_period_multiplier: float = 2.0  # Rapid change periods


CONSCIOUSNESS_HIGH_THRESHOLD = 0.7
CONSCIOUSNESS_LOW_THRESHOLD = 0.3

# Historical period detection thresholds
CRISIS_THRESHOLD = 0.6
STABILITY_THRESHOLD = 0.3

# Threshold for crisis intensity checks within dialectical adjustments
CRISIS_INTENSITY_THRESHOLD = 0.6

# Minimum threshold constants for revolutionary potential checks
MIN_OBJECTIVE_FACTOR = 0.3    # Minimum objective factor required for revolution
MIN_SUBJECTIVE_FACTOR = 0.15  # Minimum subjective factor required for revolution

class TheoryInformedWeightingScheme:
    """Implements Marx's theoretical hierarchy in quantitative weighting."""

    def __init__(self):
        self.weights = TheoreticalWeights()
        self.dialectical_relationships = self._define_dialectical_relationships()

    def _define_dialectical_relationships(self) -> dict[str, dict[str, float]]:
        """Define how indicators dialectically influence each other.

        Based on Marx's analysis:
        - Economic base determines superstructure (but with feedback)
        - Class struggle drives historical change
        - Consciousness emerges from material conditions
        """
        return {
            # Economic base influences consciousness
            "exploitation_rate": {
                "class_consciousness": 0.8,    # High exploitation → potential consciousness
                "revolutionary_potential": 0.7,
                "ideological_hegemony": -0.6,  # Negatively related
            },

            # Material security affects consciousness
            "subsistence_security": {
                "class_consciousness": -0.5,   # Security can reduce militancy
                "revolutionary_potential": -0.7,
                "solidarity_level": 0.4,       # But enables organization
            },

            # Class distribution determines political possibilities
            "class_distribution": {
                "revolutionary_potential": 0.8,  # Proletarian majority needed
                "collective_action": 0.7,
                "ideological_hegemony": -0.6,
            },

            # Alienation feeds back into class struggle
            "total_alienation": {
                "class_consciousness": 0.6,    # Alienation can spark awareness
                "solidarity_level": -0.5,      # But also atomizes workers
                "revolutionary_potential": 0.4,
            },
        }

    def calculate_class_polarization(self, indicators: dict[str, float]) -> float:
        """Calculate class polarization with theory-informed weights.

        Marx emphasized that inequality alone doesn't determine class struggle.
        The key is the relationship between:
        1. Concentration of capital (ownership)
        2. Immiseration of workers (material conditions)
        3. Collective organization potential (consciousness)
        """
        gini = indicators.get("gini_coefficient", 0)
        top10_share = indicators.get("income_share_top10", 0)
        bottom10_share = indicators.get("income_share_bottom10", 0)
        poverty_rate = indicators.get("poverty_headcount", 0)

        # Primary weight: Gini coefficient (overall inequality structure)
        gini_component = gini * 0.4

        # Secondary: Income concentration at extremes
        concentration_component = (
            top10_share * 0.25 +           # Capital concentration
            (1.0 - bottom10_share) * 0.15  # Worker impoverishment (inverted)
        )

        # Tertiary: Absolute poverty (immiseration)
        poverty_component = poverty_rate * 0.2

        polarization = gini_component + concentration_component + poverty_component

        # Apply theoretical bounds
        return float(np.clip(polarization, 0.0, 1.0))

    def calculate_labor_conditions(self, indicators: dict[str, float]) -> float:
        """Calculate labor conditions emphasizing worker power vs exploitation.

        Marx's focus: Not just employment rates, but the terms of employment
        and workers' position in the class struggle.
        """
        labor_participation = indicators.get("labor_force_participation", 0)
        unemployment_rate = indicators.get("unemployment_rate", 0)  # Already inverted
        wage_workers = indicators.get("wage_salaried_workers", 0)
        vulnerable_employment = indicators.get("vulnerable_employment", 0)  # Already inverted

        # Primary: Worker security and organization potential
        security_component = (
            unemployment_rate * 0.35 +      # Job security (inverted unemployment)
            vulnerable_employment * 0.25    # Employment quality (inverted vulnerability)
        )

        # Secondary: Labor force structure
        structure_component = (
            labor_participation * 0.25 +    # Worker engagement
            wage_workers * 0.15            # Proletarianization level
        )

        conditions = security_component + structure_component

        return float(np.clip(conditions, 0.0, 1.0))

    def apply_dialectical_adjustments(self,
                                   base_indicators: dict[str, float],
                                   consciousness_level: float) -> dict[str, float]:
        """Apply dialectical feedback effects between base and superstructure.

        Marx: "The philosophers have only interpreted the world in various ways;
        the point is to change it."
        """
        adjusted = base_indicators.copy()

        # High consciousness can improve material conditions through struggle
        if consciousness_level > CONSCIOUSNESS_HIGH_THRESHOLD:
            # Organized workers achieve better conditions
            adjusted["labor_conditions"] = min(1.0,
                adjusted.get("labor_conditions", 0) + 0.1)
            adjusted["subsistence_security"] = min(1.0,
                adjusted.get("subsistence_security", 0) + 0.05)

        # Low consciousness allows greater exploitation
        elif consciousness_level < CONSCIOUSNESS_LOW_THRESHOLD:
            # Disorganized or unaware populations may see increased exploitation
            adjusted["exploitation_rate"] = min(1.0,
                adjusted.get("exploitation_rate", 0) + 0.05)
            adjusted["ideological_hegemony"] = min(1.0,
                adjusted.get("ideological_hegemony", 0) + 0.05)

        # Crisis periods amplify all contradictions
        crisis_indicators = adjusted.get("crisis_intensity", 0)
        if crisis_indicators > CRISIS_INTENSITY_THRESHOLD:
            # Crisis sharpens class struggle
            for key in ["class_antagonism", "revolutionary_potential"]:
                if key in adjusted:
                    adjusted[key] = min(1.0, adjusted[key] * 1.2)

        return adjusted

    def calculate_revolutionary_potential(self,
                                       material_conditions: dict[str, float],
                                       consciousness_metrics: dict[str, float]) -> float:
        """Calculate revolutionary potential using Marx's conditions for revolution.

        Marx identified key conditions:
        1. Objective conditions: Crisis of ruling class, material immiseration
        2. Subjective conditions: Class consciousness, organization
        3. Historical moment: "The old is dying, the new cannot be born"
        """
        # Objective conditions (70% weight - material basis)
        exploitation = material_conditions.get("exploitation_rate", 0)
        class_antagonism = material_conditions.get("class_antagonism", 0)
        crisis_intensity = material_conditions.get("crisis_intensity", 0)

        objective_factor = (
            exploitation * 0.3 +        # Material basis for revolt
            abs(class_antagonism) * 0.25 +  # Sharpened contradictions
            crisis_intensity * 0.15     # System instability
        )

        # Subjective conditions (30% weight - consciousness and organization)
        class_consciousness = consciousness_metrics.get("class_consciousness", 0)
        collective_action = consciousness_metrics.get("collective_action_frequency", 0)
        solidarity = consciousness_metrics.get("solidarity_level", 0)

        subjective_factor = (
            class_consciousness * 0.15 + # Political awareness
            collective_action * 0.1 +    # Organizational capacity
            solidarity * 0.05            # Solidarity / cohesion
        )

        revolutionary_potential = objective_factor + subjective_factor

        # Apply theoretical constraints
        # Revolution requires BOTH objective AND subjective conditions
        if objective_factor < MIN_OBJECTIVE_FACTOR or subjective_factor < MIN_SUBJECTIVE_FACTOR:
            revolutionary_potential *= 0.5  # Insufficient conditions

        return float(np.clip(revolutionary_potential, 0.0, 1.0))


class HistoricalContextWeights:
    """Adjust weights based on historical period and context."""

    @staticmethod
    def crisis_period_adjustments() -> dict[str, float]:
        """Weight adjustments during economic/political crises.

        Crisis periods intensify contradictions and accelerate change.
        """
        return {
            "class_antagonism": 1.5,        # Crisis sharpens conflict
            "revolutionary_potential": 1.8, # Revolutionary situations emerge
            "ideological_hegemony": 0.7,    # Ruling ideas lose grip
            "solidarity_level": 1.3,        # People unite in struggle
            "subsistence_security": 0.6,    # Material conditions worsen
        }

    @staticmethod
    def stable_period_adjustments() -> dict[str, float]:
        """Weight adjustments during periods of stability/growth."""
        return {
            "ideological_hegemony": 1.2,    # Ruling ideas seem natural
            "subsistence_security": 1.1,    # Material improvements
            "revolutionary_potential": 0.5, # Reform rather than revolution
        }

    @staticmethod
    def detect_historical_period(indicators: dict[str, float]) -> str:
        """Detect current historical period to apply appropriate weights."""
        crisis_score = (
            indicators.get("unemployment_rate", 0.05) +  # Economic stress
            indicators.get("inequality_trend", 0) +      # Growing inequality
            indicators.get("political_instability", 0)   # Political crisis
        ) / 3

        if crisis_score > CRISIS_THRESHOLD:
            return "crisis"
        elif crisis_score < STABILITY_THRESHOLD:
            return "stable"
        else:
            # Transitional/moderate period where neither crisis nor stability dominates
            return "transitional"

def example_theoretical_weighting():
    """Demonstrate theory-informed quantification."""
    # Ensure basic logging configuration when run as a script
    logging.basicConfig(level=logging.INFO)
    scheme = TheoryInformedWeightingScheme()

    # Sample USA data
    usa_indicators = {
        "gini_coefficient": 0.418,
        "income_share_top10": 0.304,
        "income_share_bottom10": 0.018,
        "poverty_headcount": 0.012,
        "labor_force_participation": 0.619,
        "unemployment_rate": 0.959,  # Inverted
        "wage_salaried_workers": 0.939,
        "vulnerable_employment": 0.963,  # Inverted
    }

    consciousness_metrics = {
        "class_consciousness": 0.3,
        "collective_action_frequency": 0.2,
        "solidarity_level": 0.5,
    }

    # Apply theoretical weighting
    class_polarization = scheme.calculate_class_polarization(usa_indicators)
    labor_conditions = scheme.calculate_labor_conditions(usa_indicators)
    revolutionary_potential = scheme.calculate_revolutionary_potential(
        usa_indicators, consciousness_metrics,
    )

    logger.info("Theory-Informed Analysis:")
    logger.info("Class Polarization: %.3f", class_polarization)
    logger.info("Labor Conditions: %.3f", labor_conditions)
    logger.info("Revolutionary Potential: %.3f", revolutionary_potential)

    # Apply dialectical adjustments
    adjusted = scheme.apply_dialectical_adjustments(
        usa_indicators, consciousness_metrics["class_consciousness"],
    )

    logger.info("Dialectical Adjustments Applied: %d indicators modified", len(adjusted))


if __name__ == "__main__":
    example_theoretical_weighting()
