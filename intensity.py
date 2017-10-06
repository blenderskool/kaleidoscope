# Intensity Node
import bpy
import os
from bpy.types import Node
import json
from . import spectrum, client
if "bpy" in locals():
    import importlib
    importlib.reload(spectrum)
    importlib.reload(client)

glass_ior = [1, #Vacuum
            1.000293, #Air
            1.000036, #Helium
            1.000132, #Hydrogen
            1.00045, #Carbon dioxide
            1.31, #Ice
            1.333333, #Water
            1.345, #Beer
            1.35, #Milk
            1.36, #Alcohol
            1.38, #Sugar Solution
            1.41, #Lens
            1.47, #Olive Oil
            1.473, #Glycerine
            1.46, #Plastic
            1.46, #Soda-lime Glass
            1.49, #Plexiglas
            1.50, #Honey
            1.52, #Crown glass
            1.53, #Nylon
            1.56, #Emerald
            1.62, #Flint glass
            2.00, #Crystal
            2.15, #Cubic zirconia
            2.42, #Diamond
            2.65, #Moissanite
            2.67] #Zinc selenide
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
custom_values_list = []
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
    bl_icon = 'NONE'
    bl_width_min = 216.3
    bl_width_max = 330.0

    def update_value(self, context):
        self.outputs['Value'].default_value = self.kaleidoscope_intensity_out_value
        IntensityNode.num_val = self.kaleidoscope_intensity_out_value
        self.update()
        return None

    def set_value(self, context):
        global custom_values_list
        kaleidoscope_props = bpy.context.scene.kaleidoscope_props
        if self.kaleidoscope_intensity_main_category == '0':
            self.kaleidoscope_intensity_out_value = glass_ior[int(self.kaleidoscope_intensity_glass_category)]
        elif self.kaleidoscope_intensity_main_category == '1':
            self.kaleidoscope_intensity_out_value = blackbody[int(self.kaleidoscope_intensity_black_body_category)]
        elif self.kaleidoscope_intensity_main_category == '2':
            name = custom_values_list[int(self.kaleidoscope_intensity_custom_category)]
            name = name.lower()
            name = name.replace(" ", "_")+".json"
            path = os.path.join(os.path.dirname(__file__), "values", name)
            value = None
            try:
                value_file = open(path, 'r')
                value = json.load(value_file)
            except:
                if kaleidoscope_props.sync_path != '':
                    path = os.path.join(kaleidoscope_props.sync_path, "values", name)
                    value_file = open(path, 'r')
                    value = json.load(value_file)

            self.kaleidoscope_intensity_out_value = value["Value"]
            IntensityNode.active_custom_preset = custom_values_list[int(self.kaleidoscope_intensity_custom_category)]
        return None
    def set_previous(self, context):
        global custom_values_list
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
        elif self.kaleidoscope_intensity_main_category == '2':
            if int(self.kaleidoscope_intensity_custom_category) > 0:
                self.kaleidoscope_intensity_custom_category = str(int(self.kaleidoscope_intensity_custom_category)-1)
            else:
                self.kaleidoscope_intensity_custom_category = str(len(custom_values_list)-1)
        return None
    def set_next(self, context):
        global custom_values_list
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
        elif self.kaleidoscope_intensity_main_category == '2':
            if int(self.kaleidoscope_intensity_custom_category) < len(custom_values_list)-1:
                self.kaleidoscope_intensity_custom_category = str(int(self.kaleidoscope_intensity_custom_category)+1)
            else:
                self.kaleidoscope_intensity_custom_category = '0'
        return None

    def get_custom_vals(self, context):
        global custom_values_list
        value_list = []
        global_values = []
        synced_values = []
        local_values = []

        custom_values_list.clear()
        check = False
        val = None
        try:
            f = open(os.path.join(os.path.dirname(__file__), "settings.json"), 'r')
            settings = json.load(f)
            val = os.path.join(settings['sync_directory'], "values")
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
                        global_values.append(name)

        i=0
        m='0'
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "values")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "values"))

        for sub in os.listdir(os.path.join(os.path.dirname(__file__), "values")):
            if os.path.isfile(os.path.join(os.path.dirname(__file__), "values", str(sub))):
                name = str(sub)
                if name.endswith('.json'):
                    name = name[:-5]
                    name = name.title()
                    name = name.replace('_', ' ')
                    if name in global_values:
                        value_list.append((m, name, "Choose the Saved Value from Library", "URL", i))
                        synced_values.append(name)
                    else:
                        value_list.append((m, name, "Choose the Saved Value from Local Library", "FILE", i))
                        local_values.append(name)
            i=i+1
            m=str(int(m)+1)

        if check == True:
            for sub in os.listdir(val):
                if os.path.isfile(os.path.join(val, str(sub))):
                    name = str(sub)
                    if name.endswith('.json'):
                        name = name[:-5]
                        name = name.title()
                        name = name.replace('_', ' ')
                        if name not in synced_values and name not in local_values:
                            value_list.append((m, name, "Choose the Saved Value from the Synced Library", "WORLD", i))
                i=i+1
                m=str(int(m)+1)

        for x in value_list:
            custom_values_list.append(x[1])
        return value_list

    num_val = 0.0
    active_custom_preset = None

    kaleidoscope_intensity_next_button = bpy.props.BoolProperty(name="Next", description="Select the Next Predefined Value", default=False, update=set_next)
    kaleidoscope_intensity_prev_button = bpy.props.BoolProperty(name="Previous", description="Select the Previous Predefined Value", default=False, update=set_previous)
    kaleidoscope_intensity_info = bpy.props.BoolProperty(name="Info", description="View/Hide Information about this category", default=False)

    kaleidoscope_intensity_out_value = bpy.props.FloatProperty(name="Value", description="The Value of the Intensity Node", precision=6, default=1.00, update=update_value)

    kaleidoscope_intensity_main_category = bpy.props.EnumProperty(name="Main Category", description="Select the Type of Values to be used for the node", items=(('0', 'Glass IOR', 'Select the Glass IOR Predefined values'),
                                                                                                                                         ('1', 'Blackbody', 'Select the Blackbody Predefined values'),
                                                                                                                                         ('2','Custom', 'Select the Custom Predefined values')), default='0', update=set_value)
    kaleidoscope_intensity_glass_category = bpy.props.EnumProperty(name="Glass IOR", description="Select the Predefined Value for the Index of Refraction (IOR)", items=(('0', 'Vacuum', ''),
                                                                                                                                                ('1', 'Air', ''),
                                                                                                                                                ('2', 'Helium', ''),
                                                                                                                                                ('3', 'Hydrogen', ''),
                                                                                                                                                ('4', 'Carbon dioxide', ''),
                                                                                                                                                ('5', 'Ice', ''),
                                                                                                                                                ('6', 'Water', ''),
                                                                                                                                                ('7', 'Beer', ''),
                                                                                                                                                ('8', 'Alcohol', ''),
                                                                                                                                                ('9', 'Sugar Solution', ''),
                                                                                                                                                ('10', 'Milk', ''),
                                                                                                                                                ('11', 'Lens', ''),
                                                                                                                                                ('12', 'Olive Oil', ''),
                                                                                                                                                ('13', 'Glycerine', ''),
                                                                                                                                                ('14', 'Plastic', ''),
                                                                                                                                                ('15', 'Soda-lime Glass', ''),
                                                                                                                                                ('16', 'Plexiglas', ''),
                                                                                                                                                ('17', 'Honey', ''),
                                                                                                                                                ('18', 'Crown glass', ''),
                                                                                                                                                ('19', 'Nylon', ''),
                                                                                                                                                ('20', 'Emerald', ''),
                                                                                                                                                ('21', 'Flint glass', ''),
                                                                                                                                                ('22', 'Crystal', ''),
                                                                                                                                                ('23', 'Cubic zirconia', ''),
                                                                                                                                                ('24', 'Diamond', ''),
                                                                                                                                                ('25', 'Moissanite', ''),
                                                                                                                                                ('26', 'Zinc selenide', '')), default='0', update=set_value)
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
    kaleidoscope_intensity_custom_category = bpy.props.EnumProperty(name="Custom Values", description="Seleect the Predefined Values from the Custom Category", items=get_custom_vals, update=set_value)

    def init(self, context):
        self.outputs.new('NodeSocketFloat', "Value")
        self.outputs["Value"].default_value = self.kaleidoscope_intensity_out_value
        self.width = 216.3

    def update(self):
        out = ""
        try:
            for world in bpy.data.worlds:
                for node in world.node_tree.nodes:
                    if node.bl_idname == "intensity.node":
                        for out in node.outputs:
                            if out.is_linked:
                                for o in out.links:
                                    if o.is_valid:
                                        if o.to_node.bl_idname == "NodeReroute":
                                            spectrum.update_reroutes("WorldNodeTree", world.name, node.name, o.to_node.name, "Value")
                                        o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
        except:
            pass

        try:
            for lamps in bpy.data.lamps:
                try:
                    for node in lamps.node_tree.nodes:
                        if node.bl_idname == "intensity.node":
                            for out in node.outputs:
                                if out.is_linked:
                                    for o in out.links:
                                        if o.is_valid:
                                            if o.to_node.bl_idname == "NodeReroute":
                                                spectrum.update_reroutes("LampNodeTree", lamps.name, node.name, o.to_node.name, "Value")
                                            o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
                except:
                    continue
        except:
            pass
        try:
            for mat in bpy.data.materials:
                try:
                    for node in mat.node_tree.nodes:
                        if node.bl_idname == "intensity.node":
                            for out in node.outputs:
                                if out.is_linked:
                                    for o in out.links:
                                        if o.is_valid:
                                            if o.to_node.bl_idname == "NodeReroute":
                                                spectrum.update_reroutes("ShaderNodeTree", mat.name, node.name, o.to_node.name, "Value")
                                            o.to_socket.node.inputs[o.to_socket.name].default_value = out.default_value
                except:
                    continue
        except:
            pass

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        intensity_ui(self, context, layout, self.name)
        global node_name
        node_name = self.name

    #Node Label
    def draw_label(self):
        return "Intensity"

