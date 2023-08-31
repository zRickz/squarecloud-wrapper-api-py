# Example

```python

import squarecloud as square
from squarecloud.utils.loops import Loop

client = square.Client('<YOUR_API_KEY>', debug=True)

async def callbackFunction(logsData, app_id):
    print(f'New logs from {app_id}:\n{logsData.logs}')

async def main():
    my_app = await client.app('<YOUR_APP_ID>') # Get your app object
    LoopManager = Loop('<YOUR_LOOP_TYPE>', my_app, callbackFunction) # Create a Loop Manager
    await LoopManager.start() # Start the loop
```

## Loop Class Arguments

- **loop_type**: The type of your loop [Available: 'logs' or 'backups']
- **app**: The application object of the app you want to use for this loop
- **callback**: The callback function to be called when new data is available
- [OPTIONAL] **cooldown**: The number of seconds to wait per iteration. Default is relative to the current loop type.
- [OPTIONAL] **as_thread**: True if you want to use as a thread, false otherwise. Defaults is True.