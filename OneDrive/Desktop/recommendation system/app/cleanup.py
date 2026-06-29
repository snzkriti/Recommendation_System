import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

print("Deleting recommendations...")
supabase.table("recommendations").delete().neq("id", 0).execute()

print("Deleting trend embeddings...")
supabase.table("trend_embeddings").delete().neq("id", 0).execute()

print("Deleting trend data...")
supabase.table("trend_data").delete().neq("id", 0).execute()

print("Cleanup complete.")