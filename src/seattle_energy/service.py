import pandas as pd
import bentoml
from pydantic import BaseModel, Field, validator
import pandera as pa
from pandera import Column, Check

MODEL_NAME = "random_forest_energy"
MODEL_TAG = "latest"

model_ref = bentoml.sklearn.get(f"{MODEL_NAME}:{MODEL_TAG}")
model = bentoml.sklearn.load_model(f"{MODEL_NAME}:{MODEL_TAG}")
FEATURE_COLUMNS = model_ref.custom_objects["features"]


class EnergyInput(BaseModel):
    log_surface: float = Field(..., gt=0, description="Logarithm of the building floor area")
    percent_electricity: float = Field(..., ge=0.0, le=100.0, description="Electricity share of total energy")
    has_parking: int = Field(..., ge=0, le=1)
    BuildingAge: int = Field(..., ge=0)
    surface_per_floor: float = Field(..., gt=0)

    Use_Hotel: int = Field(0, ge=0, le=1)
    Use_Office: int = Field(0, ge=0, le=1)
    Use_Retail_Store: int = Field(0, ge=0, le=1)
    Use_Other: int = Field(0, ge=0, le=1)
    Use_Non_Refrigerated_Warehouse: int = Field(0, ge=0, le=1)
    Use_K12_School: int = Field(0, ge=0, le=1)
    Use_Medical_Office: int = Field(0, ge=0, le=1)
    Use_Worship_Facility: int = Field(0, ge=0, le=1)
    Use_Unknown: int = Field(0, ge=0, le=1)

    @validator(
        "Use_Hotel",
        "Use_Office",
        "Use_Retail_Store",
        "Use_Other",
        "Use_Non_Refrigerated_Warehouse",
        "Use_K12_School",
        "Use_Medical_Office",
        "Use_Worship_Facility",
        "Use_Unknown",
    )
    def binary_flag(cls, value):
        if value not in (0, 1):
            raise ValueError("Each usage flag must be 0 or 1")
        return value


schema = pa.DataFrameSchema(
    {
        "log_surface": Column(float, Check.gt(0)),
        "percent_electricity": Column(float, Check.in_range(0.0, 100.0)),
        "has_parking": Column(int, Check.isin([0, 1])),
        "BuildingAge": Column(int, Check.ge(0)),
        "surface_per_floor": Column(float, Check.gt(0)),
        "Use_Hotel": Column(int, Check.isin([0, 1])),
        "Use_Office": Column(int, Check.isin([0, 1])),
        "Use_Retail_Store": Column(int, Check.isin([0, 1])),
        "Use_Other": Column(int, Check.isin([0, 1])),
        "Use_Non_Refrigerated_Warehouse": Column(int, Check.isin([0, 1])),
        "Use_K12_School": Column(int, Check.isin([0, 1])),
        "Use_Medical_Office": Column(int, Check.isin([0, 1])),
        "Use_Worship_Facility": Column(int, Check.isin([0, 1])),
        "Use_Unknown": Column(int, Check.isin([0, 1])),
    }
)


@bentoml.service(name="energy_prediction_service")
class EnergyService:

    @bentoml.api
    def ping(self) -> dict:
        return {"message": "Service is ready"}

    @bentoml.api
    def predict(self, input_data: EnergyInput) -> dict:
        data = pd.DataFrame([input_data.dict()])
        schema.validate(data)
        data = data.reindex(columns=FEATURE_COLUMNS, fill_value=0)
        prediction = model.predict(data)
        return {"prediction_kBtu": float(prediction[0])}
