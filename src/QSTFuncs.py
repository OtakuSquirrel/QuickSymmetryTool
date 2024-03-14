import maya.OpenMaya as om
import maya.cmds as cmds
import maya

def bake_custom_pivot():
    """
    对当前选择的对象执行MEL命令BakeCustomPivot。
    """
    # 检查是否有对象被选择
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return

    # 对当前选择的对象执行BakeCustomPivot命令
    maya.mel.eval('BakeCustomPivot;')

    print("BakeCustomPivot has been applied to the selected objects.")

def setSelectedPoint0(axis):
    """
    将选中的顶点在指定轴上归零（在对象空间中）

    参数:
    - axis: 需要归零的轴，可以是 'x', 'y', 或 'z'
    """

    # 获取当前选择的顶点
    selected_vertices = cmds.ls(selection=True, flatten=True)

    if not selected_vertices:
        cmds.warning("No vertex selevted")
        return

    # 确定轴的索引，这样我们就可以根据 'x', 'y', 或 'z' 来修改对应的位置值
    axis_index = {'x': 0, 'y': 1, 'z': 2}.get(axis.lower())
    if axis_index is None:
        cmds.warning("Wrong axis".format(axis))
        return

    for vertex in selected_vertices:
        # 获取顶点当前的位置（在对象空间中）
        current_position = cmds.pointPosition(vertex, local=True)

        # 将指定轴上的位置设置为0
        current_position[axis_index] = 0

        # 移动顶点到新位置
        cmds.move(current_position[0], current_position[1], current_position[2], vertex, localSpace=True)


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
    maya.mel.eval('Symmetrize;')

def symmetricModelling():
    cmds.symmetricModelling(topoSymmetry=True)
