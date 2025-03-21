extends Node

var data = {}
var save = JSON.new()
var path = "user://data.json"
var load_path = "res://scripts/default.json"

func _ready() -> void:
	create_new_save()

func savef(content) -> void:
	var file = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(save.stringify(content))
	file.close()
	file = null
func read():
	var file = FileAccess.open(path,FileAccess.READ)
	var content = save.parse_string(file.get_as_text())
	return content
func create_new_save():
	var file = FileAccess.open("res://scripts/default.json",FileAccess.READ)
	var content = save.parse_string(file.get_as_text())
	data = content;
	savef(content)
func _on_save_pressed() -> void:
	savef(data)
