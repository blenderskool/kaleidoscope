bl_info = {
    "name": "Prism - A small package of nodes for Cycles Materials",
    "author": "Akash Hamirwasia",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "Cycles > NodeEditor > MaterialView > Add Node Menu",
    "description": "A Complete Toolkit of Nodes to Make your Materials even more colorful and physically accurate",
    "warning": "",
    "wiki_url": "http://www.blenderskool.cf",
    "tracker_url": "",
    "category": "Node"}

import bpy
from . import spectrum, intensity
import nodeitems_utils, zipfile, os
import urllib
import urllib.request
from nodeitems_utils import NodeCategory, NodeItem
from bpy_extras.io_utils import ImportHelper

class PrismCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        b = False
        if context.space_data.tree_type == 'ShaderNodeTree':
            b = True
        return b

# all categories in a list
node_categories = [
    PrismCategory("PRISMNODES", "Prism", items=[
        NodeItem("spectrum_palette.node"),
        NodeItem("intensity.node")
        ]),
    ]

class Prism(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
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
        row.operator(Prism_Import.bl_idname, text='Import Files', icon='PACKAGE') #Install Presets button
        row.label("")
        col.label()
        if bpy.context.scene.prism_props_import_files == True:
            col.label("There was a problem in importing the files.", icon='ERROR')

class Prism_Import(bpy.types.Operator, ImportHelper): #Importing Presets
    """Install .zip file in the add-on"""
    bl_idname = "enrich.install_presets"
    bl_label = "Install Files"

    filename_ext = ".zip"

    filter_glob = bpy.props.StringProperty(
            default="*.zip",
            options={'HIDDEN'},
            )

    def execute(self, context):
        try:
            zipref = zipfile.ZipFile(self.filepath, 'r')
            path = os.path.dirname(__file__)
            if (path != ""):
                zipref.extractall(path) #Extract to the Enrich add-on Folder
                zipref.close()
            bpy.context.scene.prism_props_import_files = False
        except:
            bpy.context.scene.prism_props_import_files = True
        return {'FINISHED'}

def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        pass
    spectrum.register()
    intensity.register()
    bpy.types.Scene.prism_props_import_files = bpy.props.BoolProperty(name="Prism Import", description="Checks if the zip file is properly imported", default=False)
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    spectrum.unregister()
    intensity.unregister()
    del bpy.types.Scene.prism_props_import_files
    bpy.utils.unregister_module(__name__)
