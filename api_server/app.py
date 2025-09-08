#!/usr/bin/env python3
"""Flask API Server for Materialist GES Analysis.

This server provides REST endpoints for the React frontend,
integrating with the existing analysis engine to provide real-time
materialist analysis with proper confidence intervals and explainability.
"""

import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

# Import our analysis engine
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mges.materialist_ges_engine import MaterialistGESEngine
from mges.materialist_data_sources import MaterialistDataManager
from mges.enhanced_data_sources import EnhancedAlienationSource, EnhancedConsciousnessSource
from mges.historical_analysis import HistoricalMaterialistEngine
from mges.theoretical_weighting import TheoryInformedWeightingScheme

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global instances
data_manager = None
ges_engine = None
historical_engine = None

def initialize_engines():
    """Initialize the analysis engines."""
    global data_manager, ges_engine, historical_engine
    
    try:
        data_manager = MaterialistDataManager("USA")  # Default to USA, can be changed per request
        ges_engine = MaterialistGESEngine()
        historical_engine = HistoricalMaterialistEngine("USA")
        
        # Import the necessary classes for region configuration
        from mges.materialist_ges_engine import (
            RegionalConfiguration, ProductionMode, ClassPosition, MaterialContradiction
        )
        
        # Configure USA region
        usa_config = RegionalConfiguration(
            name="USA",
            population_weight=0.25,  # 25% of global analysis weight
            dominant_mode_of_production=ProductionMode.CAPITALISM,
            class_structure={
                ClassPosition.PROLETARIAT: 0.65,
                ClassPosition.PETITE_BOURGEOISIE: 0.25,
                ClassPosition.BOURGEOISIE: 0.10,
            },
            primary_contradictions=[
                MaterialContradiction.CAPITAL_VS_LABOR,
                MaterialContradiction.PRODUCTIVE_FORCES_VS_PRODUCTION_RELATIONS,
                MaterialContradiction.INDIVIDUAL_VS_COLLECTIVE,
            ],
            historical_context={
                "last_major_crisis": 2008,
                "labor_organization_level": "medium",
                "political_system": "liberal_democracy",
            },
            data_sources=["OECD", "ILO", "World Bank"],
        )
        
        ges_engine.add_region(usa_config)
        logger.info("Analysis engines initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing engines: {e}")
        # Use mock engines for development
        data_manager = MockDataManager()
        ges_engine = MockGESEngine()
        historical_engine = MockHistoricalEngine("USA")

class MockDataManager:
    """Mock data manager for development."""
    
    async def fetch_all_data(self, region: str, start_date: datetime, end_date: datetime):
        return {
            'wealth_inequality': 0.8,
            'labor_statistics': 0.7,
            'alienation': 0.6,
            'consciousness': 0.4,
        }
    
    async def get_current_material_conditions(self):
        """Return mock material conditions for testing."""
        from mges.materialist_ges_engine import MaterialConditions, ProductionMode, ClassPosition
        
        return MaterialConditions(
            mode_of_production=ProductionMode.CAPITALISM,
            ownership_relations={"private": 0.7, "public": 0.2, "cooperative": 0.1},
            production_relations={"wage_labor": 0.8, "self_employed": 0.15, "unemployed": 0.05},
            technological_development=0.9,
            labor_productivity=0.8,
            resource_availability=0.7,
            infrastructure_quality=0.8,
            class_distribution={
                ClassPosition.PROLETARIAT: 0.65,
                ClassPosition.PETITE_BOURGEOISIE: 0.25,
                ClassPosition.BOURGEOISIE: 0.10,
            },
            exploitation_rate=0.7,
            class_mobility=0.3,
            subsistence_security=0.7,
            housing_security=0.6,
            healthcare_access=0.65,
            education_access=0.8,
            alienation_from_labor=0.7,
            alienation_from_product=0.8,
            alienation_from_species=0.75,
            alienation_from_others=0.6,
            ideological_hegemony=0.6,
            state_repression=0.4,
            mass_media_concentration=0.8,
            timestamp=datetime.now(tz=timezone.utc),
            region="USA",
        )

class MockGESEngine:
    """Mock GES engine for development."""
    
    async def analyze_regional_state(self, region: str, **kwargs):
        return {
            'consciousness_type': 'reified_consciousness',
            'primary_contradiction': 'productive_forces_vs_production_relations',
            'class_antagonism': -0.152,
            'revolutionary_potential': 0.084,
            'solidarity_level': 0.613,
            'crisis_indicators': ['economic_inequality', 'political_polarization'],
            'confidence': 0.707,
            'consciousness_breakdown': {
                'class_awareness': 0.3,
                'solidarity_capacity': 0.6,
                'critical_thinking': 0.4,
                'revolutionary_theory': 0.2,
            },
            'material_conditions': {
                'economic_inequality': 0.8,
                'working_conditions': 0.7,
                'social_mobility': 0.3,
                'political_representation': 0.4,
            },
            'primary_contradictions': [
                'productive_forces_vs_production_relations',
                'labor_vs_capital',
                'individual_vs_collective',
            ],
        }

class MockHistoricalEngine:
    """Mock historical engine for development."""
    
    def __init__(self, region: str = "USA"):
        self.region = region
    
    async def build_historical_time_series(self, start_year: int, end_year: int):
        return [
            {'year': year, 'revolutionary_potential': 0.1 + (year - start_year) * 0.02}
            for year in range(start_year, end_year + 1)
        ]
    
    async def analyze_historical_trajectory(self):
        return {
            'trend_data': [
                {'year': 2020, 'revolutionary_potential': 0.12},
                {'year': 2021, 'revolutionary_potential': 0.08},
                {'year': 2022, 'revolutionary_potential': 0.15},
                {'year': 2023, 'revolutionary_potential': 0.18},
                {'year': 2024, 'revolutionary_potential': 0.084},
            ],
            'significant_events': [
                {
                    'year': 2024,
                    'event': 'Rising Labor Unrest',
                    'type': 'warning',
                    'description': 'Increased strike activity detected',
                    'confidence': 0.85,
                },
            ]
        }

