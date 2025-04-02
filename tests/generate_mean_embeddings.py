import os
import json
import numpy as np

# 📥 Input embedding ֆայլ
INPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/embeddings.json"
# 📤 Output ֆայլ՝ միջին embedding-ներով
OUTPUT_PATH = "data/cache/warehouse_1/new_video/embeddings/mean_embeddings.json"

# Բեռնում ենք բոլոր embedding-ները
with open(INPUT_PATH, "r") as f:
    all_embeddings = json.load(f)

# Հաշվում ենք միջինը յուրաքանչյուր ID-ի համար
mean_embeddings = {}
for track_id, vectors in all_embeddings.items():
    arr = np.array(vectors)
    mean = np.mean(arr, axis=0)
    mean_embeddings[track_id] = mean.tolist()

# Պահպանում ենք նոր ֆայլ
with open(OUTPUT_PATH, "w") as f:
    json.dump(mean_embeddings, f)

print(f"✅ Միջին embedding-ները պահվեցին՝ {OUTPUT_PATH}")
