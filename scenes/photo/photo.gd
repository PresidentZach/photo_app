extends Node
class_name Photo

# Notes:
# - When you create a new Photo, it automatically saves itself to Supabase.
# - You can only set the ID once (first time the object is created).
# - Updating the image URL or tags automatically updates the database.

var id: int = 0
var image_url: String = ""
var tags: Array = []

# Reference to Supabase node
var supabase: Node

# Constructor - Creates a photo object
func _init(_id: int = 0, _image_url: String = "", _tags: Array = []) -> void:
	id = _id
	image_url = _image_url
	tags = _tags

# Once the node is in the scene tree, find Supabase and save if necessary
func _ready() -> void:
	print("✅ Photo _ready() called!")

	# Find SupabaseRequest node dynamically
	var root = get_tree().root
	var software_manager = root.find_child("SoftwareManager", true, false)

	if software_manager:
		supabase = software_manager.find_child("SupabaseRequest", true, false)
		if supabase:
			print("✅ SupabaseRequest found!")
		else:
			print("❌ ERROR: SupabaseRequest NOT found! Check node name.")
	else:
		print("❌ ERROR: SoftwareManager NOT found! Is it your main scene?")

	# Only call save() if Supabase is found
	if image_url != "" and supabase:
		print("✅ Calling save() because image_url exists!")
		save()

# Setter for ID (Shouldn't be changed after creation)
func set_id(new_id: int) -> void:
	if id == 0:  # Only allow setting if ID is not already assigned
		id = new_id
	else:
		print("❌ ERROR: Cannot change an existing photo ID.")

# Getter for ID
func get_id() -> int:
	return id

# Setter for Image URL
func set_image_url(new_url: String) -> void:
	image_url = new_url
	update_photo()

# Getter for Image URL
func get_image_url() -> String:
	return image_url

# Setter for Tags
func set_tags(new_tags: Array) -> void:
	tags = new_tags
	update_photo()

# Getter for Tags
func get_tags() -> Array:
	return tags

# Save a new photo to the database
func save() -> void:
	if supabase:
		var data = {
			"image_url": image_url,
			"tags": tags
		}
		print("🛠️ Sending data to Supabase:", JSON.stringify(data))
		supabase.request_supabase("/photos", HTTPClient.METHOD_POST, data)
	else:
		print("❌ ERROR: Supabase node not found. Save operation failed.")

# Update the photo in the database (ID must exist)
func update_photo() -> void:
	if id == 0:
		print("❌ ERROR: Photo ID is not set. Cannot update.")
		return
	var endpoint = "/photos?id=eq." + str(id)
	supabase.request_supabase(endpoint, HTTPClient.METHOD_PATCH, {"image_url": image_url, "tags": tags})
