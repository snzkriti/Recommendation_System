import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# FashionCLIP model (CLIP-based)
model = CLIPModel.from_pretrained("patrickjohncyh/fashion-clip")
processor = CLIPProcessor.from_pretrained("patrickjohncyh/fashion-clip")


def get_image_embedding(image_path, text):

    image = Image.open(image_path).convert("RGB")

    inputs = processor(
        text=[text],
        images=image,
        return_tensors="pt",
        padding=True
    )

    outputs = model(**inputs)

    # final embedding
    embedding = outputs.image_embeds + outputs.text_embeds

    return embedding[0].detach().numpy()


# -----------------------------
# BUILD TEXT
# -----------------------------
def build_text(row):
    return f"""
    {row['product_display_name']}
    {row['gender']}
    {row['master_category']}
    {row['sub_category']}
    {row['article_type']}
    {row['base_colour']}
    {row['season']}
    {row['usage']}
    """


# -----------------------------
# MAIN EMBEDDING LOOP
# -----------------------------
def run():

    res = supabase.table("products").select("*").execute()
    products = res.data

    print("Products:", len(products))

    for i, p in enumerate(products):

        try:
            image_path = p["image_path"]
            text = build_text(p)

            emb = get_image_embedding(image_path, text)

            supabase.table("embeddings").upsert({
                "product_id": p["id"],
                "embedding": emb.tolist()
            }).execute()

            if i % 100 == 0:
                print(f"Processed {i}")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    run()