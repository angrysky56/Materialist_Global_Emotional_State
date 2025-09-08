# Materialist Global Emotional State (MGES)

Materialist Global Emotional State (MGES) is a Python project designed to analyze, aggregate, and interpret emotional states from various data sources. It provides a framework for integrating materialist data sources and generating a global emotional state engine.

📊 Current System Capabilities
Successfully analyzing economic conditions using live World Bank data:
For USA (using 2023-2024 World Bank data):

Gini Coefficient: 41.8% (high inequality)
Labor Force Participation: 61.9%
Unemployment Rate: 4.1%
Wage Workers: 93.9% (high proletarianization)
Poverty Rate: 1.2% (official World Bank measure)

Materialist Analysis Results:

Class Structure: 75.1% Proletariat, 19.1% Intelligentsia, 3% Petite Bourgeoisie
Exploitation Rate: 0.280 (moderate)
Revolutionary Potential: 0.084 (very low - matches current US conditions)
Consciousness Type: Reified Consciousness (false consciousness dominant)

✅ All Tests Passing

9/9 tests successful including full end-to-end integration
Real-time World Bank API connectivity verified
Complete materialist analysis pipeline operational

🚀 Ready for Next Phase
Phase 2: Data Integration is now COMPLETE ✅
System is ready for Phase 3: Historical Analysis which would add:

Historical trend analysis of class contradictions
Crisis prediction algorithms
Revolutionary potential forecasting
Class consciousness evolution tracking

## Features
- Integration of multiple materialist data sources
- Aggregation and analysis of emotional state data
- Extensible engine for global emotional state computation
- Modular design for easy extension and testing

## Project Structure
```
implementation_roadmap.md         # Project roadmap and planning
pyproject.toml                    # Python project configuration
mges/
    materialist_data_sources.py   # Data source integration logic
    materialist_ges_engine.py     # Core engine for emotional state analysis

test_phase2_integration.py        # Integration tests
```

## Installation
Clone the repository and install with uv pip:
```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r pyproject.toml
# or uv sync
```

## Usage
Import the MGES engine and data sources in your Python code:
```python
from mges.materialist_ges_engine import MaterialistGESEngine
from mges.materialist_data_sources import DataSource

# Example usage
engine = MaterialistGESEngine()
data = DataSource().get_data()
result = engine.analyze(data)
print(result)
```

## Testing
Run integration tests with:
```bash
python test_phase2_integration.py
```

## Contributing
Contributions are welcome! Please see `implementation_roadmap.md` for current plans and open tasks.

## License
Specify your license here (e.g., MIT, Apache 2.0).

## Contact
For questions or suggestions, open an issue or contact the maintainer.
