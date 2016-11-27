# Intensity Node
import bpy
import bpy.utils.previews
import os
from bpy.types import Node

glass_ior = [1,
            1.000293,
            1.000036,
            1.000132,
            1.00045,
            1.333,
            1.36,
            1.47,
            1.31,
            1.46,
            1.49,
            1.52,
            1.62,
            2.15,
            2.42,
            2.65,
            2.67]
blackbody = [1700,
            1850,
            2400,
            2550,
            2700,
            3000,
            3200,
            3350,
            4150,
            5000,
            5000,
            6000,
            6200,
            6500,
            9500,
            27000]

node_name = ""
class IntensityTreeNode:
    @classmethod
    def poll(cls, ntree):
        b = False
        if ntree.bl_idname == 'ShaderNodeTree':
            b = True
        return b

# Derived from the Node base type.
class IntensityNode(Node, IntensityTreeNode):
    """Intensity node"""
    bl_idname = 'intensity.node'
    bl_label = 'Intensity'
    bl_icon = 'INFO'

    def update_value(self, context):
        if bpy.context.space_data.shader_type == 'WORLD':
            for node in bpy.context.scene.world.node_tree.nodes:
                if node.name.startswith("Intensity"):
                    node.outputs["Value"].default_value = self.kaleidoscope_intensity_out_value
                    #update_caller(self, input_name="Value")
                    self.update()
        elif bpy.context.space_data.shader_type == 'OBJECT':
            for node in bpy.context.object.active_material.node_tree.nodes:
                if node.name.startswith("Intensity"):
                    node.outputs["Value"].default_value = self.kaleidoscope_intensity_out_value
                    #update_caller(self, input_name="Value")
                    self.update()
        return None

    def set_value(self, context):
        if self.kaleidoscope_intensity_main_category == '0':
            self.kaleidoscope_intensity_out_value = glass_ior[int(self.kaleidoscope_intensity_glass_category)]
        elif self.kaleidoscope_intensity_main_category == '1':
            self.kaleidoscope_intensity_out_value = blackbody[int(self.kaleidoscope_intensity_black_body_category)]
        return None
    def set_previous(self, context):
        if self.kaleidoscope_intensity_main_category == '0':
            if int(self.kaleidoscope_intensity_glass_category) > 0:
                self.kaleidoscope_intensity_glass_category = str(int(self.kaleidoscope_intensity_glass_category)-1)
            else:
                self.kaleidoscope_intensity_glass_category = str(len(glass_ior)-1)
        elif self.kaleidoscope_intensity_main_category == '1':
            if int(self.kaleidoscope_intensity_black_body_category) > 0:
                self.kaleidoscope_intensity_black_body_category = str(int(self.kaleidoscope_intensity_black_body_category)-1)
            else:
                self.kaleidoscope_intensity_black_body_category = str(len(blackbody)-1)
        return None
    def set_next(self, context):
        if self.kaleidoscope_intensity_main_category == '0':
            if int(self.kaleidoscope_intensity_glass_category) < 16:
                self.kaleidoscope_intensity_glass_category = str(int(self.kaleidoscope_intensity_glass_category)+1)
            else:
                self.kaleidoscope_intensity_glass_category = '0'
        elif self.kaleidoscope_intensity_main_category == '1':
            if int(self.kaleidoscope_intensity_black_body_category) < 15:
                self.kaleidoscope_intensity_black_body_category = str(int(self.kaleidoscope_intensity_black_body_category)+1)
            else:
                self.kaleidoscope_intensity_black_body_category = '0'
        return None

    kaleidoscope_intensity_next_button = bpy.props.BoolProperty(name="Next", description="Select the Next Predefined Value", default=False, update=set_next)
    kaleidoscope_intensity_prev_button = bpy.props.BoolProperty(name="Previous", description="Select the Previous Predefined Value", default=False, update=set_previous)
    kaleidoscope_intensity_info = bpy.props.BoolProperty(name="Info", description="View/Hide Information about this category", default=False)

    kaleidoscope_intensity_out_value = bpy.props.FloatProperty(name="Value", description="The Value of the Intensity Node", precision=6, default=1.00, update=update_value)

    kaleidoscope_intensity_main_category = bpy.props.EnumProperty(name="Main Category", description="Select the Type of Values to be used for the node", items=(('0', 'Glass IOR', 'Select the Glass IOR Predefined values'),
                                                                                                                                         ('1', 'Blackbody', 'Select the Blackbody Predefined values')), default='0', update=set_value)
    kaleidoscope_intensity_glass_category = bpy.props.EnumProperty(name="Glass IOR", description="Select the Predefined Value for the Index of Refraction (IOR)", items=(('0', 'Vacuum', ''),
                                                                                                                                                ('1', 'Air', ''),
                                                                                                                                                ('2', 'Helium', ''),
                                                                                                                                                ('3', 'Hydrogen', ''),
                                                                                                                                                ('4', 'Carbon dioxide', ''),
                                                                                                                                                ('5', 'Water', ''),
                                                                                                                                                ('6', 'Ethanol', ''),
                                                                                                                                                ('7', 'Olive Oil', ''),
                                                                                                                                                ('8', 'Ice', ''),
                                                                                                                                                ('9', 'Soda-lime Glass', ''),
                                                                                                                                                ('10', 'Plexiglas', ''),
                                                                                                                                                ('11', 'Crown glass', ''),
                                                                                                                                                ('12', 'Flint glass', ''),
                                                                                                                                                ('13', 'Cubic zirconia', ''),
                                                                                                                                                ('14', 'Diamond', ''),
                                                                                                                                                ('15', 'Moissanite', ''),
                                                                                                                                                ('16', 'Zinc selenide', '')), default='0', update=set_value)
    kaleidoscope_intensity_black_body_category = bpy.props.EnumProperty(name="Blackbody", description="Select the Predefined Value for the Blackbody (Color Temperature)", items=(('0', 'Match Flame', ''),
                                                                                                                                                          ('1', 'Candle Flame', ''),
                                                                                                                                                          ('2', 'Standard incandescent lamps', ''),
                                                                                                                                                          ('3', 'Soft White incandescent lamps', ''),
                                                                                                                                                          ('4', 'Standard LED lamps', ''),
                                                                                                                                                          ('5', 'Warm White LED lamps', ''),
                                                                                                                                                          ('6', 'Studio lamps', ''),
                                                                                                                                                          ('7', 'Studio CP light', ''),
                                                                                                                                                          ('8', 'Moonlight', ''),
                                                                                                                                                          ('9', 'Horizon Daylight', ''),
                                                                                                                                                          ('10', 'Compact fluorescent lamps (CFL)', ''),
                                                                                                                                                          ('11', 'Electronic Flash', ''),
                                                                                                                                                          ('12', 'Short-arc lamp', ''),
                                                                                                                                                          ('13', 'Daylight', ''),
                                                                                                                                                          ('14', 'LCD, CRT screen', ''),
                                                                                                                                                          ('15', 'Clear Blue Sky', '')), default='0', update=set_value)

    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Value")
        self.outputs["Value"].default_value = self.kaleidoscope_intensity_out_value
        self.width = 187

    def update(self):
        out = ""
        #try:
        if bpy.context.space_data.shader_type == 'WORLD':
            for world in bpy.data.worlds:
                try:
                    for node in world.node_tree.nodes:
                        if node.name.startswith("Intensity"):
                            for out in node.outputs:
                                if out.is_linked:
                                    for o in out.links:
                                        if o.is_valid:
                                            o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
                except:
                    continue
        elif bpy.context.space_data.shader_type == 'OBJECT':
            for mat in bpy.data.materials:
                try:
                    for node in mat.node_tree.nodes:
                        if node.name.startswith("Intensity"):
                            for out in node.outputs:
                                if out.is_linked:
                                    for o in out.links:
                                        if o.is_valid:
                                            o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
                except:
                    continue
        #except:
            #pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        IntensityUI(self, context, layout, self.name)
        global node_name
        node_name = self.name

    #Node Label
    def draw_label(self):
        return "Intensity"


