import os
from dotenv import load_dotenv
from supabase import create_client
from unsplash_fetch import get_unsplash_data

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)



TREND_KEYWORDS = [
    "cargo pants",
    "oversized hoodie",
    "streetwear",
    "linen shirt",
    "denim jacket"
]

for keyword in TREND_KEYWORDS:

    trend = get_unsplash_data(keyword)

    if trend:

        supabase.table("trend_data").insert({
            "keyword": trend["keyword"],
            "image_url": trend["image_url"],
            "description": trend["description"]
        }).execute()

        print("Saved:", keyword)