import maya.cmds as cmds
from importlib import reload
import QSTFuncs
reload(QSTFuncs)

def create_qst_ui():
    # 创建窗口
    width = 240
    height = 240
    qst_window = cmds.window(title='QuickSymmetryTool', widthHeight=(width, height))

    # 创建布局
    main_layout = cmds.columnLayout(adjustableColumn=True)

    # 第一行：选择清零点
    cmds.text(label='1. select points need to be reset', height=40)

    # 第二行：三个等大的按钮
    cmds.rowLayout(nc=3, columnWidth3=(width/3, width/3, width/3))
    cmds.button(label='X', command='QSTFuncs.setSelectedPoint0(axis="x")', width=width/3)
    cmds.button(label='Y', command='QSTFuncs.setSelectedPoint0(axis="y")', width=width/3)
    cmds.button(label='Z', command='QSTFuncs.setSelectedPoint0(axis="z")', width=width/3)
    cmds.setParent('..')

    # 第三行：选择对称轴
    cmds.text(label='2. select an edge for symmetry', height=40)

    # 第四行：按钮，启用拓扑对称
    cmds.button(label='enable topology symmetry', command='QSTFuncs.symmetricModelling()')

    # 第五行：选择区域
    cmds.text(label='4. select section', height=40)

    # 第六行：两个按钮
    cmds.rowLayout(nc=2, columnWidth2=(width/2, width/2))
    cmds.button(label='1', command='QSTFuncs.selection1()', width=width/2)
    cmds.button(label='2', command='QSTFuncs.selection2()', width=width/2)
    cmds.setParent('..')

    # 第七行：按钮，执行
    cmds.rowLayout(nc=3, columnWidth3=(width / 3, width / 3, width / 3))
    cmds.button(label='exec X', command='QSTFuncs.symSelection("x")', width=width / 3)
    cmds.button(label='exec Y', command='QSTFuncs.symSelection("y")', width=width / 3)
    cmds.button(label='exec Z', command='QSTFuncs.symSelection("z")', width=width / 3)
    cmds.setParent('..')


    # 显示窗口
    cmds.showWindow(qst_window)