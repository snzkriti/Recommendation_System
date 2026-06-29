import os
import requests
import tempfile

from PIL import Image
from dotenv import load_dotenv
from transformers import CLIPProcessor, CLIPModel
from supabase import create_client
# this is a very heavy code, don't touch!

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)



model = CLIPModel.from_pretrained(
    "patrickjohncyh/fashion-clip"
)

processor = CLIPProcessor.from_pretrained(
    "patrickjohncyh/fashion-clip"
)


def download_image(url):

    r = requests.get(url)

    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    )

    temp.write(r.content)
    temp.close()

    return temp.name


rows = supabase.table(
    "trend_data"
).select("*").execute().data


for trend in rows:

    image_path = download_image(
        trend["image_url"]
    )

    image = Image.open(
        image_path
    ).convert("RGB")

    inputs = processor(
        text=[trend["description"]],
        images=image,
        return_tensors="pt",
        padding=True
    )

    outputs = model(**inputs)

    embedding = (
        outputs.image_embeds
        + outputs.text_embeds
    )

    vector = embedding[
        0
    ].detach().numpy().tolist()

    supabase.table(
        "trend_embeddings"
    ).insert({
        "trend_id": trend["id"],
        "embedding": vector
    }).execute()

    print("Embedded:", trend["keyword"])