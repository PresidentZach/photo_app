extends Node

const SUPABASE_URL = "https://aiglsybtzbvindkwxzph.supabase.co"
const API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFpZ2xzeWJ0emJ2aW5ka3d4enBoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg3MDI2NjUsImV4cCI6MjA1NDI3ODY2NX0.NaHQc4gkyP0RplgjAORuLFuMk0z0trP7BV608mJx5pw"

@onready var http_request = get_node("supabase_request")  # Reference HTTPRequest node

# Function to make API requests
func request_supabase(endpoint: String, method: int, data: Dictionary = {}):
	var headers = ["apikey: " + API_KEY, "Content-Type: application/json"]
	var body = "" if data.is_empty() else JSON.stringify(data)
	
	http_request.request(SUPABASE_URL + endpoint, headers, method, body)
	http_request.request_completed.connect(_on_request_completed)  # Fixed callable error

# Handle API responses
func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray):
	var response_text = body.get_string_from_utf8()
	print("Response Code: ", response_code)
	print("Response: ", response_text)

func _ready() -> void:
	request_supabase("/rest/v1/photo", HTTPClient.METHOD_GET)
