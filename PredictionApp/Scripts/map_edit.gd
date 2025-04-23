# Authors: Xavier Santiago (santiago25@up.edu)

extends Control
class_name Map_Editor

# keep track of path
var points: Array[Vector2] = []
var icons: Array[Node2D] = []

# how far away we can click to select a node
var dead_range = 10 # distance a point is considered clicked on

# what to render for each node
var path_node := load("res://Scenes/path_node.tscn")

# whether or not we are currently repositioning a node
var mouse_held = false

# which node we are moving (if any)
var selected_index = -1
var is_ruler = false

# offset of selected node from mouse
var drag_offset = Vector2.ZERO
var drawable = true

# whether or not this scene is in focus
# Godot does not have private variables, _ prefix
# denotes variables which should be treated as private
var _is_preview = true

# ui things
@onready var scale_units := $Scale/OptionButton
@onready var scale_value := $Scale/SpinBox
@onready var img_scale := $"Utils/Resize Slider"
@onready var ui_containers = [$"Menu Bar", $Scale, $Utils]

# scaling points
@onready var ruler = [$"Path Node", $"Path Node2"]
@onready var ruler_anchors

# Main scene reference ant utils
var main_ref: Main

# File dialogue for save/oad
@onready var file_popup := $FileDialog
enum FileType {LOAD_IMAGE, LOAD_PATH, SAVE_PATH}
var file_type : FileType

# background image
@onready var reference := $Reference
@onready var reference_scale := $"Utils/Resize Slider"

func _ready() -> void:
	ruler_anchors = [ruler[0].position, ruler[1].position]
	
func _process(delta: float) -> void:
	# drag point if necessary
	if selected_index >= 0 && mouse_held:
		if is_ruler:
			ruler[selected_index].position = get_global_mouse_position()-position+drag_offset
		else:
			points[selected_index] = get_global_mouse_position()-position+drag_offset
			icons[selected_index].position = get_global_mouse_position()-position+drag_offset
		
	# draw lines along path
	queue_redraw()
	
func _draw():
	# draw measurement stick
	if ruler[0] && ruler[1]:
		draw_line(ruler[0].position, ruler[1].position, Color.BLUE, 1.0)
	
	# draw path
	for i in range(len(points)):
		var color = Color.YELLOW # most lines
		if i == 0:
			color = Color.GREEN # start line
		if i == len(points)-1:
			color = Color.RED # end line
			
		# get points to draw arrow between
		var pos1 = points[i]
		var pos2 = points[0] # if last point use first point
		if i < len(points)-1:
			pos2 = points[i+1]
		
		# draw connecting line
		draw_line(pos1, pos2, color, 1.0)
		# draw little arrows
		var v = pos2-pos1
		v = v.normalized()*10
		draw_line(pos2-v, pos2-v-v.rotated(PI/8), color, 1.0)
		draw_line(pos2-v, pos2-v-v.rotated(-PI/8), color, 1.0)

