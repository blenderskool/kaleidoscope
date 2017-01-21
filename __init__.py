bl_info = {
    "name": "Kaleidoscope - A small package of nodes for materials",
    "author": "Akash Hamirwasia",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "NodeEditor > MaterialView > Add Node Menu",
    "description": "A Complete Toolkit of Nodes to Make your Materials even more colorful and physically accurate",
    "warning": "",
    "wiki_url": "http://blskl.cf/kaldocs",
    "tracker_url": "http://blskl.cf/kalbugs",
    "category": "Node"}


if "bpy" in locals():
    import importlib
    importlib.reload(spectrum)
    importlib.reload(intensity)
    importlib.reload(addon_updater_ops)
else:
    from . import spectrum, intensity, addon_updater_ops

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

    node_type = bpy.props.EnumProperty(name="Kaleidoscope Node Type", description="Choose the type of Node which you want to use", items=(('0', '', '', 'NODETREE', 0), ('1', 'Spectrum', 'Use the Spectrum Palette Node'), ('2', 'Intensity', 'Use the Intensity Node')), default=None, update=set_kaleidoscope_node)

    def init(self, context):
        self.width = 200
        pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        col = layout.column(align=True)
        col.label()
        col.label("Kaleidoscope Hybrid is just a")
        col.label("quick node to choose the nodes")
        col.label("that come with Kaleidoscope.")
        col.label()
        col.label("Select any one of the option to")
        col.label("to use the node that comes with")
        col.label("Kaleidoscope")
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
    bl_idname = __name__

    def draw(self, context):
        kaleidoscope_props=bpy.context.scene.kaleidoscope_props
        layout = self.layout
        box = layout.box()
        col = box.column()
        row = col.row()
        row.alignment ='CENTER'
        row.label("INSTALLING FILES")
        col.label()
        col.label("1) Download the .zip files which has the files to import. DO NOT EXTRACT IT")
        col.label("2) Click the 'Import Files' button below, and select the .zip file")
        col.label("     NOTE: SELECT ONLY 1 ZIP FILE ONCE")
        col.label("3) Click the 'Install Files' button. The files should be installed")
        col.label()
        row = col.row()
        row.scale_y = 1.2
        row.label("")
        row.operator(KaleidoscopeImport.bl_idname, text='Import Files', icon='PACKAGE') #Install Files button
        row.label("")
        col.separator()
        row = col.row()
        row.scale_y = 1.12
        row.label("")
        row.operator(KaleidoscopeExport.bl_idname, text='Export Files', icon='OOPS') #Install Files button
        row.label("")
        if bpy.context.scene.kaleidoscope_props.import_files == True:
            col.label("There was a problem in importing the files.", icon='ERROR')
        col.label()

        row = col.row(align=True)
        for i in range(0, 5):
            row.separator()
        split = row.split(percentage=0.31, align=True)
        col = split.column(align=True)
        col.label("Path to Sync:")
        col = split.column(align=True)
        col.prop(bpy.context.scene.kaleidoscope_props, "sync_path", text="")
        for i in range(0, 5):
            row.separator()
        col.separator()

        box2 = box.box()
        col2 = box2.column(align=True)
        row = col2.row(align=True)
        if kaleidoscope_props.sync_help == False:
            row.prop(kaleidoscope_props, "sync_help", text="View Information for Syncing", toggle=True, icon='LAYER_USED')
        else:
            row.prop(kaleidoscope_props, "sync_help", text="Hide Information for Syncing", toggle=True, icon='LAYER_ACTIVE')
            col3 = box2.column(align=True)
            col3.separator()
            col3.label("Kaleidoscope add-on has the feature to sync the Saved Palettes and Values in a cloud storage.")
            col3.label("This allows you to Use Saved palettes and Values on any system, anywhere.")
            col3.label()
            col3.label("Instructions to setup Syncing:")
            col3.label("   1) Start by signing up with a Cloud Storage Service (Eg. Dropbox, Google Drive, etc.)")
            col3.label("   2) Then install the Desktop Application (NOTE: Only Popular Cloud Services Provide this)")
            col3.label("   3) Select the Sync folder that was created by Desktop Application, in the sync path above")
            col3.label()
            col3.label("It's done. Whatever is saved in that folder, would automatically transfer to the Cloud which can be used later on.")
            col3.label()
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("Keys:")
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("- Saved Locally, and is NOT synced.", icon='FILE')
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("- NOT saved Locally, but is synced.", icon='WORLD')
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("- Saved Locally and synced too.", icon='URL')
            col3.separator()
            col3.separator()
            row = col3.row(align=True)
            row.scale_y = 1.15
            row.label()
            row.operator('wm.url_open', text="Video Tutorial", icon='CLIP').url = "http://blskl.cf/kaldocs"
            row.label()
            col3.separator
        col4 = box.column(align=True)
        col4.separator()
        addon_updater_ops.update_settings_ui(self, context, box)

        row = box.row(align=True)
        split = row.split(percentage=0.8)
        col1 = split.column(align=True)
        row1 = col1.row(align=True)
        row1.separator()
        row1_1 = row1.row(align=True)
        row1_1.alignment = 'CENTER'
        row1_1.label("Created by Akash Hamirwasia")
        col2 = split.column(align=True)
        row2 = col2.row()
        row2.scale_y = 1.2
        row2.operator('wm.url_open', text="Support Me", icon='SOLO_ON').url="http://blskl.cf/kalsupport"

