# MTG-CLIP

Fine-tuned CLIP model for recognizing Magic: The Gathering cards from artwork.

## Pipeline
1. Download Scryfall bulk data
2. Build (image, text) dataset
3. Fine-tune CLIP with contrastive learning
4. Retrieve card identity from image

## Train
python src/train.py
