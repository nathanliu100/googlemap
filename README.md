# GeoJSON project

The project can do a brand or a category nearby search for specific locations, and get the Geodata into an excel document as tabular format. For example, you want to know how many fast-food restaurants (includes addresses) within 5 miles of Ivy League schools.

## Installation

This was created and tested using Python3.7 and using some libraries including [openpyxl](https://openpyxl.readthedocs.io/), [googlemaps](https://github.com/googlemaps/google-maps-services-python), [prettyprinter](https://github.com/tommikaikkonen/prettyprinter), [urllib3](https://urllib3.readthedocs.io). These libraries are needed. To install with pip:

```bash
pip install openpyxl
pip install googlemaps
pip install urllib3
pip install prettyprinter
```
## Google Map API

The project also requires [Google Map API Key](https://developers.google.com/maps). Please register and fill your API Key into the program.

```bash
api_key = 'Enter your Google Map API HERE'

if api_key is False:
    print("API is False")
else:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and acknowledgment
This code is inspired by Dr. Charles through his course Python for Everybody

## License
[MIT](https://choosealicense.com/licenses/mit/)