class KaleidoscopeImport(bpy.types.Operator, ImportHelper): #Importing Files
    """Install .zip file in the add-on"""
    bl_idname = "kaleidoscope.install_files"
    bl_label = "Install Files"

    filename_ext = ".kal"

    filter_glob = bpy.props.StringProperty(
            default="*.kal",
            options={'HIDDEN'},
            )
    def execute(self, context):
        try:
            zipref = zipfile.ZipFile(self.filepath, 'r')
            path = os.path.dirname(__file__)
            if (path != ""):
                zipref.extractall(path) #Extract to the Enrich add-on Folder
                zipref.close()
            bpy.context.scene.kaleidoscope_props.import_files = False
        except:
            bpy.context.scene.kaleidoscope_props.import_files = True
        return {'FINISHED'}

class KaleidoscopeExport(bpy.types.Operator, ExportHelper):
    """Export the Saved Palettes and Values in a .zip format"""
    bl_idname = 'kaleidoscope.export_files'
    bl_label = 'Export Files'

    filename_ext = ".zip"

    filter_glob = bpy.props.StringProperty(
            default="*.zip",
            options={'HIDDEN'}
            )

    def execute(self, context):
        try:
            if self.filepath.endswith(".zip") == False:
                self.filepath = self.filepath+".zip"

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
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        zf.write(absname, arcname)
            zf.close()
            self.report({'INFO'}, "Files Exported Successfully to "+self.filepath)
        except:
            self.report({'ERROR'}, "There was an error, please check the file path!")
        return{'FINISHED'}

class KaleidoscopeProps(bpy.types.PropertyGroup):
    def set_sync_path(self, context):
        settings = {"sync_directory": bpy.context.scene.kaleidoscope_props.sync_path}
        path = os.path.join(os.path.dirname(__file__), "settings.json")
        s = json.dumps(settings, sort_keys=True)
        with open(path, 'w') as f:
            f.write(s)
        return None

    import_files = bpy.props.BoolProperty(name="Kaleidoscope Import", description="Checks if the zip file is properly imported", default=False)
    sync_help = bpy.props.BoolProperty(name="Syncing Information", description="View/Hide Information on how to setup Syncing", default=False)

    check = False
    val = None
    try:
        f = open(os.path.join(os.path.dirname(__file__), "settings.json"), 'r')
        settings = json.load(f)
        val = settings["sync_directory"]
        check = True
    except:
        check = False
    if check == True:
        sync_path = bpy.props.StringProperty(name="Sync Path", description="Select the Directory to Sync", subtype='DIR_PATH', default=val, update=set_sync_path)
    else:
        sync_path = bpy.props.StringProperty(name="Sync Path", description="Select the Directory to Sync", subtype='DIR_PATH', default="", update=set_sync_path)

def register():
    bpy.utils.register_module(__name__)
    spectrum.register()
    intensity.register()
    addon_updater_ops.register(bl_info)
    bpy.types.Scene.kaleidoscope_props = bpy.props.PointerProperty(type=KaleidoscopeProps)
    nodeitems_utils.register_node_categories("KALEIDOSCOPE_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("KALEIDOSCOPE_NODES")
    spectrum.unregister()
    intensity.unregister()
    addon_updater_ops.unregister()
    del bpy.types.Scene.kaleidoscope_props
    bpy.utils.unregister_module(__name__)
