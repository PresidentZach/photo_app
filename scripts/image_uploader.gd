extends Node

# URL of your FastAPI server
const API_URL = "http://127.0.0.1:8000/classify/"

# Function to upload an image
func upload_image(image_path: String):
	var file = File.new()
	if file.file_exists(image_path):
		file.open(image_path, File.READ)
		var image_data = file.get_buffer(file.get_len())
		file.close()

		var http_request = HTTPRequest.new()
		add_child(http_request)

		# Connect the request_completed signal to a function
		http_request.connect("request_completed", self, "_on_request_completed")

		# Make a POST request to upload the image
		var err = http_request.request(API_URL, image_data, true, HTTPClient.METHOD_POST, ["Content-Type: application/octet-stream"])
		if err != OK:
			print("Error sending request: ", err)
	else:
		print("File does not exist.")

# Callback function for when the request is completed
func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var response = JSON.parse(body.get_string_from_utf8())
		if response.error == OK:
			print("Tags received: ", response.result["results"])
		else:
			print("Error parsing response: ", response.error)
	else:
		print("Request failed with code: ", response_code)

# Function to call when you want to upload an image
func _on_upload_button_pressed():
	var image_path = "res://path_to_your_image.png"  # Update with the path to your image
	upload_image(image_path)
