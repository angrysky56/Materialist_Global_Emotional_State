import asyncio
from mges.materialist_ges_engine import MaterialistGESEngine, create_default_regional_configs
from mges.materialist_data_sources import MaterialistDataManager

def print_usa_analysis():
    async def run_analysis():
        # Initialize engine and configs
        engine = MaterialistGESEngine()
        configs = create_default_regional_configs(["USA"])
        for config in configs:
            engine.add_region(config)

        # Collect material conditions for USA
        manager = MaterialistDataManager("USA")
        conditions = await manager.get_current_material_conditions()

        # Analyze emotional state
        state = engine.analyze_regional_state("USA", conditions)
        print("Materialist GES Analysis for USA:")
        print(f"  Consciousness Type: {state.consciousness_type.value}")
        print(f"  Primary Contradiction: {state.primary_contradiction.value}")
        print(f"  Class Antagonism: {state.class_antagonism:.3f}")
        print(f"  Revolutionary Potential: {state.revolutionary_potential:.3f}")
        print(f"  Solidarity Level: {state.solidarity_level:.3f}")
        print(f"  Crisis Indicators: {state.crisis_indicators}")
        print(f"  Analysis Confidence: {state.confidence:.3f}")

        # Global indices
        global_indices = engine.compute_global_indices()
        print("\nGlobal Indices:")
        print(f"  Global Class Consciousness: {global_indices['global_class_consciousness']:.3f}")
        print(f"  Global Revolutionary Potential: {global_indices['global_revolutionary_potential']:.3f}")
        print(f"  Global Crisis Intensity: {global_indices['global_crisis_intensity']:.3f}")

    asyncio.run(run_analysis())

if __name__ == "__main__":
    print_usa_analysis()
