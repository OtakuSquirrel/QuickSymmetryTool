# 快速对称工具
import maya.cmds as cmds
import maya
def bake_custom_pivot():
    # 检查是否有对象被选择
    selected_objects = cmds.ls(selection=True)
    if not selected_objects:
        cmds.warning("No objects selected.")
        return
    # 对当前选择的对象执行BakeCustomPivot命令
    maya.mel.eval('BakeCustomPivot;')
    print("BakeCustomPivot has been applied to the selected objects.")

def zeroAndSym(axis):
    # 获取当前选择的边
    selectedEdges = cmds.ls(selection=True, fl=True)
    if not selectedEdges:
        print("没有选择任何边。")
        return
    
    # 记录第0个边
    firstEdge = selectedEdges[0]
    print(firstEdge)
    # 将选择的边转换为顶点
    selectedVertices = cmds.polyListComponentConversion(selectedEdges, toVertex=True)
    selectedVertices = cmds.ls(selectedVertices, fl=True)

    # 确定轴的索引，这样我们就可以根据 'x', 'y', 或 'z' 来修改对应的位置值
    axis_index = {'x': 0, 'y': 1, 'z': 2}.get(axis.lower())
    if axis_index is None:
        cmds.warning("Wrong axis".format(axis))
        return

    for vertex in selectedVertices:
        # 获取顶点当前的位置（在对象空间中）
        current_position = cmds.pointPosition(vertex, local=True)
        # 将指定轴上的位置设置为0
        current_position[axis_index] = 0
        # 移动顶点到新位置
        cmds.move(current_position[0], current_position[1], current_position[2], vertex, localSpace=True)

    # 开启拓扑对称建模并选择第0个边
    cmds.select(firstEdge)
    cmds.symmetricModelling(topoSymmetry=True)
    edge = firstEdge

def selection1():
    cmds.select(clear=True)
    cmds.select(symmetrySide=2)

def selection2():
    cmds.select(clear=True)
    cmds.select(symmetrySide=1)

def symSelection():
    maya.mel.eval('Symmetrize;')

def bugSymSelection():
    cmds.symmetricModelling(topoSymmetry=False)
    maya.mel.eval('Symmetrize;')

def disableSymmetricModelling():

    cmds.symmetricModelling(topoSymmetry=False)

def create_qst_ui():
    # 创建窗口
    width = 320
    height = 460
    row_height = 30  # 统一行高
    window_name = 'QuickSymmetryTool'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    qst_window = cmds.window(window_name, title='QuickSymmetryTool', widthHeight=(width, height))

    # 创建布局
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # 烘焙选中的
    cmds.text(label='Select the object you want to symmetry', height=row_height)
    cmds.button(label='Bake transform', height=row_height, command="QST.bake_custom_pivot()")

    # 对称轴选择说明
    cmds.text(label='Select symmetrical axis：', height=row_height)

    # 第一步：从xyz三个值中选择一个作为对称轴
    axis_option_menu = cmds.optionMenu(label='', height=row_height)
    cmds.menuItem(label='x')
    cmds.menuItem(label='y')
    cmds.menuItem(label='z')

    # 归零点按钮说明
    cmds.text(label='Please select edges in the middle', height=row_height)

    # 第二步：一个按钮，根据选择的轴归零点
    cmds.button(label='Zero and sym', height=row_height, command=lambda x: zeroAndSym(axis=cmds.optionMenu(axis_option_menu, query=True, value=True)))


    # 选择按钮说明
    cmds.text(label='Select the points\n(highlighted will be retained):', height=row_height)

    # 第三步：并列的两个按钮，分别执行selection1()，selection2()
    selection_row = cmds.rowLayout(numberOfColumns=2, columnWidth2=(width/2, width/2), adjustableColumn=True)

    cmds.button(label='Section1', height=row_height, command=lambda x: selection1(),width=width/2)
    cmds.button(label='Section2', height=row_height, command=lambda x: selection2(),width=width/2)
    cmds.setParent('..')  # 返回到上一级布局

    # 第四步：一个按钮，执行symSelection()，参数取决于第一步选择的对称轴
    cmds.button(label='Execute', height=row_height, command='QST.symSelection()')
    cmds.button(label='Bug Execute', height=row_height, command='QST.bugSymSelection()')

    # 显示窗口
    cmds.showWindow(qst_window)