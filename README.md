# Materialist Global Emotional State (MGES)

Materialist Global Emotional State (MGES) is a Python project designed to analyze, aggregate, and interpret emotional states from various data sources. It provides a framework for integrating materialist data sources and generating a global emotional state engine.

![alt text](image.png)

## Features
- Integration of multiple materialist data sources
- Aggregation and analysis of emotional state data
- Extensible engine for global emotional state computation
- Modular design for easy extension and testing


## Installation- this may not be completely correct- api_server has a req.txt- will try to make a setup script

Clone the repository and install with uv pip:
```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r pyproject.toml
# or uv sync
```
# Start API server (Terminal 1)
cd api_server && python app.py

# Start frontend (Terminal 2)
cd web_interface && npm install && npm start

Web UI is untested currently. Sep 8 2025

## External Usage- probably not needed

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
MIT.

## Contact
For questions or suggestions, open an issue or contact angrysky56.