def IntensityUI(self, context, layout, current_node):
        kaleidoscope_intensity_props = self
        col = layout.column(align=False)
        row = col.row()
        split = row.split(percentage=0.9)
        col1 = split.column(align=True)
        col1.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_main_category", text="")
        col2 = split.column(align=True)
        col2.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_info", text="", icon='INFO', toggle=True, emboss=False)
        if kaleidoscope_intensity_props.kaleidoscope_intensity_info == True:
            box = col.box()
            colb = box.column(align=True)
            if kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '0':
                colb.label("Glass IOR")
                colb.label()
                colb.label("The IOR (Index of Refraction)")
                colb.label("Value, is the ratio between")
                colb.label("speed of light ray in vacuum")
                colb.label("to the speed in the medium")
                colb.label()
                colb.label("So, the IOR value defines")
                colb.label("that how much slower a light")
                colb.label("ray would travel in a medium")
                colb.label("compared to that in vacuum.")
                colb.label("This value is important and")
                colb.label("it controls the refractions")
                colb.label("caused by the light ray.")
                colb.label()

            elif kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '1':
                colb.label("Blackbody")
                colb.label()
                colb.label("A Blackbody radiator radiates")
                colb.label("light, with a specific")
                colb.label("temperature, and this temperature")
                colb.label("defines a specific hue to that")
                colb.label("light ray.")
                colb.label()
                colb.label("This characteristic of light")
                colb.label("is important in the fields of")
                colb.label("Photography, Lighting, and many")
                colb.label("more.")
                colb.label()

            colb.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_info", text="Close Help", icon='INFO', toggle=True)
        col.label()
        row = col.row(align=True)
        split1 = row.split(percentage=0.05)
        col1 = split1.column(align=True)
        col1.prop(kaleidoscope_intensity_props, 'kaleidoscope_intensity_prev_button', text="", icon="TRIA_LEFT", emboss=False, toggle=True)

        col2 = split1.column(align=True)
        row = col2.row(align=True)
        split2 = row.split(percentage=0.95)
        col3 = split2.column(align=True)
        if kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '0':
            col3.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_glass_category", text="")
        elif kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '1':
            col3.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_black_body_category", text="")
        col4 = split2.column(align=True)
        col4.prop(kaleidoscope_intensity_props, 'kaleidoscope_intensity_next_button', text="", icon="TRIA_RIGHT", emboss=False, toggle=True)
        col.label()
        col.prop(kaleidoscope_intensity_props, 'kaleidoscope_intensity_out_value')
        col.label()
        row2 = col.row(align=True)
        row2.operator('wm.url_open', text="", icon_value=icons_dict["blenderskool"].icon_id, emboss=False).url="http://www.blenderskool.cf"
        row2_1 = row2.row()
        row2_1.alignment = 'CENTER'
        row2_1.label("Akash Hamirwasia")
        row2.operator('wm.url_open', text="", icon_value=icons_dict["youtube"].icon_id, emboss=False).url="http://www.youtube.com/AkashHamirwasia1"


def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        pass
    global icons_dict
    icons_dict = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    icons_dict.load("blenderskool", os.path.join(icons_dir, "blenderskool_logo.png"), 'IMAGE')
    icons_dict.load("youtube", os.path.join(icons_dir, "youtube_icon.png"), 'IMAGE')
    bpy.app.handlers.frame_change_pre.append(pre_frame_change)

def unregister():
    global icons_dict
    bpy.utils.previews.remove(icons_dict)
    bpy.utils.unregister_module(__name__)

def pre_frame_change(scene):
    if scene.render.engine == 'CYCLES':
        for m in bpy.data.materials:
            try:
                if m.node_tree is not None:
                    for n in m.node_tree.nodes:
                        if n.bl_idname == 'intensity.node':
                            v = n.kaleidoscope_intensity_out_value
                            n.kaleidoscope_intensity_out_value = v
            except:
                continue
