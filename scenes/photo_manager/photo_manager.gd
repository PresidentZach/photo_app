extends Node
const photo = preload("res://scenes/photo/photo.gd")  # Adjust the path to where your Photo.gd file is

var list_of_photos = []  # Stores all Photo objects

func _ready() -> void:
	return

func fetch_photos_from_database(user_id: String) -> void:
	var query = SupabaseQuery.new().from("photo").select("*").eq("photo_creator", user_id)
	var response = await Supabase.database.query(query)

	if response.success:
		list_of_photos.clear()  # Remove old entries
		for record in response.data:
			var photo_scene = photo.new()  # Create new photo object
			photo_scene.load_from_database(record)  # Load data from DB
			list_of_photos.append(photo_scene)

func add_photo_to_database(new_photo: photo) -> void:
	await new_photo.insert_to_database()  # Calls method in Photo class
	list_of_photos.append(new_photo)  # Add to global list

func update_photo_in_database(existing_photo: photo) -> void:
	await existing_photo.update_database()  # Calls method in Photo class

func delete_photo(photo_to_remove: photo) -> void:
	await photo_to_remove.delete_from_database()  # Calls method in Photo class
	list_of_photos.erase(photo_to_remove)
