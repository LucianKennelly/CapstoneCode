extends Node
var data = preload("res://data/testNov8.csv")
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	data = load("res://data/testNov8.csv")


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


func _on_run_pressed() -> void:
	print(data.records)
