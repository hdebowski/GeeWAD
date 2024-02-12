# GeeWAD - Gee Web Analysis Dashboard v1.0.0.

_**What?**_ Web dashboard application based on **Google Earth Engine API**. 

_**How works?**_ The project is focused on analyzing satellite images with **GUI instead of coding**.

_**Why?**_ As a result, the project aims to make it easier to work with satellite analysis and to expand its capabilities at a later stage.

## 1. Setup & Installation 

Clone the Repository [GeeWAD](https://github.com/hdebowski/GeeWAD).
```bash
git clone https://github.com/hdebowski/GeeWAD
```

Run the Application
```bash
python run.py
```

In the last step, **log in with your Google account** and accept the necessary permissions.

## 2. Quick Look 
![](Animation.gif)


## 3. Features

GeeWAD version 1.0.0. offers 4 datasets and basic usage of analysis satellite image data.

### 3.1. Available operations
- Add satellite datasets to map
- Make band compositions for multispectral satellite data
- Apply index for multispectral satellite data
- Change date range for multispectral satellite data
- Change area of interest (Draw a polygon → click a polygon → click the button "Apply AOI - Area Of Interest")
- Reset analysis
  
### 3.2. Available Datasets
- [Sentinel 2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- [Landsat 8](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC08_C02_T1_TOA)
- [SRTM](https://developers.google.com/earth-engine/datasets/catalog/CGIAR_SRTM90_V4)
- [World Cover](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v100)

## 4. Techonologies
- Python
- Flask
- Google Earth Engine API
- HTML
- CSS
- JavaScript
- AJAX

## 5. Future versions
Future versions of the application will contain:
- support unsupervised classification
- download images
- improved form dynamics
- more datasets
- histograms


## 6. Developed by
[Hubert Dębowski](https://github.com/hdebowski)
