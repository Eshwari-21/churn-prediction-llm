import pandas as pd
from model_loader import scaler, columns

def preprocess(data):
    df = pd.DataFrame([data])

    if "customer_id" in df.columns:
        df = df.drop("customer_id", axis=1)

    df = pd.get_dummies(df)

    df = df.reindex(columns=columns, fill_value=0)

    scaled = scaler.transform(df)

    return scaled[0]