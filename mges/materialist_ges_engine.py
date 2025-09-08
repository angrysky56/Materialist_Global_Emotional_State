#!/usr/bin/env python3

"""Materialist Global Emotional State (GES) Engine.

------------------------------------------------
A systematic analysis of mass human emotional trajectories based on
materialist dialectics and Marx's understanding of collective consciousness.

Core Theoretical Framework:
- Social being determines consciousness (not abstract emotional substrates)
- Emotions emerge from material conditions and class relations
- Dialectical analysis of contradictions in production relations
- Historical materialism: emotions change with modes of production
- Class consciousness vs false consciousness analysis

"""

import asyncio
import logging
import math
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sqlmodel import SQLModel

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

# Threshold constants for crisis detection and analysis (avoid magic numbers in code)
CRISIS_INDICATOR_THRESHOLD = 0.7
HIGH_EXPLOITATION_THRESHOLD = CRISIS_INDICATOR_THRESHOLD
HIGH_REPRESSION_THRESHOLD = CRISIS_INDICATOR_THRESHOLD
HIGH_ALIENATION_THRESHOLD = CRISIS_INDICATOR_THRESHOLD
# Threshold below which ideological hegemony indicates a legitimacy crisis
LEGITIMACY_CRISIS_THRESHOLD = 0.3
# Threshold below which subsistence security indicates a subsistence crisis
SUBSISTENCE_CRISIS_THRESHOLD = 0.4
# Threshold above which the proletariat constitutes a clear majority of the population
PROLETARIAT_MAJORITY_THRESHOLD = 0.8
# Threshold above which technological development creates a constraint vis-à-vis existing ownership relations
TECH_DEVELOPMENT_CONSTRAINT_THRESHOLD = 0.8
# Threshold for private ownership share that indicates a constraint against socialized ownership (avoid magic numbers)
PRIVATE_OWNERSHIP_CONSTRAINT_THRESHOLD = 0.6
# Thresholds for consciousness/collective-action comparisons (replace magic numbers)
COLLECTIVE_ACTION_REVOLUTIONARY_THRESHOLD = 0.6
FALSE_CONSCIOUSNESS_STRONG_THRESHOLD = 0.6
CONSCIOUSNESS_REVOLUTIONARY_THRESHOLD = 0.7

# Limit for stored historical states per region (replace magic numbers in the codebase)
HISTORICAL_STATES_LIMIT = 1000

class RegionNotConfiguredError(Exception):
    """Raised when an analysis is requested for a region that has not been configured."""

    def __init__(self, region: str):
        super().__init__(f"Region {region} not configured")

# =============================================================================
# THEORETICAL FOUNDATIONS: MATERIAlIST DIALECTICS
# =============================================================================

class ProductionMode(Enum):
    """Historical modes of production that determine emotional superstructure."""

    PRIMITIVE_COMMUNISM = "primitive_communism"
    SLAVE_SOCIETY = "slave_society"
    FEUDALISM = "feudalism"
    CAPITALISM = "capitalism"
    SOCIALISM = "socialism"
    ADVANCED_COMMUNISM = "advanced_communism"


class ClassPosition(Enum):
    """Class positions that determine material interests and emotional responses."""

    BOURGEOISIE = "bourgeoisie"          # Owners of means of production
    PETITE_BOURGEOISIE = "petite_bourgeoisie"  # Small business owners
    PROLETARIAT = "proletariat"          # Wage laborers
    LUMPENPROLETARIAT = "lumpenproletariat"    # Unemployed/underemployed
    PEASANTRY = "peasantry"              # Agricultural workers
    INTELLIGENTSIA = "intelligentsia"     # Educated professional class


class MaterialContradiction(Enum):
    """Primary contradictions in production relations that drive emotional dynamics."""

    CAPITAL_VS_LABOR = "capital_vs_labor"
    USE_VALUE_VS_EXCHANGE_VALUE = "use_value_vs_exchange_value"
    SOCIAL_PRODUCTION_VS_PRIVATE_APPROPRIATION = "social_production_vs_private_appropriation"
    PRODUCTIVE_FORCES_VS_PRODUCTION_RELATIONS = "productive_forces_vs_production_relations"
    INDIVIDUAL_VS_COLLECTIVE = "individual_vs_collective"


