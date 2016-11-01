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
import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

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

def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        pass
    spectrum.register()
    intensity.register()
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)

def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    spectrum.unregister()
    intensity.unregister()
    bpy.utils.unregister_module(__name__)
