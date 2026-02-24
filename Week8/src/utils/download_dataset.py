from datasets import load_dataset

# Alpaca dataset (already instruction-tuning format)
dataset = load_dataset("tatsu-lab/alpaca")

print(dataset)

dataset.save_to_disk("raw_data/alpaca")
