import joblib
import pandas as pd


def load_model(model_path, encoders_path):
    model = joblib.load(model_path)
    label_encoders = joblib.load(encoders_path)

    return model, label_encoders


def generate_dropdown_options(label_encoders, columns):
    dropdowns = {}

    for col in columns:
        if col in label_encoders:
            dropdowns[col] = list(label_encoders[col].classes_)

    return dropdowns


def make_prediction(model, label_encoders, user_input):
    input_df = pd.DataFrame([user_input])

    for col, encoder in label_encoders.items():
        if col in user_input:
            input_df[col] = encoder.transform(input_df[col])

    prediction = model.predict(input_df)
    predicted_variety = label_encoders["variety"].inverse_transform(prediction)

    return predicted_variety[0]


def display_metrics(metrics_path):
    metrics = pd.read_csv(metrics_path, sep="\t")

    return metrics