class ConsciousnessType(Enum):
    """Types of collective consciousness that determine emotional expression."""

    CLASS_CONSCIOUSNESS = "class_consciousness"      # Awareness of true class interests
    FALSE_CONSCIOUSNESS = "false_consciousness"      # Distorted understanding of interests
    REVOLUTIONARY_CONSCIOUSNESS = "revolutionary_consciousness"  # Active opposition to current system
    REIFIED_CONSCIOUSNESS = "reified_consciousness"  # Accepts capitalism as natural


# =============================================================================
# MATERIAL DRIVERS: BASE DETERMINES SUPERSTRUCTURE
# =============================================================================

@dataclass
class MaterialConditions:
    """Concrete material conditions that determine emotional superstructure."""

    # ECONOMIC BASE (Primary)
    mode_of_production: ProductionMode
    ownership_relations: dict[str, float]  # Distribution of property ownership
    production_relations: dict[str, float]  # Class power relations

    # MATERIAL FORCES OF PRODUCTION
    technological_development: float  # 0-1 scale of productive capacity
    labor_productivity: float        # Output per worker
    resource_availability: float     # Access to natural resources
    infrastructure_quality: float    # Physical infrastructure

    # CLASS RELATIONS (Driving Force)
    class_distribution: dict[ClassPosition, float]  # Population by class
    exploitation_rate: float         # Surplus value extraction rate
    class_mobility: float           # Ability to change class position

    # MATERIAL WELFARE INDICATORS
    subsistence_security: float     # Basic survival needs met
    housing_security: float         # Adequate shelter
    healthcare_access: float        # Physical wellbeing
    education_access: float         # Knowledge development

    # ALIENATION INDICATORS (From Marx's theory)
    alienation_from_labor: float    # Control over work process
    alienation_from_product: float  # Ownership of work output
    alienation_from_species: float  # Connection to human nature
    alienation_from_others: float   # Social solidarity vs competition

    # SUPERSTRUCTURAL REFLECTIONS (Secondary)
    ideological_hegemony: float     # Dominant class's cultural control
    state_repression: float         # Government coercion level
    mass_media_concentration: float # Information control

    timestamp: datetime
    region: str


@dataclass
class CollectiveEmotionalState:
    """Collective emotional state as determined by material conditions.

    Based on Marx's understanding that consciousness is collective, not individual.
    """

    # PRIMARY EMOTIONAL DIMENSIONS (Material-Based)
    class_antagonism: float          # Intensity of class conflict (-1 to 1)
    revolutionary_potential: float   # Readiness for systemic change (0-1)
    solidarity_level: float         # Working class unity (0-1)
    alienation_intensity: float     # Overall alienation level (0-1)

    # DIALECTICAL CONTRAdICTIONS (Dynamic Tensions)
    primary_contradiction: MaterialContradiction
    contradiction_intensity: float  # How acute the contradiction (0-1)
    resolution_tendency: float      # Direction of contradiction resolution (-1 to 1)

    # CONSCIOUSNESS ANALYSIS
    consciousness_type: ConsciousnessType
    consciousness_clarity: float    # How clearly class interests are perceived (0-1)
    ideological_influence: float    # Degree of false consciousness (0-1)

    # HISTORICAL TRAJECTORY
    historical_momentum: float      # Direction of historical development (-1 to 1)
    crisis_indicators: list[str]    # Signs of systemic crisis

    # METADATA
    timestamp: datetime
    region: str
    material_conditions: MaterialConditions
    confidence: float = 0.0


@dataclass
class RegionalConfiguration:
    """Configuration for analyzing a regional collective emotional state."""

    name: str
    population_weight: float
    dominant_mode_of_production: ProductionMode
    class_structure: dict[ClassPosition, float]
    primary_contradictions: list[MaterialContradiction]
    historical_context: dict[str, Any]
    data_sources: list[str] = field(default_factory=list)


# =============================================================================
# CORE DIALECTICAL ANALYSIS ENGINE
# =============================================================================

