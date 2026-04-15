# Seattle Building Energy Forecast — Student Case Study

This repository is a learning project for predicting energy consumption in Seattle buildings. It is designed to help students run a complete data science workflow, verify results, and innovate with new models and APIs.

This exercise was originally built using Seattle data, but it is intended to be adapted by students for their own energy consumption datasets. For example, Auroville students can reuse the same pipeline with local data and use the exercise to explore regional and ecological energy issues.

## Purpose and scope

This case study aims to help every student:
- transform raw energy data into model-ready features
- train and evaluate a regression model
- package the model as a production-ready service
- serve predictions through an API
- build confidence in the complete ML lifecycle

> No final model metrics or numeric results are provided here. Students must run the pipeline themselves and interpret the outputs.

## Learning objectives

By working with this project, students should be able to:
- prepare raw data for machine learning
- perform feature engineering for regression
- split data into training and test sets
- evaluate model performance with R², MAE, and RMSE
- wrap a model in a BentoML API
- verify service behavior with client requests
- extend the pipeline with new models, features, or endpoints

## Syllabus

This case study is part of a data engineering and machine learning curriculum focused on real-world applications in environmental prediction (inspired by Seattle emissions and energy data). The syllabus covers:

### Pedagogical Objectives
- Understand the end-to-end data science pipeline from raw data to deployed API.
- Develop skills in data preprocessing, model training, and production deployment.
- Learn best practices for reproducible and scalable ML projects.
- Encourage experimentation and critical thinking in model improvement.

### Key Competencies Acquired
- Data manipulation with Pandas and NumPy.
- Feature engineering for predictive modeling.
- Regression analysis and hyperparameter tuning with Scikit-learn.
- API development and validation with BentoML and Pydantic.
- Containerization and deployment with Docker.
- Version control and collaborative development with Git and GitHub.

### Assessment and Evaluation
- Successful execution of the full pipeline (data preparation, training, serving).
- Ability to interpret model metrics and suggest improvements.
- Extension of the project with new features or models.
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

## Repository structure

- `README.md` — this student guide and workflow reference
- `pyproject.toml` / `requirements.txt` — dependency definitions
- `Dockerfile` — container configuration for deployment
- `bentofile.yaml` — BentoML packaging configuration
- `data/raw/` — original raw Seattle dataset
- `data/processed/` — processed dataset ready for modeling
- `src/seattle_energy/` — modular pipeline code
  - `data_processing.py` — data cleaning and feature engineering
  - `model_training.py` — training, evaluation, and BentoML export
  - `service.py` — BentoML service and validation logic
- `notebooks/` — interactive notebooks for each stage
  - `01_prepare_data.ipynb` — load raw data, explore features, and build the cleaned dataset
  - `02_train_model.ipynb` — train a baseline model, compare with a Random Forest, and save the BentoML model
  - `03_run_service.ipynb` — start the BentoML API service and verify endpoints with live requests
  - `04_test_api.ipynb` — test the prediction endpoint with example payloads

> The local folder `old-projet/` contains reference notebooks and files that are intentionally ignored on GitHub. The public student workflow is in `notebooks/`.

## Step-by-step student workflow

**Note**: This repository provides a skeleton framework for the exercise. Students must adapt the notebooks and modules to their own datasets and requirements. For example:
- Modify data processing to handle local energy consumption data (e.g., from Auroville or other regions).
- Add ecological metrics like carbon footprint calculations or renewable energy indicators.
- Experiment with different models (e.g., add regression variants or neural networks).
- Customize API endpoints for specific use cases, such as batch predictions or model explainability.
- Ensure data privacy and compliance with local regulations.

The notebooks guide you through the process, but creativity and adaptation are key to mastering the concepts.

### 1. Install dependencies

The recommended approach is Poetry:

```bash
poetry install
```

If you prefer pip:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

### 2. Install Jupyter Notebook

To run the notebooks, install Jupyter Notebook with Poetry or pip:

```bash
poetry run python -m notebook
```

Or with pip:

```bash
python -m pip install notebook
python -m notebook
```

### 3. Open the notebooks

Open the notebook server and launch the notebooks inside the `notebooks/` folder. The main workflow is:
- `notebooks/01_prepare_data.ipynb`
- `notebooks/02_train_model.ipynb`
- `notebooks/03_run_service.ipynb`
- `notebooks/04_test_api.ipynb`

### 4. Prepare the dataset

Use `notebooks/01_prepare_data.ipynb` to load raw Seattle data, build model-ready features, and save the processed dataset.

After this step, `data/processed/feature_engineered_cleaned_for_bento.csv` is created.

### 5. Train a model

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

## Important note for students

This repository is intentionally focused on process and learning. It does not include final numeric results, model scores, or precomputed conclusions. The value comes from:
- running the workflow yourself
- observing the output
- comparing choices
- explaining what changes improved the model
