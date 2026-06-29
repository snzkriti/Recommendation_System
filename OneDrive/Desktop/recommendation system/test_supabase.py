from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

result = supabase.table("products").select("id").limit(1).execute()

print("Connected Successfully!")
print(result.data)