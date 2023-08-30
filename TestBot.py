import os
from asyncio import run
from threading import Thread

from dotenv import load_dotenv

import squarecloud as square
from squarecloud.utils import loops

load_dotenv()

client = square.Client(os.getenv('API_KEY'), debug=False)

async def printLog(logs):
    [print(f'[NOVA LOG DETECTADA]: {log}') for log in logs.logs.split('\n')]

async def main():
    app = await client.app(os.getenv('TESTAPP_ID'))
    await loops.Logs.loop(app, printLog, as_thread=False)

run(main())