class DialecticalAnalyzer:
    """Analyzes contradictions in material conditions using dialectical methodology.

    Based on Engels' three laws of dialectics:
    1. Unity and struggle of opposites
    2. Transformation of quantity into quality
    3. Negation of the negation
    """

    def __init__(self):
        self.contradiction_matrices = {}
        self.historical_patterns = {}

    def analyze_primary_contradiction(
        self,
        material_conditions: MaterialConditions,
    ) -> tuple[MaterialContradiction, float, float]:
        """Identify the primary contradiction driving emotional dynamics.

        Returns:
            - Primary contradiction type
            - Intensity of contradiction (0-1)
            - Resolution tendency (-1 to 1, negative = reactionary, positive = progressive)

        """
        # Analyze capital vs labor contradiction
        capital_labor_intensity = self._analyze_capital_labor_contradiction(material_conditions)

        # Analyze productive forces vs production relations
        forces_relations_intensity = self._analyze_forces_relations_contradiction(material_conditions)

        # Analyze use value vs exchange value
        value_intensity = self._analyze_value_contradiction(material_conditions)

        # Determine primary contradiction
        contradictions = {
            MaterialContradiction.CAPITAL_VS_LABOR: capital_labor_intensity,
            MaterialContradiction.PRODUCTIVE_FORCES_VS_PRODUCTION_RELATIONS: forces_relations_intensity,
            MaterialContradiction.USE_VALUE_VS_EXCHANGE_VALUE: value_intensity,
        }

        primary = max(contradictions.items(), key=lambda x: x[1])
        primary_contradiction, intensity = primary

        # Calculate resolution tendency based on historical momentum
        resolution_tendency = self._calculate_resolution_tendency(
            primary_contradiction, material_conditions,
        )

        return primary_contradiction, intensity, resolution_tendency

    def _analyze_capital_labor_contradiction(self, conditions: MaterialConditions) -> float:
        """Analyze intensity of capital vs labor contradiction."""
        # Higher exploitation rate increases contradiction
        exploitation_component = conditions.exploitation_rate

        # Greater class inequality increases contradiction
        bourgeois_share = conditions.class_distribution.get(ClassPosition.BOURGEOISIE, 0.01)
        proletariat_share = conditions.class_distribution.get(ClassPosition.PROLETARIAT, 0.5)
        class_polarization = abs(bourgeois_share - proletariat_share)

        # Lower subsistence security increases contradiction
        material_deprivation = 1.0 - conditions.subsistence_security

        # Combine factors
        intensity = np.mean([exploitation_component, class_polarization, material_deprivation])

        return float(np.clip(intensity, 0.0, 1.0))

    def _analyze_forces_relations_contradiction(self, conditions: MaterialConditions) -> float:
        """Analyze contradiction between productive forces and production relations."""
        # High technological development vs old production relations
        tech_development = conditions.technological_development

        # Productive capacity vs actual utilization (crises of overproduction)
        productivity_gap = conditions.labor_productivity - conditions.subsistence_security

        # Infrastructure development vs ownership constraints
        infrastructure_constraint = conditions.infrastructure_quality * (1 - conditions.ownership_relations.get("public", 0.3))

        intensity = np.mean([tech_development, np.clip(productivity_gap, 0, 1), infrastructure_constraint])

        return float(np.clip(intensity, 0.0, 1.0))

    def _analyze_value_contradiction(self, conditions: MaterialConditions) -> float:
        """Analyze use value vs exchange value contradiction."""
        # Market commodification vs human needs
        commodification = 1.0 - conditions.subsistence_security

        # Private ownership vs social production
        private_ownership = conditions.ownership_relations.get("private", 0.7)
        social_production = conditions.labor_productivity  # Proxy for social cooperation

        intensity = np.mean([commodification, private_ownership * social_production])

        return float(np.clip(intensity, 0.0, 1.0))

    def _calculate_resolution_tendency(
        self,
        contradiction: MaterialContradiction,
        conditions: MaterialConditions,
    ) -> float:
        """Calculate tendency for contradiction resolution.

        Returns:
            -1 to 1 scale:
            -1 = Reactionary resolution (strengthen capitalism)
             0 = Stagnation
            +1 = Progressive resolution (toward socialism)

        """
        # Base tendency on class consciousness and organization
        proletariat_share = conditions.class_distribution.get(ClassPosition.PROLETARIAT, 0.5)
        consciousness_factor = 1.0 - conditions.ideological_hegemony
        organization_factor = 1.0 - conditions.alienation_from_others

        # Account for repressive capacity of ruling class
        repression_factor = conditions.state_repression

        # Progressive tendency
        progressive_force = proletariat_share * consciousness_factor * organization_factor

        # Reactionary tendency
        reactionary_force = repression_factor * conditions.ideological_hegemony

        # Net tendency
        tendency = progressive_force - reactionary_force

        return np.clip(tendency, -1.0, 1.0)


