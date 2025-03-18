extends Node

# NOTE I don't think the update function is working or the set functions maybe.
# also, make it so there's a function in photo manager that loops and creates all the photos in a global list. You don't need
# a dictionary because photos have Id's and stuff, or maybe you can use the id as the dictionary key? 

# make a way for the photo manager to create objects and insert the values. Get's list from database? 

# will add and update function do the same thing? 

var photo_id: int = -1 # should be a unique value; not shared with any other photo
# defaults to -1 because database assigns 1+ as an id, so -1 means it's not in the database and so hasn't been assigned an id
var photo_url: String # should be a unique value; not shared with any other photo
var photo_date_created: int = 00000000
var photo_creator: String
var verified_tags: bool
var tags: Array

# getter and setter methods that work
# 

func _ready() -> void:
	print("📸 Creating photo entry in database...")
	update_database("https://thisIsATestForAlex.jpg", "testForAlex3/16/25", false, [3, 16, 2025])
	#set_photo_creator("test")
	
	# test for getter and setter functions
	get_photo_id()
	

func update_database(new_photo_url: String, new_photo_creator: String, new_verified_tags: bool, new_tags: Array) -> void:
	
	# if no photo exists in the database, create one. Otherwise, update the contents of the photo. 
	
	# setting the photo's creation date
	if photo_date_created == 00000000: # if photo_date_created hasn't been initialized yet
		photo_date_created = get_date()
	
	var query = SupabaseQuery.new().from("photo").insert([
		{
			# don't set the photo_id because the database does that
			"photo_url": new_photo_url,
			"photo_date_created": photo_date_created,
			"photo_creator": new_photo_creator,
			"verified_tags": new_verified_tags,
			"tags": new_tags
		}
	])
	
	# assigning the global variables of the photo scene the new / updated values
	photo_id = await get_photo_id()
	photo_url = new_photo_url
	photo_creator = new_photo_creator
	verified_tags = new_verified_tags
	tags = new_tags
	
	var response = await Supabase.database.query(query)

func get_photo_id() -> int:
	
	# fetch the photo_id
	var query = SupabaseQuery.new().from("photo").select(["photo_id"]).eq("photo_url", photo_url)
	var response = await Supabase.database.query(query)
	
	# return the photo_id
	return photo_id

# no method to set photo id because that is prohibited

func get_photo_url() -> String:
	# get the value from the database, set photo_url to it, and then return it? 
	
	return photo_url

func set_photo_url() -> void:
	return

func get_date() -> int:
	
	# this method doesn't actually get the date of the photo, it get's the current date 
	# on the device you're using when the photo is being created.
	
	var computer_date = Time.get_datetime_dict_from_system()
	
	# Extract month, day, and year
	#var month = str(date.month).pad_zeros(2)
	#var day = str(date.day).pad_zeros(2)
	#var year = str(date.year)
	
	var date = 00000000 # formatted MMDDYYYY
	return date

func get_photo_creator() -> String:
	# update the photo to make sure all info is correct before returning it
	return photo_creator

func set_photo_creator(new_photo_creator: String) -> void:
	if new_photo_creator.length() > 0:
		photo_creator = new_photo_creator
		print("photo_creator set for ", photo_url)
	else:
		print("Failed to set photo_creator for ", photo_url)

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

func delete() -> void:
	return
