import uuid
import jsonlines

from datasets import load_dataset

DATASET_ID = "wangrongsheng/HealthCareMagic-100k-en"
OUTPUT_JSONL_PATH = "data/HealthCareMagic-3k-en.jsonl"

ds = load_dataset(DATASET_ID)

# print(ds.keys())
ift_dataset = []
count = 0 
for data in ds["train"]: # 3000 samples
    illness_description = data["input"] + "\n\n" + data["instruction"]
    doctor_response = data["output"]
    ift_dataset.append(
        {
            "prompt_id": str(uuid.uuid4()),
            "prompt": illness_description,
            "completion": doctor_response,
        }
    )
    count += 1
    if count % 1000 == 0:
        print(f"Processed {count} samples")
    if count == 3000:
        break

jsonlines.open(OUTPUT_JSONL_PATH, "w").write_all(ift_dataset)
