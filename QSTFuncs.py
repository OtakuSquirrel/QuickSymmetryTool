import maya.OpenMaya as om
import maya.cmds as cmds
def setSelectedPoint0(axis):
    # Get the active selection list
    selection_list = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selection_list)

    # Iterate over the selection list
    iterator = om.MItSelectionList(selection_list)
    while not iterator.isDone():
        dag_path = om.MDagPath()
        component = om.MObject()
        iterator.getDagPath(dag_path, component)

        # Check the component type and retrieve its indices
        if component.hasFn(om.MFn.kMeshVertComponent):
            # Vertex component
            vertex_iter = om.MItMeshVertex(dag_path, component)
            while not vertex_iter.isDone():
                pos = vertex_iter.position()

                if axis == 'x':
                    pos.x = 0.0
                elif axis == 'y':
                    pos.y = 0.0
                elif axis == 'z':
                    pos.z = 0.0

                vertex_iter.setPosition(pos)
                vertex_iter.next()

        iterator.next()

def selectHalfSide(axis, dir='+'):
    axis = dir + axis
    selected = om.MSelectionList()
    om.MGlobal.getActiveSelectionList(selected)
    meshObject = om.MObject()
    dagPath = om.MDagPath()
    selected.getDependNode(0, meshObject)
    selected.getDagPath(0, dagPath)

    itmesh = om.MItMeshVertex(dagPath)
    itmesh.reset()

    newSelectionList = om.MSelectionList()

    while not itmesh.isDone():
        itPoint = itmesh.position()
        if axis == '+x':
            if itPoint.x > 0:
                newSelectionList.add(dagPath, itmesh.currentItem())
        elif axis == '-x':
            if itPoint.x < 0:
                newSelectionList.add(dagPath, itmesh.currentItem())
        elif axis == '+y':
            if itPoint.y > 0:
                newSelectionList.add(dagPath, itmesh.currentItem())
        elif axis == '-y':
            if itPoint.y < 0:
                newSelectionList.add(dagPath, itmesh.currentItem())
        elif axis == '+z':
            if itPoint.z > 0:
                newSelectionList.add(dagPath, itmesh.currentItem())
        elif axis == '-z':
            if itPoint.z < 0:
                newSelectionList.add(dagPath, itmesh.currentItem())

        itmesh.next()
    om.MGlobal.setActiveSelectionList(newSelectionList)
    newSelectionList.clear()

def mirrorAxis(axis,pos):
    p=pos
    if axis == 'x':
        p[0] *= -1
    elif axis == 'y':
        p[1] *= -1
    elif axis == 'z':
        p[2] *= -1
    return p

def selection1():
    cmds.select(clear=True)
    cmds.select(symmetrySide=1)

def selection2():
    cmds.select(clear=True)
    cmds.select(symmetrySide=2)

def symSelection(axis):
    selectionList = cmds.ls(selection=True, flatten=True)
    for item in selectionList:
        cmds.select(clear=True)
        cmds.select(item)
        cmds.select(symmetry=1)
        cmds.select(item, deselect=True)
        symPoint = cmds.ls(selection=True)

        originPos = cmds.xform(item, query=True, translation=True, objectSpace=True)
        symPos = cmds.xform(symPoint, query=True, translation=True, objectSpace=True)
        targetPos = mirrorAxis(axis, originPos)
        cmds.xform(symPoint, translation=targetPos, objectSpace=True)

def symmetricModelling():
    cmds.symmetricModelling(topoSymmetry=True)
