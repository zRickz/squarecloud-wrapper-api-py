from ..app import Application
from ..errors import SquareException
from asyncio import sleep, iscoroutinefunction, run
import threading

class LogsLoop:
    def __init__(self, app: Application, callback: callable, cooldown: int) -> None:
        self.app = app
        self.callback = callback
        self.cooldown = cooldown
    
    async def _loop(self):
        old_logs = ""
        while True:
            new_logs = await self.app.logs()
            if new_logs != old_logs:
                old_logs = new_logs
                await self.callback(old_logs)
            await sleep(self.cooldown)

    async def start(self):
        thread = threading.Thread(target=lambda: run(self._loop()))
        thread.daemon = True
        thread.start()
        print('[LOGS LOOP] Started!')
        
class Logs:
    
    @classmethod
    async def loop(self, app: Application, callback: callable, cooldown: int = 15, as_thread=True) -> LogsLoop:   
        """
        Get logs loop

        Args:
            app (Application): The app to get logs from
            callback (callable): A callback function that will be called when logs are available
            cooldown (int, optional): A cooldown time in seconds to wait for logs to be available. Default to 15.

        Returns:
            Union[LogsLoop, LogsData]
        """
        if not iscoroutinefunction(callback):
            return SquareException("Invalid Callback Function")
        if cooldown < 15:
            return SquareException("Cooldown must be greater than 15 seconds")
        
        loop = LogsLoop(app=app, callback=callback, cooldown=cooldown)
        
        if as_thread:
            return loop 
        else:
            await loop._loop()