import pickle
import os

def load_model():
    base = os.path.dirname(__file__)

    model = pickle.load(open(os.path.join(base, "../models/churn_model.pkl"), "rb"))
    scaler = pickle.load(open(os.path.join(base, "../models/scaler.pkl"), "rb"))
    columns = pickle.load(open(os.path.join(base, "../models/columns.pkl"), "rb"))

    return model, scaler, columns