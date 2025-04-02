import json
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import os

# 📥 Input path
INPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/mean_embeddings.json"
# 📤 Output path
OUTPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/clusters.json"

# 📦 Բեռնում ենք միջին embedding-ները
with open(INPUT_PATH, "r") as f:
    mean_embeddings = json.load(f)

# Փոխում ենք dict → list ձևաչափ՝ clustering-ի համար
id_list = list(mean_embeddings.keys())
embedding_matrix = np.array([mean_embeddings[id_] for id_ in id_list])

# 🤝 Կիրառում ենք Agglomerative Clustering
clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=5.0)
cluster_labels = clustering.fit_predict(embedding_matrix)

# 📦 Պատրաստում ենք նոր dict՝ ըստ խմբերի
clusters = {}
for idx, label in enumerate(cluster_labels):
    cluster_name = f"cluster_{label}"
    if cluster_name not in clusters:
        clusters[cluster_name] = []
    clusters[cluster_name].append(id_list[idx])

# 💾 Պահպանում ենք արդյունքը
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(clusters, f, indent=2)

print(f"✅ ID-ները դասավորվեցին {len(clusters)} խմբի մեջ։ Արդյունքը՝ {OUTPUT_PATH}")
