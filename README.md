# FirstCash.py

#### *A basic Python library to communicate with the FirstCash mobile app API.*

This is a super basic library designed for querying the FirstCash mobile app API, which
allows the developer to search for stores, items, and more. One major advantage of this
library is it exposes API methods that aren't in use on the FirstCash [inventory website](https://search.cashamerica.com/),
such as limiting your search to specific stores or multiple categories.

Note: This library does require an API key. While this is easy to obtain, I doubt they're legal to distribute,
so you have to attain one on your own.

#### Features:
- Methods/attributes extensively explained within
- Use of modern Python built-in typing capabilities
- Asynchronous functionality

## Installation:
**This library requires at least Python 3.9 or higher.** <br>

Linux/macOS/Unix:
```commandline
python3 -m pip install -U firstcash.py
```

Windows:
```commandline
py -m -3 pip install -U firstcash.py
```

## Usage:
```python
import firstcash
from asyncio import run

firstcash_client: firstcash.APIClient = APIClient(api_key="<api key>")

async def main():
    response: firstcash.StoreItemResponse = await firstcash_client.searchItemsByGeoLocation(
        category_code=0,  # Zero for all categories
        search_latitude=39.105,
        search_longitude=-94.593,
        search_radius=20  # In miles
    )
    
    for item in response.results:
        print(item)

run(main())
```

(More examples provided in the [documentation](https://github.com/AgentLoneStar007/FirstCash.Py/tree/main/docs).)