class ClassConsciousnessAnalyzer:
    """Analyzes development of class consciousness vs false consciousness.

    Based on Marx's theory that workers develop from "class in itself"
    to "class for itself" through collective struggle.
    """

    def __init__(self):
        self.consciousness_indicators = {}

    def analyze_consciousness_type(
        self,
        material_conditions: MaterialConditions,
    ) -> tuple[ConsciousnessType, float]:
        """Determine dominant type of consciousness and its clarity.

        Returns:
            - Consciousness type
            - Clarity level (0-1)

        """
        # Calculate class consciousness indicators
        class_solidarity = 1.0 - material_conditions.alienation_from_others
        material_awareness = 1.0 - material_conditions.ideological_hegemony
        collective_action = self._calculate_collective_action_capacity(material_conditions)

        class_consciousness_level = float(np.clip(np.mean([class_solidarity, material_awareness, collective_action]), 0.0, 1.0))

        # Calculate false consciousness indicators
        ideological_penetration = material_conditions.ideological_hegemony
        media_influence = material_conditions.mass_media_concentration
        individual_competition = material_conditions.alienation_from_others

        false_consciousness_level = float(np.clip(np.mean([ideological_penetration, media_influence, individual_competition]), 0.0, 1.0))
        # Determine dominant consciousness type using clear, non-overlapping conditions
        if class_consciousness_level > CONSCIOUSNESS_REVOLUTIONARY_THRESHOLD and collective_action > COLLECTIVE_ACTION_REVOLUTIONARY_THRESHOLD:
            return ConsciousnessType.REVOLUTIONARY_CONSCIOUSNESS, class_consciousness_level
        if class_consciousness_level > false_consciousness_level:
            return ConsciousnessType.CLASS_CONSCIOUSNESS, class_consciousness_level
            return ConsciousnessType.CLASS_CONSCIOUSNESS, class_consciousness_level
        if (
            material_conditions.mode_of_production == ProductionMode.CAPITALISM
            and false_consciousness_level > FALSE_CONSCIOUSNESS_STRONG_THRESHOLD
        ):
            return ConsciousnessType.REIFIED_CONSCIOUSNESS, false_consciousness_level

        return ConsciousnessType.FALSE_CONSCIOUSNESS, false_consciousness_level

    def _calculate_collective_action_capacity(self, conditions: MaterialConditions) -> float:
        """Calculate capacity for collective action based on material conditions."""
        # Factors that enable collective action
        workplace_concentration = conditions.labor_productivity  # Proxy for large-scale production
        communication_access = 1.0 - conditions.mass_media_concentration
        organizational_freedom = 1.0 - conditions.state_repression
        material_security = conditions.subsistence_security  # Can't organize if starving

        capacity = np.mean([workplace_concentration, communication_access, organizational_freedom, material_security])

        return float(np.clip(capacity, 0.0, 1.0))


# =============================================================================
# MATERIAlIST GES ENGINE
# =============================================================================

