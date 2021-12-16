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
    occluded_faces = []
    result = rt.OverlappingFaces.Check(rt.currentTime, source, pymxs.byref(occluded_faces))
    rt.polyop.setFaceSelection(source,result)
    #~ rt.subObjectLevel = 4
    #~rt.polyop.attach(source,box)

    #~ faces = []
    #~ result = rt.OverlappingFaces.Check(rt.currentTime, source, pymxs.mxsreference(faces))
    #~ rt.polyop.setFaceSelection(source,faces)
    #~ rt.subObjectLevel = 4

main()