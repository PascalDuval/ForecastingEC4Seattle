# Seattle Building Energy Forecast — Guide étudiant

Ce dépôt est un projet d'apprentissage complet pour prédire la consommation énergétique des bâtiments de Seattle. Il couvre l'intégralité du cycle de vie ML : nettoyage des données → feature engineering → entraînement → déploiement API.

> **Aucun résultat numérique n'est fourni.** Vous devez exécuter le pipeline vous-même et interpréter les sorties.

---

## Table des matières

1. [Prérequis](#1-prérequis)
2. [Cloner le dépôt](#2-cloner-le-dépôt)
3. [Créer et activer l'environnement](#3-créer-et-activer-lenvironnement)
4. [Installer les dépendances](#4-installer-les-dépendances)
5. [Lancer Jupyter et les notebooks](#5-lancer-jupyter-et-les-notebooks)
6. [Entraîner le modèle](#6-entraîner-le-modèle)
7. [Démarrer le service BentoML](#7-démarrer-le-service-bentoml)
8. [Tester l'API](#8-tester-lapi)
9. [Déploiement Docker (optionnel)](#9-déploiement-docker-optionnel)
10. [Structure du projet](#10-structure-du-projet)
11. [Objectifs pédagogiques](#11-objectifs-pédagogiques)

---

## 1. Prérequis

Avant de commencer, vérifiez que vous disposez de :

| Outil | Version minimale | Vérification |
|---|---|---|
| Python | **3.11** | `python --version` |
| pip | dernière | `pip --version` |
| Git | toute version récente | `git --version` |

> **Windows** : utilisez PowerShell ou le terminal VS Code. Évitez l'invite de commandes classique (`cmd`).

---

## 2. Cloner le dépôt

```bash
git clone https://github.com/PascalDuval/ForecastingEC4Seattle.git
cd ForecastingEC4Seattle
```

---

## 3. Créer et activer l'environnement

Choisissez **une seule** des deux options ci-dessous. L'option A (venv) est la plus simple.

### Option A — venv + pip (recommandé pour débuter)

**Créer l'environnement virtuel :**

```bash
python -m venv .venv
```

**Activer l'environnement :**

- Windows (PowerShell) :
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
  > Si PowerShell bloque l'exécution de scripts, exécutez d'abord :
  > `Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned`

- macOS / Linux :
  ```bash
  source .venv/bin/activate
  ```

Une fois activé, votre invite affiche `(.venv)` au début.

---

### Option B — Poetry (gestion avancée des dépendances)

```bash
# Installer Poetry si ce n'est pas déjà fait
pip install poetry

# Installer les dépendances et créer l'environnement automatiquement
poetry install

# Activer le shell Poetry
poetry shell
```

---

## 4. Installer les dépendances

> Si vous utilisez Poetry (option B), cette étape est déjà effectuée par `poetry install`.

Avec l'environnement activé (option A) :

```bash
pip install -r requirements.txt
```

Pour vérifier que tout est bien installé :

```bash
python -c "import pandas, sklearn, bentoml; print('OK')"
```

---

## 5. Lancer Jupyter et les notebooks

Avec l'environnement activé, démarrez Jupyter :

```bash
jupyter notebook
```

Un onglet s'ouvre dans votre navigateur. Naviguez vers le dossier `notebooks/` et exécutez les notebooks **dans l'ordre** :

| Fichier | Contenu |
|---|---|
| `00_exploratory_analysis.ipynb` | Analyse exploratoire des données brutes |
| `01_clean_data.ipynb` | Nettoyage et purge des outliers |
| `02_feature_engineering.ipynb` | Construction des features |
| `03_train_model.ipynb` | Entraînement et évaluation du modèle |
| `04_run_service.ipynb` | Démarrage du service BentoML |
| `05_test_api.ipynb` | Tests de l'API avec des requêtes HTTP |

**Dans VS Code**, vous pouvez aussi ouvrir directement un `.ipynb`. Vérifiez que le kernel sélectionné correspond bien à votre environnement virtuel (`.venv` ou Poetry).

> **Important** : exécutez les notebooks dans l'ordre. Chaque notebook produit des fichiers utilisés par le suivant.

---

## 6. Entraîner le modèle

Le notebook `03_train_model.ipynb` entraîne le modèle et le sauvegarde dans le store BentoML local.

Vous pouvez aussi l'entraîner en ligne de commande (environnement activé) :

```bash
python -c "
from seattle_energy.model_training import train_and_save
train_and_save()
"
```

Pour lister les modèles enregistrés :

```bash
bentoml models list
```

---

## 7. Démarrer le service BentoML

Une fois le modèle enregistré, démarrez l'API de prédiction :

```bash
bentoml serve seattle_energy.service:EnergyService --reload
```

Le service écoute sur **http://localhost:3000**.

- Interface Swagger interactive : [http://localhost:3000](http://localhost:3000)
- Laisser ce terminal ouvert pendant les tests.

> `--reload` recharge automatiquement le code si vous modifiez `src/seattle_energy/service.py`.

---

## 8. Tester l'API

Ouvrez un **nouveau terminal** (avec l'environnement activé) et exécutez le notebook `05_test_api.ipynb`, ou lancez directement :

```bash
python old_scripts/test_api.py
```

Vous pouvez aussi tester manuellement avec `curl` :

```bash
curl -X POST http://localhost:3000/predict \
  -H "Content-Type: application/json" \
  -d '{"BuildingType": "Office", "GrossFloorArea": 5000, "YearBuilt": 1990}'
```

---

## 9. Déploiement Docker (optionnel)

Pour construire et lancer le service dans un conteneur Docker :

```bash
# Construire l'image
docker build -t seattle-energy-service .

# Lancer le conteneur
docker run -p 3000:3000 seattle-energy-service
```

Le service est alors accessible à la même adresse : [http://localhost:3000](http://localhost:3000).

---

## 10. Structure du projet

```
dataprojet6/
├── data/
│   ├── raw/                   # Données brutes originales
│   └── processed/             # Données nettoyées et feature-engineered
├── notebooks/                 # Notebooks à exécuter dans l'ordre
│   ├── 00_exploratory_analysis.ipynb
│   ├── 01_clean_data.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_train_model.ipynb
│   ├── 04_run_service.ipynb
│   └── 05_test_api.ipynb
├── src/
│   └── seattle_energy/        # Code source du projet (package Python)
│       ├── data_processing.py
│       ├── model_training.py
│       └── service.py
├── tests/                     # Tests unitaires
├── bentofile.yaml             # Configuration du service BentoML
├── Dockerfile                 # Image Docker du service
├── pyproject.toml             # Métadonnées et dépendances (Poetry)
└── requirements.txt           # Dépendances pip
```

---

## 11. Objectifs pédagogiques

Ce projet vous permet d'acquérir les compétences suivantes :

- **Préparation des données** : nettoyage, détection d'outliers, encodage, normalisation
- **Feature engineering** : construction de variables pertinentes pour la régression
- **Modélisation** : entraînement, validation croisée, optimisation des hyperparamètres (R², MAE, RMSE)
- **Déploiement** : emballage du modèle avec BentoML, exposition via une API REST
- **Containerisation** : packaging Docker pour un déploiement reproductible
- **Bonnes pratiques** : gestion de l'environnement, versionnage avec Git

### Évaluation

- Pipeline complet exécuté sans erreur
- Interprétation des métriques de performance
- Extension du projet : nouveau modèle, nouvelle feature, ou nouvel endpoint API
- Documentation of changes and rationale in commit messages or a personal report.

### Prerequisites
- Basic Python programming.
- Familiarity with data structures (lists, dictionaries).
- Understanding of basic statistics (mean, variance).
- No prior ML experience required, but curiosity for experimentation is essential.

### Timeline and Milestones
- **Week 1**: Data exploration and cleaning.
- **Week 2**: Feature engineering and model training.
- **Week 3**: API development and testing.
- **Week 4**: Deployment, extensions, and final report.

## Explanation of Key Methods

This project demonstrates core data engineering and machine learning methods for predicting building energy consumption. Below is an overview of the major approaches used, aligned with standard practices in predictive analytics.

### 1. Data Cleaning and Preprocessing
- **Method**: Filtering invalid data, handling missing values, and type conversion.
- **Tools**: Pandas for data manipulation.
- **Why**: Ensures data quality; removes outliers and inconsistencies that could bias the model.
- **Implementation**: In `data_processing.py`, functions like `safe_float` convert strings to numbers, and filters exclude non-positive energy values.

### 2. Feature Engineering
- **Method**: Creating derived features from raw data, such as logarithmic transformations, binary flags, and categorical encoding.
- **Tools**: NumPy for mathematical operations.
- **Why**: Improves model performance by capturing non-linear relationships and domain knowledge (e.g., building size impacts).
- **Implementation**: Log-transform surface area, calculate energy percentages, and encode building types as binary flags.

### 3. Model Training and Evaluation
- **Method**: Supervised regression with Random Forest, hyperparameter optimization via randomized search, and cross-validation.
- **Tools**: Scikit-learn for modeling and metrics.
- **Why**: Random Forest handles non-linear data well; evaluation metrics (R², MAE, RMSE) assess accuracy and error.
- **Implementation**: In `model_training.py`, train/test split (80/20), RandomizedSearchCV for tuning, and metrics calculation.

### 4. Model Packaging and Serving
- **Method**: Export model to BentoML, define API with input validation, and serve via HTTP.
- **Tools**: BentoML for ML serving, Pydantic for schemas.
- **Why**: Enables production deployment; validation prevents invalid predictions.
- **Implementation**: In `service.py`, EnergyService class with predict endpoint; schemas ensure correct input format.

### 5. Deployment and Containerization
- **Method**: Package application in Docker for portability.
- **Tools**: Docker for containers.
- **Why**: Ensures consistent environments across systems; simplifies scaling.
- **Implementation**: Dockerfile builds image with dependencies; runs BentoML service in production mode.

These methods form a robust foundation for environmental data projects, emphasizing reproducibility and scalability.

## Deployment with Docker and BentoML

Once you've trained your model and built the API, you can deploy it in a production-like environment using Docker and BentoML. This section explains what these tools do and how to use them.

### Why Docker and BentoML?
- **BentoML**: A framework for serving machine learning models as APIs. It packages your model, code, and dependencies into a "bento" (a deployable unit) that can run predictions via HTTP requests. This makes your ML model accessible like a web service.
- **Docker**: A tool for containerization. It packages your entire application (including BentoML) into a lightweight, portable container that runs consistently on any system. This ensures your model works the same way everywhere, without "it works on my machine" issues.

Together, they allow you to turn your trained model into a real API that can be deployed on servers, clouds, or shared with others.

### Deployment Steps
1. **Train and Save Your Model**: Run the notebooks to train your model and save it with BentoML (done in `03_train_model.ipynb`).
2. **Build the Bento**: BentoML automatically packages your model based on `bentofile.yaml`.
3. **Containerize with Docker**: Build a Docker image that includes your bento and all dependencies.
4. **Run the Container**: Start the API service inside the container.

### Commands to Deploy
After completing the notebooks:

1. **Build the BentoML service** (this packages your model):
   ```bash
   bentoml build
   ```

2. **Build the Docker image** (this creates a container with your service):
   ```bash
   docker build -t seattle-energy-api .
   ```

3. **Run the Docker container** (this starts the API on port 3000):
   ```bash
   docker run -p 3000:3000 seattle-energy-api
   ```

4. **Test the API** (send a prediction request):
   ```bash
   curl -X POST "http://localhost:3000/predict" \
        -H "Content-Type: application/json" \
        -d '{
          "log_surface": 11.2,
          "percent_electricity": 45.0,
          "has_parking": 1,
          "BuildingAge": 45,
          "surface_per_floor": 9000.0,
          "Use_Hotel": 0,
          "Use_Office": 1,
          "Use_Retail_Store": 0,
          "Use_Other": 0,
          "Use_Non_Refrigerated_Warehouse": 0,
          "Use_K12_School": 0,
          "Use_Medical_Office": 0,
          "Use_Worship_Facility": 0,
          "Use_Unknown": 0
        }'
   ```

> **Note for Students**: Docker requires installation on your machine. If you don't have Docker, you can still run the BentoML service directly with `bentoml serve seattle_energy.service:EnergyService --port 3000` after training the model.

## Repository structure

- `README.md` — this student guide and workflow reference
- `pyproject.toml` / `requirements.txt` — dependency definitions for Python packages
- **Deployment Files** (for production API):
  - `Dockerfile` — Docker container configuration for running the API in production
  - `bentofile.yaml` — BentoML configuration for packaging the ML model and service
- `data/raw/` — original raw Seattle dataset
- `data/processed/` — processed dataset ready for modeling
- `src/seattle_energy/` — core reusable pipeline modules shared by notebooks and service code
  - `data_processing.py` — data cleaning and feature engineering
  - `model_training.py` — training, evaluation, and BentoML export
  - `service.py` — BentoML service and validation logic
- `notebooks/` — interactive notebooks for each stage
  - `00_exploratory_analysis.ipynb` — inspect the raw dataset, semantic column meanings, and initial data selection logic
  - `01_clean_data.ipynb` — clean the filtered dataset, remove invalid rows, deduplicate, and detect outliers
  - `02_feature_engineering.ipynb` — build model-ready features from the cleaned dataset
  - `03_train_model.ipynb` — train a baseline model, compare with a Random Forest, and save the BentoML model
  - `04_run_service.ipynb` — start the BentoML API service and verify endpoints with live requests
  - `05_test_api.ipynb` — test the prediction endpoint with example payloads

> The local folder `old-projet/` contains reference notebooks and files that are intentionally ignored on GitHub. The public student workflow is in `notebooks/`.
> `old_scripts/` is not required for the core pipeline logic; il s’agit de simples scripts de lancement autour du package `src/seattle_energy/`.

## Step-by-step student workflow

**Note**: This repository provides a skeleton framework for the exercise. Students must adapt the notebooks and modules to their own datasets and requirements. For example:
- Modify data processing to handle local energy consumption data (e.g., from Auroville or other regions).
- Add ecological metrics like carbon footprint calculations or renewable energy indicators.
- Experiment with different models (e.g., add regression variants or neural networks).
- Customize API endpoints for specific use cases, such as batch predictions or model explainability.
- Ensure data privacy and compliance with local regulations.

The notebooks guide you through the process, but creativity and adaptation are key to mastering the concepts.

### 4. Explore the raw dataset

Use `notebooks/00_exploratory_analysis.ipynb` first to inspect the raw Seattle dataset, understand the main column groups, check missing values, and create a filtered purge dataset for the data preparation step.

### 5. Clean the filtered dataset

Use `notebooks/01_clean_data.ipynb` to clean the filtered dataset, remove invalid and duplicate rows, and create a reliable model dataset. This notebook also detects combined energy and surface outliers and saves them to `data/outliers_surface_energy.csv`.

> The notebooks can reuse shared routines from `src/seattle_energy/` either when the package is installed in the Python environment or by adding `src` to `sys.path` in the notebook.

### 6. Feature engineering

Use `notebooks/02_feature_engineering.ipynb` to analyze derived metrics from the cleaned dataset, compute electricity share and log-transformed features, detect important outliers, and save the final model-ready dataset.

After this step, `data/processed/feature_engineered_cleaned_for_bento.csv` is created.

After this step, `data/processed/feature_engineered_cleaned_for_bento.csv` is created.

### 7. Train a model

Use `notebooks/02_train_model.ipynb` to train and evaluate the model, then save it to BentoML.

This notebook performs:
- train/test split
- baseline model evaluation with `LinearRegression`
- randomized hyperparameter search for a Random Forest model
- calculation of R², MAE, and RMSE
- comparison between baseline and advanced model
- saving the trained model to the BentoML store

### 6. Serve the model as an API

Use `notebooks/03_run_service.ipynb` to review the BentoML service and learn how to start it. The notebook explains how to launch the service in a separate terminal and how to call the endpoints from Python. The service runs on port `3000` and exposes:
- `POST /predict` — prediction endpoint
- `GET /ping` — health check

### 7. Verify the API

Use `notebooks/04_test_api.ipynb` to send a sample request to the live service and inspect the response. This notebook shows the expected input format and how to consume predictions in a reproducible way.

## Extending the exercise

Once the base pipeline works, students should try:
- creating new features in `src/seattle_energy/data_processing.py`
- comparing different regressors such as `LinearRegression`, `GradientBoostingRegressor`, or `XGBRegressor`
- improving validation rules and schema checks
- tuning hyperparameters more systematically
- adding a new API endpoint for model metadata or feature explanation
- packaging the service with `bentoml build`

## Concepts and vocabulary

Use these terms while you work:
- raw data
- feature engineering
- target variable
- regression model
- train/test split
- evaluation metrics
- BentoML service
- API endpoint
- schema validation
- model export

## BentoML and deployment

The model is exported using BentoML in `src/seattle_energy/model_training.py`. The service is defined in `src/seattle_energy/service.py`.

To build a Bento archive manually:

```bash
bentoml build
```

Then serve it with:

```bash
bentoml serve seattle_energy.service:EnergyService --port 3000
```

## API Methods and Cloud Deployment

This section provides methods for working with the API, from local testing to cloud deployment. These approaches help students understand API development and production scaling.

### Local API Usage with BentoML

BentoML is used to create a simple, validated API for predictions. To run the API locally:

1. **Start the service**:
   ```bash
   bentoml serve seattle_energy.service:EnergyService --port 3000
   ```

2. **Available endpoints**:
   - `GET /ping`: Health check (returns a status message).
   - `POST /predict`: Prediction endpoint. Send JSON data for energy forecast.

3. **Example request** (using `notebooks/04_test_api.ipynb` or tools like Postman):
   ```json
   {
     "log_surface": 8.5,
     "percent_electricity": 0.7,
     "Use_Office": 1,
     "Use_Hotel": 0
     // Include other binary flags for building types
   }
   ```
   Response: A JSON with the predicted energy value.

4. **Validation**: The API uses Pydantic schemas to validate inputs. Invalid data returns a 400 error.

5. **Extending the API**: Add new endpoints in `src/seattle_energy/service.py` using `@bentoml.api`. For example, add a GET endpoint for model metadata.

### Containerized Deployment with Docker

For production-like testing:

1. **Build the image**:
   ```bash
   docker build -t seattle-energy-app .
   ```

2. **Run the container**:
   ```bash
   docker run -p 3000:3000 seattle-energy-app
   ```

The API is now accessible on port 3000, isolated in a container.

### Cloud Deployment with Google Cloud Run

For global access and scalability, deploy to Google Cloud Platform (GCP). This uses serverless containers.

#### Prerequisites
- Google Cloud account (free tier available).
- Install Google Cloud CLI (`gcloud`): Download from https://cloud.google.com/sdk/docs/install.
- Enable APIs: Cloud Run and Container Registry.

#### Steps
1. **Authenticate and set project**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud services enable run.googleapis.com containerregistry.googleapis.com
   ```

2. **Build and push Docker image to GCR**:
   ```bash
   docker tag seattle-energy-app gcr.io/YOUR_PROJECT_ID/seattle-energy-app
   docker push gcr.io/YOUR_PROJECT_ID/seattle-energy-app
   ```

3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy seattle-energy-app \
     --image gcr.io/YOUR_PROJECT_ID/seattle-energy-app \
     --platform managed \
     --port 3000 \
     --allow-unauthenticated
   ```
   GCP provides a public URL (e.g., `https://seattle-energy-app-xxxx.run.app`).

4. **Test the deployed API**:
   Use the same JSON payload with the GCP URL:
   ```bash
   curl -X POST https://seattle-energy-app-xxxx.run.app/predict \
     -H "Content-Type: application/json" \
     -d '{"log_surface": 8.5, "percent_electricity": 0.7, "Use_Office": 1, "Use_Hotel": 0}'
   ```

#### Pedagogical Benefits
- **Local API**: Teaches API basics and validation.
- **Docker**: Introduces containerization for portability.
- **Cloud**: Demonstrates serverless deployment, scalability, and integration with GCP services (e.g., Cloud Storage for data).

Experiment with these methods to understand production ML APIs.

## Commands to run the full workflow

Below are the key commands to run the complete pipeline. Make sure dependencies are installed and the Python environment is configured.

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Exploratory analysis (Notebook 00)
Open and run `notebooks/00_exploratory_analysis.ipynb` in Jupyter to inspect the raw data and create the filtered dataset.

### 3. Data cleaning (Notebook 01)
Open and run `notebooks/01_clean_data.ipynb` to clean the filtered dataset.

### 4. Feature engineering (Notebook 02)
Open and run `notebooks/02_feature_engineering.ipynb` to create model-ready features.

### 5. Model training (Notebook 03)
Open and run `notebooks/03_train_model.ipynb` to train and save the model.

### 6. Run the API service (Notebook 04)
Open `notebooks/04_run_service.ipynb` and run the cell to start the BentoML service:
```bash
bentoml serve seattle_energy.service:EnergyService --port 3000
```

### 7. Test the API (Notebook 05)
Open and run `notebooks/05_test_api.ipynb` to test the API with example requests.

### Alternative commands for direct script execution
If you prefer running Python scripts instead of notebooks:

- Data cleaning:
```bash
python -c "from src.seattle_energy.data_processing import clean_data; clean_data('data/2016_Building_Energy_Benchmarking_Purge.csv', 'data/2016_Building_Energy_Benchmarking_ML.csv')"
```

- Feature engineering:
```bash
python -c "from src.seattle_energy.data_processing import build_feature_dataframe; df = build_feature_dataframe('data/2016_Building_Energy_Benchmarking_ML.csv'); df.to_csv('data/processed/feature_engineered_cleaned_for_bento.csv', index=False)"
```

- Model training:
```bash
python -c "from src.seattle_energy.model_training import train_and_save_model; train_and_save_model('data/processed/feature_engineered_cleaned_for_bento.csv')"
```

- Run the service:
```bash
bentoml serve src/seattle_energy/service.py:EnergyService --port 3000
```
## Testing

To verify that all dependencies and modules are correctly installed and importable, run the import test:

```bash
python tests/test_imports.py
```

This script checks that the key modules (`data_processing`, `model_training`, `service`) can be imported without errors. If successful, it prints "All imports successful". If there are issues, it will display the specific import error.

Run this test after installing dependencies to ensure the environment is set up correctly before running the notebooks or scripts.
- Test the API:
```bash
python src/seattle_energy/test_api.py
```

### Build and deploy with Docker
- Build the image:
```bash
docker build -t seattle-energy .
```

- Run the container:
```bash
docker run -p 3000:3000 seattle-energy
```

## Important note for students

This repository is intentionally focused on process and learning. It does not include final numeric results, model scores, or precomputed conclusions. The value comes from:
- running the workflow yourself
- observing the output
- comparing choices
- explaining what changes improved the model