class MaterialistGESEngine:
    """Global Emotional State Engine based on materialist dialectics.

    Analyzes collective emotional trajectories as products of material
    conditions and class relations, not abstract psychological substrates.
    """

    def __init__(self):
        self.regions: dict[str, RegionalConfiguration] = {}
        self.dialectical_analyzer = DialecticalAnalyzer()
        self.consciousness_analyzer = ClassConsciousnessAnalyzer()
        self.historical_states: dict[str, list[CollectiveEmotionalState]] = {}
        self.latest_states: dict[str, CollectiveEmotionalState] = {}

        logger.info("Initialized Materialist GES Engine")

    def add_region(self, config: RegionalConfiguration) -> None:
        """Add a region for materialist analysis."""
        self.regions[config.name] = config
        self.historical_states[config.name] = []
        logger.info("Added region for materialist analysis: %s", config.name)

    def analyze_regional_state(
        self,
        region: str,
        material_conditions: MaterialConditions,
    ) -> CollectiveEmotionalState:
        """Analyze and return the collective emotional state for a region based on material conditions.

        This is the core method that applies materialist dialectics to determine emotional
        superstructure from the economic base.
        """
        if region not in self.regions:
            # Use a dedicated exception class to encapsulate message formatting
            raise RegionNotConfiguredError(region)

        config = self.regions[region]

        # STEP 1: Dialectical analysis of primary contradictions
        primary_contradiction, contradiction_intensity, resolution_tendency = \
            self.dialectical_analyzer.analyze_primary_contradiction(material_conditions)

        # STEP 2: Class consciousness analysis
        consciousness_type, consciousness_clarity = \
            self.consciousness_analyzer.analyze_consciousness_type(material_conditions)

        # STEP 3: Calculate emotional dimensions from material base

        # Class antagonism emerges from exploitation and class polarization
        class_antagonism = self._calculate_class_antagonism(material_conditions)

        # Revolutionary potential based on contradiction intensity and consciousness
        revolutionary_potential = self._calculate_revolutionary_potential(
            contradiction_intensity, consciousness_clarity, consciousness_type,
        )

        # Solidarity level based on collective vs individual orientation
        solidarity_level = self._calculate_solidarity_level(material_conditions)

        # Alienation intensity from Marx's four types of alienation
        alienation_intensity = self._calculate_alienation_intensity(material_conditions)

        # Historical momentum based on resolution tendency
        historical_momentum = resolution_tendency

        # Crisis indicators based on contradiction analysis
        crisis_indicators = self._identify_crisis_indicators(material_conditions, primary_contradiction)

        # Create collective emotional state
        state = CollectiveEmotionalState(
            class_antagonism=class_antagonism,
            revolutionary_potential=revolutionary_potential,
            solidarity_level=solidarity_level,
            alienation_intensity=alienation_intensity,
            primary_contradiction=primary_contradiction,
            contradiction_intensity=contradiction_intensity,
            resolution_tendency=resolution_tendency,
            consciousness_type=consciousness_type,
            consciousness_clarity=consciousness_clarity,
            ideological_influence=material_conditions.ideological_hegemony,
            historical_momentum=historical_momentum,
            crisis_indicators=crisis_indicators,
            timestamp=datetime.now(tz=timezone.utc),
            region=region,
            material_conditions=material_conditions,
        )

        # Compute and store confidence for this analysis
        state.confidence = self._calculate_analysis_confidence(material_conditions)

        # Store state
        self.historical_states[region].append(state)
        self.latest_states[region] = state

        # Limit historical data
        if len(self.historical_states[region]) > HISTORICAL_STATES_LIMIT:
            self.historical_states[region] = self.historical_states[region][-HISTORICAL_STATES_LIMIT:]

        # Use parameterized logging to defer string interpolation to the logging system
        logger.info("Analyzed materialist emotional state for %s: %s", region, consciousness_type.value)

        return state

    def _calculate_class_antagonism(self, conditions: MaterialConditions) -> float:
        """Calculate class antagonism based on material class relations.

        High when:
        - High exploitation rate
        - Large wealth inequality
        - Low class mobility
        - High competition between workers
        """
        exploitation_factor = conditions.exploitation_rate

        # Class polarization
        bourgeois_share = conditions.class_distribution.get(ClassPosition.BOURGEOISIE, 0.01)
        proletariat_share = conditions.class_distribution.get(ClassPosition.PROLETARIAT, 0.5)
        class_polarization = abs(bourgeois_share * 100 - proletariat_share)  # Wealth concentration

        mobility_constraint = 1.0 - conditions.class_mobility
        worker_competition = conditions.alienation_from_others

        # Combine factors
        antagonism = np.mean([
            exploitation_factor,
            np.clip(class_polarization / 50, 0, 1),  # Normalize
            mobility_constraint,
            worker_competition,
        ])

        # Scale to -1 to 1 (negative = class collaboration, positive = class conflict)
        return float((antagonism * 2) - 1)

    def _calculate_revolutionary_potential(
        self,
        contradiction_intensity: float,
        consciousness_clarity: float,
        consciousness_type: ConsciousnessType,
    ) -> float:
        """Calculate revolutionary potential based on objective and subjective conditions.

        Requires both:
        - Objective conditions: High contradiction intensity
        - Subjective conditions: Class consciousness.
        """
        # Objective factor: material contradictions
        objective_factor = contradiction_intensity

        # Subjective factor: consciousness development
        if consciousness_type == ConsciousnessType.REVOLUTIONARY_CONSCIOUSNESS:
            subjective_factor = consciousness_clarity
        elif consciousness_type == ConsciousnessType.CLASS_CONSCIOUSNESS:
            subjective_factor = consciousness_clarity * 0.7
        else:
            subjective_factor = consciousness_clarity * 0.3

        # Revolutionary potential requires both factors
        potential = objective_factor * subjective_factor

        return np.clip(potential, 0.0, 1.0)

    def _calculate_solidarity_level(self, conditions: MaterialConditions) -> float:
        """Calculate working class solidarity based on material conditions.

        High when:
        - Low alienation from others
        - Shared material interests
        - Collective production processes
        - Low ideological division
        """
        interpersonal_solidarity = 1.0 - conditions.alienation_from_others
        shared_interests = conditions.class_distribution.get(ClassPosition.PROLETARIAT, 0.5)
        collective_production = conditions.labor_productivity  # Proxy for socialized production
        ideological_unity = 1.0 - conditions.ideological_hegemony

        solidarity = np.mean([
            interpersonal_solidarity,
            shared_interests,
            collective_production,
            ideological_unity,
        ])

        return float(np.clip(solidarity, 0.0, 1.0))

    def _calculate_alienation_intensity(self, conditions: MaterialConditions) -> float:
        """Calculate overall alienation intensity from Marx's four types.

        Marx identified four types of alienation under capitalism:
        1. From labor process
        2. From product of labor
        3. From species-being (human nature)
        4. From other workers
        """
        alienation_types = [
            conditions.alienation_from_labor,
            conditions.alienation_from_product,
            conditions.alienation_from_species,
            conditions.alienation_from_others,
        ]

        intensity = float(np.clip(np.mean(alienation_types), 0.0, 1.0))
        return intensity

    def _identify_crisis_indicators(
        self,
        conditions: MaterialConditions,
        primary_contradiction: MaterialContradiction,
    ) -> list[str]:
        """Identify indicators of systemic crisis based on contradictions."""
        indicators: list[str] = []
        checks = [
            (conditions.exploitation_rate > HIGH_EXPLOITATION_THRESHOLD, "extreme_exploitation"),
            (conditions.subsistence_security < SUBSISTENCE_CRISIS_THRESHOLD, "subsistence_crisis"),
            (conditions.class_distribution.get(ClassPosition.PROLETARIAT, 0.5) > PROLETARIAT_MAJORITY_THRESHOLD, "proletariat_majority"),
            (conditions.state_repression > HIGH_REPRESSION_THRESHOLD, "repressive_state_apparatus"),
            (conditions.ideological_hegemony < LEGITIMACY_CRISIS_THRESHOLD, "legitimacy_crisis"),
            (conditions.alienation_from_others > HIGH_ALIENATION_THRESHOLD, "social_fragmentation"),
            (conditions.alienation_from_species > HIGH_ALIENATION_THRESHOLD, "human_nature_crisis"),
        ]

        for cond, label in checks:
            if cond:
                indicators.append(label)

        # Composite condition for productive forces vs relations crisis
        if (
            primary_contradiction == MaterialContradiction.PRODUCTIVE_FORCES_VS_PRODUCTION_RELATIONS
            and conditions.technological_development > TECH_DEVELOPMENT_CONSTRAINT_THRESHOLD
            and conditions.ownership_relations.get("private", 0.7) > PRIVATE_OWNERSHIP_CONSTRAINT_THRESHOLD
        ):
            indicators.append("productive_forces_constraint")

        return indicators

    def _calculate_analysis_confidence(self, conditions: MaterialConditions) -> float:
        """Calculate confidence in the materialist analysis."""
        # Higher confidence with:
        # - Clear class divisions
        # - Developed productive forces
        # - Less ideological confusion

        class_clarity = max(conditions.class_distribution.values()) - min(conditions.class_distribution.values())
        productive_development = conditions.technological_development
        ideological_clarity = 1.0 - conditions.ideological_hegemony

        confidence = np.mean([class_clarity, productive_development, ideological_clarity])

        return float(np.clip(confidence, 0.1, 1.0))

    def compute_global_indices(self) -> dict[str, Any]:
        """Compute global indices based on materialist analysis.

        Instead of abstract "emotional indices", compute material indicators:
        - Global class consciousness level
        - Revolutionary potential index
        - Crisis intensity index
        - Historical momentum indicator
        """
        if not self.latest_states:
            return {
                "global_class_consciousness": 0.0,
                "global_revolutionary_potential": 0.0,
                "global_crisis_intensity": 0.0,
                "global_historical_momentum": 0.0,
                "timestamp": datetime.now(tz=timezone.utc),
            }

        states = list(self.latest_states.values())
        weights = np.array([self.regions[state.region].population_weight for state in states])
        weights = weights / np.sum(weights)  # Normalize

        # Global class consciousness (weighted average)
        consciousness_scores = []
        for state in states:
            if state.consciousness_type == ConsciousnessType.REVOLUTIONARY_CONSCIOUSNESS:
                score = state.consciousness_clarity
            elif state.consciousness_type == ConsciousnessType.CLASS_CONSCIOUSNESS:
                score = state.consciousness_clarity * 0.7
            else:
                score = state.consciousness_clarity * 0.3
            consciousness_scores.append(score)

        global_class_consciousness = np.average(consciousness_scores, weights=weights)

        # Global revolutionary potential
        global_revolutionary_potential = np.average(
            [s.revolutionary_potential for s in states], weights=weights,
        )

        # Global crisis intensity (based on contradiction intensity)
        global_crisis_intensity = np.average(
            [s.contradiction_intensity for s in states], weights=weights,
        )

        # Global historical momentum
        global_historical_momentum = np.average(
            [s.historical_momentum for s in states], weights=weights,
        )

        # Identify global crisis indicators
        all_crisis_indicators = []
        for state in states:
            all_crisis_indicators.extend(state.crisis_indicators)

        crisis_frequency = {}
        for indicator in all_crisis_indicators:
            crisis_frequency[indicator] = crisis_frequency.get(indicator, 0) + 1

        return {
            "global_class_consciousness": global_class_consciousness,
            "global_revolutionary_potential": global_revolutionary_potential,
            "global_crisis_intensity": global_crisis_intensity,
            "global_historical_momentum": global_historical_momentum,
            "dominant_crisis_indicators": dict(sorted(crisis_frequency.items(), key=lambda x: x[1], reverse=True)[:5]),
            "timestamp": datetime.now(tz=timezone.utc),
            "analysis_confidence": np.average([s.confidence for s in states], weights=weights),
        }

    def get_regional_summary(self) -> dict[str, dict[str, Any]]:
        """Get materialist analysis summary for all regions."""
        summary = {}

        for region in self.regions:
            latest_state = self.latest_states.get(region)
            if not latest_state:
                continue

            region_summary = {
                "material_analysis": {
                    "mode_of_production": latest_state.material_conditions.mode_of_production.value,
                    "dominant_class": max(latest_state.material_conditions.class_distribution.items(), key=lambda x: x[1])[0].value,
                    "exploitation_rate": latest_state.material_conditions.exploitation_rate,
                    "alienation_intensity": latest_state.alienation_intensity,
                },
                "consciousness_analysis": {
                    "consciousness_type": latest_state.consciousness_type.value,
                    "consciousness_clarity": latest_state.consciousness_clarity,
                    "ideological_influence": latest_state.ideological_influence,
                },
                "dialectical_analysis": {
                    "primary_contradiction": latest_state.primary_contradiction.value,
                    "contradiction_intensity": latest_state.contradiction_intensity,
                    "resolution_tendency": latest_state.resolution_tendency,
                    "historical_momentum": latest_state.historical_momentum,
                },
                "collective_emotions": {
                    "class_antagonism": latest_state.class_antagonism,
                    "revolutionary_potential": latest_state.revolutionary_potential,
                    "solidarity_level": latest_state.solidarity_level,
                },
                "crisis_indicators": latest_state.crisis_indicators,
                "data_points": len(self.historical_states.get(region, [])),
                "population_weight": self.regions[region].population_weight,
                "analysis_confidence": latest_state.confidence,
            }

            summary[region] = region_summary

        return summary


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

