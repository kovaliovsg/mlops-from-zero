from fastapi import FastAPI
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression

iris = load_iris()
model = LogisticRegression(max_iter=500).fit(iris.data, iris.target)
app = FastAPI(title="Flower Predictor")

@app.get("/predict")
def predict(sepal_length: float, sepal_width: float,
            petal_length: float, petal_width: float):
    flower = [[sepal_length, sepal_width, petal_length, petal_width]]
    return {"flower": str(iris.target_names[model.predict(flower)[0]])}
