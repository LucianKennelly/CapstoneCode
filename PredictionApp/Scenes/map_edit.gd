extends Control

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

var mouse_over_ui = false

# scaling points
@onready var ruler = [$"Path Node", $"Path Node2"]

func _ready() -> void:
	pass
	
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
		if i < len(points)-1:
			draw_line(points[i], points[i+1], Color.GREEN, 1.0)
		else:
			draw_line(points[i], points[0], Color.RED, 1.0)

func _input(event):
	if mouse_over_ui:
		return
	# Mouse in viewport coordinates.
	if event is InputEventMouseButton:
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
				# add to current scene
				add_child(newNode)
				# keep track of point
				icons.insert(insert_at, newNode)
				points.insert(insert_at, mouse_pos)
				# allow dragging most recent point
				selected_index = insert_at


func _on_ui_zone_1_mouse_entered() -> void:
	mouse_over_ui = true


func _on_ui_zone_1_mouse_exited() -> void:
	mouse_over_ui = false


func _on_ui_zone_2_mouse_entered() -> void:
	mouse_over_ui = true


func _on_ui_zone_2_mouse_exited() -> void:
	mouse_over_ui = false
