bl_info = {
    "name": "Kaleidoscope - A small package of nodes for materials",
    "author": "Akash Hamirwasia",
    "version": (1, 1, 0),
    "blender": (2, 81, 0),
    "location": "NodeEditor > MaterialView > Add Node Menu",
    "description": "A Complete Toolkit of Nodes to Make your Materials even more colorful and physically accurate",
    "warning": "",
    "wiki_url": "http://blskl.cf/kaldocs",
    "tracker_url": "http://blskl.cf/kalbugs",
    "category": "Node"}


if "bpy" in locals():
    import importlib
    importlib.reload(client)
    importlib.reload(spectrum)
    importlib.reload(intensity)
    importlib.reload(addon_updater_ops)
else:
    from . import client, spectrum, intensity, addon_updater_ops

import bpy
import nodeitems_utils, zipfile, os, json
from nodeitems_utils import NodeCategory, NodeItem
from bpy.types import Node
from bpy_extras.io_utils import ImportHelper, ExportHelper

class KaleidoscopeHybridTreeNode:
    @classmethod
    def poll(cls, ntree):
        b = False
        if ntree.bl_idname == 'ShaderNodeTree':
            b = True
        return b

# Derived from the Node base type
class KaleidoscopeHybridNode(Node, KaleidoscopeHybridTreeNode):
    """Kaleidoscope Hybrid node"""
    bl_idname = 'kaleidoscope_hybrid.node'
    bl_label = 'Kaleidoscope Hybrid'
    bl_icon = 'INFO'

    def set_kaleidoscope_node(self, context):
        node_type = self.node_type
        loc = self.location
        if node_type == '1':
            if bpy.context.space_data.shader_type == 'WORLD':
                spectrum_node = bpy.context.scene.world.node_tree.nodes.new(type='spectrum_palette.node')
                spectrum_node.location = loc
                bpy.context.scene.world.node_tree.nodes.remove(self)
            elif bpy.context.space_data.shader_type == 'OBJECT':
                spectrum_node = bpy.context.object.active_material.node_tree.nodes.new(type='spectrum_palette.node')
                spectrum_node.location = loc
                bpy.context.object.active_material.node_tree.nodes.remove(self)
        elif node_type == '2':
            if bpy.context.space_data.shader_type == 'WORLD':
                intensity_node = bpy.context.scene.world.node_tree.nodes.new(type='intensity.node')
                intensity_node.location = loc
                bpy.context.scene.world.node_tree.nodes.remove(self)
            elif bpy.context.space_data.shader_type == 'OBJECT':
                intensity_node = bpy.context.object.active_material.node_tree.nodes.new(type='intensity.node')
                intensity_node.location = loc
                bpy.context.object.active_material.node_tree.nodes.remove(self)
        return None

    node_type: bpy.props.EnumProperty(name="Kaleidoscope Node Type", description="Choose the type of Node which you want to use", items=(('0', '', '', 'NODETREE', 0), ('1', 'Spectrum', 'Use the Spectrum Palette Node'), ('2', 'Intensity', 'Use the Intensity Node')), default=None, update=set_kaleidoscope_node)

    def init(self, context):
        self.width = 200
        pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.label()
        col.label(text="Kaleidoscope Hybrid is just a")
        col.label(text="quick node to choose the nodes")
        col.label(text="that come with Kaleidoscope.")
        col.label()
        col.label(text="Select any one of the option to")
        col.label(text="to use the node that comes with")
        col.label(text="Kaleidoscope")
        col.label()
        row = col.row(align=True)
        row.prop(self, 'node_type', expand = True)

    #Node Label
    def draw_label(self):
        return "Kaleidoscope Hybrid"

class KaleidoscopeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        b = False
        if context.space_data.tree_type == 'ShaderNodeTree':
            b = True
        return b

# all categories in a list


node_categories = [
    KaleidoscopeCategory("KALEIDOSCOPENODES", "Kaleidoscope", items=[
        NodeItem("kaleidoscope_hybrid.node"),
        NodeItem("spectrum_palette.node"),
        NodeItem("intensity.node")
        ]),
    ]

class Kaleidoscope(bpy.types.AddonPreferences):
    bl_idname = "kaleidoscope"

    def draw(self, context):
        kaleidoscope_props=bpy.context.scene.kaleidoscope_props
        layout = self.layout
        box = layout.box()
        col = box.column()
        row = col.row()
        row.alignment ='CENTER'
        row.label(text="INSTALLING FILES")
        col.label()
        col.label(text="1) Download the .zip files which has the files to import. DO NOT EXTRACT IT")
        col.label(text="2) Click the 'Import Files' button below, and select the .zip file")
        col.label(text="     NOTE: SELECT ONLY 1 ZIP FILE ONCE")
        col.label(text="3) Click the 'Install Files' button. The files should be installed")
        col.label()
        row = col.row()
        row.scale_y = 1.2
        row.label()
        row.operator(KaleidoscopeImport.bl_idname, text='Import Files', icon='IMPORT') #Install Files button
        row.label()
        col.separator()
        row = col.row()
        row.scale_y = 1.12
        row.label()
        row.operator(KaleidoscopeExport.bl_idname, text='Export Files', icon='EXPORT') #Install Files button
        row.label()
        if bpy.context.scene.kaleidoscope_props.import_files == True:
            col.label(text="There was a problem in importing the files.", icon='ERROR')
        col.label()

        addon_updater_ops.update_settings_ui(self, context)

        row = box.row(align=True)
        split = row.split(factor=0.8)
        col1 = split.column(align=True)
        row1 = col1.row(align=True)
        row1.separator()
        row1_1 = row1.row(align=True)
        row1_1.alignment = 'CENTER'
        row1_1.label(text="Created by Akash Hamirwasia")
        col2 = split.column(align=True)
        row2 = col2.row()
        row2.scale_y = 1.2
        row2.operator('wm.url_open', text="Support Me", icon='SOLO_ON').url="http://blskl.cf/kalsupport"

