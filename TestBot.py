import squarecloud as square
from squarecloud.utils import loops
from asyncio import run
from dotenv import load_dotenv
import os
from threading import Thread

load_dotenv()

client = square.Client(os.getenv('API_KEY'), debug=False)

async def printLog(logs):
    [print(f'[NOVA LOG DETECTADA]: {log}') for log in logs.logs.split('\n')]

async def main():
    app = await client.app('4107543a7fa74c0695ddbc1e77960fd0')
    await loops.Logs.loop(app, printLog, as_thread=False)

run(main())