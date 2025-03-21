extends Node

# global variables of the photo with default values
var id: int = -1 # primary, unique
var name_: String = "no_name" # unique

func _ready() -> void:
	
	await update_self_in_database("tag_name_test")
	
	print(await get_id())
	print(await get_name())
	await set_name("new_tag_name_test")
	print(await get_name())

func update_self_in_database(update_name: String):
	
	# NOTE if this tag is not in the database, then it will be added
	# NOTE id is decided by the database
	
	# setting the global variables of this scene
	name_ = update_name
	
	var query = SupabaseQuery.new().from("tag").insert([
		{
			"name": name_
		}
	])
	
	var response = await Supabase.database.query(query)
	id = await get_id()

func get_id() -> int:
	var query = SupabaseQuery.new().from("tag").select(["id"]).eq("name", name_)
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		id = -1
		print("Supabase query error when fetching tag.id:", task.error.message)
		return id
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		id = int(task.data[0]["id"])
		return id
	
	# if all else fails
	id = -1
	print("No data returned when fetching tag.id.")
	return id
func get_name_() -> String:
	var query = SupabaseQuery.new().from("photo").select(["name"]).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		name_ = "no_name"
		print("Supabase query error when fetching tag.name:", task.error.message)
		return name_
	
	# if fetching was successful
	if task.data and task.data.size() > 0:
		name_ = task.data[0]["name"]
		return name_
	
	# if all else fails
	name_ = "no_name"
	print("No data returned when fetching tag.name.")
	return name_

func set_name_(new_name: String) -> void:
	
	# check to see if the id holds a value
	if id == -1:
		print("tag.id not set, so tag.name cannot be set.")
		return
	
	name_ = new_name # setting the global url
	var query = SupabaseQuery.new().from("tag").update({"name": name}).eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when fetching
	if task.error:
		print("Supabase query error when setting tag.name:", task.error.message)
		return

# delete this tag from the database
func remove_self_from_database() -> void:
	
	# check to see if the id holds a value
	if id == -1:
		print("tag.id not set, so this tag can't be deleted.")
		return
	
	var query = SupabaseQuery.new().from("tag").delete().eq("id", str(id))
	var task = Supabase.database.query(query)
	
	# connect signal to process response when query is done
	await task.completed
	
	# if there's an error when deleting the photo
	if task.error:
		print("Supabase query error when deleting tag of tag.id: ", id, " ", task.error.message)
		return
	
	print("Successfully deleted tag of tag.id: ", id)
