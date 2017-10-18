# Spectrum Palette Node
import bpy
import json, os
import urllib.request
from bpy.types import Node
from mathutils import Color
from collections import Counter
import random
import requests, math
import xml.etree.ElementTree as ET
from . import client
if "bpy" in locals():
    import importlib
    importlib.reload(client)

PaletteHistory = []
Palette_idHistory = [0, 0, 0]
palette = {}

shuffle_time = 1
before_shuffle_colors=[]

community_maintain = False
community_palette = {}
online_check = True

lovers_id = None
for i in range(1, 16):
    PaletteHistory.append(Color())

for i in range(0, 15):
    if i % 5 == 0:
        PaletteHistory[i].r = 0.009
        PaletteHistory[i].g = 0.421
        PaletteHistory[i].b = 0.554
    elif i % 5 == 1:
        PaletteHistory[i].r = 0.267
        PaletteHistory[i].g = 0.639
        PaletteHistory[i].b = 0.344
    elif i % 5 == 2:
        PaletteHistory[i].r = 0.612
        PaletteHistory[i].g = 0.812
        PaletteHistory[i].b = 0.194
    elif i % 5 == 3:
        PaletteHistory[i].r = 0.974
        PaletteHistory[i].g = 0.465
        PaletteHistory[i].b = 0.08
    elif i % 5 == 4:
        PaletteHistory[i].r = 1.0
        PaletteHistory[i].g = 0.08
        PaletteHistory[i].b = 0.087

class SpectrumTreeNode:
    @classmethod
    def poll(cls, ntree):
        b = False
        if ntree.bl_idname == 'ShaderNodeTree':
            b = True
        return b

