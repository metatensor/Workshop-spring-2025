# How to use 
```bash
python llpr.py --model_path=model-pet.pt --output-figure="ethanol_llpr_vs_true_error_pet.pdf"
```

```bash
mtt export https://huggingface.co/lab-cosmo/pet-mad/resolve/main/models/pet-mad-latest.ckpt
```

```bash
python llpr.py --model_path=pet-mad-latest.pt --output-figure="ethanol_llpr_vs_true_error_petmad.pdf"
```
