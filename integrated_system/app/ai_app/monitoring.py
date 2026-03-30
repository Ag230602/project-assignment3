from __future__ import annotations

from collections import deque
from statistics import mean
from threading import Lock
from time import time


class MonitoringService:
    def __init__(self, max_events: int = 100):
        self._max_events = max_events
        self._events = deque(maxlen=max_events)
        self._errors = deque(maxlen=max_events)
        self._lock = Lock()
        self._started_at = time()

    def record_success(self, path: str, latency_ms: float, used_fallback_model: bool):
        with self._lock:
            self._events.append(
                {
                    "path": path,
                    "latency_ms": round(latency_ms, 2),
                    "used_fallback_model": used_fallback_model,
                    "status": "success",
                    "timestamp": time(),
                }
            )

    def record_error(self, path: str, latency_ms: float, error_message: str):
        payload = {
            "path": path,
            "latency_ms": round(latency_ms, 2),
            "error_message": error_message,
            "status": "error",
            "timestamp": time(),
        }
        with self._lock:
            self._events.append(payload)
            self._errors.append(payload)

    def summary(self) -> dict:
        with self._lock:
            events = list(self._events)
            errors = list(self._errors)

        latencies = [event["latency_ms"] for event in events]
        fallback_count = sum(1 for event in events if event.get("used_fallback_model"))
        total_requests = len(events)
        error_count = len(errors)
        success_count = total_requests - error_count

        return {
            "uptime_seconds": round(time() - self._started_at, 2),
            "total_requests": total_requests,
            "successful_requests": success_count,
            "error_count": error_count,
            "fallback_responses": fallback_count,
            "average_latency_ms": round(mean(latencies), 2) if latencies else 0.0,
            "recent_errors": errors[-5:],
        }
