extends Node

var data = {}
var save = JSON.new()
var save_path = "user://Data.dat"
var save_profile = "user://default.json"

func _ready() -> void:
	create_new_save()

func savef(content) -> void:
	var file = FileAccess.open(save_profile, FileAccess.WRITE)
	file.store_string(save.stringify(content))
	file.close()
	file = null
func savepath(content) -> void:
	var file = FileAccess.open(save_path, FileAccess.WRITE)
	print(content)
	file.store_var(content)
	file.close()
	file = null
func readpath():
	var file = FileAccess.open(save_path,FileAccess.READ)
	var content = file.get_var()
	return content
func read():
	var file = FileAccess.open(save_profile,FileAccess.READ)
	var content = save.parse_string(file.get_as_text())
	return content
func create_new_save():
	#var file = FileAccess.open(save_profile,FileAccess.READ)
	#var content = save.parse_string(file.get_as_text())
	#data = content;
	#savef(content)
	#file = FileAccess.open(save_path,FileAccess.READ)
	#content = file.get_var()
	#data = content;
	#savef(content)
	pass
func _on_save_pressed() -> void:
	savef(data)