def create_default_regional_configs(region_names: list[str]) -> list[RegionalConfiguration]:
    """Create default regional configurations for materialist analysis."""
    # Approximate current class structures (these should be empirically determined)
    default_class_structures = {
        "USA": {
            ClassPosition.BOURGEOISIE: 0.02,
            ClassPosition.PETITE_BOURGEOISIE: 0.15,
            ClassPosition.PROLETARIAT: 0.70,
            ClassPosition.LUMPENPROLETARIAT: 0.10,
            ClassPosition.INTELLIGENTSIA: 0.03,
        },
        "CHN": {
            ClassPosition.BOURGEOISIE: 0.01,
            ClassPosition.PETITE_BOURGEOISIE: 0.20,
            ClassPosition.PROLETARIAT: 0.60,
            ClassPosition.PEASANTRY: 0.15,
            ClassPosition.INTELLIGENTSIA: 0.04,
        },
        "IND": {
            ClassPosition.BOURGEOISIE: 0.01,
            ClassPosition.PETITE_BOURGEOISIE: 0.10,
            ClassPosition.PROLETARIAT: 0.40,
            ClassPosition.PEASANTRY: 0.45,
            ClassPosition.LUMPENPROLETARIAT: 0.04,
        },
    }

    # Default to capitalist mode with generic class structure
    default_structure = {
        ClassPosition.BOURGEOISIE: 0.02,
        ClassPosition.PETITE_BOURGEOISIE: 0.15,
        ClassPosition.PROLETARIAT: 0.65,
        ClassPosition.PEASANTRY: 0.10,
        ClassPosition.LUMPENPROLETARIAT: 0.08,
    }

    configs = []

    for region_name in region_names:
        class_structure = default_class_structures.get(region_name, default_structure)

        config = RegionalConfiguration(
            name=region_name,
            population_weight=1.0 / len(region_names),  # Equal weight for now
            dominant_mode_of_production=ProductionMode.CAPITALISM,
            class_structure=class_structure,
            primary_contradictions=[
                MaterialContradiction.CAPITAL_VS_LABOR,
                MaterialContradiction.PRODUCTIVE_FORCES_VS_PRODUCTION_RELATIONS,
            ],
            historical_context={
                "development_level": "developed" if region_name in ["USA", "DEU", "UK"] else "developing",
                "colonial_history": region_name not in ["USA", "UK", "DEU", "FRA"],
                "socialist_experience": region_name in ["CHN", "VNM", "CUB"],
            },
            data_sources=["economic_indicators", "labor_statistics", "social_movements"],
        )

        configs.append(config)

    return configs


