import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder


merged_file = '../../data/03_final/merged_files.tsv'
final_df = pd.read_csv(merged_file, sep='\t')

label_encoders = {}

for column in final_df.columns:
    if final_df[column].dtype == 'object':
        le = LabelEncoder()
        final_df[column] = le.fit_transform(final_df[column])
        label_encoders[column] = le

X = final_df.drop(columns=['variety'])
y = final_df['variety']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42, n_estimators=100)
model.fit(X_train, y_train)

joblib.dump(model, 'random_forest_model.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
classification_report_str = classification_report(y_test, y_pred, output_dict=False)
classification_report_dict = classification_report(y_test, y_pred, output_dict=True)
confusion_matrix_result = confusion_matrix(y_test, y_pred)

metrics = {
    'Metric': ['Accuracy'],
    'Value': [accuracy]
}

for key, value in classification_report_dict.items():
    if isinstance(value, dict):
        metrics['Metric'].append(f"{key} precision")
        metrics['Value'].append(value['precision'])
        metrics['Metric'].append(f"{key} recall")
        metrics['Value'].append(value['recall'])
        metrics['Metric'].append(f"{key} f1-score")
        metrics['Value'].append(value['f1-score'])

metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv('metrics.tsv', sep='\t', index=False)
