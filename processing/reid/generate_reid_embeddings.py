import torch
import torchreid

# ✅ Օգտագործենք GPU եթե կա
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Using device: {device}")

# ✅ Բեռնում ենք pre-trained OSNet մոդելը
model = torchreid.models.build_model(
    name='osnet_x1_0',
    num_classes=1000,
    pretrained=True
)

model.eval()
model.to(device)

print("✅ Re-ID մոդելը բեռնված է ու պատրաստ է embedding գեներացնելու։")

import os
import json

from torchvision import transforms
from PIL import Image
import numpy as np
from tqdm import tqdm

# 📁 Input folder՝ ID-ներով դասավորված crop-եր
INPUT_DIR = "tests/reid_samples"
# 📁 Output folder՝ embedding-ների պահման համար
OUTPUT_DIR = "data/cache/warehouse_1/new_video/embeddings"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🧠 Torchvision transforms (նախամշակում մոդելի համար)
transform = transforms.Compose([
    transforms.Resize((256, 128)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# 📦 Արդյունքը՝ { "id_1": [embedding1, embedding2, ...], ... }
all_embeddings = {}

for id_folder in tqdm(os.listdir(INPUT_DIR), desc="🔍 Processing IDs"):
    id_path = os.path.join(INPUT_DIR, id_folder)
    if not os.path.isdir(id_path):
        continue

    embeddings = []
    for img_file in os.listdir(id_path):
        img_path = os.path.join(id_path, img_file)
        img = Image.open(img_path).convert("RGB")
        tensor = transform(img).unsqueeze(0).to(device)

        with torch.no_grad():
            emb = model(tensor)
        embeddings.append(emb.squeeze().cpu().numpy().tolist())

    all_embeddings[id_folder] = embeddings

# 💾 Պահում ենք որպես JSON
output_path = os.path.join(OUTPUT_DIR, "embeddings.json")
with open(output_path, "w") as f:
    json.dump(all_embeddings, f)

print(f"✅ Embedding-ները պահպանվեցին՝ {output_path}")

