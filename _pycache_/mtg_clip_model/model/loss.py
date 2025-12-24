import torch
import torch.nn.functional as F

def clip_contrastive_loss(img_feat, txt_feat, temperature=0.07):
    img_feat = F.normalize(img_feat, dim=1)
    txt_feat = F.normalize(txt_feat, dim=1)

    logits = img_feat @ txt_feat.T / temperature
    labels = torch.arange(len(logits), device=logits.device)

    loss_i = F.cross_entropy(logits, labels)
    loss_t = F.cross_entropy(logits.T, labels)

    return (loss_i + loss_t) / 2
