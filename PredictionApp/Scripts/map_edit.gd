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

# ui buttons
@onready var scale_units := $Scale/OptionButton
@onready var scale_value := $Scale/SpinBox

# scaling points
@onready var ruler = [$"Path Node", $"Path Node2"]
@onready var ruler_anchors

# reference to main scene
var main_ref: Main

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
	#print(icons)
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
	if !self.visible:
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
			print(points[i].distance_to(mouse_pos))
			if points[i].distance_to(mouse_pos) <= dead_range:
				selected_index = i
				drag_offset = icons[i].position-mouse_pos
				break
				
		for i in range(len(ruler)):
			print(ruler[i].position.distance_to(mouse_pos))
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
					if perp_dist < dead_range:
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

# check whether mouse in draw area (i.e. not over UI)
func _on_ui_zone_1_mouse_entered() -> void:
	drawable = true

func _on_ui_zone_1_mouse_exited() -> void:
	drawable = false

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
		if scale_units.get_item_text(scale_units.selected) == "ft":
			scale_factor /= 3.28084 # feet to meters conversion, 99.9999968% accuracy
		var p_scaled = (p_mirrored/ruler[0].position.distance_to(ruler[1].position))*scale_factor
		path_data.append(p_scaled)
	
	return path_data


func _on_save_pressed() -> void:
	SaveManager.savepath(points)
	#print(export_path())

# reverse list
func _on_reverse_pressed() -> void:
	points.reverse()
	points.insert(0, points.back())
	points.pop_back()
	
	icons.reverse()
	icons.insert(0, icons.back())
	icons.pop_back()

# return to main scene
func _on_back_pressed() -> void:
	main_ref.return_to_focus()

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


func _on_load_map_pressed() -> void:
	#print(points)
	#print(SaveManager.readpath())
	reset()
	points = SaveManager.readpath()
	var data: Array[Node2D] = []
	icons.clear()
	for each in points:
		var newNode: Node2D = path_node.instantiate()
		newNode.global_position = Vector2(each[0],each[1])
		add_child(newNode)
		icons.append(newNode)
	print(icons)
