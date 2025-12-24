import json
from PIL import Image
from torch.utils.data import Dataset

class MTGClipDataset(Dataset):
    def __init__(self, jsonl_path, image_transform, tokenizer):
        self.samples = []
        self.image_transform = image_transform
        self.tokenizer = tokenizer

        with open(jsonl_path, "r", encoding="utf-8") as f:
            for line in f:
                self.samples.append(json.loads(line))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]

        image = Image.open(item["image_path"]).convert("RGB")

        text = (
            f"Magic the Gathering card named {item['name']}. "
            f"Type: {item['type_line']}. "
            f"Rules text: {item['oracle_text']}"
        )

        image = self.image_transform(image)
        text = self.tokenizer(text)[0]

        return image, text