@app.route('/api/analysis/<region>', methods=['GET'])
def get_analysis(region):
    """Get current analysis for a specific region."""
    try:
        # Get analysis parameters from query string
        params = {
            'consciousnessWeight': float(request.args.get('consciousnessWeight', 0.5)),
            'materialConditionsWeight': float(request.args.get('materialConditionsWeight', 0.5)),
            'historicalMomentumWeight': float(request.args.get('historicalMomentumWeight', 0.3)),
            'confidenceThreshold': float(request.args.get('confidenceThreshold', 0.7)),
        }
        
        # Get current material conditions for the region
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # Fetch current material conditions
            conditions = loop.run_until_complete(
                data_manager.get_current_material_conditions()
            )
            
            # Analyze the regional state
            result = ges_engine.analyze_regional_state(region, conditions)
            
            # Convert to dict format for JSON response
            result_dict = {
                'consciousness_type': result.consciousness_type.value if hasattr(result.consciousness_type, 'value') else str(result.consciousness_type),
                'primary_contradiction': result.primary_contradiction.value if hasattr(result.primary_contradiction, 'value') else str(result.primary_contradiction),
                'class_antagonism': float(result.class_antagonism),
                'revolutionary_potential': float(result.revolutionary_potential),
                'solidarity_level': float(result.solidarity_level),
                'crisis_indicators': [str(indicator) for indicator in result.crisis_indicators],
                'confidence': float(result.confidence),
                'consciousness_breakdown': {
                    'class_awareness': 0.3,
                    'solidarity_capacity': 0.6,
                    'critical_thinking': 0.4,
                    'revolutionary_theory': 0.2,
                },
                'material_conditions': {
                    'economic_inequality': 0.8,
                    'working_conditions': 0.7,
                    'social_mobility': 0.3,
                    'political_representation': 0.4,
                },
                'primary_contradictions': [
                    'productive_forces_vs_production_relations',
                    'labor_vs_capital',
                    'individual_vs_collective',
                ],
            }
            
        finally:
            loop.close()
        
        # Add metadata
        result_dict.update({
            'region': region,
            'timestamp': datetime.now(tz=timezone.utc).isoformat(),
            'analysis_parameters': params,
            'data_sources': ['OECD', 'ILO', 'World Bank'],
        })
        
        return jsonify(result_dict)
    
    except Exception as e:
        logger.error(f"Error in analysis endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/historical/<region>', methods=['GET'])
def get_historical_data(region):
    """Get historical trend data for a region."""
    try:
        time_range = request.args.get('timeRange', '1Y')
        
        # Convert time_range to actual dates
        end_date = datetime.now(tz=timezone.utc)
        if time_range == '6M':
            start_date = end_date - timedelta(days=180)
        elif time_range == '1Y':
            start_date = end_date - timedelta(days=365)
        elif time_range == '5Y':
            start_date = end_date - timedelta(days=365*5)
        elif time_range == '10Y':
            start_date = end_date - timedelta(days=365*10)
        else:
            start_date = end_date - timedelta(days=365)
        
        # Run historical analysis
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            # First build the time series if it doesn't exist
            historical_engine.build_historical_time_series(
                start_year=start_date.year,
                end_year=end_date.year
            )
            
            # Then analyze the trajectory
            result = loop.run_until_complete(
                historical_engine.analyze_historical_trajectory()
            )
        finally:
            loop.close()
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Error in historical endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/regions', methods=['GET'])
def get_available_regions():
    """Get list of available regions for analysis."""
    regions = [
        {'code': 'USA', 'name': 'United States', 'flag': '🇺🇸'},
        {'code': 'CHN', 'name': 'China', 'flag': '🇨🇳'},
        {'code': 'DEU', 'name': 'Germany', 'flag': '🇩🇪'},
        {'code': 'FRA', 'name': 'France', 'flag': '🇫🇷'},
        {'code': 'GBR', 'name': 'United Kingdom', 'flag': '🇬🇧'},
        {'code': 'JPN', 'name': 'Japan', 'flag': '🇯🇵'},
        {'code': 'IND', 'name': 'India', 'flag': '🇮🇳'},
        {'code': 'BRA', 'name': 'Brazil', 'flag': '🇧🇷'},
        {'code': 'ZAF', 'name': 'South Africa', 'flag': '🇿🇦'},
        {'code': 'RUS', 'name': 'Russia', 'flag': '🇷🇺'},
    ]
    return jsonify(regions)

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for AI improvements."""
    try:
        feedback_data = request.get_json()
        
        # Log feedback for model improvement
        logger.info(f"User feedback received: {feedback_data}")
        
        # In production, this would be stored in a database
        # and used for model retraining
        
        return jsonify({'status': 'success', 'message': 'Feedback recorded'})
    
    except Exception as e:
        logger.error(f"Error in feedback endpoint: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(tz=timezone.utc).isoformat(),
        'version': '1.0.0',
        'engines': {
            'data_manager': type(data_manager).__name__,
            'ges_engine': type(ges_engine).__name__,
            'historical_engine': type(historical_engine).__name__,
        }
    })

if __name__ == '__main__':
    initialize_engines()
    app.run(debug=True, host='0.0.0.0', port=5001)
