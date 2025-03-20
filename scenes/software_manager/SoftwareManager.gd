extends Control  # Ensure your script extends Control if it's your root node

var uploadButton: Button
var imageDisplay: TextureRect
var tagsLabel: Label
var fileDialog: FileDialog

func _ready():
	print("hi")
	uploadButton = $uploadButton
	imageDisplay = $imageDisplay
	tagsLabel = $tagsLabel
	fileDialog = $FileDialog

	
	# Connect the signals
	if uploadButton:
		uploadButton.connect("pressed", Callable(self, "_on_upload_button_pressed"))
		print("Connected upload button signal")
		fileDialog.connect("file_selected", Callable(self, "_on_file_selected"))

func _on_upload_button_pressed():
	print("Upload button pressed")
	fileDialog.popup_centered()

func _on_file_selected(file_path: String):
	load_image(file_path)
	
func load_image(file_path: String):
	var image = Image.new()
	var error = image.load(file_path)

	if error == OK:
		var texture = ImageTexture.new()
		texture.create_from_image(image)
		imageDisplay.texture = texture
		tagsLabel.text = "Image loaded successfully!"
	else:
		tagsLabel.text = "Failed to load image."
