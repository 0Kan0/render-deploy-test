import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML

path = Path.cwd() / "src\data"

df = pd.read_csv(path/"Dropout.csv", skipinitialspace=True)
df.set_index("StudentID", inplace=True)
#Reemplazo la variable objetivo con valores numericos
df["Target"] = df["Target"].replace({"Dropout": 0, "No dropout": 1})

#Divido el dataset 20% test y 80% entrenamiento
X_train, X_test, y_train, y_test = train_test_split(
    df[df.columns[:-1]], df["Target"], test_size=0.20
)

#Escoge el mejor modelo
model = AutoML(algorithms=["Baseline", "Linear", "Decision Tree", "Random Forest", "Extra Trees", "Xgboost", "LightGBM", "CatBoost", "Neural Network", "Nearest Neighbors"],
               start_random_models=1,
               train_ensemble=True,
               explain_level=2,
               validation_strategy={
                    "validation_type": "split",
                    "train_ratio": 0.80,
                    "shuffle" : True,
                    "stratify" : True,
               })

#Entreno el modelo
trained_model = model.fit(X_train, y_train)

#Genero el reporte (se usa en la pestaña AutoML Report)
model_report = trained_model.report()