class SpectrumProperties(bpy.types.PropertyGroup):
    """Properties of Spectrum which are created for every new scene"""
    def update_color_1(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 1"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color1
                        update_caller(self, input_name="Color 1")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 1"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color1
                        update_caller(self, input_name="Color 1")
        for lamps in bpy.data.lamps:
            if lamps.node_tree is not None:
                for node in lamps.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 1"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color1
                        update_caller(self, input_name="Color 1")
        return None

    def update_color_2(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 2"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color2
                        update_caller(self, input_name="Color 2")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 2"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color2
                        update_caller(self, input_name="Color 2")
        for lamps in bpy.data.lamps:
            if lamps.node_tree is not None:
                for node in lamps.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 2"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color2
                        update_caller(self, input_name="Color 2")
        return None

    def update_color_3(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 3"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color3
                        update_caller(self, input_name="Color 3")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 3"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color3
                        update_caller(self, input_name="Color 3")
        for lamps in bpy.data.lamps:
            if lamps.node_tree is not None:
                for node in lamps.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 3"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color3
                        update_caller(self, input_name="Color 3")
        return None
    def update_color_4(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 4"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color4
                        update_caller(self, input_name="Color 4")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 4"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color4
                        update_caller(self, input_name="Color 4")
        for lamps in bpy.data.lamps:
            if lamps.node_tree is not None:
                for node in lamps.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 4"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color4
                        update_caller(self, input_name="Color 4")
        return None

    def update_color_5(self, context):
        for world in bpy.data.worlds:
            if world.node_tree is not None:
                for node in world.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 5"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color5
                        update_caller(self, input_name="Color 5")
        for mat in bpy.data.materials:
            if mat.node_tree is not None:
                for node in mat.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 5"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color5
                        update_caller(self, input_name="Color 5")
        for lamps in bpy.data.lamps:
            if lamps.node_tree is not None:
                for node in lamps.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        node.outputs["Color 5"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color5
                        update_caller(self, input_name="Color 5")
        return None
    def set_type(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        kaleidoscope_spectrum_props.random_int = int(kaleidoscope_spectrum_props.gen_type)
        kaleidoscope_spectrum_props.random_custom_int = int(kaleidoscope_spectrum_props.custom_gen_type)
        kaleidoscope_spectrum_props.random_online_int = int(kaleidoscope_spectrum_props.online_type)
        return None
    def set_global_settings(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        c = Color()
        for i in range(0,5):
            if kaleidoscope_spectrum_props.history_count == 0:
                exec("c.r = PaletteHistory[1"+str(i)+"].r")
                exec("c.g = PaletteHistory[1"+str(i)+"].g")
                exec("c.b = PaletteHistory[1"+str(i)+"].b")
            elif kaleidoscope_spectrum_props.history_count == 1:
                exec("c.r = PaletteHistory["+str(i+5)+"].r")
                exec("c.g = PaletteHistory["+str(i+5)+"].g")
                exec("c.b = PaletteHistory["+str(i+5)+"].b")
            elif kaleidoscope_spectrum_props.history_count == 2:
                exec("c.r = PaletteHistory["+str(i)+"].r")
                exec("c.g = PaletteHistory["+str(i)+"].g")
                exec("c.b = PaletteHistory["+str(i)+"].b")
            c.v = c.v+kaleidoscope_spectrum_props.value_slider
            c.s = c.s+kaleidoscope_spectrum_props.saturation_slider
            c.h = c.h+kaleidoscope_spectrum_props.hue_slider
            exec("kaleidoscope_spectrum_props.color"+str(i+1)+" = c.r, c.g, c.b, 1.0")
            exec("kaleidoscope_spectrum_props.color"+str(i+1)+" = c.r, c.g, c.b, 1.0")
            exec("kaleidoscope_spectrum_props.color"+str(i+1)+" = c.r, c.g, c.b, 1.0")
        return None
    def get_saved_palettes(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        saved_palettes_list = []
        global_palette = []
        local_palette = []
        synced_palette = []

        check = False
        val = None
        try:
            f = open(os.path.join(os.path.dirname(__file__), "settings.json"), 'r')
            settings = json.load(f)
            val = os.path.join(settings['sync_directory'], "palettes")
            f.close()
            check = True
        except:
            check = False

        if val is not None:
            if not os.path.exists(val):
                os.makedirs(val)

        if check == True:
            for sub in os.listdir(val):
                if os.path.isfile(os.path.join(val, str(sub))):
                    name = str(sub)
                    if name.endswith('.json'):
                        name = name[:-5]
                        name = name.title()
                        name = name.replace('_', ' ')
                        global_palette.append(name)

        i=0
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "palettes")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "palettes"))

        for sub in os.listdir(os.path.join(os.path.dirname(__file__), "palettes")):
            if os.path.isfile(os.path.join(os.path.dirname(__file__), "palettes", str(sub))):
                name = str(sub)
                if name.endswith('.json'):
                    name = name[:-5]
                    name = name.title()
                    name = name.replace('_', ' ')
                    if name in global_palette:
                        saved_palettes_list.append((name, name, "Choose the Saved Palette from Library", "URL", i))
                        synced_palette.append(name)
                    else:
                        saved_palettes_list.append((name, name, "Choose the Saved Palette from Local Library", "FILE", i))
                        local_palette.append(name)
            i=i+1

        if check == True:
            for sub in os.listdir(val):
                if os.path.isfile(os.path.join(val, str(sub))):
                    name = str(sub)
                    if name.endswith('.json'):
                        name = name[:-5]
                        name = name.title()
                        name = name.replace('_', ' ')
                        if name not in synced_palette and name not in local_palette:
                            saved_palettes_list.append((name, name, "Choose the Saved Palette from the Synced Library", "WORLD", i))
                i=i+1

        return saved_palettes_list
    def import_saved_palette(self, context):
        kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
        name = kaleidoscope_spectrum_props.saved_palettes
        name = name.lower()
        name = name.replace(' ', '_')
        name = name+".json"
        try:
            path = os.path.join(os.path.dirname(__file__), "palettes", name)
            palette_file = open(path, 'r')
            self.palette = json.load(palette_file)
        except:
            if bpy.context.scene.kaleidoscope_props.sync_path != '':
                path = os.path.join(bpy.context.scene.kaleidoscope_props.sync_path, "palettes", name)
                palette_file = open(path, 'r')
                self.palette = json.load(palette_file)
        for i in range(1, 6):
            exec("kaleidoscope_spectrum_props.color"+str(i)+" = hex_to_rgb(self.palette[kaleidoscope_spectrum_props.saved_palettes]['color"+str(i)+"'])")
        palette_file.close()
        set_palettes_list(self, context)
        return None

    def set_ramp(self, context):
        set_color_ramp(self)
        return None

    def set_base_color(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        if kaleidoscope_spectrum_props.use_realtime_base == True:
            bpy.ops.spectrum_palette.palette_gen('INVOKE_DEFAULT')
        return None

    value_slider = bpy.props.FloatProperty(name="Global Brightness", description="Control the Overall Brightness of the Palette", min=-0.5, max=0.5, default=0.0, update=set_global_settings)
    saturation_slider = bpy.props.FloatProperty(name="Global Saturation", description="Control the Overall Saturation of the Palette", min=-0.5, max=0.5, default=0.0, update=set_global_settings)
    hue_slider = bpy.props.FloatProperty(name="Global Hue", description="Control the Overall Hue of the Palette", min=0.0, max=1.0, default=0, update=set_global_settings)
    color1 = bpy.props.FloatVectorProperty(name="Color1", description="Set Color 1 for the Palette", subtype="COLOR", default=(0.009, 0.421, 0.554,1.0), size=4, max=1.0, min=0.0, update=update_color_1)
    color2 = bpy.props.FloatVectorProperty(name="Color2", description="Set Color 2 for the Palette", subtype="COLOR", default=(0.267, 0.639, 0.344,1.0), size=4, max=1.0, min=0.0, update=update_color_2)
    color3 = bpy.props.FloatVectorProperty(name="Color3", description="Set Color 3 for the Palette", subtype="COLOR", default=(0.612, 0.812, 0.194,1.0), size=4, max=1.0, min=0.0, update=update_color_3)
    color4 = bpy.props.FloatVectorProperty(name="Color4", description="Set Color 4 for the Palette", subtype="COLOR", default=(0.974, 0.465, 0.08,1.0), size=4, max=1.0, min=0.0, update=update_color_4)
    color5 = bpy.props.FloatVectorProperty(name="Color5", description="Set Color 5 for the Palette", subtype="COLOR", default=(1.0, 0.08, 0.087,1.0), size=4, max=1.0, min=0.0, update=update_color_5)

    hue = bpy.props.FloatVectorProperty(name="Hue", description="Set the Color for the Base Color to be used in Palette Generation", subtype="COLOR", size=4, max=1.0, min=0.0, default=(random.random(), random.random(), random.random(), 1.0), update=set_base_color)
    gen_type = bpy.props.EnumProperty(name="Type of Palette", description="Select the Rule for the Color Palette Generation", items=(('0','Monochromatic','Use Monochromatic Rule for Palette'),('1','Analogous','Use Analogous Rule for Palette'),('2','Complementary','Use Complementary Rule for Palette'),('3','Triadic','Use Triadic Rule for Palette'),('4','Custom','Use Custom Rule for Palette')), update=set_type, default="0")
    custom_gen_type = bpy.props.EnumProperty(name="Type of Custom Rule", description="Select the Custom rule for Custom Palette Generation", items=(('0', 'Vibrant', 'Uses Two Vibrant Colors, along with shades of black and white'), ('1', 'Gradient', 'Use Color with same hue, but gradual change in Saturation and Value'), ('2', 'Pop out', 'Pop out effect uses one color in combination with shades of black and white'), ('4', 'Online', 'Get Color Palettes from Internet'), ('3', 'Random Rule', 'Use any Rule or color Effect to generate the palette'), ('5', 'Random', 'Randomly Generated Color scheme, not following any rule!'), ('6', 'Image', 'Use Image')), update=set_type, default="0")
    online_type = bpy.props.EnumProperty(name="Type of Online Palette", description="Select the Type of Online Palettes", items=(('0', 'Standard', 'Use the Online Palettes that I have selected just for you. This includes the best picks by me'), ('1', 'Community', 'Explore the Color Palettes added by users all around the world'), ('2', 'COLOURlovers', '')), default='0', update=set_type)
    saved_palettes = bpy.props.EnumProperty(name="Saved Palettes", description="Stores the Saved Palettes", items=get_saved_palettes, update=import_saved_palette)

    use_custom = bpy.props.BoolProperty(name="Use Custom", description="Use Custom Values for Base Color", default=False)
    use_global = bpy.props.BoolProperty(name="Use Global Controls", description="Use Global Settings to control the overall Color of the Palette", default=False)
    use_internet_libs = bpy.props.BoolProperty(name="Internet Library Checker", description="Checks if the palette generated is from Internet library", default=False)
    use_organize = bpy.props.BoolProperty(name="Organize the Color Palette", description="Organize the Color palette generated", default=False)
    use_realtime_base = bpy.props.BoolProperty(name="Real Time Base Color", description="Use Real time Update of the Base Color in the Palette", default=False)
    view_help = bpy.props.BoolProperty(name="Color Rule Help", description="Get some knowledge about this color rule", default=False)
    assign_colorramp_world = bpy.props.BoolProperty(name="Assign ColorRamp World", description="Assign the Colors from Spectrum to ColorRamp in the World Material", default=False, update=set_ramp)

    random_int = bpy.props.IntProperty(name="Random Integer", description="Used to use Random color rules and effects", default=0)
    random_custom_int = bpy.props.IntProperty(name="Random Custom Integer", description="Used to use Random color rules and effects", default=0)
    random_online_int = bpy.props.IntProperty(name="Random Online Integer", description="Used the use Random color rules from online type", default=0)
    new_file = bpy.props.IntProperty(name="File Count",description="", default=1)
    new_community_file = bpy.props.IntProperty(name="Community File Count",description="", default=1)
    online_palette_index = bpy.props.IntProperty(name="Palette Index", description="Stores the Index of the Online Palette")

    history_count = bpy.props.IntProperty(name="History Counter", description="Value to Count the Current History Value", default=0)

    save_palette_name = bpy.props.StringProperty(name="Save Palette Name", description="Name to be used to save this palette", default="My Palette")
    colorramp_world_name = bpy.props.StringProperty(name="ColorRamp name World", description="Select the ColorRamp in the World Material to assign the Colors", default="", update=set_ramp)
    img_name = bpy.props.StringProperty(name = "Choose a Texture",description="Load an Image Texture",subtype='FILE_PATH')

class SpectrumMaterialProps(bpy.types.PropertyGroup):
    """Spectrum Properties for Every Material"""

    def set_ramp(self, context):
        set_color_ramp(self)
        return None

    colorramp_name = bpy.props.StringProperty(name="ColorRamp name", description="Select the ColorRamp to assign the Colors", default="", update=set_ramp)
    assign_colorramp = bpy.props.BoolProperty(name="Assign ColorRamp", description="Assign the Colors from Spectrum to ColorRamp in the Object Material", default=False, update=set_ramp)

def set_color_ramp(self):
    """Set the Colors from the Palette to a ColorRamp node"""
    kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
    ramp = None
    ramp_world = None
    if kaleidoscope_spectrum_props.assign_colorramp_world == True:
        try:
            try:
                ramp_world = bpy.context.scene.world.node_tree.nodes[kaleidoscope_spectrum_props.colorramp_world_name].color_ramp
            except:
                if kaleidoscope_spectrum_props.assign_colorramp_world == True:
                    try:
                        self.report({'WARNING'}, "There is Not a Valid ColorRamp Node in the World Material")
                    except AttributeError:
                        pass
            if kaleidoscope_spectrum_props.colorramp_world_name != "" and kaleidoscope_spectrum_props.assign_colorramp_world == True:
                try:
                    for i in range(0, len(ramp_world.elements)):
                            if kaleidoscope_spectrum_props.assign_colorramp_world == True:
                                exec("ramp_world.elements["+str(i)+"].color[0] = kaleidoscope_spectrum_props.color"+str(i+1)+"[0]")
                                exec("ramp_world.elements["+str(i)+"].color[1] = kaleidoscope_spectrum_props.color"+str(i+1)+"[1]")
                                exec("ramp_world.elements["+str(i)+"].color[2] = kaleidoscope_spectrum_props.color"+str(i+1)+"[2]")
                                ramp_world.elements[0].color[3] = 1.0
                except:
                    pass
        except:
            pass

    for mat in bpy.data.materials:
        spectrum_active = mat.kaleidoscope_spectrum_props
        if spectrum_active.assign_colorramp == True and spectrum_active.colorramp_name != "":
            try:
                if spectrum_active is not None:
                    ramp = mat.node_tree.nodes[spectrum_active.colorramp_name].color_ramp
            except:
                if spectrum_active.assign_colorramp == True:
                    try:
                        self.report({'WARNING'}, "There is Not a Valid ColorRamp Node in '"+mat.name+"'")
                    except AttributeError:
                        pass
            if spectrum_active.colorramp_name != "" and spectrum_active.assign_colorramp == True:
                try:
                    for i in range(0, len(ramp.elements)):
                            if spectrum_active.assign_colorramp == True:
                                exec("ramp.elements["+str(i)+"].color[0] = kaleidoscope_spectrum_props.color"+str(i+1)+"[0]")
                                exec("ramp.elements["+str(i)+"].color[1] = kaleidoscope_spectrum_props.color"+str(i+1)+"[1]")
                                exec("ramp.elements["+str(i)+"].color[2] = kaleidoscope_spectrum_props.color"+str(i+1)+"[2]")
                                ramp.elements[0].color[3] = 1.0
                except:
                    pass

class SpectrumNode(Node, SpectrumTreeNode):
    """The Spectrum Node with all the Attributes"""
    bl_idname = 'spectrum_palette.node'
    bl_label = 'Spectrum Palette'
    bl_icon = 'NONE'
    bl_width_min = 226.0
    bl_width_max = 350.0

    def init(self, context):
        self.outputs.new('NodeSocketColor', "Color 1")
        self.outputs.new('NodeSocketColor', "Color 2")
        self.outputs.new('NodeSocketColor', "Color 3")
        self.outputs.new('NodeSocketColor', "Color 4")
        self.outputs.new('NodeSocketColor', "Color 5")
        self.outputs["Color 1"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color1
        self.outputs["Color 2"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color2
        self.outputs["Color 3"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color3
        self.outputs["Color 4"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color4
        self.outputs["Color 5"].default_value = bpy.context.scene.kaleidoscope_spectrum_props.color5
        self.width = 226

    def update(self):
        if bpy.context.scene.render.engine == 'CYCLES':
            out = ""
            try:
                for world in bpy.data.worlds:
                    for node in world.node_tree.nodes:
                        if node.bl_idname == 'spectrum_palette.node':
                            for out in node.outputs:
                                if out.is_linked:
                                    for o in out.links:
                                        if o.is_valid:
                                            if o.to_node.bl_idname == "NodeReroute":
                                                update_reroutes("WorldNodeTree", world.name, node.name, o.to_node.name, out.name)
                                            o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
            except:
                pass

            try:
                for lamps in bpy.data.lamps:
                    try:
                        for node in lamps.node_tree.nodes:
                            if node.bl_idname == 'spectrum_palette.node':
                                for out in node.outputs:
                                    if out.is_linked:
                                        for o in out.links:
                                            if o.is_valid:
                                                if o.to_node.bl_idname == "NodeReroute":
                                                    update_reroutes("LampNodeTree", lamps.name, node.name, o.to_node.name, out.name)
                                                o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
                    except:
                        continue
            except:
                pass
            try:
                for mat in bpy.data.materials:
                    try:
                        for node in mat.node_tree.nodes:
                            if node.bl_idname == 'spectrum_palette.node':
                                for out in node.outputs:
                                    if out.is_linked:
                                        for o in out.links:
                                            if o.is_valid:
                                                if o.to_node.bl_idname == "NodeReroute":
                                                    update_reroutes("ShaderNodeTree", mat.name, node.name, o.to_node.name, out.name)
                                                o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
                    except:
                        continue
            except:
                pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        SpectrumPaletteUI(self, context, layout)

    #Node Label
    def draw_label(self):
        return "Spectrum Palette"

def SpectrumPaletteUI(self, context, layout):
    """Spectrum Palette Interface, which can be accessed from any other class"""
    kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
    col = layout.column(align=True)
    row = col.row(align=True)
    split = row.split(percentage=0.8)
    col1 = split.column(align=True)
    col1.prop(kaleidoscope_spectrum_props, "gen_type", text="Rule")
    if kaleidoscope_spectrum_props.gen_type == "4":
        col1.prop(kaleidoscope_spectrum_props, "custom_gen_type", "Type")
        if kaleidoscope_spectrum_props.custom_gen_type == "4":
            col1.prop(kaleidoscope_spectrum_props, "online_type", "Source")
    col2 = split.column()
    row2 = col2.row(align=True)
    colr = row2.column(align=True)
    if (kaleidoscope_spectrum_props.gen_type != '4' or kaleidoscope_spectrum_props.custom_gen_type == '3' or kaleidoscope_spectrum_props.custom_gen_type == '0' or kaleidoscope_spectrum_props.custom_gen_type == '2') and kaleidoscope_spectrum_props.use_internet_libs == False:
        colr.enabled = True
    else:
        colr.enabled = False
    if kaleidoscope_spectrum_props.use_organize == False:
        colr.prop(kaleidoscope_spectrum_props, "use_organize", toggle=True, text="", icon='SNAP_OFF', emboss=False)
    else:
        colr.prop(kaleidoscope_spectrum_props, "use_organize", toggle=True, text="", icon='SNAP_ON', emboss=False)
    colr = row2.column(align=True)
    colr.prop(kaleidoscope_spectrum_props, "view_help", toggle=True, text="", icon='INFO', emboss=False)
    if kaleidoscope_spectrum_props.view_help == True:
        box = layout.box()
        col_box = box.column(align=True)
        if kaleidoscope_spectrum_props.gen_type == "0":
            col_box.label("Monochromatic Scheme is the")
            col_box.label("most basic color rule. It has")
            col_box.label("colors of same hue, but with")
            col_box.label("varying saturation and")
            col_box.label("brightness. It is useful when")
            col_box.label("used in a proper way.")
            col_box.label()
        elif kaleidoscope_spectrum_props.gen_type == "1":
            col_box.label("Analogous Scheme uses")
            col_box.label("colors of different hues. It")
            col_box.label("uses one color as base color")
            col_box.label("and uses colors near it in the")
            col_box.label("color wheel, with varying")
            col_box.label("saturation and brightness.")
            col_box.label()
        elif kaleidoscope_spectrum_props.gen_type == "2":
            col_box.label("Complementary Scheme is")
            col_box.label("interesting rule where colors")
            col_box.label("opposite to each other in the")
            col_box.label("color wheel are used. This")
            col_box.label("scheme should be used")
            col_box.label("carefully because of contrasting")
            col_box.label("shades.")
            col_box.label()
        elif kaleidoscope_spectrum_props.gen_type == "3":
            col_box.label("Triadic Scheme uses")
            col_box.label("one color as base color")
            col_box.label("and other two colors are")
            col_box.label("chosen from the color wheel")
            col_box.label("such that all three form an")
            col_box.label("equilateral triangle.")
            col_box.label()
        elif kaleidoscope_spectrum_props.gen_type == "4":
            col_box.label("Custom schemes are some")
            col_box.label("simple rules exclusive to")
            col_box.label("this add-on")
            col_box.label()
            if kaleidoscope_spectrum_props.custom_gen_type == "0":
                col_box.label("Vibrant scheme uses two")
                col_box.label("visually appealing color shades")
                col_box.label("and others are shades of black")
                col_box.label("and white")
                col_box.label()
            elif kaleidoscope_spectrum_props.custom_gen_type == "1":
                col_box.label("Gradient scheme is similar")
                col_box.label("to Monochromatic scheme, and")
                col_box.label("it uses fixed hue with fixed")
                col_box.label("change and goes light to dark")
                col_box.label("from left to form gradient of")
                col_box.label("colors.")
                col_box.label()
            elif kaleidoscope_spectrum_props.custom_gen_type == "2":
                col_box.label("Pop Out scheme is similar to")
                col_box.label("Vibrant scheme, but this uses")
                col_box.label("two same colors and other three")
                col_box.label("are shades of black and white.")
                col_box.label("Really Minimal Color Scheme.")
                col_box.label()
            elif kaleidoscope_spectrum_props.custom_gen_type == "4":
                if kaleidoscope_spectrum_props.online_type == "0":
                    col_box.label("Standard Online mode provides")
                    col_box.label("you with some amazing color")
                    col_box.label("palettes that I have personally")
                    col_box.label("added for you.")
                    col_box.label()
                elif kaleidoscope_spectrum_props.online_type == "1":
                    col_box.label("Community Online mode provides")
                    col_box.label("you with the published color")
                    col_box.label("palettes that users have added")
                    col_box.label("using the add-on.")
                    col_box.label()
                    col_box.label("NOTE: I don't personally add")
                    col_box.label("palettes to this list. If palette")
                    col_box.label("does not look good, it will get")
                    col_box.label("removed")
                    col_box.label()
                elif kaleidoscope_spectrum_props.online_type == "2":
                    col_box.label("COLOURlovers site has amazing")
                    col_box.label("color palettes added by users.")
                    col_box.label("This Source provides you with all")
                    col_box.label("those amazing palettes directly")
                    col_box.label("inside Blender.")
                    col_box.label()
            elif kaleidoscope_spectrum_props.custom_gen_type == "3":
                col_box.label("Random option allows you to")
                col_box.label("generate a palette from any rule")
                col_box.label("in a click. It is helpful when")
                col_box.label("you need want to find the best")
                col_box.label("palette of a base color.")
                col_box.label()
            elif kaleidoscope_spectrum_props.custom_gen_type == "5":
                col_box.label("If you are really angry, and")
                col_box.label("want to try any color for your")
                col_box.label("scene, then use this option.")
                col_box.label("This option 'Randomly' generates")
                col_box.label("the colors for the palette.")
                if kaleidoscope_spectrum_props.use_internet_libs == True:
                    col_box.label()
        if kaleidoscope_spectrum_props.use_internet_libs == True:
            if kaleidoscope_spectrum_props.custom_gen_type == '3':
                if kaleidoscope_spectrum_props.random_online_int != 2:
                    col_box.label("Palette ID: "+str(kaleidoscope_spectrum_props.online_palette_index+1))
                elif kaleidoscope_spectrum_props.random_online_int == 2:
                    col_box.label("Palette ID: "+str(lovers_id))
            else:
                if kaleidoscope_spectrum_props.online_type != "2":
                    col_box.label("Palette ID: "+str(kaleidoscope_spectrum_props.online_palette_index+1))
                elif kaleidoscope_spectrum_props.online_type == "2":
                    col_box.label("Palette ID: "+str(lovers_id))
            row = col_box.row(align=True)
            row.scale_y = 1.1
            row.operator("wm.url_open", text="Problem?", icon="HELP").url="http://blskl.cf/kalbugs"
        if kaleidoscope_spectrum_props.gen_type != '4' and kaleidoscope_spectrum_props.custom_gen_type != '4':
            col_box.label()
        col_box.prop(kaleidoscope_spectrum_props, "view_help", text="Close Help", icon='INFO')
    col = layout.column(align=True)
    if kaleidoscope_spectrum_props.use_internet_libs == False:
        col.enabled = True
    else:
        col.enabled = False
    if kaleidoscope_spectrum_props.gen_type == "4" and kaleidoscope_spectrum_props.custom_gen_type == "4":
        col.enabled = False
    if kaleidoscope_spectrum_props.use_custom == False:
        col.prop(kaleidoscope_spectrum_props, "use_custom", text="Use Custom Base Color", toggle=True, icon="LAYER_USED")
    else:
        col.prop(kaleidoscope_spectrum_props, "use_custom", text="Hide Custom Base Color", toggle=True, icon="LAYER_ACTIVE")
        box = col.box()

        col1 = box.column()
        row = col1.row(align=True)
        row.label("Base Color:")
        row.prop(kaleidoscope_spectrum_props, "hue", text="")
        row.prop(kaleidoscope_spectrum_props, "use_realtime_base", text="", icon='RESTRICT_VIEW_OFF')

    col2 = layout.column(align=True)
    row = col2.row(align=True)
    row.prop(kaleidoscope_spectrum_props, "color1", text="")
    row.prop(kaleidoscope_spectrum_props, "color2", text="")
    row.prop(kaleidoscope_spectrum_props, "color3", text="")
    row.prop(kaleidoscope_spectrum_props, "color4", text="")
    row.prop(kaleidoscope_spectrum_props, "color5", text="")
    row2 = col2.row(align=True)
    row2.scale_y = 1.2
    row2.operator(PaletteGenerate.bl_idname, text="Refresh Palette", icon="COLOR")
    col3 = layout.column(align=True)
    if online_check == False:
        col3.label("There was some problem,", icon='ERROR')
        col3.label("try again")
    if community_maintain == True:
        col3.label("The Community Palettes,", icon='INFO')
        col3.label("are not available now")
    if kaleidoscope_spectrum_props.use_global == False:
        col3.prop(kaleidoscope_spectrum_props, "use_global", text="View Global Controls", icon='LAYER_USED', toggle=True)
    else:
        col3.prop(kaleidoscope_spectrum_props, "use_global", text="Hide Global Controls", icon='LAYER_ACTIVE', toggle=True)
        box = col3.box()
        col4 = box.column(align=True)
        row4 = col4.row(align=True)
        col4.prop(kaleidoscope_spectrum_props, "hue_slider", text="Hue", slider=True)
        col4.prop(kaleidoscope_spectrum_props, "saturation_slider", text="Saturation", slider=True)
        col4.prop(kaleidoscope_spectrum_props, "value_slider", text="Value", slider=True)

    col4 = layout.column(align=True)
    col4.label()
    row4 = col4.row(align=True)
    if kaleidoscope_spectrum_props.history_count != 2:
        row4.operator(PreviousPalette.bl_idname, text="", icon="TRIA_LEFT")
    else:
        row4.separator()
        row4.separator()
    row4.operator(PaletteInvert.bl_idname, text="Invert", icon="ARROW_LEFTRIGHT")
    row4.operator(PaletteShuffle.bl_idname, text="Shuffle", icon="LOOP_BACK")
    if kaleidoscope_spectrum_props.history_count != 0:
        row4.operator(NextPalette.bl_idname, text="", icon="TRIA_RIGHT")
    else:
        row4.separator()
        row4.separator()
    col4.label()
    row5 = col4.row(align=True)
    if len(kaleidoscope_spectrum_props.saved_palettes) !=0:
        row5.prop(kaleidoscope_spectrum_props, "saved_palettes", text="")
    else:
        row5.label("No Saved Palettes")
    row5.operator(client.SavePaletteMenu.bl_idname, text="", icon='ZOOMIN')
    if len(kaleidoscope_spectrum_props.saved_palettes) != 0:
        row5.operator(client.DeletePaletteMenu.bl_idname, text="", icon='ZOOMOUT')

    row5.operator(client.PublishPaletteMenu.bl_idname, text="", icon='WORLD')
    col4.label()
    #col4.prop(kaleidoscope_spectrum_props, "img_name")
    row6 = col4.row(align=True)
    try:
        if bpy.context.space_data.shader_type == 'WORLD':
            row6.prop_search(kaleidoscope_spectrum_props,"colorramp_world_name", bpy.context.scene.world.node_tree, "nodes",text="Ramp", icon='NODETREE')
            row6.prop(kaleidoscope_spectrum_props, "assign_colorramp_world", text="", icon='RESTRICT_COLOR_ON', toggle=True)
        elif bpy.context.space_data.shader_type == 'OBJECT':
            row6.prop_search(bpy.context.object.active_material.kaleidoscope_spectrum_props,"colorramp_name", bpy.context.object.active_material.node_tree, "nodes",text="Ramp", icon='NODETREE')
            row6.prop(bpy.context.object.active_material.kaleidoscope_spectrum_props, "assign_colorramp", text="", icon='RESTRICT_COLOR_ON', toggle=True)
        col4.label()
    except:
        pass
    row7 = col4.row(align=True)
    row7_1 = row7.row(align=True)
    row7_1.alignment = 'CENTER'
    row7_1.label("Akash Hamirwasia")
    row7_1.scale_y = 1.2
    row7_1.operator('wm.url_open', text="Support Me", icon='SOLO_ON').url='http://blskl.cf/kalsupport'

def update_caller(caller, input_name):
    kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
    for world in bpy.data.worlds:
        if world.node_tree is not None:
            for node in world.node_tree.nodes:
                if node.bl_idname == 'spectrum_palette.node':
                    if node.outputs[input_name].is_linked:
                        for o in node.outputs[input_name].links:
                            if o.is_valid:
                                if o.to_node.bl_idname == "NodeReroute":
                                    update_reroutes("WorldNodeTree", world.name, node.name, o.to_node.name, input_name)
                                o.to_socket.node.inputs[o.to_socket.name].default_value = node.outputs[input_name].default_value

    for mat in bpy.data.materials:
        if mat.node_tree is not None:
            for node in mat.node_tree.nodes:
                if node.bl_idname == 'spectrum_palette.node':
                    if node.outputs[input_name].is_linked:
                        for o in node.outputs[input_name].links:
                            if o.is_valid:
                                if o.to_node.bl_idname == "NodeReroute":
                                    update_reroutes("ShaderNodeTree", mat.name, node.name, o.to_node.name, input_name)
                                o.to_socket.node.inputs[o.to_socket.name].default_value = node.outputs[input_name].default_value

    for lamps in bpy.data.lamps:
        if lamps.node_tree is not None:
            try:
                for node in lamps.node_tree.nodes:
                    if node.bl_idname == 'spectrum_palette.node':
                        if node.outputs[input_name].is_linked:
                            for o in node.outputs[input_name].links:
                                if o.is_valid:
                                    if o.to_node.bl_idname == "NodeReroute":
                                        update_reroutes("LampNodeTree", lamps.name, node.name, o.to_node.name, input_name)
                                    o.to_socket.node.inputs[o.to_socket.name].default_value = node.outputs[input_name].default_value
            except:
                continue

    for mat in bpy.data.materials:
        if mat.kaleidoscope_spectrum_props.assign_colorramp == True or kaleidoscope_spectrum_props.assign_colorramp_world == True:
            set_color_ramp(caller)
            break

def update_reroutes(tree_type, material_name, kaleidoscope_node_name, reroute_name, input_name):
    if tree_type == "ShaderNodeTree":
        node_tree_type = bpy.data.materials[material_name]
    elif tree_type == "WorldNodeTree":
        node_tree_type = bpy.data.worlds[material_name]
    elif tree_type == "LampNodeTree":
        node_tree_type = bpy.data.lamps[material_name]
    else:
        return ("NodeTree Type not in [\"ShaderNodeTree\", \"WorldNodeTree\", \"LampNodeTree\"]")

    reroute = node_tree_type.node_tree.nodes[reroute_name]
    node = node_tree_type.node_tree.nodes[kaleidoscope_node_name]
    links = node_tree_type.node_tree.links
    try:
        if reroute.outputs['Output'].is_linked:
            for ro in reroute.outputs['Output'].links:
                if ro.is_valid:
                    next_node = node_tree_type.node_tree.nodes[ro.to_node.name]
                    links.new(node.outputs[input_name], next_node.inputs[ro.to_socket.name])
                    if next_node.bl_idname == "NodeReroute":
                        update_reroutes(tree_type, material_name, kaleidoscope_node_name, next_node.name, input_name)
    except:
        pass


def hex_to_rgb(value, alpha=True):
    """Convets a Hex code to a Blender RGB Value"""
    gamma = 2.2
    value = value.lstrip('#')
    lv = len(value)
    fin = list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    r = pow(fin[0] / 255, gamma)
    g = pow(fin[1] / 255, gamma)
    b = pow(fin[2] / 255, gamma)
    fin.clear()
    fin.append(r)
    fin.append(g)
    fin.append(b)
    if alpha == True:
        fin.append(1.0)
    return tuple(fin)

def rgb_to_hex(rgb):
    """Converts Blender RGB Value to Hex code"""
    gamma = 1/2.2
    fin = list(rgb)
    r = fin[0]*255
    g = fin[1]*255
    b = fin[2]*255
    r = int(255*pow(r / 255, gamma))
    g = int(255*pow(g / 255, gamma))
    b = int(255*pow(b / 255, gamma))
    fin.clear()
    fin.append(r)
    fin.append(g)
    fin.append(b)
    fin = tuple(fin)
    return '#%02x%02x%02x' % fin

def hex_to_real_rgb(value):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return list(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def real_rgb_to_hex(value):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % value

def Spectrum_Engine():
    """Generates the Color Palettes. Use the PaletteGenerate Class for Palettes, as this requires some custom properties"""
    kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
    kaleidoscope_spectrum_props.hue_slider = 0.0
    kaleidoscope_spectrum_props.saturation_slider = 0.0
    kaleidoscope_spectrum_props.value_slider = 0.0

    c = Color()
    c.hsv = 1.0, 0.0, 1.0
    index = [0, 1, 2, 3, 4]
    random.shuffle(index)
    color_palette = ["", "", "", "", ""]
    c.hsv = random.random(), random.random(), random.random()
    if random.randint(0, 3) /2 == 0:
        c.h = 0.0
    if c.v >= 0.95:
        c.v = c.v-0.1
    elif c.v <= 0.4:
        c.v = c.v+0.2

    if kaleidoscope_spectrum_props.use_custom == True:
        if kaleidoscope_spectrum_props.hue != (0.0, 0.0, 0.0, 1.0):
            c.r = random.uniform(kaleidoscope_spectrum_props.hue[0]-0.1, kaleidoscope_spectrum_props.hue[0]+0.05)
            c.g = random.uniform(kaleidoscope_spectrum_props.hue[1]-0.1, kaleidoscope_spectrum_props.hue[1]+0.05)
            c.b = random.uniform(kaleidoscope_spectrum_props.hue[2]-0.1, kaleidoscope_spectrum_props.hue[2]+0.05)

    #Monochromatic
    if kaleidoscope_spectrum_props.gen_type == "0" or kaleidoscope_spectrum_props.random_int == 0:
        Hue = c.h
        Saturation_less= 0.0
        if c.s <=0.1:
            Saturation_less = 0.0
        else:
            Saturation_less = random.uniform(0.1, c.s)

        if Saturation_less == c.s:
            Saturation_less = random.uniform(0.1, c.s)

        if Saturation_less < 0.25:
            Saturation_less = 0.4

        Saturation_more = random.uniform(c.s+0.1, c.s+0.2)

        Value_less = random.uniform(0.2, c.v)
        Value_more = random.uniform(c.v+0.1, c.v+0.3)

        if Value_less == 0.0:
            Value_less = 0.3
        elif Value_more == 0.0:
            Value_more = 0.7

        c1 = Color()
        c1.hsv = Hue, Saturation_more, Value_more

        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[0]] = rgb_to_hex((c1.r, c1.g, c1.b))
        else:
            color_palette[0] = rgb_to_hex((c1.r, c1.g, c1.b))

        c1.hsv = Hue, Saturation_more+0.1, Value_more
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[1]] = rgb_to_hex((c1.r, c1.g, c1.b))
        else:
            color_palette[1] = rgb_to_hex((c1.r, c1.g, c1.b))

        c1.hsv = Hue, c.s, c.v
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[2]] = rgb_to_hex((c1.r, c1.g, c1.b))
        else:
            color_palette[2] = rgb_to_hex((c1.r, c1.g, c1.b))

        c1.hsv = Hue, Saturation_more+0.1, Value_less-0.1
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[3]] = rgb_to_hex((c1.r, c1.g, c1.b))
        else:
            color_palette[3] = rgb_to_hex((c1.r, c1.g, c1.b))

        c1.hsv = Hue, Saturation_less, Value_less-0.1
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[4]] = rgb_to_hex((c1.r, c1.g, c1.b))
        else:
            color_palette[4] = rgb_to_hex((c1.r, c1.g, c1.b))
        kaleidoscope_spectrum_props.use_internet_libs = False

    elif kaleidoscope_spectrum_props.gen_type == "1" or kaleidoscope_spectrum_props.random_int == 1:
        #Analogous
        Saturation = random.uniform(c.s, 1)
        if Saturation <= 0.4:
            Saturation = Saturation+0.35
        Value = c.v
        if (Value <= 1.0 or Value>1.0) and Value >= 0.8:
            Value = Value-0.1
        if Value <=0.3:
            Value = 0.7
        Value1 = random.uniform(Value+0.1, Value+0.25)
        if (Value1 <= 1.0 or Value1>1.0) and Value1 >= 0.8:
            Value1 = Value1-0.3
        if Value1 <=0.3:
            Value1 = 0.7
        Hue1 = random.uniform(c.h+0.2, c.h+0.3)
        Hue = random.uniform(c.h, c.h+0.2)
        if Hue1 == Hue:
            Hue1 = Hue1-0.1
        if Hue == 0:
            Hue1 = 0.1
        c2 = Color()
        c2.hsv = Hue1, Saturation-0.2, Value
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[0]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[2] = rgb_to_hex((c2.r, c2.g, c2.b))

        Hue1_2 = random.uniform(c.h-0.07, c.h-0.2)
        if Hue1_2 == Hue1:
            Hue1_2 = Hue1_2-0.1
        c2.hsv = Hue, Saturation+0.2, Value1
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[1]] = rgb_to_hex((c2.r, c2.g, c2.b))
            color_palette[index[2]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[1] = rgb_to_hex((c2.r, c2.g, c2.b))
            color_palette[0] = rgb_to_hex((c2.r, c2.g, c2.b))

        Hue_1 = random.uniform(c.h, c.h-0.3)
        if Hue_1==0:
            Hue_1 = 0.9
        if Hue_1 == Hue:
            Hue_1 = Hue_1-0.08
        if c.h == 0.0:
            Hue_1 = 1-abs(Hue_1)
            Hue1_2 = 1-abs(Hue1_2)
        c2.hsv = Hue1_2, Saturation, Value1
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[3]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[3] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue_1, Saturation, Value
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[4]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[4] = rgb_to_hex((c2.r, c2.g, c2.b))
        kaleidoscope_spectrum_props.use_internet_libs = False

    elif kaleidoscope_spectrum_props.gen_type == "2" or kaleidoscope_spectrum_props.random_int == 2:
        #Complementary
        Hue = c.h
        Hue1 = 0.0
        if Hue>=0.5:
            Hue1=Hue-0.5
        else:
            Hue1=Hue+0.5
        Saturation = c.s
        if Saturation <=1.0 and Saturation >=0.95:
            Saturation = Saturation-0.1
        if Saturation <=0.3:
            Saturation = Saturation+0.25
        Saturation_more = random.uniform(Saturation+0.05, Saturation+0.2)
        Saturation_less = random.uniform(Saturation-0.2, Saturation-0.05)
        if Saturation_more <=1.0 and Saturation_more >=0.95:
            Saturation_more = Saturation_more-0.1
        if Saturation_more <=0.6:
            Saturation_more = Saturation_more+0.45

        if Saturation_less <=1.0 and Saturation_less >=0.95:
            Saturation_less = Saturation_less-0.15

        Value = c.v
        Value_more = random.uniform(Value+0.05, Value+0.2)
        Value_less = random.uniform(Value-0.2, Value-0.05)
        if Value_more >=0.0 and Value_more <0.1:
            Value_more = Value_more+0.35
        if Value_less >=0.0 and Value_less <0.1:
            Value_less = Value_less+0.3

        c2 = Color()
        c2.hsv = Hue, Saturation_more, Value_less
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[0]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[0] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue, Saturation_less, Value_more
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[1]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[1] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue, Saturation, Value
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[2]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[2] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue1, Saturation_more, Value_less
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[3]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[3] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue1, Saturation, Value
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[4]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[4] = rgb_to_hex((c2.r, c2.g, c2.b))
        kaleidoscope_spectrum_props.use_internet_libs = False

    elif kaleidoscope_spectrum_props.gen_type == "3" or kaleidoscope_spectrum_props.random_int == 3:
        #Triad
        Hue = c.h
        Hue2 = Hue+0.34
        Hue3 = Hue+0.34+0.34
        if Hue >0.34:
            if Hue > 0.66:
                Hue2 = Hue-0.34
                Hue3 = Hue-0.34-0.34
            Hue2 = Hue+0.34
            Hue3 = Hue-0.34

        Saturation = c.s
        if Saturation <=0.1:
            Saturation = 0.6
        elif Saturation <=0.6:
            Saturation = Saturation+0.45
        if Saturation >= 0.95:
            Saturation = Saturation-0.2
        Saturation_more = random.uniform(Saturation+0.07, Saturation+0.2)
        Saturation_less = random.uniform(Saturation-0.2, Saturation-0.07)
        Saturation_lesser = random.uniform(Saturation-0.1, Saturation-0.08)

        if Saturation_more <=1.0 and Saturation_more >=0.95:
            Saturation_more = Saturation_more-0.1
        if Saturation_more <=0.6:
            Saturation_more = Saturation_more+0.45

        if Saturation_lesser>=1.0 and Saturation_lesser >=0.85:
            Saturation_lesser = 0.7
        if Saturation_lesser <=0.6:
            Saturation_lesser = Saturation_lesser+0.35

        Value = c.v
        Value_less = 0
        if Value<=0.4:
            Value = 0.6
        Value_less = random.uniform(Value-0.2, Value-0.07)

        c2 = Color()
        c2.hsv = Hue, Saturation_more, Value_less
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[0]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[0] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue, Saturation, Value
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[1]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[1] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue3, Saturation_lesser, Value
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[2]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[2] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue2, Saturation_less-0.07, Value_less+0.1
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[3]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[3] = rgb_to_hex((c2.r, c2.g, c2.b))

        c2.hsv = Hue2, Saturation_less+0.07, Value_less-0.2
        if kaleidoscope_spectrum_props.use_organize == False:
            color_palette[index[4]] = rgb_to_hex((c2.r, c2.g, c2.b))
        else:
            color_palette[4] = rgb_to_hex((c2.r, c2.g, c2.b))
        kaleidoscope_spectrum_props.use_internet_libs = False

    elif kaleidoscope_spectrum_props.gen_type == "4" or kaleidoscope_spectrum_props.random_int == 4:
        global online_check
        if kaleidoscope_spectrum_props.custom_gen_type == "0" or kaleidoscope_spectrum_props.random_custom_int == 0:
            #Vibrant
            Hue = c.h
            while True:
                if Hue <=0.1 and Hue>=0.0:
                    Hue = random.random()
                    if kaleidoscope_spectrum_props.use_custom == True:
                        if kaleidoscope_spectrum_props.hue != (0.0, 0.0, 0.0, 1.0):
                            c_rgb = Color()
                            c_rgb.r = kaleidoscope_spectrum_props.hue[0]
                            c_rgb.g = kaleidoscope_spectrum_props.hue[1]
                            c_rgb.b = kaleidoscope_spectrum_props.hue[2]
                            Hue = random.uniform(c_rgb.h-0.1, c_rgb.h+0.1)
                else:
                    break
            Hue1 = 0.0
            if Hue > 0.7:
                Hue1 = Hue-random.random()
            else:
                Hue1 = Hue+random.random()

            Saturation = c.s
            if Saturation <= 0.7:
                Saturation = 0.8
            Value1 = c.v
            if Value1<0.5:
                Value1 = Value1+0.3
            Value = random.uniform(Value1-0.3, Value1-0.23)

            c2 = Color()
            c2.hsv = 0.0, 0.0, random.uniform(0.3, 0.7)
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[0]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[3] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = 0.0, 0.0, random.uniform(0, 0.5)
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[1]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[4] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = 0.0, 0.0, random.uniform(0.7, 1)
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[2]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[2] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = Hue, Saturation, Value1
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[3]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[1] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = Hue1, Saturation, Value
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[4]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[0] = rgb_to_hex((c2.r, c2.g, c2.b))
            kaleidoscope_spectrum_props.use_internet_libs = False
        elif kaleidoscope_spectrum_props.custom_gen_type=="1" or kaleidoscope_spectrum_props.random_custom_int == 1:
            #Gradient
            Hue = c.h
            Value = c.v
            Saturation = c.s+0.1

            c1 = Color()
            c1.hsv = Hue, 0.2, 0.9
            color_palette[0] = rgb_to_hex((c1.r, c1.g, c1.b))

            c1.hsv = Hue, 0.3, 0.9-0.1
            color_palette[1] = rgb_to_hex((c1.r, c1.g, c1.b))

            c1.hsv = Hue, Saturation, Value
            color_palette[2] = rgb_to_hex((c1.r, c1.g, c1.b))

            c1.hsv = Hue, 0.9-0.1, 0.1+0.1
            color_palette[3] = rgb_to_hex((c1.r, c1.g, c1.b))

            c1.hsv = Hue, 0.9, 0.1
            color_palette[4] = rgb_to_hex((c1.r, c1.g, c1.b))
            kaleidoscope_spectrum_props.use_internet_libs = False
        elif kaleidoscope_spectrum_props.custom_gen_type == "2" or kaleidoscope_spectrum_props.random_custom_int == 2:
            #Popout
            Hue = c.h
            Saturation = c.s
            if Saturation<0.9:
                Saturation = 0.95
            Value = c.v
            c2 = Color()
            c2.hsv = 0.0, 0.0, random.uniform(0.3, 0.7)
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[0]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[3] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = Hue, Saturation, Value
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[1]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[0] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = 0.0, 0.0, random.uniform(0, 0.2)
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[2]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[4] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = Hue, Saturation-0.1, Value
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[3]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[1] = rgb_to_hex((c2.r, c2.g, c2.b))

            c2.hsv = 0.0, 0.0, random.uniform(0.7, 1)
            if kaleidoscope_spectrum_props.use_organize == False:
                color_palette[index[4]] = rgb_to_hex((c2.r, c2.g, c2.b))
            else:
                color_palette[2] = rgb_to_hex((c2.r, c2.g, c2.b))

            kaleidoscope_spectrum_props.use_internet_libs = False
        elif kaleidoscope_spectrum_props.custom_gen_type == "4" or kaleidoscope_spectrum_props.random_custom_int == 3:
            global palette
            global community_maintain
            global community_palette
            #Online
            if kaleidoscope_spectrum_props.online_type == '0' or kaleidoscope_spectrum_props.random_online_int == 0:
                try:
                    if kaleidoscope_spectrum_props.new_file != 0:
                        palette_file = str(urllib.request.urlopen("http://blskl.cf/kalonlinepal").read(), 'UTF-8')
                        kaleidoscope_spectrum_props.new_file = 0
                        palette = json.loads(palette_file)
                    index = random.randint(0, len(palette)-1)
                    for i in range(0, 20):
                        if kaleidoscope_spectrum_props.online_palette_index == index or Palette_idHistory[1] == index or Palette_idHistory[0] == index:
                            index = random.randint(0, len(palette)-1)
                        else:
                            break
                    kaleidoscope_spectrum_props.online_palette_index = index
                    online_check = True

                    for i in range(0, 5):
                        color_palette[i] = palette[index]["color"+str(i+1)]['hex']
                    kaleidoscope_spectrum_props.use_internet_libs = True
                except:
                    online_check = False
            elif kaleidoscope_spectrum_props.online_type == '1' or kaleidoscope_spectrum_props.random_online_int == 1:
                try:
                    community_palette_file = None
                    if kaleidoscope_spectrum_props.new_community_file != 0:
                        community_palette_file = str(urllib.request.urlopen("http://blskl.cf/kalcommunitypal").read(), 'UTF-8')
                        if community_palette_file == "Off":
                            community_maintain = True
                            for i in range(0, 5):
                                color_palette[i] = "000000"
                        else:
                            kaleidoscope_spectrum_props.new_community_file = 0
                            community_palette = json.loads(community_palette_file)
                            community_maintain = False
                    if community_palette_file != "Off":
                        index = random.randint(0, len(community_palette['Palettes'])-1)
                        for i in range(0, 20):
                            if kaleidoscope_spectrum_props.online_palette_index == index or Palette_idHistory[1] == index or Palette_idHistory[0] == index:
                                index = random.randint(0, len(community_palette)-1)
                            else:
                                break
                        kaleidoscope_spectrum_props.online_palette_index = index+1
                        online_check = True

                        for i in range(0, 5):
                            color_palette[i] = str(community_palette['Palettes'][index]["Color_"+str(i+1)].rstrip('t'))
                        kaleidoscope_spectrum_props.use_internet_libs = True
                except:
                    online_check = False
            elif kaleidoscope_spectrum_props.online_type == "2" or kaleidoscope_spectrum_props.random_online_int == 2:
                global lovers_id
                while True:
                    try:
                        req = requests.get("http://blskl.cf/kalCOLOURloversapi")
                        data = ET.fromstring(req.text)
                        for i in range(0, 5):
                            print(str(data[0][9][i].text))
                            color_palette[i] = str(data[0][9][i].text)
                            lovers_id = str(data[0][0].text)
                        online_check = True
                        kaleidoscope_spectrum_props.use_internet_libs = True
                        break
                    except requests.ConnectionError:
                        for i in range(0, 5):
                            color_palette[i] = "000000"
                        online_check = False
                        kaleidoscope_spectrum_props.use_internet_libs = False
                        break
                    except:
                        continue
        elif kaleidoscope_spectrum_props.custom_gen_type == "5" or kaleidoscope_spectrum_props.random_custom_int == 4:
            #Random
            if kaleidoscope_spectrum_props.use_custom == True:
                color_palette[index[0]] = rgb_to_hex((kaleidoscope_spectrum_props.hue[0], kaleidoscope_spectrum_props.hue[1], kaleidoscope_spectrum_props.hue[2]))
            else:
                color_palette[index[0]] = (''.join([random.choice('0123456789ABCDEF') for x in range(6)]))
            color_palette[index[1]] = (''.join([random.choice('0123456789ABCDEF') for x in range(6)]))
            color_palette[index[2]] = (''.join([random.choice('0123456789ABCDEF') for x in range(6)]))
            color_palette[index[3]] = (''.join([random.choice('0123456789ABCDEF') for x in range(6)]))
            color_palette[index[4]] = (''.join([random.choice('0123456789ABCDEF') for x in range(6)]))
            kaleidoscope_spectrum_props.use_internet_libs = False
        elif kaleidoscope_spectrum_props.custom_gen_type == "6":
            colors = []
            final_colors = []
            fin_colors = []
            kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
            img = bpy.data.images.load(kaleidoscope_spectrum_props.img_name)
            img.scale(30, img.size[1]/img.size[0]*30)

            for i in range(0, len(img.pixels), 4):
                colors.append(img.pixels[i:i+4])

            colors = filter(None, colors)
            words_to_count = (word for word in colors)
            c = Counter(words_to_count)
            c = list(c.items())
            color1 = c[0][0] # most dominant
            col = hex_to_real_rgb(rgb_to_hex(color1))
            final_colors.append(color1)
            for i in range(1, len(c)):
                color2 = hex_to_real_rgb(rgb_to_hex(c[i][0]))
                res = math.pow((color2[0]-col[0]), 2) + math.pow((color2[1]-col[1]), 2) + math.pow((color2[2]-col[2]), 2)
                if res <= 3:
                    continue
                else:
                    for j in range(0, len(final_colors)):
                        in_color = hex_to_real_rgb(rgb_to_hex(final_colors[j]))
                        res = math.pow((color2[0]-in_color[0]), 2) + math.pow((color2[1]-in_color[1]), 2) + math.pow((color2[2]-in_color[2]), 2)
                        if res <= 3:
                            continue
                        else:
                            fin_colors.append(c[i][0])
            print(fin_colors)
            for i in range(0, 5):
                color_palette[i] = rgb_to_hex(fin_colors[i][0])
    return color_palette

def set_palettes_list(caller, context):
    """Saves the Palettes for History Purposes"""
    kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
    #Palette History 1
    PaletteHistory[4].r = PaletteHistory[9].r
    PaletteHistory[4].g = PaletteHistory[9].g
    PaletteHistory[4].b = PaletteHistory[9].b

    PaletteHistory[3].r = PaletteHistory[8].r
    PaletteHistory[3].g = PaletteHistory[8].g
    PaletteHistory[3].b = PaletteHistory[8].b

    PaletteHistory[2].r = PaletteHistory[7].r
    PaletteHistory[2].g = PaletteHistory[7].g
    PaletteHistory[2].b = PaletteHistory[7].b

    PaletteHistory[1].r = PaletteHistory[6].r
    PaletteHistory[1].g = PaletteHistory[6].g
    PaletteHistory[1].b = PaletteHistory[6].b

    PaletteHistory[0].r = PaletteHistory[5].r
    PaletteHistory[0].g = PaletteHistory[5].g
    PaletteHistory[0].b = PaletteHistory[5].b
    Palette_idHistory[0] = Palette_idHistory[1]

    #Palette History 2
    PaletteHistory[9].r = PaletteHistory[14].r
    PaletteHistory[9].g = PaletteHistory[14].g
    PaletteHistory[9].b = PaletteHistory[14].b

    PaletteHistory[8].r = PaletteHistory[13].r
    PaletteHistory[8].g = PaletteHistory[13].g
    PaletteHistory[8].b = PaletteHistory[13].b

    PaletteHistory[7].r = PaletteHistory[12].r
    PaletteHistory[7].g = PaletteHistory[12].g
    PaletteHistory[7].b = PaletteHistory[12].b

    PaletteHistory[6].r = PaletteHistory[11].r
    PaletteHistory[6].g = PaletteHistory[11].g
    PaletteHistory[6].b = PaletteHistory[11].b

    PaletteHistory[5].r = PaletteHistory[10].r
    PaletteHistory[5].g = PaletteHistory[10].g
    PaletteHistory[5].b = PaletteHistory[10].b
    Palette_idHistory[1] = Palette_idHistory[2]

    #Palette History 3
    PaletteHistory[14].r = kaleidoscope_spectrum_props.color5[0]
    PaletteHistory[14].g = kaleidoscope_spectrum_props.color5[1]
    PaletteHistory[14].b = kaleidoscope_spectrum_props.color5[2]

    PaletteHistory[13].r = kaleidoscope_spectrum_props.color4[0]
    PaletteHistory[13].g = kaleidoscope_spectrum_props.color4[1]
    PaletteHistory[13].b = kaleidoscope_spectrum_props.color4[2]

    PaletteHistory[12].r = kaleidoscope_spectrum_props.color3[0]
    PaletteHistory[12].g = kaleidoscope_spectrum_props.color3[1]
    PaletteHistory[12].b = kaleidoscope_spectrum_props.color3[2]

    PaletteHistory[11].r = kaleidoscope_spectrum_props.color2[0]
    PaletteHistory[11].g = kaleidoscope_spectrum_props.color2[1]
    PaletteHistory[11].b = kaleidoscope_spectrum_props.color2[2]

    PaletteHistory[10].r = kaleidoscope_spectrum_props.color1[0]
    PaletteHistory[10].g = kaleidoscope_spectrum_props.color1[1]
    PaletteHistory[10].b = kaleidoscope_spectrum_props.color1[2]
    Palette_idHistory[2] = kaleidoscope_spectrum_props.online_palette_index

    kaleidoscope_spectrum_props.history_count = 0

class PaletteGenerate(bpy.types.Operator):
    """Generate a new Color Palette"""
    bl_idname="spectrum_palette.palette_gen"
    bl_label="Refresh Palette"

    def invoke(self, context, event):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        if event.shift:
            if kaleidoscope_spectrum_props.gen_type == '4' and kaleidoscope_spectrum_props.custom_gen_type == '4':
                if kaleidoscope_spectrum_props.online_type == "0":
                    kaleidoscope_spectrum_props.new_file = 1
                    self.report({'INFO'}, "Online Palettes list has been updated")
                elif kaleidoscope_spectrum_props.online_type == "1":
                    kaleidoscope_spectrum_props.new_community_file = 1
                    self.report({'INFO'}, "Community Palettes list has been updated")
        self.execute(context)
        return {'FINISHED'}

    def execute(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        if kaleidoscope_spectrum_props.custom_gen_type != "3":
            color_palette = Spectrum_Engine()
            kaleidoscope_spectrum_props.color1 = hex_to_rgb(color_palette[0])
            kaleidoscope_spectrum_props.color2 = hex_to_rgb(color_palette[1])
            kaleidoscope_spectrum_props.color3 = hex_to_rgb(color_palette[2])
            kaleidoscope_spectrum_props.color4 = hex_to_rgb(color_palette[3])
            kaleidoscope_spectrum_props.color5 = hex_to_rgb(color_palette[4])
        else:
            num = random.randint(0, 2)
            if num % 2 == 0:
                kaleidoscope_spectrum_props.random_int = 4
            else:
                kaleidoscope_spectrum_props.random_int = random.randint(0, 4)
            kaleidoscope_spectrum_props.random_custom_int = random.randint(0, 4)
            kaleidoscope_spectrum_props.random_online_int = random.randint(0, 2)
            color_palette = Spectrum_Engine()
            kaleidoscope_spectrum_props.color1 = hex_to_rgb(color_palette[0])
            kaleidoscope_spectrum_props.color2 = hex_to_rgb(color_palette[1])
            kaleidoscope_spectrum_props.color3 = hex_to_rgb(color_palette[2])
            kaleidoscope_spectrum_props.color4 = hex_to_rgb(color_palette[3])
            kaleidoscope_spectrum_props.color5 = hex_to_rgb(color_palette[4])
        set_palettes_list(self, context)
        for mat in bpy.data.materials:
            if mat.kaleidoscope_spectrum_props.assign_colorramp == True or kaleidoscope_spectrum_props.assign_colorramp_world == True:
                set_color_ramp(self)
                break

        global shuffle_time
        global before_shuffle_colors
        shuffle_time=1

        before_shuffle_colors.clear()
        return{'FINISHED'}

class PreviousPalette(bpy.types.Operator):
    """View the Previous Palette"""
    bl_idname="spectrum_palette.palette_previous"
    bl_label="Previous Palette"

    def execute(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        kaleidoscope_spectrum_props.history_count = kaleidoscope_spectrum_props.history_count+1
        if kaleidoscope_spectrum_props.history_count == 2:
            for i in range(0, 5):
                exec("kaleidoscope_spectrum_props.color"+str(i+1)+"[0] = PaletteHistory["+str(i)+"].r")
                exec("kaleidoscope_spectrum_props.color"+str(i+1)+"[1] = PaletteHistory["+str(i)+"].g")
                exec("kaleidoscope_spectrum_props.color"+str(i+1)+"[2] = PaletteHistory["+str(i)+"].b")

            kaleidoscope_spectrum_props.online_palette_index = Palette_idHistory[0]

        elif kaleidoscope_spectrum_props.history_count == 1:
            kaleidoscope_spectrum_props.color1[0] = PaletteHistory[5].r
            kaleidoscope_spectrum_props.color1[1] = PaletteHistory[5].g
            kaleidoscope_spectrum_props.color1[2] = PaletteHistory[5].b

            kaleidoscope_spectrum_props.color2[0] = PaletteHistory[6].r
            kaleidoscope_spectrum_props.color2[1] = PaletteHistory[6].g
            kaleidoscope_spectrum_props.color2[2] = PaletteHistory[6].b

            kaleidoscope_spectrum_props.color3[0] = PaletteHistory[7].r
            kaleidoscope_spectrum_props.color3[1] = PaletteHistory[7].g
            kaleidoscope_spectrum_props.color3[2] = PaletteHistory[7].b

            kaleidoscope_spectrum_props.color4[0] = PaletteHistory[8].r
            kaleidoscope_spectrum_props.color4[1] = PaletteHistory[8].g
            kaleidoscope_spectrum_props.color4[2] = PaletteHistory[8].b

            kaleidoscope_spectrum_props.color5[0] = PaletteHistory[9].r
            kaleidoscope_spectrum_props.color5[1] = PaletteHistory[9].g
            kaleidoscope_spectrum_props.color5[2] = PaletteHistory[9].b

            kaleidoscope_spectrum_props.online_palette_index = Palette_idHistory[1]

        elif kaleidoscope_spectrum_props.history_count == 0:
            kaleidoscope_spectrum_props.color1[0] = PaletteHistory[10].r
            kaleidoscope_spectrum_props.color1[1] = PaletteHistory[10].g
            kaleidoscope_spectrum_props.color1[2] = PaletteHistory[10].b

            kaleidoscope_spectrum_props.color2[0] = PaletteHistory[11].r
            kaleidoscope_spectrum_props.color2[1] = PaletteHistory[11].g
            kaleidoscope_spectrum_props.color2[2] = PaletteHistory[11].b

            kaleidoscope_spectrum_props.color3[0] = PaletteHistory[12].r
            kaleidoscope_spectrum_props.color3[1] = PaletteHistory[12].g
            kaleidoscope_spectrum_props.color3[2] = PaletteHistory[12].b

            kaleidoscope_spectrum_props.color4[0] = PaletteHistory[13].r
            kaleidoscope_spectrum_props.color4[1] = PaletteHistory[13].g
            kaleidoscope_spectrum_props.color4[2] = PaletteHistory[13].b

            kaleidoscope_spectrum_props.color5[0] = PaletteHistory[14].r
            kaleidoscope_spectrum_props.color5[1] = PaletteHistory[14].g
            kaleidoscope_spectrum_props.color5[2] = PaletteHistory[14].b

            kaleidoscope_spectrum_props.online_palette_index[2] = Palette_idHistory[2]

        kaleidoscope_spectrum_props.hue_slider = 0.0
        kaleidoscope_spectrum_props.saturation_slider = 0.0
        kaleidoscope_spectrum_props.value_slider = 0.0

        global shuffle_time
        shuffle_time=1
        return{'FINISHED'}

class NextPalette(bpy.types.Operator):
    """View the Next Palette"""
    bl_idname="spectrum_palette.palette_next"
    bl_label="Next Palette"

    def execute(self, context):
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        kaleidoscope_spectrum_props.history_count = kaleidoscope_spectrum_props.history_count-1
        if kaleidoscope_spectrum_props.history_count == 1:
            kaleidoscope_spectrum_props.color1[0] = PaletteHistory[5].r
            kaleidoscope_spectrum_props.color1[1] = PaletteHistory[5].g
            kaleidoscope_spectrum_props.color1[2] = PaletteHistory[5].b

            kaleidoscope_spectrum_props.color2[0] = PaletteHistory[6].r
            kaleidoscope_spectrum_props.color2[1] = PaletteHistory[6].g
            kaleidoscope_spectrum_props.color2[2] = PaletteHistory[6].b

            kaleidoscope_spectrum_props.color3[0] = PaletteHistory[7].r
            kaleidoscope_spectrum_props.color3[1] = PaletteHistory[7].g
            kaleidoscope_spectrum_props.color3[2] = PaletteHistory[7].b

            kaleidoscope_spectrum_props.color4[0] = PaletteHistory[8].r
            kaleidoscope_spectrum_props.color4[1] = PaletteHistory[8].g
            kaleidoscope_spectrum_props.color4[2] = PaletteHistory[8].b

            kaleidoscope_spectrum_props.color5[0] = PaletteHistory[9].r
            kaleidoscope_spectrum_props.color5[1] = PaletteHistory[9].g
            kaleidoscope_spectrum_props.color5[2] = PaletteHistory[9].b

            kaleidoscope_spectrum_props.online_palette_index = Palette_idHistory[1]

        elif kaleidoscope_spectrum_props.history_count == 0:
            kaleidoscope_spectrum_props.color1[0] = PaletteHistory[10].r
            kaleidoscope_spectrum_props.color1[1] = PaletteHistory[10].g
            kaleidoscope_spectrum_props.color1[2] = PaletteHistory[10].b

            kaleidoscope_spectrum_props.color2[0] = PaletteHistory[11].r
            kaleidoscope_spectrum_props.color2[1] = PaletteHistory[11].g
            kaleidoscope_spectrum_props.color2[2] = PaletteHistory[11].b

            kaleidoscope_spectrum_props.color3[0] = PaletteHistory[12].r
            kaleidoscope_spectrum_props.color3[1] = PaletteHistory[12].g
            kaleidoscope_spectrum_props.color3[2] = PaletteHistory[12].b

            kaleidoscope_spectrum_props.color4[0] = PaletteHistory[13].r
            kaleidoscope_spectrum_props.color4[1] = PaletteHistory[13].g
            kaleidoscope_spectrum_props.color4[2] = PaletteHistory[13].b

            kaleidoscope_spectrum_props.color5[0] = PaletteHistory[14].r
            kaleidoscope_spectrum_props.color5[1] = PaletteHistory[14].g
            kaleidoscope_spectrum_props.color5[2] = PaletteHistory[14].b

            kaleidoscope_spectrum_props.online_palette_index = Palette_idHistory[2]

        kaleidoscope_spectrum_props.hue_slider = 0.0
        kaleidoscope_spectrum_props.saturation_slider = 0.0
        kaleidoscope_spectrum_props.value_slider = 0.0

        global shuffle_time
        shuffle_time=1
        return{'FINISHED'}

class PaletteShuffle(bpy.types.Operator):
    """Shuffle the Order of colors in the Palette"""
    bl_idname="spectrum_palette.palette_shuffle"
    bl_label="Shufle Palette"

    def invoke(self, context, event):
        global shuffle_time
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        if event.shift:
            if shuffle_time != 1:
                global before_shuffle_colors
                for i in range(1, 6):
                    exec("kaleidoscope_spectrum_props.color"+str(i)+" = before_shuffle_colors["+str(i-1)+"]")
                shuffle_time = 1
                self.report({'INFO'}, 'Palette was reset to the order before it was shuffled')
            else:
                self.report({'INFO'}, 'Palette is not shuffled')
        else:
            self.execute(context)
        return {'FINISHED'}

    def execute(self, context):
        global before_shuffle_colors
        global shuffle_time
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props

        col1 = Color()
        col2 = Color()
        col3 = Color()
        col4 = Color()
        col5 = Color()

        for i in range(1, 6):
            exec("col"+str(i)+".r = kaleidoscope_spectrum_props.color"+str(i)+"[0]")
            exec("col"+str(i)+".g = kaleidoscope_spectrum_props.color"+str(i)+"[1]")
            exec("col"+str(i)+".b = kaleidoscope_spectrum_props.color"+str(i)+"[2]")

        if shuffle_time == 1:
            before_shuffle_colors.clear()
            before_shuffle_colors.extend([(col1.r, col1.g, col1.b, 1.0), (col2.r, col2.g, col2.b, 1.0), (col3.r, col3.g, col3.b, 1.0), (col4.r, col4.g, col4.b, 1.0), (col5.r, col5.g, col5.b, 1.0)])

        index = [1, 2, 3, 4, 5]
        random.shuffle(index)

        for i in range(1, 6):
            exec("kaleidoscope_spectrum_props.color"+str(index[i-1])+" = col"+str(i)+".r, col"+str(i)+".g, col"+str(i)+".b, 1.0")

        current_history()
        shuffle_time=shuffle_time+1
        return{'FINISHED'}

def current_history():
    kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props

    kaleidoscope_spectrum_props.history_count = 0.0

    PaletteHistory[14].r = kaleidoscope_spectrum_props.color5[0]
    PaletteHistory[14].g = kaleidoscope_spectrum_props.color5[1]
    PaletteHistory[14].b = kaleidoscope_spectrum_props.color5[2]

    PaletteHistory[13].r = kaleidoscope_spectrum_props.color4[0]
    PaletteHistory[13].g = kaleidoscope_spectrum_props.color4[1]
    PaletteHistory[13].b = kaleidoscope_spectrum_props.color4[2]

    PaletteHistory[12].r = kaleidoscope_spectrum_props.color3[0]
    PaletteHistory[12].g = kaleidoscope_spectrum_props.color3[1]
    PaletteHistory[12].b = kaleidoscope_spectrum_props.color3[2]

    PaletteHistory[11].r = kaleidoscope_spectrum_props.color2[0]
    PaletteHistory[11].g = kaleidoscope_spectrum_props.color2[1]
    PaletteHistory[11].b = kaleidoscope_spectrum_props.color2[2]

    PaletteHistory[10].r = kaleidoscope_spectrum_props.color1[0]
    PaletteHistory[10].g = kaleidoscope_spectrum_props.color1[1]
    PaletteHistory[10].b = kaleidoscope_spectrum_props.color1[2]

    kaleidoscope_spectrum_props.hue_slider = 0.0
    kaleidoscope_spectrum_props.saturation_slider = 0.0
    kaleidoscope_spectrum_props.value_slider = 0.0

class PaletteInvert(bpy.types.Operator):
    """Invert the order of colors in the Palette"""
    bl_idname = "spectrum_palette.palette_invert"
    bl_label = "Invert Palette"

    def execute(self, context):
        global shuffle_time
        global before_shuffle_colors
        kaleidoscope_spectrum_props = bpy.context.scene.kaleidoscope_spectrum_props
        color1 = Color()
        color2 = Color()
        color3 = Color()
        color4 = Color()
        color5 = Color()

        for i in range(1, 6):
            exec("color"+str(i)+".r = kaleidoscope_spectrum_props.color"+str(i)+"[0]")
            exec("color"+str(i)+".g = kaleidoscope_spectrum_props.color"+str(i)+"[1]")
            exec("color"+str(i)+".b = kaleidoscope_spectrum_props.color"+str(i)+"[2]")

        if shuffle_time == 1:
            before_shuffle_colors.clear()
            before_shuffle_colors.extend([(color1.r, color1.g, color1.b, 1.0), (color2.r, color2.g, color2.b, 1.0), (color3.r, color3.g, color3.b, 1.0), (color4.r, color4.g, color4.b, 1.0), (color5.r, color5.g, color5.b, 1.0)])

        for i in range(1, 6):
            exec("kaleidoscope_spectrum_props.color"+str(6-i)+"[0] = color"+str(i)+".r")
            exec("kaleidoscope_spectrum_props.color"+str(6-i)+"[1] = color"+str(i)+".g")
            exec("kaleidoscope_spectrum_props.color"+str(6-i)+"[2] = color"+str(i)+".b")

        current_history()
        shuffle_time = shuffle_time+1
        return{'FINISHED'}

def register():
    bpy.types.Scene.kaleidoscope_spectrum_props = bpy.props.PointerProperty(type=SpectrumProperties)
    bpy.types.Material.kaleidoscope_spectrum_props = bpy.props.PointerProperty(type=SpectrumMaterialProps)
    bpy.app.handlers.frame_change_pre.append(pre_spectrum_frame_change)

def unregister():
    bpy.context.scene.kaleidoscope_spectrum_props.new_file = 1
    bpy.context.scene.kaleidoscope_spectrum_props.new_community_file = 1
    del bpy.types.Scene.kaleidoscope_spectrum_props
    del bpy.types.Material.kaleidoscope_spectrum_props
    palette.clear()

def pre_spectrum_frame_change(scene):
    v = scene.kaleidoscope_spectrum_props.color1
    scene.kaleidoscope_spectrum_props.color1 = v

    v = scene.kaleidoscope_spectrum_props.color2
    scene.kaleidoscope_spectrum_props.color2 = v

    v = scene.kaleidoscope_spectrum_props.color3
    scene.kaleidoscope_spectrum_props.color3 = v

    v = scene.kaleidoscope_spectrum_props.color4
    scene.kaleidoscope_spectrum_props.color4 = v

    v = scene.kaleidoscope_spectrum_props.color5
    scene.kaleidoscope_spectrum_props.color5 = v

    """v = scene.kaleidoscope_spectrum_props.hue_slider
    scene.kaleidoscope_spectrum_props.hue_slider = v

    v = scene.kaleidoscope_spectrum_props.saturation_slider
    scene.kaleidoscope_spectrum_props.saturation_slider = v

    v = scene.kaleidoscope_spectrum_props.value_slider
    scene.kaleidoscope_spectrum_props.value_slider = v"""

    for mat in bpy.data.materials:
        if mat.node_tree is not None:
            for node in mat.node_tree.nodes:
                if node.bl_idname == 'spectrum_palette.node':
                    v = mat.kaleidoscope_spectrum_props.assign_colorramp
                    mat.kaleidoscope_spectrum_props.assign_colorramp = v

    for world in bpy.data.worlds:
        if world.node_tree is not None:
            for node in world.node_tree.nodes:
                if node.bl_idname == 'spectrum_palette.node':
                    v = world.kaleidoscope_spectrum_props.assign_colorramp
                    world.kaleidoscope_spectrum_props.assign_colorramp = v

    for lamps in bpy.data.lamps:
        if lamps.node_tree is not None:
            for node in lamps.node_tree.nodes:
                if node.bl_idname == 'spectrum_palette.node':
                    v = lamps.kaleidoscope_spectrum_props.assign_colorramp
                    lamps.kaleidoscope_spectrum_props.assign_colorramp = v
