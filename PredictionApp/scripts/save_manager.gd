extends Node

var profiledata = {"cc":0,"acceleration":0,"weight":0,"friction":0,"max_speed":0,"scaling":0}
var pathdata: Array[Vector2] = []
var json = JSON.new()
var path_dir = ""
var profile_dir = ""
	
func save_path(path: String, content) -> void:
	path_dir = path
	save(path, content)

func save_profile(path: String, content) -> void:
	profile_dir = path
	save(path, content)
	
func read_path(path: String):
	path_dir = path
	return read(path)
	
func read_profile(path: String):
	profile_dir = path
	return read(path)

func save(path, content):
	var file = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(json.stringify(content))
	file.close()
	file = null

func read(path):
	var file = FileAccess.open(path,FileAccess.READ)
	#if (file != null):
	var content = json.parse_string(file.get_as_text())
	file.close()
	file = null
	return content
