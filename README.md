# FirstCash.py

#### *A basic Python library to communicate with the FirstCash mobile app API.*

This is a super basic library designed for querying the FirstCash mobile app API, which
allows the developer to search for stores, items, and more. One major advantage of this
library is it exposes API methods that aren't in use on the FirstCash [inventory website](https://search.cashamerica.com/),
such as limiting your search to specific stores or multiple categories.

Note: This library does require an API key. While one is very is easy to obtain if you just look
a little for it, I doubt they're legal to distribute, so you have to attain one on your own.

#### Features:
- Methods/attributes extensively explained within
- Use of modern Python built-in typing capabilities
- Asynchronous functionality

## Installation:
**This library requires at least Python 3.12 or higher.** <br>

### Pip:

---
Windows:
```commandline
py -3 -m pip install -U firstcash.py
```

Linux/macOS/Unix:
```bash
python3 -m pip install -U firstcash.py
```

### UV:

---
Windows/macOS/Linux/Unix:
```bash
uv add firstcash.py
```

## Usage:
```python
from firstcash import APIClient, StoreItemResponse
from asyncio import run

firstcash_client: APIClient = APIClient(api_key="<api key>")

async def main():
    try:
        response: StoreItemResponse = await firstcash_client.searchItemsByGeoLocation(
            category_code=0,  # Zero for all categories
            search_latitude=39.105,
            search_longitude=-94.593,
            search_radius=20  # In miles
        )
        
        for item in response.results:
            print(item)
    finally:
        await firstcash_client.closeAsyncRequestClient()

run(main())
```

(More examples provided in the [documentation](https://github.com/AgentLoneStar007/FirstCash.Py/tree/main/docs).)

## Contributing:
To build this library, a normal virtual environment is required (A.K.A. not UV).
First, install the build requirements:
```bash
python -m pip install -r requirements.txt
```
Then run the build script for either Linux or Windows:
```bash
# Linux
./scripts/build_and_install.sh

# Windows
scripts/build_and_install.bat
```
This will uninstall any existing versions of the library, build the newest version, and install it
into the environment.

I'll add more to this in the future!

## TODO:
- [ ] Add a test suite
- [x] Add some documentation and examples
- [ ] Add more extensive error handling
- [ ] Add a cache to store recently queried items and store details internally
