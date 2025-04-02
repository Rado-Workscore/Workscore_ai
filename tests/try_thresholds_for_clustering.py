import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# 📥 Input embeddings
INPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/mean_embeddings.json"

# Բեռնում ենք embedding-ները
with open(INPUT_PATH, "r") as f:
    data = json.load(f)

ids = list(data.keys())
embeddings = np.array([data[i] for i in ids])

# Փորձում ենք տարբեր thresholds
print("🔍 Testing thresholds...")
for threshold in np.arange(0.5, 10.5, 0.5):
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=threshold
    )
    labels = clustering.fit_predict(embeddings)
    num_clusters = len(set(labels))
    print(f"Threshold = {threshold:.1f} → {num_clusters} խմբեր")
