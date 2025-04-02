import json
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import cosine_distances
import os

# 📥 Input embeddings
INPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/mean_embeddings.json"
# 📤 Output clustered IDs
OUTPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/dbscan_clusters.json"

# Բեռնում ենք embedding-ները
with open(INPUT_PATH, "r") as f:
    data = json.load(f)

ids = list(data.keys())
embeddings = np.array([data[i] for i in ids])

# Հաշվում ենք cosine հեռավորություններ
distance_matrix = cosine_distances(embeddings)

# 🤖 Կիրառում ենք DBSCAN՝ Cosine հեռավորության վրա
clustering = DBSCAN(eps=0.111, min_samples=1, metric="precomputed")
labels = clustering.fit_predict(distance_matrix)

# Պատրաստում ենք արդյունքը՝ ըստ խմբերի
clusters = {}
for idx, label in enumerate(labels):
    cluster_name = f"cluster_{label}"
    clusters.setdefault(cluster_name, []).append(ids[idx])

# Պահպանում ենք
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(clusters, f, indent=2)

print(f"✅ DBSCAN արդյունքը պահպանվեց՝ {OUTPUT_PATH}")
print(f"📦 Ստացվեց {len(clusters)} խումբ")
