from __future__ import annotations
from typing import List

from app.services.commands import Command


class CommandManager:
    """
    Invoker (Command pattern).
    Keeps history stacks to support undo/redo.
    """
    def __init__(self) -> None:
        self._undo: List[Command] = []
        self._redo: List[Command] = []

    def run(self, cmd: Command) -> None:
        cmd.execute()
        self._undo.append(cmd)
        self._redo.clear()

    def undo(self) -> bool:
        if not self._undo:
            return False
        cmd = self._undo.pop()
        cmd.undo()
        self._redo.append(cmd)
        return True

    def redo(self) -> bool:
        if not self._redo:
            return False
        cmd = self._redo.pop()
        cmd.execute()
        self._undo.append(cmd)
        return True