"""
NOTE: For now, these functions just works for backups and logs.
"""

import threading
from asyncio import iscoroutinefunction, run, sleep

from ..app import Application, LogsData
from ..errors import SquareException

from typing import Union

class LogsLoop:
    def __init__(self, app: Application, callback: callable, cooldown: int) -> None:
        self.app = app
        self.callback = callback
        self.cooldown = cooldown
        
    def __str__(self) -> str:
        return 'logs'
    
    async def _loop(self):
        old_logs = ""
        while True:
            new_logs = await self.app.logs()
            if new_logs != old_logs:
                old_logs = new_logs
                await self.callback(old_logs, self.app.id)
            await sleep(self.cooldown)

    async def start(self):
        thread = threading.Thread(target=lambda: run(self._loop()))
        thread.daemon = True
        thread.start()

class BackupsLoop:
    def __init__(self, app: Application, callback: callable, cooldown: int) -> None:
        self.app = app
        self.callback = callback
        self.cooldown = cooldown
        
    def __str__(self) -> str:
        return 'backups'
    
    async def _loop(self):
        while True:
            backup_link = await self.app.backup()
            await self.callback(backup_link, self.app.id)
            await sleep(self.cooldown)

    async def start(self):
        thread = threading.Thread(target=lambda: run(self._loop()))
        thread.daemon = True
        thread.start()

_cooldown_min = {
    'logs': 15,
    'backups': 60
}

class Loop:
    def __init__(self, loop_type: str,  app: Application, callback: callable, cooldown: int = 15, as_thread=True):
        """
        Get a loop

        Args:
            loop_type (str): The type of the loop [Available: 'logs' or 'backups'].
            app (Application): The app to get events from
            callback (callable): A callback function that will be called when new events are available.
            cooldown (int, optional): A cooldown time in seconds to wait for events to be available. Default to 15.

        Returns:
            Union[LogsLoop, LogsData, BackupsLoop, BackupsData]
        """
        self.app = app
        self.callback = callback
        self.cooldown = cooldown
        self.as_thread = as_thread
        self.loop_type = loop_type.lower()
        self._minimum_cooldown = _cooldown_min[loop_type]
        
        if self.loop_type not in _cooldown_min.keys():
            return SquareException("Invalid Loop Type")
        if not iscoroutinefunction(self.callback):
            return SquareException("Invalid Callback Function")
        if self.cooldown < self.minimum_cooldown:
            return SquareException(f"Cooldown must be greater than {self._minimum_cooldown} seconds")
    
    async def start(self):
        match(self.loop_type):
            case 'logs':
                loop = LogsLoop(self.app, self.callback, self.cooldown)
            case 'backups':
                loop = BackupsLoop(self.app, self.callback, self.cooldown)

        return await loop.start if self.as_thread else await loop._loop()