func _input(event):
	if _is_preview:
		return
	# Mouse in viewport coordinates.
	if event is InputEventMouseButton && drawable:
		# save mouse state
		mouse_held = event.pressed
		
		# if event was from release, return
		if !mouse_held:
			return
		
		# have to adjust for control node position
		var mouse_pos = event.position-position
		
		# check if we clicked on an existing node
		selected_index = -1
		is_ruler = false
		for i in range(len(points)):
			if points[i].distance_to(mouse_pos) <= dead_range:
				selected_index = i
				drag_offset = icons[i].position-mouse_pos
				break
				
		for i in range(len(ruler)):
			if ruler[i].position.distance_to(mouse_pos) <= dead_range:
				selected_index = i
				drag_offset = ruler[i].position-mouse_pos
				is_ruler = true
				break
		if is_ruler:
			return
				
		# check if we clicked on scale nodes
		
			
		# if we clicked on an existing node, check event type
		if selected_index >= 0:
			# 1 = left, 2 = right, 3 = middle
			if event.button_index == 1:
				if event.double_click:
					icons[0].scale = Vector2(1,1)
					for i in range(selected_index):
						points.append(points[0])
						icons.append(icons[0])
						points.remove_at(0)
						icons.remove_at(0)
					icons[0].scale = Vector2(1.4,1.4)
					
					selected_index = -1
					
			elif event.button_index == 2:
				icons[selected_index].queue_free() # delete object instance
				points.remove_at(selected_index)
				icons.remove_at(selected_index)
			
				selected_index = -1
				
		# if clicked empty space, add node
		else:
			# check if we want to add point in middle of path
			var insert_at = len(points)
			for i in range(len(points)-1):
				var p1 = points[i]
				var p2 = points[i+1]
				
				# check if in right area
				var dist = p1.distance_to(p2)
				if p1.distance_to(mouse_pos) < dist && p2.distance_to(mouse_pos) < dist:
					var perp_dist =  p1.distance_to(mouse_pos)*sin((p2-p1).angle_to(mouse_pos-p1))
					if abs(perp_dist) < dead_range:
						insert_at = i+1
					
			# 1 = left, 2 = right, 3 = middle
			if event.button_index == 1:
				# create new node instance
				var newNode: Node2D = path_node.instantiate()
				# move to correct position
				newNode.global_position = mouse_pos
				if len(points) == 0:
					# if this is first point created, automatically set as start
					newNode.scale = Vector2(1.4,1.4)
				# add to current scene
				add_child(newNode)
				# keep track of point
				icons.insert(insert_at, newNode)
				points.insert(insert_at, mouse_pos)
					
				# allow dragging most recent point
				selected_index = insert_at

######################################
### HELPER/SCENE CHANGE FUNCTIONS ####
######################################

# check whether mouse in draw area (i.e. not over UI)
func _on_ui_zone_1_mouse_entered() -> void:
	drawable = true

func _on_ui_zone_1_mouse_exited() -> void:
	drawable = false
	
# return to main scene
func _on_back_pressed() -> void:
	Global.points = export_path()
	#get_tree().change_scene_to_file("res://Scenes/main.tscn")
	main_ref.return_to_focus()
	set_preview(true)
	
# reverse list
func _on_reverse_pressed() -> void:
	points.reverse()
	points.insert(0, points.back())
	points.pop_back()
	
	icons.reverse()
	icons.insert(0, icons.back())
	icons.pop_back()

# reset path
func reset() -> void:
	# reset list of points
	points.clear()
	
	# delete all icon objects then delete list
	for each in icons:
		each.queue_free()
	icons.clear()
	
	# reset ruler position
	ruler[0].position = ruler_anchors[0]
	ruler[1].position = ruler_anchors[1]

	# reset scale
	scale_value.get_line_edit().text = "1"
	scale_units.selected = 0
	
	# reset reference image
	reference.texture = null
	
# remove UI if we are using the scene to render a preview of the map
# not fully implemented, currently just render background image on main screen
func set_preview(val: bool) -> void:
	_is_preview = val
	if _is_preview:
		self.visible = false # remove when implementing fully
		for each in ui_containers:
			each.visible = false
	else:
		self.visible = true # remove when implementing fully
		for each in ui_containers:
			each.visible = true
			
func set_main(main: Node) -> void:
	main_ref = main

######################################
### FUNCTIONS FOR DATA FORMATTING ####
######################################

# returns the list of points formatted such that
# - start position is at 0, 0
# - coordinates are listed in meters
func export_path() -> Array[Vector2]:
	var path_data: Array[Vector2] = []
	
	# adjust points so start is at [0,0] and coordinates are in meters from start
	for each in points:
		var p_translated = each-points[0]
		# coords in screen space have 0,0 at top left, for sake of intuition we flip the y axis
		var p_mirrored = Vector2(p_translated.x, -p_translated.y)
		var scale_factor = int(scale_value.get_line_edit().text)
		if scale_units.get_selected_id() == 1:
			scale_factor *= 0.3048 # feet to meters conversion
		var p_scaled = (p_mirrored/ruler[0].position.distance_to(ruler[1].position))*scale_factor
		path_data.append(p_scaled)
	
	return path_data

