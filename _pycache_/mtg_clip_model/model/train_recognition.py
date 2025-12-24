import torch
import open_clip
from torch.utils.data import DataLoader
from tqdm import tqdm

from build_data import MTGClipDataset

def main():


    # ===============================
    # CONFIG
    # ===============================
    DATASET_PATH = r"C:\Users\pholl\OneDrive\Desktop\_pycache_\mtg_clip_model\data\processed\mtg_pairs.jsonl"
    BATCH_SIZE = 64
    EPOCHS = 5
    LR = 1e-5
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    # ===============================
    # MODEL
    # ===============================
    model, _, preprocess = open_clip.create_model_and_transforms(
        model_name="ViT-B-32",
        pretrained="openai"
    )
    tokenizer = open_clip.get_tokenizer("ViT-B-32")

    model = model.to(DEVICE)
    model.train()

    # ===============================
    # DATA
    # ===============================
    dataset = MTGClipDataset(
        jsonl_path=DATASET_PATH,
        image_transform=preprocess,
        tokenizer=tokenizer
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4,
        pin_memory=True
    )

    # ===============================
    # OPTIMIZER
    # ===============================
    optimizer = torch.optim.AdamW(model.parameters(), lr=LR)
    loss_fn = open_clip.loss.ClipLoss()

    # ===============================
    # TRAIN LOOP
    # ===============================
    for epoch in range(EPOCHS):
        total_loss = 0

        for images, texts in tqdm(loader, desc=f"Epoch {epoch+1}/{EPOCHS}"):
            images = images.to(DEVICE)
            texts = texts.to(DEVICE)

            optimizer.zero_grad()

            image_features = model.encode_image(images)
            text_features = model.encode_text(texts)

            # Normalize (important for CLIP)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)

            logit_scale = model.logit_scale.exp()

            loss = loss_fn(image_features, text_features, logit_scale)


            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(loader)
        print(f"Epoch {epoch+1} avg loss: {avg_loss:.4f}")

    # ===============================
    # SAVE MODEL
    # ===============================
    torch.save(model.state_dict(), "mtg_clip_finetuned.pt")
    print("Training complete. Model saved.")

if __name__ == "__main__":
    import torch.multiprocessing as mp
    mp.freeze_support()   # required on Windows
    main()
