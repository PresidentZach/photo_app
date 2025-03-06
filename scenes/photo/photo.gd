extends Node

# NOTE I don't think the update function is working or the set functions maybe.

var photo_id: int = -1 # should be a unique value; not shared with any other photo
# defaults to -1 because database assigns 1+ as an id, so -1 means it's not in the database and so hasn't been assigned an id
var photo_url: String # should be a unique value; not shared with any other photo
var photo_creator: String
var verified_tags: bool
var tags: Array

func _ready() -> void:
	print("📸 Creating photo entry in database...")
	add_photo_to_database("https://example.com/sample2.jpg", "Alex Scalcione", false, [1, 37, 20])
	set_photo_creator("Zachary Stofko")

func add_photo_to_database(new_photo_url: String, new_photo_creator: String, new_verified_tags: bool, new_tags: Array):
	
	# assign the values to the photo variables
	
	# check if photo_url already exists
	
	photo_url = new_photo_url
	photo_creator = new_photo_creator
	verified_tags = new_verified_tags
	tags = new_tags
	
	var query = SupabaseQuery.new().from("photo").insert([
		{
			# don't set the photo_id because the database does that
			"photo_url": photo_url,
			"photo_creator": photo_creator,
			"verified_tags": verified_tags,
			"tags": tags
		}
	])
	
	photo_id = await get_photo_id()
	
	var response = await Supabase.database.query(query)

func get_photo_id() -> int:
	
	# fetch the photo_id
	var query = SupabaseQuery.new().from("photo").select(["photo_id"]).eq("photo_url", photo_url)
	var response = await Supabase.database.query(query)
	
	# return the photo_id
	return photo_id

func set_photo_id(new_photo_id) -> void:
	
	var existing_ids = await get_existing_photo_ids()
	if new_photo_id in existing_ids:
		photo_id = new_photo_id
		update_photo()
		print("")
	else:
		print("Failed to set photo_creator for ", photo_url)

func get_photo_url() -> String:
	# update the photo to make sure all info is correct before returning it
	update_photo()
	return photo_url

func get_photo_creator() -> String:
	# update the photo to make sure all info is correct before returning it
	update_photo()
	return photo_creator

func set_photo_creator(new_photo_creator: String) -> void:
	if new_photo_creator.length() > 0:
		photo_creator = new_photo_creator
		update_photo()
		print("photo_creator set for ", photo_url)
	else:
		print("Failed to set photo_creator for ", photo_url)

func update_photo():
	
	# var photo_id = get_photo_id()
	
	#if photo_id == -1:
	#	print("Failed to update photo in database for ", photo_url)
	#	return
	
	var query = SupabaseQuery.new().from("photo").update({
		# don't set the photo_id because the database does that
		"photo_url": photo_url,
		"photo_creator": photo_creator,
		"verified_tags": verified_tags,
		"tags": tags
	}).eq("photo_id", str(photo_id))
	
	var response = await Supabase.database.query(query)
	
	return

func get_existing_photo_ids() -> Array:
	
	# list we will update with all the existing photo ids to see if a photo exists in the database
	var query = SupabaseQuery.new().from("photo").select(["photo_id"])
	var response = await Supabase.database.query(query)
	
	if response.success:
		var photo_ids = []
		for record in response.data:
			photo_ids.append(record.photo_id)
		return photo_ids
	
	return []

func get_existing_photo_urls() -> Array:
	
	# list we will update with all the existing photo ids to see if a photo exists in the database
	var query = SupabaseQuery.new().from("photo").select(["photo_url"])
	var response = await Supabase.database.query(query)
	
	if response.success:
		var photo_urls = []
		for record in response.data:
			photo_urls.append(record.photo_url)
		return photo_urls
	
	return []