# converts vector2 arrays to proper format to saving as json
func format_list(list: Array[Vector2]) -> Array[Array]:
	var new_list: Array[Array] = []
	for each in list:
		new_list.append([each.x, each.y])
	return new_list
	
# Undoes above function
func restore_list(list: Array) -> Array[Vector2]:
	var new_list: Array[Vector2] = []
	for each in list:
		new_list.append(Vector2(each[0], each[1]))
	return new_list
	
######################################
###### FUNCTIONS FOR SAVE/LOAD #######
######################################

func _on_save_pressed() -> void:
	file_popup.set_file_mode(FileDialog.FILE_MODE_SAVE_FILE) # select single file setting
	file_type = FileType.SAVE_PATH
	file_popup.clear_filters()
	file_popup.add_filter("*.json") # only look for json files
	file_popup.title = "Select a Location"
	file_popup.popup_centered_ratio()

func _on_load_map_pressed() -> void:
	file_popup.set_file_mode(FileDialog.FILE_MODE_OPEN_FILE) # select single file setting
	file_type = FileType.LOAD_PATH
	file_popup.clear_filters()
	file_popup.add_filter("*.json") # only look for json files
	file_popup.title = "Select a File"
	file_popup.popup_centered_ratio()

func _on_file_dialog_file_selected(path: String) -> void:
	if file_type == FileType.LOAD_PATH:
		# reset current data
		reset()
		
		# load data from file
		var data = SaveManager.read_path(path)
	
		# read config values
		scale_value.get_line_edit().text = data.scale.value
		scale_units.select(data.scale.unit)
		ruler[0].position = Vector2(data.ruler[0][0],data.ruler[0][1])
		ruler[1].position = Vector2(data.ruler[1][0],data.ruler[1][1])
		
		# calculate reverse scaling factor
		var scale_factor = int(scale_value.get_line_edit().text)
		if scale_units.get_selected_id() == 1:
			scale_factor *= 0.3048 # feet to meters conversion
		scale_factor = ruler[0].position.distance_to(ruler[1].position)/scale_factor
		
		# repopulate lists
		for each in data.raw:
			var point = Vector2(each[0], each[1])
			var newNode: Node2D = path_node.instantiate()
			newNode.global_position = point
			add_child(newNode)
			icons.append(newNode)
			points.append(point)
			
		# set calculation data
		Global.points = restore_list(data.formatted)
	
	elif file_type == FileType.SAVE_PATH:
		var export_data = {}
		# define config dict
		export_data["scale"] = {
			"value": scale_value.get_line_edit().text, 
			"unit": scale_units.get_selected_id()
		}
			
		export_data["ruler"] = [
			[ruler[0].position.x,ruler[0].position.y], 
			[ruler[1].position.x,ruler[1].position.y]
		]
		export_data["raw"] = format_list(points)
		export_data["formatted"] = format_list(export_path())
		
		# pass to save manager to write to file
		SaveManager.save_path(path, export_data)
		
	elif file_type == FileType.LOAD_IMAGE:
		var image = Image.load_from_file(path)
		var texture = ImageTexture.create_from_image(image)
		# reset image size
		reference_scale.value = 0
		reference.scale = Vector2(1,1)
		reference.texture = texture

func _on_load_image_pressed() -> void:
	file_popup.set_file_mode(FileDialog.FILE_MODE_OPEN_FILE) # select single file setting
	file_type = FileType.LOAD_IMAGE
	file_popup.clear_filters()
	file_popup.add_filter("*.png") # only look for usable image files
	file_popup.add_filter("*.jpg")
	file_popup.add_filter("*.jpeg")
	file_popup.title = "Select a File"
	file_popup.popup_centered_ratio()

func _on_resize_slider_value_changed(value: float) -> void:
	var s = 2**value
	reference.scale = Vector2(s,s)
