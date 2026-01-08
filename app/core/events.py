from __future__ import annotations
from typing import Protocol, Dict, Any, List


class Observer(Protocol):
    def update(self, event: str, payload: Dict[str, Any]) -> None:
        ...


class EventBus:
    """
    Observer pattern:
    - Subject = EventBus
    - Observers = anything that implements update(event, payload)
    """
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def subscribe(self, obs: Observer) -> None:
        if obs not in self._observers:
            self._observers.append(obs)

    def unsubscribe(self, obs: Observer) -> None:
        if obs in self._observers:
            self._observers.remove(obs)

    def notify(self, event: str, payload: Dict[str, Any]) -> None:
        for obs in list(self._observers):
            obs.update(event, payload)


class ConsoleObserver:
    def update(self, event: str, payload: Dict[str, Any]) -> None:
        print(f"[EVENT] {event} - {payload}")