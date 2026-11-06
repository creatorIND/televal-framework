# System Telemetry Validation Framework

**Status:** Active Development (Ongoing)

An automated, Python-based test framework designed to validate simulated low-power subsystem telemetry, focusing on functional constraints, stress handling, and hardware stability scenarios.

This project bridges the gap between hardware testing and modern software validation practices by enforcing strict data schemas on device logs and utilizing continuous integration pipelines to catch subsystem failures (e.g., thermal spikes, memory leaks, and connectivity drops).

## System Architecture

The framework is broken down into three core modules:

1. **Telemetry Emitter (`generator.py`)**
    - Simulates continuous asynchronous device logs.
    - Purposefully injects random hardware anomalies (CPU crossing 85°C, memory approaching 1GB limits, WLAN disconnects) to simulate stress scenarios.
2. **Validation Engine (`parser.py`)**
    - Moves away from fragile Regex parsing by utilizing **Pydantic** for strict data schema enforcement.
    - Automatically traps, categorizes, and logs any telemetry data that breaches acceptable operating parameters.
3. **Automated Test Matrices (`test_telemetry.py`)**
    - Evaluates the parsed telemetry against acceptable failure-rate thresholds (e.g., thermal spike rates must remain <15% under load).

## Tech Stack

- **Python 3.12:** Core scripting and data processing.
- **Pydantic:** Chosen for strict end-to-end type safety and schema validation, mirroring the robustness of Zod in web ecosystems, applied here to hardware data streams.
- **Pytest:** Drives the test matrices and provides detailed execution summaries.
- **GitHub Actions:** CI/CD integration to ensure tests execute automatically against every new code push, enabling continuous validation.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate the simulated log stream (outputs telemetry_data.json)
python3 generator.py

# 3. Run the strict validation parser manually
python3 parser.py

# 4. Execute the test matrices
pytest test_telemetry.py -v
```
