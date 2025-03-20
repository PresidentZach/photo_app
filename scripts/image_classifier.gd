extends Node

var http_request: HTTPRequest

func _ready():
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.connect("request_completed", self, "_on_request_completed")

func classify_image(image_path):
	var file = File.new()
	if file.open(image_path, File.READ) == OK:
		var image_data = file.get_buffer(file.get_len())
		var headers = ["Content-Type: multipart/form-data"]
		
		var form_data = HTTPClient.new().multipart_form_data_create()
		HTTPClient.new().multipart_form_data_add_file(form_data, "file", image_path, image_data)

		http_request.request("http://localhost:8000/classify/", headers, false, HTTPClient.METHOD_POST, form_data)
	else:
		print("Failed to open image file.")

func _on_request_completed(result, response_code, headers, body):
	if response_code == 200:
		var json = JSON.parse(body.get_string_from_utf8())
		print("Tags: ", json.result.tags)
	else:
		print("Error in classification request")
