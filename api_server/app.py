#!/usr/bin/env python3
"""Flask API Server for Materialist GES Analysis.

This server provides REST endpoints for the React frontend,
integrating with the existing analysis engine to provide real-time
materialist analysis with proper confidence intervals and explainability.
"""

import asyncio
import logging
import os
import sys
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS

# Ensure project root on path
sys.path.append(str(Path(__file__).parent.parent))

from mges.historical_analysis import HistoricalMaterialistEngine
from mges.materialist_data_sources import MaterialistDataManager
from mges.materialist_ges_engine import (
    CollectiveEmotionalState,
    MaterialistGESEngine,
    RegionNotConfiguredError,
    create_default_regional_configs,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

###############################################################
# Engine Initialization (REAL DATA PATH)
###############################################################

ges_engine: MaterialistGESEngine | None = None
data_managers: dict[str, MaterialistDataManager] = {}
historical_engines: dict[str, HistoricalMaterialistEngine] = {}


def initialize_engines(regions: list[str] | None = None) -> tuple[MaterialistGESEngine, dict[str, MaterialistDataManager], dict[str, HistoricalMaterialistEngine]]:
    """Initialize engines with real data sources (World Bank, etc)."""
    regions = regions or ["USA", "CHN", "DEU", "FRA", "GBR", "JPN"]
    ges_engine = MaterialistGESEngine()

    # Configure regions using factory
    for cfg in create_default_regional_configs(regions):
        ges_engine.add_region(cfg)

    # Per-region data managers & historical engines
    data_managers = {r: MaterialistDataManager(r) for r in regions}
    historical_engines = {r: HistoricalMaterialistEngine(r) for r in regions}

    logger.info("Initialized engines for regions: %s", ", ".join(regions))
    return ges_engine, data_managers, historical_engines


###############################################################
# Helper serialization
###############################################################

def serialize_state(state: CollectiveEmotionalState) -> dict[str, Any]:
    """Convert CollectiveEmotionalState to JSON-serializable dict."""
    mc = state.material_conditions
    return {
        "region": state.region,
        "timestamp": state.timestamp.isoformat(),
        "consciousness_type": state.consciousness_type.value,
        "primary_contradiction": state.primary_contradiction.value,
        "class_antagonism": state.class_antagonism,
        "revolutionary_potential": state.revolutionary_potential,
        "solidarity_level": state.solidarity_level,
        "alienation_intensity": state.alienation_intensity,
        "contradiction_intensity": state.contradiction_intensity,
        "resolution_tendency": state.resolution_tendency,
        "historical_momentum": state.historical_momentum,
        "crisis_indicators": state.crisis_indicators,
        "confidence": state.confidence,
        "consciousness": {
            "clarity": state.consciousness_clarity,
            "ideological_influence": state.ideological_influence,
        },
        "material_conditions": {
            "mode_of_production": mc.mode_of_production.value,
            "ownership_relations": mc.ownership_relations,
            "production_relations": mc.production_relations,
            "technological_development": mc.technological_development,
            "labor_productivity": mc.labor_productivity,
            "resource_availability": mc.resource_availability,
            "infrastructure_quality": mc.infrastructure_quality,
            "class_distribution": {k.value: v for k, v in mc.class_distribution.items()},
            "exploitation_rate": mc.exploitation_rate,
            "class_mobility": mc.class_mobility,
            "subsistence_security": mc.subsistence_security,
            "housing_security": mc.housing_security,
            "healthcare_access": mc.healthcare_access,
            "education_access": mc.education_access,
            "alienation": {
                "labor": mc.alienation_from_labor,
                "product": mc.alienation_from_product,
                "species": mc.alienation_from_species,
                "others": mc.alienation_from_others,
            },
            "ideological_hegemony": mc.ideological_hegemony,
            "state_repression": mc.state_repression,
            "mass_media_concentration": mc.mass_media_concentration,
        },
    }


###############################################################
# Async bridging utilities
###############################################################

def run_async(coro: Any):  # Return type dynamic depending on coroutine
    """Run an async coroutine in Flask (synchronous context) safely."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    if loop.is_running():  # Should not happen in standard Flask dev server
        return asyncio.ensure_future(coro)  # Safe in already-running loop
    return loop.run_until_complete(coro)

@app.route('/api/analysis/<region>', methods=['GET'])
def get_analysis(region: str):
    """Return real-time materialist analysis for a region using live data sources."""
    if ges_engine is None:
        return jsonify({"error": "Engine not initialized"}), 500
    if region not in data_managers:
        return jsonify({"error": f"Region {region} not configured"}), 404

    params = {
        'materialConditionsWeight': float(request.args.get('materialConditionsWeight', 0.5)),
        'historicalMomentumWeight': float(request.args.get('historicalMomentumWeight', 0.3)),
        'confidenceThreshold': float(request.args.get('confidenceThreshold', 0.7)),
    }
    try:
        dm = data_managers[region]
        conditions = run_async(dm.get_current_material_conditions())
        state = ges_engine.analyze_regional_state(region, conditions)
        payload = serialize_state(state)
        payload['analysis_parameters'] = params
        payload['data_sources'] = ["World Bank", "derived_estimates"]
        return jsonify(payload)
    except RegionNotConfiguredError as rnce:
        return jsonify({"error": str(rnce)}), 404
    except Exception as e:
        logger.exception("Analysis failure for %s", region)
        return jsonify({"error": str(e)}), 500

@app.route('/api/historical/<region>', methods=['GET'])
def get_historical_data(region: str):
    """Build (if needed) and return historical materialist trajectory analysis."""
    if region not in historical_engines:
        return jsonify({"error": f"Region {region} not configured"}), 404
    try:
        time_span = request.args.get('years', '5')
        try:
            years = int(time_span)
        except ValueError:
            years = 5
        end_year = datetime.now(tz=UTC).year
        start_year = max(end_year - years + 1, end_year - 50)  # cap span to 50 years to limit load

        hist = historical_engines[region]
        # Rebuild series each call (could add caching)
        run_async(hist.build_historical_time_series(start_year, end_year))
        analysis = run_async(hist.analyze_historical_trajectory())
        analysis['request_parameters'] = {"start_year": start_year, "end_year": end_year}
        return jsonify(analysis)
    except Exception as e:
        logger.exception("Historical analysis failure for %s", region)
        return jsonify({"error": str(e)}), 500

@app.route('/api/regions', methods=['GET'])
def get_available_regions():
    """Return configured regions."""
    return jsonify([
        {"code": r, "name": r, "flag": ""} for r in sorted(data_managers.keys())
    ])

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for AI improvements."""
    try:
        feedback_data = request.get_json()

        # Log feedback for model improvement
        logger.info("User feedback received: %s", feedback_data)

        # In production, this would be stored in a database
        # and used for model retraining

        return jsonify({'status': 'success', 'message': 'Feedback recorded'})

    except Exception:
        logger.exception("Error in feedback endpoint")
        return jsonify({'error': 'internal error'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health status with engine/meta information."""
    return jsonify({
        'status': 'healthy' if ges_engine else 'uninitialized',
        'timestamp': datetime.now(tz=UTC).isoformat(),
        'version': '1.0.1',
        'regions': list(data_managers.keys()),
        'engine_configured': ges_engine is not None,
    })

if __name__ == '__main__':
    ges_engine, data_managers, historical_engines = initialize_engines()
    # Keep 0.0.0.0 for container/dev usage; consider env guard for production
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1', host=os.environ.get('FLASK_HOST', '127.0.0.1'), port=5001)
