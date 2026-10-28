# ml/train_model.py
# Melatih Random Forest dan menyimpan model.
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

df = pd.read_csv('ml/dataset_sintetis.csv')
X = df.drop('label_layak', axis=1)
y = df['label_layak']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print('=== Classification Report ===')
print(classification_report(y_test, y_pred))
print('=== Confusion Matrix ===')
print(confusion_matrix(y_test, y_pred))

joblib.dump(model, 'ml/model_rf.pkl')
print('Model disimpan di ml/model_rf.pkl')