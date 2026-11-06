import pytest
from parser import parse_and_validate_telemetry

# Load the telemetry report once for the entire test suite
@pytest.fixture(scope="module")
def report():
    return parse_and_validate_telemetry("telemetry_data.json")

def test_thermal_stability(report):
    total = report["total_processed"]
    spikes = report["error_summary"]["thermal_spikes"]
    failure_rate = (spikes / total) * 100

    # Device must maintain thermal stability (less than 15% failure rate under stress)
    assert failure_rate < 15.0, f"Thermal stability failed: {failure_rate:.1f}% spike rate"

def test_memory_allocation(report):
    total = report["total_processed"]
    leaks = report["error_summary"]["memory_leaks"]
    failure_rate = (leaks / total) * 100

    # Memory leaks should not exceed 20% of the runtime cycle
    assert failure_rate < 20.0, f"Memory threshold breached: {failure_rate:.1f}% leak rate"

def test_connectivity_uptime(report):
    total = report["total_processed"]
    drops = report["error_summary"]["connectivity_drops"]
    failure_rate = (drops / total) * 100
    
    # Wi-Fi drops must remain under 20%
    assert failure_rate < 20.0, f"Connectivity unstable: {failure_rate:.1f}% drop rate"