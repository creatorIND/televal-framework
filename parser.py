import json
from typing import Dict, Any
from pydantic import BaseModel, Field, ValidationError

class TelemetryRecord(BaseModel):
    timestamp: str
    device_id: str
    # Enforcing the hardware constraints directly in the schema
    cpu_temp_c: float = Field(le=85.0) # Fails if Temp > 85.0C
    memory_usage_mb: int = Field(le=800) # Fails if Memory > 800MB
    wifi_status: str = Field(pattern="^CONNECTED$") # Fails if not exactly "CONNECTED"

def parse_and_validate_telemetry(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r") as f:
        raw_data = json.load(f)

    report = {
        "total_processed": len(raw_data),
        "valid_records": 0,
        "failed_records": 0,
        "error_summary": {
            "thermal_spikes": 0,
            "memory_leaks": 0,
            "connectivity_drops": 0
        }
    }

    for item in raw_data:
        try:
            # Pass the raw JSON object through the strict Pydantic model
            TelemetryRecord(**item)
            report["valid_records"] += 1

        except ValidationError as e:
            report["failed_records"] += 1

            # Map Pydantic's strict errors to our business logic
            error_fields = [err["loc"][0] for err in e.errors()]

            if "cpu_temp_c" in error_fields:
                report["error_summary"]["thermal_spikes"] += 1
            if "memory_usage_mb" in error_fields:
                report["error_summary"]["memory_leaks"] += 1
            if "wifi_status" in error_fields:
                report["error_summary"]["connectivity_drops"] += 1

    return report

if __name__ == "__main__":
    # Test the parser directly
    results = parse_and_validate_telemetry("telemetry_data.json")
    print("\n--- Validation Report ---")
    print(f"Total Records: {results['total_processed']}")
    print(f"Passed: {results['valid_records']}")
    print(f"Failed: {results['failed_records']}")
    print(f"Details: {json.dumps(results['error_summary'], indent=2)}")
    print("----------------------------------\n")