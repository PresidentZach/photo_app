from app.supabase_client import supabase

class Tag:
    def __init__(self, name: str, id: int = -1):
        self.id = id
        self.name = name
        if self.id == -1:
            self.get_id() 

    def insert_into_database(self):
        data = {
            "name": self.name,
        }
        try:
            result = supabase.table("tag").insert(data).execute()
            print("Inserted tag:", result.data)
            self.id = self.get_id()
        except Exception as e:
            print("Failed to insert tag:", e)

    def get_id(self):
        try:
            result = supabase.table("tag").select("id").eq("name", self.name).execute()
            if result.data and len(result.data) > 0:
                self.id = result.data[0]["id"]
                return self.id
        except Exception as e:
            print("Error fetching tag ID:", e)
        return -1

    def set_name(self, new_name):
        if self.id == -1:
            print("tag.id not set, so tag.name cannot be updated.")
            return
        try:
            supabase.table("tag").update({"name": new_name}).eq("id", self.id).execute()
            self.name = new_name
        except Exception as e:
            print("Error updating tag name:", e)

    def delete(self):
        if self.id == -1:
            print("tag.id not set, can't delete tag.")
            return
        try:
            supabase.table("tag").delete().eq("id", self.id).execute()
            print(f"Deleted tag '{self.name}' with id {self.id}")
        except Exception as e:
            print("Error deleting tag:", e)

    def print_info(self):
        print(f"Tag ID: {self.id}")
        print(f"Tag Name: {self.name}")
