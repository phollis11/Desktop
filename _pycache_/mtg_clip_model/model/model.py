import open_clip
import torch

def load_clip(device):
    model, preprocess, tokenizer = open_clip.create_model_and_transforms(
        "ViT-B-32",
        pretrained="openai"
    )
    model = model.to(device)
    return model, preprocess, tokenizer
