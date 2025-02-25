extends Node
class_name Photo

# some of this functionality should be implemented
# in photo manager, like delete photo, which should be re-written
# to create and delete a photo prefab. 

# also, this code can easily be implimented into the
# tag objecy.

# Properties for a photo record
var id: int = 0
var image_url: String = ""
var tags: Array = []  # List of tags (could be tag names or tag IDs)

# Variable to store callback function for texture loading
var texture_callback: Callable = Callable()

# Optional: Initialize a Photo object with values.
func _init(_id: int = 0, _image_url: String = "", _tags: Array = []):
	id = _id
	image_url = _image_url
	tags = _tags

# Create a Photo object from a dictionary returned by Supabase.
func from_dict(data: Dictionary) -> Photo:
	id = data.get("id", 0)
	image_url = data.get("image_url", "")
	tags = data.get("tags", [])
	return self

# Convert the Photo object into a dictionary for sending to Supabase.
func to_dict() -> Dictionary:
	return {
		"id": id,
		"image_url": image_url,
		"tags": tags
	}

# Save a new photo record to Supabase.
func save() -> void:
	var supabase = get_node("/root/SupabaseRequest")  # Adjust this path if needed
	var data = {
		"image_url": image_url,
		"tags": tags
	}
	supabase.request_supabase("/rest/v1/photo", HTTPClient.METHOD_POST, data)

# Update an existing photo record in Supabase.
func update() -> void:
	if id == 0:
		print("Photo ID is not set. Cannot update record.")
		return
	var supabase = get_node("/root/SupabaseRequest")
	var endpoint = "/rest/v1/photo?id=eq." + str(id)
	supabase.request_supabase(endpoint, HTTPClient.METHOD_PATCH, to_dict())

# Delete the photo record from Supabase.
func delete_photo() -> void:
	if id == 0:
		print("Photo ID is not set. Cannot delete record.")
		return
	var supabase = get_node("/root/SupabaseRequest")
	var endpoint = "/rest/v1/photo?id=eq." + str(id)
	supabase.request_supabase(endpoint, HTTPClient.METHOD_DELETE)

# Load the photo’s image from the given image_url as a texture.
func load_texture(callback: Callable) -> void:
	var http_request = HTTPRequest.new()
	add_child(http_request)

	# Store callback function for later use
	texture_callback = callback
	
	# Connect HTTPRequest's signal to the _on_texture_loaded function
	http_request.request_completed.connect(_on_texture_loaded)
	http_request.request(image_url)

# Callback for when the image download is complete.
func _on_texture_loaded(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var image = Image.new()
		if image.load_png_from_buffer(body) == OK:
			var texture = ImageTexture.new()
			texture.create_from_image(image)
			if texture_callback.is_valid():
				texture_callback.call(texture)
		else:
			print("Failed to create image from buffer.")
	else:
		print("Failed to load image. Response code: ", response_code)
