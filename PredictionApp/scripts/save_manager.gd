extends Node

var profiledata = {"cc":0,"acceleration":0,"weight":0,"friction":0,"max_speed":0,"scaling":0}
var pathdata: Array[Vector2] = []
var save = JSON.new()
var path_dir = ""
var profile_dir = ""
	
func save_path(content) -> void:
	var file = FileAccess.open(path_dir, FileAccess.WRITE)
	print(content)
	file.store_var(content)
	file.close()
	file = null
	
func read_path():
	var file = FileAccess.open(path_dir,FileAccess.READ)
	var content = file.get_var()
	file.close()
	file = null
	#print(content)
	return content
	
func save_profile(path: String, content) -> void:
	profile_dir = path
	var file = FileAccess.open(profile_dir, FileAccess.WRITE)
	file.store_string(save.stringify(content))
	file.close()
	file = null
	
func read_profile(path: String):
	profile_dir = path
	var file = FileAccess.open(profile_dir,FileAccess.READ)
	#if (file != null):
	var content = save.parse_string(file.get_as_text())
	file.close()
	file = null
	return content
