from supabase_client import supabase
from datetime import datetime

class Photo:
    def __init__(self, url="no_url", creator="no_creator", tags=None):
        self.id = -1
        self.url = url
        self.creator = creator
        self.date_created = self.calculate_date()
        self.tags = tags if tags else [39909]

    def calculate_date(self):
        # Format: "MM-DD-YYYY"
        return datetime.now().strftime("%m-%d-%Y")

    def insert_into_database(self):
        data = {
            "url": self.url,
            "creator": self.creator,
            "date_created": self.date_created,
            "tags": self.tags
        }
        try:
            result = supabase.table("photo").insert(data).execute()
            print("Inserted photo:", result.data)
            self.id = self.get_id()
        except Exception as e:
            print("Failed to insert photo:", e)

    def get_id(self):
        try:
            result = supabase.table("photo").select("id").eq("url", self.url).execute()
            if result.data and len(result.data) > 0:
                self.id = result.data[0]["id"]
                return result.data[0]["id"]
        except Exception as e:
            print("Error fetching photo ID:", e)
        return -1

    def get_url(self):
        return self._fetch_field("url")

    def get_creator(self):
        return self._fetch_field("creator")

    def get_date_created(self):
        return self._fetch_field("date_created")

    def get_tags(self):
        return self._fetch_field("tags")

    def _fetch_field(self, field_name):
        if self.id == -1:
            print(f"photo.id not set, so photo.{field_name} cannot be fetched.")
            return None
        try:
            result = supabase.table("photo").select(field_name).eq("id", self.id).execute()
            if result.data and len(result.data) > 0:
                return result.data[0][field_name]
        except Exception as e:
            print(f"Error fetching photo.{field_name}:", e)
        return None

    def set_url(self, new_url):
        self._update_field("url", new_url)

    def set_creator(self, new_creator):
        self._update_field("creator", new_creator)

    def set_tags(self, new_tags):
        self._update_field("tags", new_tags)

    def _update_field(self, field_name, new_value):
        if self.id == -1:
            print(f"photo.id not set, so photo.{field_name} cannot be set.")
            return
        try:
            supabase.table("photo").update({field_name: new_value}).eq("id", self.id).execute()
            setattr(self, field_name, new_value)
        except Exception as e:
            print(f"Error updating photo.{field_name}:", e)

    def print_info(self):
        print("photo.id: ", self.get_id())
        print("photo.url: ", self.get_url())
        print("photo.creator: ", self.get_creator())
        print("photo.data_created: ", self.get_date_created())
        print("photo.tags: ", self.get_tags())

    def remove_from_database(self):
        if self.id == -1:
            print("photo.id not set, so this photo can't be deleted.")
            return
        try:
            supabase.table("photo").delete().eq("id", self.id).execute()
            print("Successfully deleted photo with id:", self.id)
        except Exception as e:
            print("Error deleting photo:", e)

# Example usage
if __name__ == "__main__":

    # example of creating a photo object
    #             url of the photo          creator id        tag id array
    photo = Photo("testURL_afterSetMethod", "78915398457983", [2, 3, 4])

    photo.insert_into_database()

    '''
    NOTE: While you technically CAN get the photo id using photo.id, please
    use photo.get_id(), which will properly fetch from the database. 
    print(photo.id) # incorrect! Just get's the id value in the photo class and not from the database.
    print("photo.id: ", photo.get_id()) # correct :)
    '''
    
    photo.print_info()
