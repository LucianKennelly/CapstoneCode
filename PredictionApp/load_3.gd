extends Button

@onready var my_popup = $"../../Popupwindow" # Use % instead of $ for autoloaded scenes

func _ready():
	# Use Callable() for connecting signals in Godot 4
	pressed.connect(_on_button_pressed)

func _on_button_pressed():
	my_popup.popup_centered()  # Show the popup in the center


func _on_close_button_pressed() -> void:
	pass # Replace with function body.
