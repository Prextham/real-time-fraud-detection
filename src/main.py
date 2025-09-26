# src/main.py

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from pathlib import Path # Import the Path library

# --- This is the new, robust pathing logic ---
# It finds the directory where main.py is located and looks for the model there.
BASE_DIR = Path(__file__).resolve().parent
# ---

# 1. Initialize the FastAPI app
app = FastAPI(title="Real-Time Fraud Detection API", version="1.0")

# 2. Load the trained model using the corrected path
model_path = BASE_DIR / "fraud_model.joblib"
model = joblib.load(model_path)
print("Model loaded successfully.")


# 3. Define the request body structure using Pydantic
class Transaction(BaseModel):
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    scaled_amount: float
    scaled_time: float

# 4. Create the prediction endpoint
@app.post("/predict")
def predict(transaction: Transaction):
    input_data = pd.DataFrame([transaction.dict()])
    prediction = model.predict(input_data)
    is_fraud = int(prediction[0])
    return {"is_fraud": is_fraud}

# This allows running the app from the root directory using `python src/main.py`
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)