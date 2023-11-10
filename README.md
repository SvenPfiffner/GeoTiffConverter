# GeoTiffConverter
![python_v3.8.18](https://img.shields.io/badge/Python-3.8.18-green)
![unit_tests](https://github.com/SvenPfiffner/GeoTiffConverter/actions/workflows/python-app.yml/badge.svg?branch=main)
![Banner](https://github.com/SvenPfiffner/GeoTiffConverter/blob/main/geotiff.png?raw=true)

## Installation
Run ```pip install -r requirements.txt``` in the root directory

## Usage
Run ```python gui.py``` in the root directory to start the WebUI. It will be accessible under **http://127.0.0.1:7860/**

### Supported systems
The converter is based on the implementation of [pyproj](https://pypi.org/project/pyproj/). A list of supported map projections for the TIFF files is given [here](https://proj.org/en/9.3/operations/projections/index.html)