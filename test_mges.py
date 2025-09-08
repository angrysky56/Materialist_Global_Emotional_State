from datetime import UTC, datetime, timedelta, timezone

import pytest

from mges.materialist_data_sources import LaborStatisticsSource, MaterialistDataManager, WealthInequalitySource
from mges.materialist_ges_engine import MaterialistGESEngine, create_default_regional_configs


@pytest.mark.asyncio
async def test_wealth_inequality_source():
    source = WealthInequalitySource("USA")
    start_date = datetime.now(UTC) - timedelta(days=365)
    end_date = datetime.now(UTC)
    data_points = await source.fetch_data(start_date, end_date)
    assert isinstance(data_points, list)
    if data_points:
        raw_data = {dp.indicator_name: dp.value for dp in data_points}
        indicator = source.calculate_indicator([raw_data])
        assert isinstance(indicator, float)

@pytest.mark.asyncio
async def test_labor_statistics_source():
    source = LaborStatisticsSource("USA")
    start_date = datetime.now(UTC) - timedelta(days=365)
    end_date = datetime.now(UTC)
    data_points = await source.fetch_data(start_date, end_date)
    assert isinstance(data_points, list)
    if data_points:
        raw_data = {dp.indicator_name: dp.value for dp in data_points}
        indicator = source.calculate_indicator([raw_data])
        assert isinstance(indicator, float)

@pytest.mark.asyncio
async def test_materialist_data_manager():
    manager = MaterialistDataManager("USA")
    raw_data = await manager.collect_all_data()
    assert isinstance(raw_data, dict)
    conditions = manager.construct_material_conditions(raw_data)
    assert hasattr(conditions, "mode_of_production")

@pytest.mark.asyncio
async def test_full_ges_analysis():
    engine = MaterialistGESEngine()
    configs = create_default_regional_configs(["USA"])
    for config in configs:
        engine.add_region(config)
    manager = MaterialistDataManager("USA")
    conditions = await manager.get_current_material_conditions()
    state = engine.analyze_regional_state("USA", conditions)
    assert hasattr(state, "consciousness_type")
    global_indices = engine.compute_global_indices()
    assert "global_class_consciousness" in global_indices