def intensity_ui(self, context, layout, current_node):
        global custom_values_list
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

            elif kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '2':
                colb.label("Custom Values")
                colb.label()
                colb.label("This Section is just for you,")
                colb.label("to save all the values for later")
                colb.label("use.")
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
        row = col3.row(align=True)
        if kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '0':
            row.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_glass_category", text="")
        elif kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '1':
            row.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_black_body_category", text="")
        elif kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '2':
            if len(custom_values_list) != 0:
                row.prop(kaleidoscope_intensity_props, "kaleidoscope_intensity_custom_category", text="")
            else:
                row.label("No Saved Value")
        row.operator(client.SaveValueMenu.bl_idname, text="", icon="ZOOMIN")
        if kaleidoscope_intensity_props.kaleidoscope_intensity_main_category == '2' and len(custom_values_list) != 0:
            row.operator(client.DeleteValueMenu.bl_idname, text="", icon="ZOOMOUT")
        col4 = split2.column(align=True)
        col4.prop(kaleidoscope_intensity_props, 'kaleidoscope_intensity_next_button', text="", icon="TRIA_RIGHT", emboss=False, toggle=True)
        col.label()
        col.prop(kaleidoscope_intensity_props, 'kaleidoscope_intensity_out_value')
        col.label()
        row2 = col.row(align=True)
        row2_1 = row2.row(align=True)
        row2_1.alignment = 'CENTER'
        row2_1.label("Akash Hamirwasia")
        row2_1.scale_y=1.2
        row2_1.operator('wm.url_open', text="Support Me", icon='SOLO_ON').url='http://blskl.cf/kalsupport'

def register():
    bpy.app.handlers.frame_change_pre.append(pre_intensity_frame_change)

def unregister():
    pass

def pre_intensity_frame_change(scene):
    for m in bpy.data.materials:
        try:
            if m.node_tree is not None:
                for n in m.node_tree.nodes:
                    if n.bl_idname == 'intensity.node':
                        v = n.kaleidoscope_intensity_out_value
                        n.kaleidoscope_intensity_out_value = v
        except:
            continue

    for lamp in bpy.data.lamps:
        try:
            if lamp.node_tree is not None:
                for n in lamp.node_tree.nodes:
                    if n.bl_idname == 'intensity.node':
                        v = n.kaleidoscope_intensity_out_value
                        n.kaleidoscope_intensity_out_value = v
        except:
            continue

    for w in bpy.data.worlds:
        try:
            if w.node_tree is not None:
                for n in w.node_tree.nodes:
                    if n.bl_idname == 'intensity.node':
                        v = n.kaleidoscope_intensity_out_value
                        n.kaleidoscope_intensity_out_value = v
        except:
            continue
