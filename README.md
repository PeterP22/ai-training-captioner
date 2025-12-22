# LoRA Training Image Captioner

Auto-caption your training images using GPT-5 Mini for high-quality LoRA fine-tuning.

## Why Captions Matter

Good captions are critical for LoRA training because they:

- **Define your trigger word** — The token you use (e.g., `MYTRIGGER`) becomes the handle to activate your LoRA at inference
- **Focus learning on the right features** — Captions tell the model which attributes matter (clothing, pose, lighting) vs. what to ignore
- **Reduce overfitting** — Poor captions cause the model to memorize whole images instead of learning disentangled, reusable features
- **Control what gets learned** — Decide whether to learn style, subject, outfit, or everything

**Bad captions = unpredictable LoRA. Good captions = clean, controllable results.**

## Installation

```bash
pip install openai
export OPENAI_API_KEY=sk-your-key-here
```

## Usage

```bash
# Caption all images in a folder
python caption.py --folder ./my_photos --trigger MYTRIGGER

# Preview captions first (no files saved)
python caption.py --folder ./my_photos --trigger MYTRIGGER --preview

# Overwrite existing captions
python caption.py --folder ./my_photos --trigger MYTRIGGER --overwrite
```

## Output

Creates a `.txt` file next to each image:

```
my_photos/
  ├── photo1.jpg
  ├── photo1.txt  ← "a photo of MYTRIGGER, wearing a blue shirt..."
  ├── photo2.jpg
  ├── photo2.txt  ← "a photo of MYTRIGGER, standing outdoors..."
```

## Caption Format

Each caption follows this structure:

```
a photo of MYTRIGGER, [clothing], [pose/expression], [setting], [lighting], [photo style]
```

Example:
```
a photo of MYTRIGGER, wearing a fitted navy henley shirt, standing outdoors with arms crossed, confident relaxed expression, golden hour sunlight from the left, urban park background with blurred trees, candid lifestyle photography style
```

## Options

| Flag | Description |
|------|-------------|
| `--folder`, `-f` | Path to images folder (required) |
| `--trigger`, `-t` | Your trigger word (required) |
| `--model`, `-m` | OpenAI model (default: `gpt-5-mini`) |
| `--preview`, `-p` | Preview without saving |
| `--overwrite`, `-o` | Overwrite existing captions |

## Tips for Best Results

1. **Use 15-30 diverse images** — varied lighting, angles, expressions, outfits
2. **Pick a unique trigger word** — something that won't appear naturally (e.g., `XYZ_PERSON`)
3. **Review captions** — edit any that seem off before training
4. **Be consistent** — same trigger word format across all captions

## License

MIT
