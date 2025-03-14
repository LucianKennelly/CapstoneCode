extends Button

@onready var my_popup = get_parent()  # Get the PopupPanel parent

func _ready():
	pressed.connect(_on_close_pressed)  # Use Callable() for signal connections

func _on_close_pressed():
	my_popup.hide()  # Hide the popup
