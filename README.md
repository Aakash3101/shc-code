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

### A. Downloading Soil Health Data

#### STEP 1

The Soil Health Data can be downloaded from using the `1_data_download.py`. This will save the data as KML files for all the periods for each district in each State/UT. All the data in a district is also stored as a JSON file named `features.json`.

Execute the command to run the script:

```bash
$ python 1_data_download.py
```

#### STEP 2

Now you select the desired years in the `2_segregate_data_by_state.py` script. And after executing it you will have a `YEAR_WISE_DATA` directory inside the `shc_data` directory, with sud-directories for the desired years. Each sub-directory will contain CSV files for each State/UT.

Execute the command to run the script:

```bash
$ python 2_segregate_data_by_state.py
```

### B. Preprocessing the Soil Health Data

#### STEP 3

After splitting the dataset into year-wise directories. Now the next step is to apply Z-score method to remove outliers district wise from the dataset. Execute the `3_data_preprocessing.ipynb` notebook to remove outliers from the dataset. The new filtered dataset will be stored in the `NORMALISED_DATA` directory in the `shc_data` directory.

There is another section in the notebook, where you select the dataset from a given period (start_date, end_date), after that we use the Z-score method to remove outliers district wise. And then save it in the `NORMALISED_DATA` diretctory.

### C. Satellite & Environmental Data (via Google Earth Engine)

#### STEP 4

After completing the preprocessing step, you can now begin downloading the Satellite data from Earth Engine using the `4_satellite_datapipeline.ipynb`. All the CSV files will be exported to your Google Drive. From there, you should download and put them in respective state folders, or however you like. Because in the next step we will be loading all the CSV files together to split them into AEZs.

#### STEP 5

Using the `5_process_satellite_to_aez.ipynb` notebook, we will concatenate all our Satellite data and then split them into AEZs. These AEZs will be saved in the `AEZS` directory under the `shc_data` directory.

---

## 🚀 Training

### A. Training the Random Forest Regressor Models

#### STEP 6

Using the `6_balanced_RF_model.ipynb` notebook, we train our Random Forest Regressor models. We select a particular AEZ and then the soil property we want to predict, and begin training it. We iteratively remove the features from the selected feature list by reviewing the feature importance of the model trained.

A 10-Fold cross validation is also conducted to find the best model by comparing the R2 scores of the Test set. The best model is then saved as a joblib file in the `rfr_joblib` directory.

---

⚠️ **Warning:**

The size of the joblib file should be less than 10MB, because for the inference we have to convert our Random Forest Regressor models to CSV files and then upload them to GEE using the GEE Python API (the payload size for the API is 10MB). There is also a limitation on the number of characters in the CSV file in a single field to be strictly less than 1 million characters. Hence `n_estimators` and `max_depth` are set to 10 and 20 respectively. If the model size is still large, first try to reduce the `max_depth` parameter and then the `n_estimators` parameter. Try to find the best possible combination for better R2 scores and file size. Alternatively, sometime reducing the `n_estimators` first can sometimes provide better models.

---

### B. Converting Random Forest Regressor Models to CSV files

#### STEP 7

Using the `7_rf_to_csv.ipynb` notebook, we will convert our models to CSV files for inference. The CSV files will be stored in the `rfr_csv` directory. Please pay attention to the above warning before proceeding to the inference.

---

## 📊 Prediction and Generation

### Inference

#### STEP 8

After completing step 7, we have our models as CSV files. We use the joblib and CSV files to automatically fetch the best selected features and the model, and then recreate our model on GEE using its Python API. We will be using the `8_predict_and_generate.ipynb` notebook.

If during inference you observe an error stating somethin similar to `Maximum description length exceeded` then it means the number of characters in a field in the CSV exceeds 1 million characters and hence you would have to reduce the model size by changing the aforementioned parameters.

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
│
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