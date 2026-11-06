import json
import random
from datetime import datetime, timedelta

def generate_telemetry(num_records = 100, output_file = "telemetry_data.json"):
    data = []
    base_time = datetime.now()

    for i in range(num_records):
        # Baseline normal operating values
        record = {
            "timestamp": (base_time + timedelta(seconds=i*5)).isoformat(),
            "device_id": "Q-SUBSYS0-01",
            "cpu_temp_c": round(random.uniform(40.0, 65.0), 1),
            "memory_usage_mb": random.randint(200, 512),
            "wifi_status": "CONNECTED"
        }

        # Inject random system anomalies to simulate stress / failures
        anomaly_trigger = random.random()

        if anomaly_trigger < 0.05:
            # Simulate a thermal spike (Above 85C threshold)
            record["cpu_temp_c"] = round(random.uniform(86.0, 105.0), 1)
        elif anomaly_trigger < 0.10:
            # Simulate a memory leak (Approaching 1GB limit)
            record["memory_usage_mb"] = random.randint(850, 1024)
        elif anomaly_trigger < 0.15:
            # Simulate a connectivity drop
            record["wifi_status"] = "DISCONNECTED"

        data.append(record)

    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Successfully generated {num_records} telemetry records in '{output_file}'")

if __name__ == "__main__":
    generate_telemetry(200)