"""Checkpoint for A model in a box. Runs inside the container: docker exec flower python checkpoint.py
It asks the served model the two questions from the video and needs nothing installed on your machine."""
import json
from urllib.request import urlopen

BASE = "http://localhost:8000/predict"
small = json.load(urlopen(f"{BASE}?sepal_length=5.1&sepal_width=3.5&petal_length=1.4&petal_width=0.2"))
big = json.load(urlopen(f"{BASE}?sepal_length=6.7&sepal_width=3.0&petal_length=5.2&petal_width=2.3"))
print("small flower:", small["flower"])
print("big flower:  ", big["flower"])
ok = small["flower"] == "setosa" and big["flower"] == "virginica"
print("CHECKPOINT OK" if ok else "CHECKPOINT FAILED")
