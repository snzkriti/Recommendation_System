from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

test = {
    "id": 999999,
    "gender": "Test",
    "master_category": "Test",
    "sub_category": "Test",
    "article_type": "Test",
    "base_colour": "Red",
    "season": "Summer",
    "year": 2024,
    "usage": "Casual",
    "product_display_name": "Test Product",
    "image_path": "images/test.jpg"
}

res = supabase.table("products").insert(test).execute()

print(res)