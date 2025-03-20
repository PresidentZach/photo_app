extends Node

# NOTE photo oject only deals with itself and doesn't create itself in
# the database. Photo Manager creates photos in the database.

# NOTE I don't think the update function is working or the set functions maybe.
# also, make it so there's a function in photo manager that loops and creates all the photos in a global list. You don't need
# a dictionary because photos have Id's and stuff, or maybe you can use the id as the dictionary key? 

# make a way for the photo manager to create objects and insert the values. Get's list from database? 

# will add and update function do the same thing? 

# global variables of the photo with default values
var id: int = -1 # unique
var photo_url: String = "none" # unique
var date_created: String = "none" # nullable
var photo_creator: int = -1 
var tags: Array = ["none"] # nullable

# getter and setter methods that work
# 

func _ready() -> void:
	#print("📸 Creating photo entry in database...")
	#update_database()
	add_to_database("temporaryURL", 23445, [1, 2, 3])
	#set_photo_creator("test")
	print(calculate_date())
	# test for getter and setter functions
	#print(await get_photo_id())
	

func add_to_database(add_photo_url: String, add_photo_creator: int, add_tags: Array) -> void:
	
	# NOTE photo_id is decided by the database
	# date is determined by day photo is added to the database
	# verified_photo_tags is decided later
	
	# setting the global variables of this scene
	# photo id is set by the databa se
	photo_url = add_photo_url
	date_created = calculate_date()
	photo_creator = add_photo_creator
	tags = add_tags
	
	var query = SupabaseQuery.new().from("photo").insert([
		{
			# don't set the photo_id because the database does that
			"photo_url": photo_url,
			"date_created": date_created,
			"photo_creator": photo_creator
			#"tags": tags
		}
	])
	
	var response = await Supabase.database.query(query)
	id = await get_photo_id()

# assumes global values are updated before updating the photo in the database
func update_database() -> void:
	
	# if no photo exists in the database, create one. Otherwise, update the contents of the photo. 
	#if photo_date_created == 00000000: # if photo_date_created hasn't been initialized yet
	#	photo_date_created = calculate_date()
	
	var query = SupabaseQuery.new().from("photo").insert([
		{
			# don't set the photo_id because the database does that
			"photo_url": photo_url,
			"date_created": date_created,
			"photo_creator": photo_creator,
			"tags": tags
		}
	])
	
	var response = await Supabase.database.query(query)
	#photo_id = await get_photo_id()
	
	

func get_photo_id() -> int:
	
	# fetch the photo_id
	var query = SupabaseQuery.new().from("photo").select(["photo_id"]).eq("photo_url", photo_url)
	var response = await Supabase.database.query(query)
	#photo_id = response.data[0]["photo_id"] # Extract the first record's ID
	
	# TODO update photo id
	
	# return the photo_id
	return 20

# no method to set photo id because that is prohibited

func get_photo_url() -> String:
	# get the value from the database, set photo_url to it, and then return it? 
	
	return photo_url

func set_photo_url() -> void:
	return

func calculate_date() -> String:
	var computer_date = Time.get_datetime_dict_from_system()
	var month = str(computer_date.month).pad_zeros(2)
	var day = str(computer_date.day).pad_zeros(2)
	var year = str(computer_date.year)
	
	# Format: "MM / DD / YYYY"
	return month + " / " + day + " / " + year

func get_photo_creator() -> String:
	# update the photo to make sure all info is correct before returning it
	return ""

func set_photo_creator(new_photo_creator: String) -> void:
	if new_photo_creator.length() > 0:
		#photo_creator = new_photo_creator
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
