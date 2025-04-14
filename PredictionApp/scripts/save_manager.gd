extends Node

var profiledata = {"cc":0,"acceleration":0,"weight":0,"friction":0,"max_speed":0,"scaling":0}
var pathdata: Array[Vector2] = [Vector2(100,100),Vector2(200,200)]
var save = JSON.new()
var save_path = "user://default_path.dat"
var save_profile = "user://default_profile.json"

func _ready() -> void:
	pathdata.append(Vector2(100,100))
	pathdata.append(Vector2(200,200))
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
	file.close()
	file = null
	#print(content)
	return content
func read():
	var file = FileAccess.open(save_profile,FileAccess.READ)
	#if (file != null):
	var content = save.parse_string(file.get_as_text())
	file.close()
	file = null
	return content
func create_new_save():
	var file = null
	var content = null
	if FileAccess.file_exists(save_profile):	
		pass
	else:
		file = FileAccess.open(save_profile,FileAccess.READ)
		content = profiledata
		savef(content)
	#file = null
	file = null
	if FileAccess.file_exists(save_path):
		pass
	else:
		file = FileAccess.open(save_path,FileAccess.READ)
		content = pathdata
		savepath(content)
