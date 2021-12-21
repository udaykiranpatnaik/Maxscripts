from pymxs import runtime as rt # pylint: disable=import-error

def combine_objects(*args):
    """
    Convert the two provided objects to meshes and merges them as a single mesh.
    """
    first = rt.convertToMesh(args[0])
    for obj in args[1:]:
        rt.attach(first, rt.convertToMesh(obj))
    rt.convertToPoly(first)
    return first

def combine_selected_objects():
    """
    Convert the selected objects into an editable mesh. The selections needs to contain
    at least 2 objects to combine.
    """
    if len(rt.selection) < 2:
        msg = "Please select at least 2 nodes to combine."
        print(msg)
        rt.messageBox(msg)
    else:
        # combine all the selected nodes into one editable mesh
        combine_objects(*rt.selection)
    source = rt.selection[0]
    return source
    
def main():
    source = combine_selected_objects()
    temp = rt.copy(source)
    box = rt.box()
    rt.select(box)
    rt.addModifier(box,rt.DeleteMesh())
    rt.convertToPoly(box)
    rt.ProBoolean.createBooleanObject(box,temp, 0, 2, 0)
    rt.convertToPoly(box)
    rt.select(box)
    obj = rt.getCurrentSelection()[0]
    rt.polyop.setFaceSelection(obj,rt.name('all'))
    rt.subObjectLevel = 4
    face_selection_obj = rt.polyop.getFaceSelection(obj)
    rt.polyop.setFaceSelection(obj,face_selection_obj)
    rt.subObjectLevel = 0
    rt.select(source)
    rt.polyop.attach(source,obj)
    rt.polyop.setFaceSelection(source,rt.name('all'))
    rt.subObjectLevel = 4
    source_face_selection = rt.getFaceSelection(source)
    rt.subObjectLevel = 0
    #~ overlapped_faces_xview = []
    #~ result = rt.OverlappingFaces.Check(rt.currentTime, source, pymxs.byref(overlapped_faces_xview))
    #~ overlapped_faces =  rt.polyop.getFaceSelection(source)
    #~ rt.polyop.setFaceSelection(source,overlapped_faces)
    #~ rt.subObjectLevel = 4
    
    
    #~rt.polyop.attach(source,box)

    #~ faces = []
    #~ result = rt.OverlappingFaces.Check(rt.currentTime, source, pymxs.mxsreference(faces))
    #~ rt.polyop.setFaceSelection(source,faces)
    #~ rt.subObjectLevel = 4
    
    #~ import MaxPlus
    #~ from pymxs import runtime as rt
    #~ obj = rt.selection[0]
    #~ print("NUM_FACES :%s" %rt.polyop.getNumFaces(obj))
    #~ rt.polyop.setFaceSelection(obj,rt.name('all'))
    #~ rt.subObjectLevel = 4
    #~ all_faces = rt.getFaceSelection(obj)

    #~ print("ALL : %s" %all_faces)
    #~ faces_xview = []
    #~ result = rt.OverlappingFaces.Check(rt.currentTime, obj, pymxs.byref(faces_xview))
    #~ overlapping_faces = result[1]
    #~ rt.polyop.setFaceSelection(obj,overlapping_faces)
    #~ rt.subObjectLevel = 4
    #~ print("OVER: %s" %overlapping_faces)
    #~ rt.subObjectLevel = 0
    #~ invert_faces = all_faces - overlapping_faces

    #~ rt.polyop.setFaceSelection(obj, invert_faces)
    #~ rt.subObjectLevel = 4

main()