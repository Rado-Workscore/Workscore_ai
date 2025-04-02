import os
import json
import shutil

# 📥 Cluster տվյալների ուղին
CLUSTERS_PATH = "data/cache/warehouse_1/new_video/embeddings/dbscan_clusters.json"
# 📥 Crop-երի սկզբնադիր տեղը
CROPS_ROOT = "tests/reid_samples"
# 📤 Նոր պանակ՝ վիզուալ դասավորած ըստ cluster-ների
OUTPUT_ROOT = "data/visual_clusters"

# Բեռնում ենք cluster-ները
with open(CLUSTERS_PATH, "r") as f:
    clusters = json.load(f)

# Մաքրում ենք output պանակը (եթե կա)
if os.path.exists(OUTPUT_ROOT):
    shutil.rmtree(OUTPUT_ROOT)
os.makedirs(OUTPUT_ROOT, exist_ok=True)

# Դասավորում ենք ըստ cluster-ի
for cluster_name, id_list in clusters.items():
    cluster_dir = os.path.join(OUTPUT_ROOT, cluster_name)
    os.makedirs(cluster_dir, exist_ok=True)

    for track_id in id_list:
        id_dir = os.path.join(CROPS_ROOT, track_id)
        if not os.path.isdir(id_dir):
            print(f"⚠️ Չկա՝ {id_dir}")
            continue

        for fname in os.listdir(id_dir):
            src_path = os.path.join(id_dir, fname)
            dst_path = os.path.join(cluster_dir, f"{track_id}_{fname}")
            shutil.copy2(src_path, dst_path)

print(f"✅ Crop-երը դասավորվեցին ըստ cluster-ների՝ {OUTPUT_ROOT}")
