import bpy
from bpy.props import CollectionProperty, StringProperty, IntProperty, BoolProperty, FloatProperty


class StringPropertyGroup(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty()


class IntPropertyGroup(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty()


class SequenceFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='Bundle')


class IterationFolder(bpy.types.PropertyGroup):
    name: StringProperty(default='Repeater')
    loop_variable_name: StringProperty(default='i')
    iterations: IntProperty(default=1)


class VariablesPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Variables')
    variables: CollectionProperty(type=StringPropertyGroup)
    values: CollectionProperty(type=IntPropertyGroup)


class FunctionsPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Functions')
    placeholders: CollectionProperty(type=StringPropertyGroup)
    replacements: CollectionProperty(type=StringPropertyGroup)


class GridMakerPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Grid') # type: ignore
    x_dimension: StringProperty(default='1')
    y_dimension: StringProperty(default='1')
    z_dimension: StringProperty(default='1')
    x_offset: StringProperty(default='0')
    y_offset: StringProperty(default='0')
    z_offset: StringProperty(default='0')
    density: StringProperty(default='0')
    is_hollow: BoolProperty(default=True)


class TransformationPanel(bpy.types.PropertyGroup):
    name: StringProperty(default='Transformation')
    x_function: StringProperty()
    timespan: FloatProperty()


class MultiItem(bpy.types.PropertyGroup):
    ITN: CollectionProperty(type=IterationFolder)
    SQN: CollectionProperty(type=SequenceFolder)
    VAR: CollectionProperty(type=VariablesPanel)

    GRD: CollectionProperty(type=GridMakerPanel)
    TRF: CollectionProperty(type=TransformationPanel)

    is_drawn: BoolProperty(default=False)
    is_active: BoolProperty(default=True)
    mode: StringProperty()
    generic_type: StringProperty()
    panel_number: IntProperty()
    parent_number: IntProperty()
    panel_id: StringProperty()
    parent_id: StringProperty(default='CONTROL_PT_Panel')

SystemDataClasses = [
    StringPropertyGroup, IntPropertyGroup,
    GridMakerPanel, TransformationPanel, VariablesPanel, FunctionsPanel,
    SequenceFolder, IterationFolder,
    MultiItem,
]

def register_property_groups():
    for system_class in SystemDataClasses:
        bpy.utils.register_class(system_class)
    bpy.types.Scene.MultiItemPool = CollectionProperty(type=MultiItem)
    bpy.types.Scene.CurrentPanelNumber = bpy.props.IntProperty(default=0)

def unregister_property_groups():
    for system_class in SystemDataClasses:
        bpy.utils.unregister_class(system_class)
    del bpy.types.Scene.MultiItemPool
    del bpy.types.Scene.CurrentPanelNumber
