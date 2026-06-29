
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Use cleaned dataset
df = pd.read_csv("cleaned_styles.csv")
df = df.fillna("")

print("Rows found:", len(df))

records = []

for _, row in df.iterrows():

    try:
        year_value = None
        if str(row["year"]).strip() != "":
            year_value = int(float(row["year"]))

        records.append({
            "id": int(row["id"]),
            "gender": row["gender"],
            "master_category": row["masterCategory"],
            "sub_category": row["subCategory"],
            "article_type": row["articleType"],
            "base_colour": row["baseColour"],
            "season": row["season"],
            "year": year_value,
            "usage": row["usage"],
            "product_display_name": row["productDisplayName"],
            "image_path": f"images/{row['id']}.jpg"
        })

    except Exception as e:
        print("Skipping row:", e)

print("Prepared:", len(records))

BATCH_SIZE = 500
success = 0

for i in range(0, len(records), BATCH_SIZE):

    batch = records[i:i+BATCH_SIZE]

    try:
        res = supabase.table("products").insert(batch).execute()

        success += len(batch)
        print(f"Uploaded {success}/{len(records)}")

    except Exception as e:
        print("Batch error:", e)

print("UPLOAD COMPLETE")