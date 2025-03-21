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
var url: String = "no_url" # unique
var creator: int = -1 
var date_created: String = "no_date" # nullable
var tags: Array = [39909] # nullable

# methods that work
# add_to_database()
# calculate_date()
# getter methods
# setter methods
# delete_self_from_database()

func _ready() -> void:
	
	await add_to_database("testURL_afterSetMethod", 78915, [2, 3, 4])


func add_to_database(add_url: String, add_creator: int, add_tags: Array) -> void:
	
	# NOTE photo_id is decided by the database
	# date is determined by day photo is added to the database
	# verified_photo_tags is decided later
	
	# setting the global variables of this scene
	# photo id is set by the databa se
	url = add_url
	date_created = calculate_date()
	creator = add_creator
	tags = add_tags
	
	var query = SupabaseQuery.new().from("photo").insert([
		{
			# don't set the photo_id because the database does that
			"url": url,
			"creator": creator,
			"date_created": date_created,
			"tags": tags
		}
	])
	
	var response = await Supabase.database.query(query)
	id = await get_id()

func get_id() -> int:
	var query = SupabaseQuery.new().from("photo").select(["id"]).eq("url", url)
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		id = -1
		print("Supabase query error when fetching photo.id:", task.error.message)
		return id
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		id = int(task.data[0]["id"])
		return id
	
	# if all else fails
	id = -1
	print("No data returned when fetching photo.id.")
	return id
func get_url() -> String:
	var query = SupabaseQuery.new().from("photo").select(["url"]).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		url = "no_url"
		print("Supabase query error when fetching photo.url:", task.error.message)
		return url
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		url = task.data[0]["url"]
		return url
	
	# if all else fails
	url = "no_url"
	print("No data returned when fetching photo.url.")
	return url
func get_creator() -> int:
	var query = SupabaseQuery.new().from("photo").select(["creator"]).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		creator = -1
		print("Supabase query error when fetching photo.creator:", task.error.message)
		return creator
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		creator = int(task.data[0]["creator"])
		return creator
	
	# if all else fails
	creator = -1
	print("No data returned when fetching photo.creator.")
	return creator
func get_date_created() -> String:
	var query = SupabaseQuery.new().from("photo").select(["date_created"]).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		date_created = "no_date"
		print("Supabase query error when fetching photo.date_created:", task.error.message)
		return date_created
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		date_created = task.data[0]["date_created"]
		return date_created
	
	# if all else fails
	date_created = "no_date"
	print("No data returned when fetching photo.date_created.")
	return date_created
func get_tags() -> Array:
	var query = SupabaseQuery.new().from("photo").select(["tags"]).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		tags = [39909]
		print("Supabase query error when fetching photo.tags:", task.error.message)
		return tags
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		tags = Array(task.data[0]["tags"])
		return tags
	
	# if all else fails
	tags = [39909]
	print("No data returned when fetching photo.tags.")
	return tags

func set_url(new_url: String) -> void:
	
	# check to see if the id holds a value
	if id == -1:
		print("photo.id not set, so photo.url cannot be set.")
		return
	
	url = new_url # setting the global url
	var query = SupabaseQuery.new().from("photo").update({"url": url}).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		print("Supabase query error when setting photo.url:", task.error.message)
		return
func set_creator(new_creator: int) -> void:
	
	# check to see if the id holds a value
	if id == -1:
		print("photo.id not set, so photo.creator cannot be set.")
		return
	
	creator = new_creator # setting the global url
	var query = SupabaseQuery.new().from("photo").update({"creator": creator}).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		print("Supabase query error when setting photo.creator:", task.error.message)
		return
func set_tags(new_tags: Array) -> void:
	
	# check to see if the id holds a value
	if id == -1:
		print("photo.id not set, so photo.tags cannot be set.")
		return
	
	tags = new_tags # setting the global url
	var query = SupabaseQuery.new().from("photo").update({"tags": tags}).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		print("Supabase query error when setting photo.tags:", task.error.message)
		return

func calculate_date() -> String:
	var computer_date = Time.get_datetime_dict_from_system()
	var month = str(computer_date.month).pad_zeros(2)
	var day = str(computer_date.day).pad_zeros(2)
	var year = str(computer_date.year)
	
	# Format: "MM / DD / YYYY"
	return month + "-" + day + "-" + year

# delete this photo from the database
func delete_self_from_database() -> void:
	
	# check to see if the id holds a value
	if id == -1:
		print("photo.id not set, so the photo can't be deleted.")
		return
	
	var query = SupabaseQuery.new().from("photo").delete().eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when deleting the photo
	if task.error:
		print("Supabase query error when deleting photo of photo.id: ", id, " ", task.error.message)
		return
	
	print("Successfully deleted photo of photo.id: ", id)
