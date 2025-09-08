#!/usr/bin/env python3
"""Historical Materialist Analysis Engine.

This module implements time-series analysis to track the evolution of
material conditions and validate theoretical predictions against
historical revolutionary periods.

Key capabilities:
1. Time-series data collection and analysis
2. Historical trajectory modeling
3. Revolutionary period validation (1848, 1917, 1968, 2011)
4. Crisis prediction based on contradiction intensity
5. Class consciousness evolution tracking
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import find_peaks

from .materialist_data_sources import MaterialistDataManager
from .materialist_ges_engine import CollectiveEmotionalState, ConsciousnessType, MaterialConditions, MaterialistGESEngine
from .theoretical_weighting import TheoryInformedWeightingScheme

logger = logging.getLogger(__name__)

# Constants for thresholds and configurations
REVOLUTIONARY_POTENTIAL_THRESHOLD = 0.6
CRISIS_INTENSITY_THRESHOLD = 0.7
CRISIS_LOW_INTENSITY_THRESHOLD = 0.3
CONSCIOUSNESS_SLOPE_RISING_THRESHOLD = 0.01
CONSCIOUSNESS_SLOPE_DECLINING_THRESHOLD = -0.01
CONTRADICTION_SLOPE_THRESHOLD = 0.005
TREND_SLOPE_THRESHOLD = 0.01
MAX_DAYS_FROM_EVENT = 365 * 2
EVENT_DATE_MONTH = 1
HISTORICAL_PROJECTION_CENTURY_SCALE = 100
INEQUALITY_U_SHAPE_LOW = 1930
INEQUALITY_U_SHAPE_POST_WAR_HIGH = 1980
LABOR_ORG_HIGH_PERIOD_START = 1930
LABOR_ORG_HIGH_PERIOD_END = 1970


@dataclass
class HistoricalEvent:
    """Represents a significant historical event for validation."""

    year: int
    event_type: str  # 'revolution', 'crisis', 'reform', 'reaction'
    region: str
    description: str
    intensity: float  # 0.0-1.0 scale

    # Theoretical characteristics
    objective_conditions: float  # Material conditions severity
    subjective_conditions: float  # Class consciousness level
    outcome: str  # 'success', 'failure', 'partial', 'suppressed'


@dataclass
class TimeSeriesPoint:
    """Single data point in historical time series."""

    date: datetime
    indicators: dict[str, float]
    consciousness_type: ConsciousnessType
    revolutionary_potential: float
    crisis_intensity: float
    confidence: float


class HistoricalValidator:
    """Validates theoretical predictions against known historical events."""

    def __init__(self):
        self.known_events = self._load_historical_events()
        self.validation_results = {}

    def _load_historical_events(self) -> list[HistoricalEvent]:
        """Load known revolutionary/crisis periods for validation."""
        return [
            # 1848 - "Spring of Peoples" European Revolutions
            HistoricalEvent(
                year=1848, event_type='revolution', region='EUR',
                description='European Revolutions of 1848',
                intensity=0.8, objective_conditions=0.9, subjective_conditions=0.6,
                outcome='partial',
            ),

            # 1871 - Paris Commune
            HistoricalEvent(
                year=1871, event_type='revolution', region='FRA',
                description='Paris Commune',
                intensity=0.9, objective_conditions=0.8, subjective_conditions=0.8,
                outcome='suppressed',
            ),

            # 1917 - Russian Revolution
            HistoricalEvent(
                year=1917, event_type='revolution', region='RUS',
                description='Russian Revolution',
                intensity=1.0, objective_conditions=0.95, subjective_conditions=0.9,
                outcome='success',
            ),

            # 1929 - Great Depression
            HistoricalEvent(
                year=1929, event_type='crisis', region='USA',
                description='Great Depression begins',
                intensity=0.9, objective_conditions=0.9, subjective_conditions=0.4,
                outcome='reform',  # New Deal response
            ),

            # 1968 - Global protest wave
            HistoricalEvent(
                year=1968, event_type='revolution', region='GLOBAL',
                description='Global protest movements',
                intensity=0.7, objective_conditions=0.6, subjective_conditions=0.8,
                outcome='partial',
            ),

            # 2008 - Financial Crisis
            HistoricalEvent(
                year=2008, event_type='crisis', region='GLOBAL',
                description='Global Financial Crisis',
                intensity=0.8, objective_conditions=0.8, subjective_conditions=0.3,
                outcome='failure',  # Limited consciousness response
            ),

            # 2011 - Arab Spring / Occupy Movement
            HistoricalEvent(
                year=2011, event_type='revolution', region='GLOBAL',
                description='Arab Spring and Occupy movements',
                intensity=0.6, objective_conditions=0.7, subjective_conditions=0.6,
                outcome='partial',
            ),
        ]

    async def validate_theoretical_predictions(self,
                                            time_series: list[TimeSeriesPoint],
                                            region: str) -> dict[str, float]:
        """Validate model predictions against historical events."""
        validation_scores = {
            'revolution_prediction_accuracy': 0.0,
            'crisis_detection_accuracy': 0.0,
            'consciousness_evolution_accuracy': 0.0,
            'overall_historical_accuracy': 0.0,
        }

        # Filter events for region
        relevant_events = [e for e in self.known_events
                          if e.region in (region, 'GLOBAL')]

        if not relevant_events:
            logger.warning("No historical events found for region %s", region)
            return validation_scores

        correct_predictions = 0
        total_predictions = 0

        for event in relevant_events:
            # Find closest time series point to event
            event_date = datetime(event.year, 1, 1, tzinfo=UTC)
            closest_point = min(time_series,
                               key=lambda p: abs((p.date - event_date).days))

            if abs((closest_point.date - event_date).days) > 365 * 2:
                continue  # Too far from event

            # Validate prediction
            if event.event_type == 'revolution':
                predicted_correctly = (
                    closest_point.revolutionary_potential > REVOLUTIONARY_POTENTIAL_THRESHOLD and
                    closest_point.consciousness_type in [
                        ConsciousnessType.CLASS_CONSCIOUSNESS,
                        ConsciousnessType.REVOLUTIONARY_CONSCIOUSNESS,
                    ]
                )
            elif event.event_type == 'crisis':
                predicted_correctly = closest_point.crisis_intensity > CRISIS_INTENSITY_THRESHOLD
            else:
                continue

            if predicted_correctly:
                correct_predictions += 1
            total_predictions += 1

            logger.info("Event %s (%s): Predicted correctly = %s",
                       event.description, event.year, predicted_correctly)

        if total_predictions > 0:
            validation_scores['overall_historical_accuracy'] = correct_predictions / total_predictions

        return validation_scores


class HistoricalTrendAnalyzer:
    """Analyzes long-term trends in material conditions and consciousness."""

    def __init__(self):
        self.weighting_scheme = TheoryInformedWeightingScheme()

    def detect_historical_patterns(self,
                                 time_series: list[TimeSeriesPoint]) -> dict[str, Any]:
        """Detect patterns in historical data."""
        if len(time_series) < 10:
            logger.warning("Insufficient data for pattern detection")
            return {}

        # Convert to DataFrame for analysis
        ts_df = self._time_series_to_dataframe(time_series)

        patterns = {
            'trends': self._analyze_trends(ts_df),
            'cycles': self._detect_cycles(ts_df),
            'crisis_patterns': self._analyze_crisis_patterns(ts_df),
            'consciousness_evolution': self._track_consciousness_evolution(ts_df),
            'contradiction_dynamics': self._analyze_contradiction_dynamics(ts_df),
        }

        return patterns

    def _time_series_to_dataframe(self, time_series: list[TimeSeriesPoint]) -> pd.DataFrame:
        """Convert time series to pandas DataFrame for analysis."""
        data = []
        for point in time_series:
            row = {
                'date': point.date,
                'revolutionary_potential': point.revolutionary_potential,
                'crisis_intensity': point.crisis_intensity,
                'consciousness_type_numeric': point.consciousness_type.value,
                'confidence': point.confidence,
            }
            # Add all indicators
            row.update(point.indicators)
            data.append(row)

        time_series_df = pd.DataFrame(data)
        # Avoid inplace operations for consistent behavior across pandas versions
        time_series_df = time_series_df.set_index('date')
        time_series_df = time_series_df.sort_index()
        return time_series_df

    def _analyze_trends(self, ts_df: pd.DataFrame) -> dict[str, float]:
        """Analyze long-term trends in key indicators."""
        trends = {}

        key_indicators = [
            'revolutionary_potential', 'crisis_intensity',
            'gini_coefficient', 'unemployment_rate', 'union_density',
        ]

        for indicator in key_indicators:
            if indicator in ts_df.columns:
                # Calculate trend slope using linear regression
                x = np.arange(len(ts_df))
                y = ts_df[indicator].ffill().to_numpy()
                if len(y) > 1:
                    slope, _, r_value, _, _ = stats.linregress(x, y)
                    trends[f'{indicator}_trend'] = slope
                    # Ensure r_value is a scalar (stats.linregress may return array-like in some contexts)
                    try:
                        # Convert r_value to a numeric scalar robustly:
                        # - np.asarray handles numpy scalars and arrays
                        # - np.squeeze reduces zero-dimensional arrays to scalars
                        # - float(...) attempts conversion to a Python float
                        r_arr = np.asarray(r_value)
                        r_scalar = np.squeeze(r_arr)
                        r_float = float(r_scalar)
                        trends[f'{indicator}_correlation'] = r_float ** 2
                    except Exception:
                        # Handle tuple/list/ndarray or objects with a numeric attribute/element as a fallback
                        try:
                            if isinstance(r_value, tuple | list | np.ndarray) and len(r_value) > 0:
                                candidate = r_value[0]
                                trends[f'{indicator}_correlation'] = float(candidate) ** 2
                            else:
                                # Safely probe for common numeric-like attributes without direct attribute access
                                candidate = None
                                for attr in ('rvalue', 'r', 'rho', 'correlation'):
                                    val = getattr(r_value, attr, None)
                                    if val is not None:
                                        candidate = val
                                        break
                                if candidate is not None:
                                    trends[f'{indicator}_correlation'] = float(candidate) ** 2
                                else:
                                    trends[f'{indicator}_correlation'] = float("nan")
                        except Exception:
                            trends[f'{indicator}_correlation'] = float("nan")

        return trends

    def _detect_cycles(self, ts_df: pd.DataFrame) -> dict[str, Any]:
        """Detect cyclical patterns in material conditions."""
        cycles = {}

        # Analyze revolutionary potential cycles
        if 'revolutionary_potential' in ts_df.columns:
            rev_pot = ts_df['revolutionary_potential'].ffill()
            peaks, _ = find_peaks(rev_pot, height=REVOLUTIONARY_POTENTIAL_THRESHOLD, distance=10)
            troughs, _ = find_peaks(-rev_pot, height=-CRISIS_LOW_INTENSITY_THRESHOLD, distance=10)

            cycles['revolutionary_peaks'] = len(peaks)
            cycles['revolutionary_troughs'] = len(troughs)

            if len(peaks) > 1:
                peak_intervals = np.diff([ts_df.index[i] for i in peaks])
                cycles['average_revolutionary_cycle'] = np.mean([
                    interval.days for interval in peak_intervals
                ]) / 365.25  # Convert to years

        # Analyze crisis cycles
        if 'crisis_intensity' in ts_df.columns:
            crisis = ts_df['crisis_intensity'].ffill()
            crisis_peaks, _ = find_peaks(crisis, height=CRISIS_INTENSITY_THRESHOLD, distance=5)
            cycles['crisis_frequency'] = len(crisis_peaks) / (len(ts_df) / 12)  # Per year

        return cycles

    def _analyze_crisis_patterns(self, ts_df: pd.DataFrame) -> dict[str, Any]:
        """Analyze patterns leading to crisis periods."""
        crisis_patterns = {
            'crisis_predictors': [],
            'recovery_patterns': [],
            'crisis_consciousness_correlation': 0.0,
        }

        if 'crisis_intensity' not in ts_df.columns:
            return crisis_patterns

        # Find crisis periods (crisis_intensity > 0.7)
        crisis_periods = ts_df[ts_df['crisis_intensity'] > 0.7]

        if len(crisis_periods) == 0:
            return crisis_patterns

        # Analyze pre-crisis conditions
        for crisis_date in crisis_periods.index:
            # Look at 2 years before crisis
            pre_crisis = ts_df[ts_df.index < crisis_date].tail(24)  # 24 months

            if len(pre_crisis) > 12:
                # Identify warning indicators
                for col in ['gini_coefficient', 'unemployment_rate', 'exploitation_rate']:
                    if col in pre_crisis.columns:
                        trend_slope = np.polyfit(range(len(pre_crisis)),
                                               pre_crisis[col].ffill().to_numpy(), 1)[0]
                        if abs(trend_slope) > TREND_SLOPE_THRESHOLD:  # Significant trend
                            crisis_patterns['crisis_predictors'].append({
                                'indicator': col,
                                'trend_slope': trend_slope,
                                'crisis_date': crisis_date,
                            })

        # Analyze consciousness during crises
        if 'consciousness_type_numeric' in ts_df.columns:
            crisis_consciousness = float(crisis_periods['consciousness_type_numeric'].mean())
            normal_consciousness = float(ts_df[ts_df['crisis_intensity'] < CRISIS_LOW_INTENSITY_THRESHOLD]['consciousness_type_numeric'].mean())

            crisis_patterns['crisis_consciousness_correlation'] = (
                crisis_consciousness - normal_consciousness
            )

        return crisis_patterns

    def _track_consciousness_evolution(self, ts_df: pd.DataFrame) -> dict[str, Any]:
        """Track evolution of class consciousness over time."""
        consciousness_evolution = {
            'consciousness_trajectory': 'stable',
            'consciousness_volatility': 0.0,
            'consciousness_crisis_response': 0.0,
        }

        if 'consciousness_type_numeric' not in ts_df.columns:
            return consciousness_evolution

        consciousness = ts_df['consciousness_type_numeric'].ffill()

        # Calculate overall trajectory
        if len(consciousness) > 10:
            x = np.arange(len(consciousness))
            lr = stats.linregress(x, consciousness)
            # Use attribute access for slope, fallback to nan if not present
            slope = float(getattr(lr, "slope", float("nan")))
            consciousness_evolution['consciousness_trajectory'] = (
                'rising' if slope > CONSCIOUSNESS_SLOPE_RISING_THRESHOLD
                else 'declining' if slope < CONSCIOUSNESS_SLOPE_DECLINING_THRESHOLD
                else 'stable'
            )

        # Calculate volatility
        consciousness_evolution['consciousness_volatility'] = float(consciousness.std())

        # Analyze consciousness response to crises
        if 'crisis_intensity' in ts_df.columns:
            high_crisis = ts_df[ts_df['crisis_intensity'] > REVOLUTIONARY_POTENTIAL_THRESHOLD - 0.01]  # Approximately 0.59, adjustable
            low_crisis = ts_df[ts_df['crisis_intensity'] < CRISIS_LOW_INTENSITY_THRESHOLD]

            if len(high_crisis) > 0 and len(low_crisis) > 0:
                crisis_consciousness = float(high_crisis['consciousness_type_numeric'].mean())
                normal_consciousness = float(low_crisis['consciousness_type_numeric'].mean())
                consciousness_evolution['consciousness_crisis_response'] = (
                    crisis_consciousness - normal_consciousness
                )

        return consciousness_evolution

    def _analyze_contradiction_dynamics(self, ts_df: pd.DataFrame) -> dict[str, Any]:
        """Analyze how contradictions develop and intensify over time."""
        contradictions = {
            'primary_contradiction_trend': 'stable',
            'contradiction_acceleration': 0.0,
            'dialectical_reversals': 0,
        }

        # Analyze main contradiction indicators
        contradiction_indicators = [
            'gini_coefficient', 'exploitation_rate', 'class_antagonism',
        ]

        contradiction_series = []
        for indicator in contradiction_indicators:
            if indicator in ts_df.columns:
                contradiction_series.append(ts_df[indicator].ffill())

        if not contradiction_series:
            return contradictions

        # Create composite contradiction intensity
        avg_contradiction = pd.concat(contradiction_series, axis=1).mean(axis=1)

        # Analyze trend
        contradiction_trend_min_points = 10
        contradiction_trend_slope_up = 0.01
        contradiction_trend_slope_down = -0.01
        if len(avg_contradiction) > contradiction_trend_min_points:
            x = np.arange(len(avg_contradiction))
            # Use stats.linregress but ensure the returned slope is converted to a numeric scalar
            lr = stats.linregress(x, avg_contradiction)
            try:
                # Attempt to extract slope robustly without assuming attribute presence
                raw_slope = getattr(lr, "slope", None)
                if raw_slope is None:
                    # linregress may return a tuple-like result in some versions
                    try:
                        raw_slope = lr[0] if isinstance(lr, tuple | list | np.ndarray) and len(lr) > 0 else lr
                    except Exception:
                        raw_slope = lr
                # Convert to a numeric scalar
                slope = float(np.squeeze(np.asarray(raw_slope)))
            except Exception:
                # If conversion fails, default to NaN so comparisons are safe
                slope = float("nan")

            contradictions['primary_contradiction_trend'] = (
                'intensifying' if slope > contradiction_trend_slope_up
                else 'resolving' if slope < contradiction_trend_slope_down
                else 'stable'
            )

        # Calculate acceleration (second derivative)
        if len(avg_contradiction) > 5:
            first_diff = np.diff(avg_contradiction)
            second_diff = np.diff(first_diff)
            contradictions['contradiction_acceleration'] = np.mean(second_diff)

        # Count dialectical reversals (major direction changes)
        if len(avg_contradiction) > 20:
            # Find peaks and troughs
            peaks, _ = find_peaks(avg_contradiction, distance=5)
            troughs, _ = find_peaks(-avg_contradiction, distance=5)
            contradictions['dialectical_reversals'] = len(peaks) + len(troughs)

        return contradictions


class HistoricalMaterialistEngine:
    """Main engine for historical materialist analysis."""

    def __init__(self, region: str):
        self.region = region
        self.data_manager = MaterialistDataManager(region)
        self.ges_engine = MaterialistGESEngine()
        self.trend_analyzer = HistoricalTrendAnalyzer()
        self.validator = HistoricalValidator()

        # Time series storage
        self.time_series: list[TimeSeriesPoint] = []

    async def build_historical_time_series(self,
                                         start_year: int,
                                         end_year: int,
                                         annual_data: bool = True) -> list[TimeSeriesPoint]:
        """Build time series of material conditions and consciousness evolution."""
        logger.info("Building historical time series for %s: %d-%d",
                   self.region, start_year, end_year)

        time_series = []

        # For now, use projection method with historical World Bank data
        # In production, would fetch actual historical data year by year
        for year in range(start_year, end_year + 1):
            try:
                # Simulate fetching historical data for this year
                date = datetime(year, 6, 1, tzinfo=UTC)  # Mid-year point

                # Get current data as baseline
                current_conditions = await self.data_manager.get_current_material_conditions()

                # Apply historical projections (simplified for demo)
                historical_conditions = self._project_historical_conditions(
                    current_conditions, year,
                )

                # Analyze emotional state for this historical period
                state = self.ges_engine.analyze_regional_state(
                    self.region, historical_conditions,
                )

                # Create time series point
                point = TimeSeriesPoint(
                    date=date,
                    indicators={
                        'gini_coefficient': historical_conditions.ideological_hegemony,
                        'exploitation_rate': historical_conditions.exploitation_rate,
                        'subsistence_security': historical_conditions.subsistence_security,
                        'unemployment_rate': 1.0 - historical_conditions.subsistence_security,
                        'union_density': 1.0 - historical_conditions.alienation_from_others,
                    },
                    consciousness_type=state.consciousness_type,
                    revolutionary_potential=state.revolutionary_potential,
                    crisis_intensity=len(state.crisis_indicators) / 5.0,  # Normalize
                    confidence=state.confidence,
                )

                time_series.append(point)

                if annual_data and year % 10 == 0:
                    logger.info("Processed year %d: rev_potential=%.3f, crisis=%.3f",
                               year, point.revolutionary_potential, point.crisis_intensity)

            except Exception as e:
                logger.warning("Failed to process year %d: %s", year, e)
                continue

        self.time_series = time_series
        return time_series

    def _project_historical_conditions(self,
                                     baseline: MaterialConditions,
                                     year: int) -> MaterialConditions:
        """Project historical conditions for a given year (simplified model)."""
        # This is a simplified projection - in production would use real historical data

        # Model major historical trends
        time_factor = (year - 2023) / 100  # Century scale

        # Historical inequality trends (U-shaped: high in 1900s, low mid-century, rising again)
        if year < 1930:
            inequality_factor = 1.2  # Gilded Age inequality
        elif year < 1980:
            inequality_factor = 0.7  # Post-war compression
        else:
            inequality_factor = 1.0 + (year - 1980) * 0.01  # Rising inequality

        # Labor organization trends
        union_factor = 2.0 if LABOR_ORG_HIGH_PERIOD_START <= year <= LABOR_ORG_HIGH_PERIOD_END else 0.5  # High unionization period mid-century, otherwise low

        # Create modified conditions
        modified = MaterialConditions(
            mode_of_production=baseline.mode_of_production,
            ownership_relations=baseline.ownership_relations,
            production_relations=baseline.production_relations,
            technological_development=max(0.1, baseline.technological_development - abs(time_factor)),
            labor_productivity=baseline.labor_productivity,
            resource_availability=baseline.resource_availability,
            infrastructure_quality=max(0.1, baseline.infrastructure_quality - abs(time_factor) * 0.5),
            class_distribution=baseline.class_distribution,
            exploitation_rate=min(1.0, baseline.exploitation_rate * inequality_factor),
            class_mobility=baseline.class_mobility,
            subsistence_security=baseline.subsistence_security / inequality_factor,
            housing_security=baseline.housing_security,
            healthcare_access=max(0.1, baseline.healthcare_access - abs(time_factor) * 0.3),
            education_access=max(0.1, baseline.education_access - abs(time_factor) * 0.2),
            alienation_from_labor=baseline.alienation_from_labor,
            alienation_from_product=baseline.alienation_from_product,
            alienation_from_species=baseline.alienation_from_species,
            alienation_from_others=max(0.1, baseline.alienation_from_others / union_factor),
            ideological_hegemony=min(1.0, baseline.ideological_hegemony * inequality_factor),
            state_repression=baseline.state_repression,
            mass_media_concentration=baseline.mass_media_concentration,
            timestamp=datetime(year, 6, 1, tzinfo=UTC),
            region=baseline.region,
        )

        return modified

    async def analyze_historical_trajectory(self) -> dict[str, Any]:
        """Perform comprehensive historical analysis."""
        if not self.time_series:
            msg = "No time series data available. Call build_historical_time_series first."
            raise ValueError(msg)

        logger.info("Analyzing historical trajectory for %s with %d data points",
                   self.region, len(self.time_series))

        # Detect patterns
        patterns = self.trend_analyzer.detect_historical_patterns(self.time_series)

        # Validate against known events
        validation = await self.validator.validate_theoretical_predictions(
            self.time_series, self.region,
        )

        # Generate comprehensive report
        analysis = {
            'region': self.region,
            'time_period': f"{self.time_series[0].date.year}-{self.time_series[-1].date.year}",
            'data_points': len(self.time_series),
            'patterns': patterns,
            'validation': validation,
            'summary': self._generate_historical_summary(patterns, validation),
        }

        return analysis

    def _generate_historical_summary(self,
                                   patterns: dict[str, Any],
                                   validation: dict[str, float]) -> str:
        """Generate human-readable summary of historical analysis."""
        summary_parts = []

        # Consciousness evolution
        if 'consciousness_evolution' in patterns:
            consciousness = patterns['consciousness_evolution']
            trajectory = consciousness.get('consciousness_trajectory', 'unknown')
            summary_parts.append(f"Class consciousness trajectory: {trajectory}")

        # Revolutionary patterns
        if 'cycles' in patterns:
            cycles = patterns['cycles']
            if 'revolutionary_peaks' in cycles:
                rev_peaks = cycles['revolutionary_peaks']
                summary_parts.append(f"Revolutionary peaks detected: {rev_peaks}")

        # Crisis patterns
        if 'crisis_patterns' in patterns:
            crisis = patterns['crisis_patterns']
            crisis_freq = len(crisis.get('crisis_predictors', []))
            summary_parts.append(f"Crisis prediction indicators: {crisis_freq}")

        # Validation accuracy
        accuracy = validation.get('overall_historical_accuracy', 0.0)
        summary_parts.append(f"Historical prediction accuracy: {accuracy:.1%}")

        return "; ".join(summary_parts)


# Example usage for testing historical analysis
async def example_historical_analysis():
    """Demonstrate historical materialist analysis."""
    # Initialize for USA
    engine = HistoricalMaterialistEngine("USA")

    # Build time series for 20th century
    time_series = await engine.build_historical_time_series(1900, 2020)

    # Analyze historical trajectory
    analysis = await engine.analyze_historical_trajectory()

    logger.info("Historical Materialist Analysis Results:")
    logger.info("Region: %s", analysis['region'])
    logger.info("Period: %s", analysis['time_period'])
    logger.info("Data Points: %d", analysis['data_points'])
    logger.info("Summary: %s", analysis['summary'])

    # Show validation results
    validation = analysis['validation']
    logger.info("\nValidation Against Historical Events:")
    logger.info("Overall Accuracy: %.1f%%", validation.get('overall_historical_accuracy', 0) * 100)


if __name__ == "__main__":
    asyncio.run(example_historical_analysis())
