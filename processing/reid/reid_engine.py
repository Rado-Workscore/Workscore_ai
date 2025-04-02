import os
import json

class ReIDEngine:
    def __init__(self, warehouse_id: str):
        config_path = os.path.join("data", "warehouses", warehouse_id, "config", "reid.json")
        with open(config_path, "r") as f:
            self.config = json.load(f)
        
        self.model_path = self.config.get("embedding_model")
        self.max_cosine_distance = self.config.get("max_cosine_distance", 0.5)
        self.nn_budget = self.config.get("nn_budget", 100)
        self.normalize = self.config.get("normalize", True)
        self.reid_threshold = self.config.get("reid_threshold", 0.5)
