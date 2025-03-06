extends Node

func _ready():
	# test to see if there's a connection to the database
	if Supabase:
		print("The connection to the database was successful. Connection URL: ", Supabase.config.supabaseUrl)
	else:
		print("The connection to the database failed.")
		get_tree().quit() #quits out of the program (for now)'
	
	create_scene("res://scenes/photo/photo.tscn")

func create_scene(scene_path: String):
	
	# path to the scene scene to load it into memory
	var scene = load(scene_path)
	
	# instantiate the scene
	var scene_instance = scene.instantiate()
	
	# adds the scene as an active child to whatever scene called it
	add_child(scene_instance)
