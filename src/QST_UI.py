import maya.cmds as cmds
from importlib import reload
import QSTFuncs
reload(QSTFuncs)

def create_qst_ui():
    # 创建窗口
    width = 400
    height = 470
    row_height = 30  # 统一行高
    window_name = 'QuickSymmetryTool'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    qst_window = cmds.window(window_name, title='QuickSymmetryTool', widthHeight=(width, height))

    # 创建布局
    main_layout = cmds.columnLayout(adjustableColumn=True, rowSpacing=10)

    # 烘焙选中的
    cmds.text(label='Select the object you want to symmetry', height=row_height)
    cmds.button(label='Bake transform', height=row_height, command="QSTFuncs.bake_custom_pivot()")

    # 对称轴选择说明
    cmds.text(label='Select symmetrical axis：', height=row_height)

    # 第一步：从xyz三个值中选择一个作为对称轴
    axis_option_menu = cmds.optionMenu(label='', height=row_height)
    cmds.menuItem(label='x')
    cmds.menuItem(label='y')
    cmds.menuItem(label='z')

    # 归零点按钮说明
    cmds.text(label='Please select the point in the middle of the model', height=row_height)

    # 第二步：一个按钮，根据选择的轴归零点
    cmds.button(label='Return to zero', height=row_height, command=lambda x: QSTFuncs.setSelectedPoint0(axis=cmds.optionMenu(axis_option_menu, query=True, value=True)))

    # 对称轴选择说明
    cmds.text(label='Select an edge for symmetry', height=row_height)

    # 第四行：按钮，启用拓扑对称
    cmds.button(label='enable topology symmetry', command='QSTFuncs.symmetricModelling()')

    # 选择按钮说明
    cmds.text(label='Select the point on one side (the highlighted part will be retained):', height=row_height)

    # 第三步：并列的两个按钮，分别执行selection1()，selection2()
    selection_row = cmds.rowLayout(numberOfColumns=2, columnWidth2=(width/2, width/2), adjustableColumn=True)

    cmds.button(label='Section1', height=row_height, command=lambda x: QSTFuncs.selection1(),width=width/2)
    cmds.button(label='Section2', height=row_height, command=lambda x: QSTFuncs.selection2(),width=width/2)
    cmds.setParent('..')  # 返回到上一级布局


    # 第四步：一个按钮，执行symSelection()，参数取决于第一步选择的对称轴
    cmds.button(label='Execute', height=row_height, command=lambda x: QSTFuncs.symSelection(cmds.optionMenu(axis_option_menu, query=True, value=True)))

    # 显示窗口
    cmds.showWindow(qst_window)

# 运行函数创建UI
# create_qst_ui()