class KaleidoscopeImport(bpy.types.Operator, ImportHelper): #Importing Files
    """Install .zip or .kal file in the add-on"""
    bl_idname = "kaleidoscope.install_files"
    bl_label = "Install Files"

    filename_ext = ".kal"

    filter_glob: bpy.props.StringProperty(
            default="*.kal;*.zip",
            options={'HIDDEN'},
            )
    def execute(self, context):
        try:
            zipref = zipfile.ZipFile(self.filepath, 'r')
            path = os.path.dirname(__file__)
            if (path != ""):
                zipref.extractall(path) #Extract to the kaleidoscope add-on Folder
                zipref.close()
            bpy.context.scene.kaleidoscope_props.import_files = False
        except:
            bpy.context.scene.kaleidoscope_props.import_files = True
        return {'FINISHED'}

class KaleidoscopeExport(bpy.types.Operator, ExportHelper):
    """Export the Saved Palettes and Values in a .zip or .kal format"""
    bl_idname = 'kaleidoscope.export_files'
    bl_label = 'Export Files'

    filename_ext = ""

    filter_glob: bpy.props.StringProperty(
            default="*.zip;*.kal",
            options={'HIDDEN'}
            )

    export_type: bpy.props.EnumProperty(name="Format", description="Format in which you want to export the Files", items=(('0', '.zip', 'Use .zip if you want to save it as a backup for yourself'),
                                        ('1', '.kal', 'Use .kal if you want to share your files with other users')), default='0')

    def execute(self, context):
        try:
            if self.export_type == '0':
                if self.filepath.endswith(".kal") == True:
                    self.filepath = self.filepath.replace(".kal", ".zip")
                if self.filepath.endswith(".zip") == False:
                    self.filepath = self.filepath+".zip"

            elif self.export_type == '1':
                if self.filepath.endswith(".zip") == True:
                    self.filepath = self.filepath.replace(".zip", ".kal")
                if self.filepath.endswith(".kal") == False:
                    self.filepath = self.filepath+".kal"

            zf = zipfile.ZipFile(self.filepath, "w", zipfile.ZIP_DEFLATED)
            path = os.path.dirname(__file__)
            abs_src = os.path.abspath(path)
            for dirname, subdirs, files in os.walk(path):
                if '__pycache__' in subdirs:
                    subdirs.remove('__pycache__')
                if 'kaleidoscope_updater' in subdirs:
                    subdirs.remove('kaleidoscope_updater')
                for filename in files: #Do not include the main code files
                    if filename.endswith(".json"):
                        if filename != "settings.json":
                            absname = os.path.abspath(os.path.join(dirname, filename))
                            arcname = absname[len(abs_src) + 1:]
                            zf.write(absname, arcname)
            zf.close()
            self.report({'INFO'}, "Files Exported Successfully to "+self.filepath)
        except:
            self.report({'ERROR'}, "There was an error, please check the file path!")
        return{'FINISHED'}

class KaleidoscopeProps(bpy.types.PropertyGroup):
    import_files: bpy.props.BoolProperty(name="Kaleidoscope Import", description="Checks if the zip file is properly imported", default=False)


classes = (
    client.CancelProcess,
    client.SavePaletteMenu,
    client.SavePaletteYes,
    client.DeletePaletteMenu,
    client.DeletePaletteYes,
    client.SaveValueMenu,
    client.SaveValueYes,
    client.DeleteValueMenu,
    client.DeleteValueYes,

    spectrum.SpectrumProperties,
    spectrum.SpectrumMaterialProps,
    spectrum.SpectrumNode,
    spectrum.PaletteGenerate,
    spectrum.PreviousPalette,
    spectrum.NextPalette,
    spectrum.PaletteShuffle,
    spectrum.PaletteInvert,

    intensity.IntensityNode,

    KaleidoscopeHybridNode,
    Kaleidoscope,
    KaleidoscopeImport,
    KaleidoscopeExport,
    KaleidoscopeProps,
)

def register():
    addon_updater_ops.register(bl_info)

    for cls in classes:
        bpy.utils.register_class(cls)

    spectrum.register()
    intensity.register()
    bpy.types.Scene.kaleidoscope_props = bpy.props.PointerProperty(type=KaleidoscopeProps)
    nodeitems_utils.register_node_categories("KALEIDOSCOPE_NODES", node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories("KALEIDOSCOPE_NODES")
    spectrum.unregister()
    intensity.unregister()
    del bpy.types.Scene.kaleidoscope_props

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
