import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Charger les données
df = pd.read_csv("dataset_sms_analyzed.csv")
df = df.fillna(False)
print(df.describe())

# Features et target
features = ["url", "iban", "phone", "montant", "url_sentiment", "sentiment_detection", "data_base"]
target = "label"

X = df[features]
y = df[target]

# Cat features
cat_features = ["url_sentiment", "sentiment_detection"]

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création modèle CatBoost
model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.05,
    depth=6,
    loss_function="Logloss",
    eval_metric="Accuracy",
    random_seed=42,
    verbose=100
)

# Training
model.fit(X_train, y_train, cat_features=cat_features, eval_set=(X_test, y_test))

# Prédict
y_pred = model.predict(X_test)

# Test
print(classification_report(y_test, y_pred))


model.save_model("catboost.json")
if __name__ == "__main__":
    print("done")
    