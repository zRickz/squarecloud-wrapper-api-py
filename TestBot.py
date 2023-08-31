import os
from asyncio import run
from threading import Thread

from dotenv import load_dotenv

import squarecloud as square
from squarecloud.utils.loops import Loop

load_dotenv()

client = square.Client(os.getenv('API_KEY'), debug=False)

async def callbackFunction(logsData, app_id):
    print(f'New logs from {app_id}:\n{logsData.logs}')
    
async def main():
    app = await client.app(os.getenv('TESTAPP_ID'))
    # await loops.Logs.loop(app, printLog)
    BackupLoop = Loop('backups', app, printBck, as_thread=False)
    await BackupLoop.start()
    
run(main())