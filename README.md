# Soil Health Mapping using Satellite Data

This repository contains code and resources for training Random Forest Regressor models to predict soil health parameters (Nitrogen, Phosphorus, Potassium, Organic Carbon) using remote sensing data (Sentinel-2) and environmental datasets (MODIS, CHIRPS, SOILGRIDS, SRTM).

---

## 📦 Installation

We recommend using a virtual environment to avoid dependency conflicts.

### 1. Clone the repository

```bash
git clone https://github.com/Aakash3101/shc-code.git
cd shc-code
````

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📥 Downloading Data

### A. Soil Health Data

### B. Satellite & Environmental Data (via Google Earth Engine)

---

## 🚀 Running the Project

---

## 📊 Evaluation

---

## 🗂 Directory Structure

```
shc-code/
│
├── shc-data/
│   ├── Agro_Ecological_Regions.geojson
│   │
│   ├── KML_files/states/
│   │   ├── HARYANA                 # State
|   |   |   ├── FARIDABAD           # District
│   │   │   ├── GURUGRAM            # KML files for each period along with
|   |   |   ├── ....                # features.json which has combined data
│   │   │   └── KARNAL              # of all the KML files for that district
│   │   ├── ....
│   │   └── BIHAR
│   │
│   ├── YEAR_WISE_DATA/
│   │   ├── 2023
│   │   |   ├── ASSAM_2023.csv      # Each State/UT as a CSV file with Soil Health Data
│   │   │   └── ....
│   │   └── 2024
│   │
│   ├── NORMALIZED_DATA/            # Soil Health Data after applying Z-score district-wise
│   │   ├── 2023
|   |   |   ├── ASSAM_2023.csv      # Each State/UT as a CSV file with Soil Health Data
│   │   │   └── ....
│   │   ├── 2024
│   │   └── AGRI_2023-24
│   │
│   ├── SATELLITE_DATA/             # Download the exported CSV files from Google Drive
│   │   ├── 2023
|   |   |   ├── ASSAM               # Each State/UT as a folder with CSV files for that state
│   │   │   └── ....
│   │   ├── 2024
│   │   └── AGRI_2023-24
│   │
│   └── AEZS/                       # Satellite data split into AEZs
│       ├── 2023
|       |   ├── AEZ2.csv            # Soil Health Data + Satellite Data for each AEZ
│       │   └── ....
│       ├── 2024
│       └── AGRI_2023-24
│
├── rfr_joblib/                     # Trained Random Forest models as joblib files
├── rfr_csv/                        # Random Forest models stored as CSV files
├── plots/
│   ├── AEZ_2                       # Plots for each AEZ
|   |   ├── N                       # Plots for each property
│   │   |   └── ....
|   |   ├── P
│   │   ├── K
|   |   └── OC
│   ├── AEZ_19
│   └── AEZ_20
├── utils/
│   ├── fetch_features.py
│   ├── get_feature_info.py
│   ├── get_layer_info.py
│   └── segregate_by_aez.py
│
├── 1_data_download.py
├── 2_segregate_data_by_state.py
├── 3_data_preprocessing.ipynb
├── 4_satellite_datapipeline.ipynb
├── 5_process_satellite_to_aez.ipynb
├── 6_balanced_RF_model.ipynb
├── 7_rf_to_csv.ipynb
├── 8_predict_and_generate.ipynb
├── .gitattributes
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 📌 Notes

* Google Earth Engine (GEE) Python API requires authentication and quota limits may apply.
* You can customize the model training script to use month-wise or season-wise satellite composites.
* For large datasets, split feature extraction and process in batches to avoid memory errors.

---

## 📃 License

MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

For issues, raise a GitHub Issue or email [aakash312000@gmail.com](mailto:aakash312000@gmail.com).