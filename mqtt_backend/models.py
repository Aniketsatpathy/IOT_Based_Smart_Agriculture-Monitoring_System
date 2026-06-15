from dataclasses import dataclass, asdict
from typing import Dict, Any

@dataclass
class SensorData:
    timestamp: str
    temperature: float
    humidity: float
    soil_moisture: int
    water_level: int
    light_intensity: int
    pump_status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], timestamp: str) -> "SensorData":
        """
        Creates a SensorData instance from a dictionary, casting fields to correct types.
        """
        return cls(
            timestamp=timestamp,
            temperature=float(data.get("temperature", 0.0)),
            humidity=float(data.get("humidity", 0.0)),
            soil_moisture=int(data.get("soil_moisture", 0)),
            water_level=int(data.get("water_level", 0)),
            light_intensity=int(data.get("light_intensity", 0)),
            pump_status=str(data.get("pump_status", "OFF")).upper()
        )


@dataclass
class AlertRecord:
    timestamp: str
    alert_type: str
    severity: str
    sensor_value: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "Timestamp": self.timestamp,
            "Alert Type": self.alert_type,
            "Severity": self.severity,
            "Sensor Value": self.sensor_value
        }


@dataclass
class PumpRecord:
    timestamp: str
    pump_status: str
    soil_moisture: int
    water_level: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
