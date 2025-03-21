extends Node

func _ready():
	
	# test if connection is successful
	database_connection_test()
	
	# create a test photo scene
	#create_scene("res://scenes/photo/photo.tscn")
	create_scene("res://scenes/tag/tag.tscn")

func database_connection_test() -> bool:
	
	# test to see if there's a connection to the database
	
	if Supabase:
		print("The connection to the database was successful. Connection URL: ", Supabase.config.supabaseUrl)
		return true
	else:
		print("The connection to the database failed.")
		return false
		get_tree().quit() # quits out of the program

func create_scene(scene_path: String):
	
	# path to the scene scene to load it into memory
	var scene = load(scene_path)
	
	# instantiate the scene
	var scene_instance = scene.instantiate()
	
	# adds the scene as an active child to whatever scene called it
	add_child(scene_instance)
