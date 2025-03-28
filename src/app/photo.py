from datetime import datetime
from supabase_client import supabase  # adjust import if needed

def insert_photo():
    # Example test photo data
    data = {
        "url": "textURL.com",
        "creator": 827364,  # Use an actual user ID if you have auth set up
        "tags": [123, 234],  # Match your DB field type
        "date_created": str(datetime.utcnow().isoformat())
    }

    try:
        result = supabase.table("photo").insert(data).execute()
        print("Inserted photo:", result.data)
    except Exception as e:
        print("Failed to insert photo:", e)

if __name__ == "__main__":
    insert_photo()
