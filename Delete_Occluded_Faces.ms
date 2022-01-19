function Main = (
		scene_objects = selection as array
		source_obj = combine_meshes(scene_objects)
		temp_obj = create_temp_mesh(source_obj)
		check_for_overlapped_faces(temp_obj)
	)

-- Combine array of selected objects in the scene
function combine_meshes objectArr = (
		first = objectArr[1]
		convertToPoly first
		for i = 2 to objectArr.count do (
			polyop.attach first objectArr[i]
		)
		return first
	)

-- Duplicating the combined meshes and booleaning with a temporary mesh to remove occluded faces
function create_temp_mesh obj = (
		select obj
		maxOps.CloneNodes obj cloneType:#copy newNodes:&obj_clone
		operand_obj = obj_clone[1]
		temp = box()
		convertToPoly temp
		select temp
		subObjectLevel = 4
		temp.selectedfaces = #{1..temp.faces.count}
		polyop.deleteFaces temp #{1..temp.faces.count}
		subObjectLevel = 0
		ProBoolean.CreateBooleanObject temp operand_obj 0 2 0
		convertToPoly temp
		return temp
	)

-- Using XnView OverlappingFaces option to check for overlapping faces between the source combined and the booleaned mesh
function check_for_overlapped_faces obj = (
		select obj
		xViewChecker.on = True	
	)

rollout DeleteOccluded "Delete Occluded Faces" width:278 height:178
(
	button 'btn_delete_faces' "Button" pos:[55,61] width:168 height:56 align:#left
	on btn_delete_faces pressed  do
	Main()	
)
CreateDialog DeleteOccluded

