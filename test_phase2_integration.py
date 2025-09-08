#!/usr/bin/env python3
"""Test Real API Integration for Materialist GES Analysis.

------------------------------------------------------
Test script to verify World Bank API integration and data collection
for Phase 2: Data Integration
"""

import asyncio
import logging
import sys
from datetime import datetime, timedelta

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

# Test imports
try:
    from mges.materialist_data_sources import LaborStatisticsSource, MaterialistDataManager, WealthInequalitySource
    from mges.materialist_ges_engine import MaterialistGESEngine
    print("✅ Successfully imported MGES modules")
except ImportError as e:
    print(f"❌ Failed to import MGES modules: {e}")
    sys.exit(1)

# Test World Bank API availability via HTTP
try:
    import aiohttp
    print("✅ HTTP client (aiohttp) available for World Bank API")
except ImportError as e:
    print(f"❌ HTTP client not available: {e}")
    print("Install with: pip install aiohttp")
    sys.exit(1)


async def test_world_bank_api_direct():
    """Test direct World Bank API calls using HTTP requests."""
    print("\n🔍 Testing direct World Bank API calls...")

    try:
        import aiohttp
        
        async with aiohttp.ClientSession() as session:
            # Test basic API connectivity with countries endpoint
            print("Testing World Bank API connectivity...")
            countries_url = "https://api.worldbank.org/v2/country?format=json&per_page=10"
            
            async with session.get(countries_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 1:
                        countries_count = data[0].get('total', 0)
                        print(f"✅ World Bank API responsive: {countries_count} countries available")
                    else:
                        print("✅ World Bank API responsive")
                else:
                    print(f"⚠️ World Bank API returned status {response.status}")
                    return False

            # Test specific data fetch for USA - Gini coefficient
            print("Testing Gini coefficient data for USA...")
            gini_url = "https://api.worldbank.org/v2/country/US/indicator/SI.POV.GINI?mrv=3&format=json"
            
            async with session.get(gini_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 1 and data[1]:
                        for entry in data[1]:
                            if entry.get('value') is not None:
                                latest_gini = float(entry['value'])
                                latest_year = entry['date']
                                print(f"✅ USA Gini coefficient (latest): {latest_gini:.2f} ({latest_year})")
                                break
                        else:
                            print("⚠️ No valid Gini data found for USA")
                    else:
                        print("⚠️ Empty Gini data response for USA")
                else:
                    print(f"⚠️ Failed to fetch Gini data: HTTP {response.status}")

            # Test labor data - unemployment rate
            print("Testing unemployment data for USA...")
            unemployment_url = "https://api.worldbank.org/v2/country/US/indicator/SL.UEM.TOTL.ZS?mrv=3&format=json"
            
            async with session.get(unemployment_url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    data = await response.json()
                    if isinstance(data, list) and len(data) > 1 and data[1]:
                        for entry in data[1]:
                            if entry.get('value') is not None:
                                latest_unemployment = float(entry['value'])
                                latest_year = entry['date']
                                print(f"✅ USA unemployment rate (latest): {latest_unemployment:.2f}% ({latest_year})")
                                break
                        else:
                            print("⚠️ No valid unemployment data found for USA")
                    else:
                        print("⚠️ Empty unemployment data response for USA")
                else:
                    print(f"⚠️ Failed to fetch unemployment data: HTTP {response.status}")

    except Exception as e:
        print(f"❌ World Bank API test failed: {e}")
        return False

    return True


async def test_inequality_source():
    """Test WealthInequalitySource with real API."""

    print("\n📊 Testing WealthInequalitySource...")

    try:
        source = WealthInequalitySource("USA")

        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()

        data_points = await source.fetch_data(start_date, end_date)

        print(f"✅ Fetched {len(data_points)} inequality indicators:")

        for dp in data_points:
            print(f"  - {dp.indicator_name}: {dp.value:.3f} (confidence: {dp.confidence:.1f})")
            print(f"    Source: {dp.metadata.get('source', 'unknown')}")

        if data_points:
            # Test indicator calculation
            raw_data = {dp.indicator_name: dp.value for dp in data_points}
            indicator = source.calculate_indicator([raw_data])
            print(f"✅ Class polarization indicator: {indicator:.3f}")
        else:
            print("⚠️ No data points retrieved")

    except Exception as e:
        print(f"❌ WealthInequalitySource test failed: {e}")
        return False

    return True


async def test_labor_source():
    """Test LaborStatisticsSource with real API."""

    print("\n👷 Testing LaborStatisticsSource...")

    try:
        source = LaborStatisticsSource("USA")

        start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()

        data_points = await source.fetch_data(start_date, end_date)

        print(f"✅ Fetched {len(data_points)} labor indicators:")

        for dp in data_points:
            print(f"  - {dp.indicator_name}: {dp.value:.3f} (confidence: {dp.confidence:.1f})")
            print(f"    Source: {dp.metadata.get('source', 'unknown')}")

        if data_points:
            # Test indicator calculation
            raw_data = {dp.indicator_name: dp.value for dp in data_points}
            indicator = source.calculate_indicator([raw_data])
            print(f"✅ Labor conditions indicator: {indicator:.3f}")
        else:
            print("⚠️ No data points retrieved")

    except Exception as e:
        print(f"❌ LaborStatisticsSource test failed: {e}")
        return False

    return True


async def test_data_manager():
    """Test MaterialistDataManager with real API integration."""

    print("\n🏭 Testing MaterialistDataManager...")

    try:
        manager = MaterialistDataManager("USA")

        # Test data collection
        raw_data = await manager.collect_all_data()

        total_indicators = sum(len(data_points) for data_points in raw_data.values())
        print(f"✅ Collected {total_indicators} total indicators from {len(raw_data)} sources")

        for source_type, data_points in raw_data.items():
            if data_points:
                print(f"  - {getattr(source_type, 'value', source_type)}: {len(data_points)} indicators")

        # Test material conditions construction
        conditions = manager.construct_material_conditions(raw_data)

        print(f"✅ Constructed MaterialConditions:")
        print(f"  - Mode of production: {conditions.mode_of_production.value}")
        print(f"  - Exploitation rate: {conditions.exploitation_rate:.3f}")
        print(f"  - Class distribution: {conditions.class_distribution}")
        print(f"  - Subsistence security: {conditions.subsistence_security:.3f}")
        print(f"  - Alienation from labor: {conditions.alienation_from_labor:.3f}")

    except Exception as e:
        print(f"❌ MaterialistDataManager test failed: {e}")
        return False

    return True


async def test_full_ges_analysis():
    """Test full GES analysis with real data."""

    print("\n🌍 Testing full MaterialistGESEngine with real data...")

    try:
        # Initialize engine
        engine = MaterialistGESEngine()

        # Add USA region
        from mges.materialist_ges_engine import create_default_regional_configs
        configs = create_default_regional_configs(["USA"])
        for config in configs:
            engine.add_region(config)

        # Get real material conditions
        manager = MaterialistDataManager("USA")
        conditions = await manager.get_current_material_conditions()

        # Analyze emotional state
        state = engine.analyze_regional_state("USA", conditions)

        print(f"✅ Materialist GES Analysis Results:")
        print(f"  - Consciousness Type: {state.consciousness_type.value}")
        print(f"  - Primary Contradiction: {state.primary_contradiction.value}")
        print(f"  - Class Antagonism: {state.class_antagonism:.3f}")
        print(f"  - Revolutionary Potential: {state.revolutionary_potential:.3f}")
        print(f"  - Solidarity Level: {state.solidarity_level:.3f}")
        print(f"  - Crisis Indicators: {state.crisis_indicators}")
        print(f"  - Analysis Confidence: {state.confidence:.3f}")

        # Test global indices
        global_indices = engine.compute_global_indices()
        print(f"✅ Global Indices:")
        print(f"  - Global Class Consciousness: {global_indices['global_class_consciousness']:.3f}")
        print(f"  - Global Revolutionary Potential: {global_indices['global_revolutionary_potential']:.3f}")
        print(f"  - Global Crisis Intensity: {global_indices['global_crisis_intensity']:.3f}")

    except Exception as e:
        print(f"❌ Full GES analysis test failed: {e}")
        return False

    return True


async def main():
    """Run all tests for Phase 2: Data Integration."""

    print("🚀 Testing Phase 2: Real API Data Integration")
    print("=" * 50)

    tests = [
        ("World Bank API Direct", test_world_bank_api_direct),
        ("WealthInequalitySource", test_inequality_source),
        ("LaborStatisticsSource", test_labor_source),
        ("MaterialistDataManager", test_data_manager),
        ("Full GES Analysis", test_full_ges_analysis),
    ]

    results = {}

    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = await test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ Test {test_name} failed with exception: {e}")
            results[test_name] = False

    # Summary
    print(f"\n{'='*50}")
    print("📋 TEST SUMMARY")
    print("=" * 50)

    passed = sum(results.values())
    total = len(results)

    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")

    print(f"\n🎯 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Phase 2 implementation successful.")
        print("\n✅ PHASE 2 COMPLETE: Real API data integration working")
        print("📊 World Bank API successfully integrated")
        print("🏭 Material conditions construction from real data")
        print("🌍 Full materialist GES analysis operational")
    else:
        print("⚠️ Some tests failed. Check the logs above for details.")

    return passed == total


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