if __name__ == "__main__":
    # Example usage
    engine = MaterialistGESEngine()

    # Add regions
    configs = create_default_regional_configs(["USA", "CHN", "DEU"])
    for config in configs:
        engine.add_region(config)

    # Example material conditions analysis
    usa_conditions = MaterialConditions(
        mode_of_production=ProductionMode.CAPITALISM,
        ownership_relations={"private": 0.85, "public": 0.15},
        production_relations={"capitalist": 0.75, "cooperative": 0.05, "state": 0.20},
        technological_development=0.9,
        labor_productivity=0.8,
        resource_availability=0.7,
        infrastructure_quality=0.8,
        class_distribution={
            ClassPosition.BOURGEOISIE: 0.02,
            ClassPosition.PETITE_BOURGEOISIE: 0.15,
            ClassPosition.PROLETARIAT: 0.70,
            ClassPosition.LUMPENPROLETARIAT: 0.10,
            ClassPosition.INTELLIGENTSIA: 0.03,
        },
        exploitation_rate=0.6,
        class_mobility=0.3,
        subsistence_security=0.7,
        housing_security=0.6,
        healthcare_access=0.7,
        education_access=0.8,
        alienation_from_labor=0.7,
        alienation_from_product=0.8,
        alienation_from_species=0.6,
        alienation_from_others=0.7,
        ideological_hegemony=0.7,
        state_repression=0.4,
        mass_media_concentration=0.8,
        timestamp=datetime.now(tz=timezone.utc),
        region="USA",
    )

    # Analyze emotional state
    state = engine.analyze_regional_state("USA", usa_conditions)

    logger.info("=== MATERIALIST GES ANALYSIS ===")
    logger.info("Region: %s", state.region)
    logger.info("Consciousness Type: %s", state.consciousness_type.value)
    logger.info("Primary Contradiction: %s", state.primary_contradiction.value)
    logger.info("Class Antagonism: %.2f", state.class_antagonism)
    logger.info("Revolutionary Potential: %.2f", state.revolutionary_potential)
    logger.info("Crisis Indicators: %s", state.crisis_indicators)
