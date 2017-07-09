#Client System for the Spectrum and Intensity Node
#Used for Saving, Deleting and Publishing Files by Kaleidoscope
import bpy
import math
try:
    import ctypes
except:
    pass
import json, os, requests
import urllib.request
from collections import OrderedDict
from . import spectrum, intensity
if "bpy" in locals():
    import importlib
    importlib.reload(spectrum)
    importlib.reload(intensity)

palette_export = {}

class CancelProcess(bpy.types.Operator):
    """Cancel the Process"""
    bl_idname = "kaleidoscope.cancel_process"
    bl_label = "Cancel Process"

    def execute(self, context):
        try:
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE)
        except AttributeError:
            pass
        return{'FINISHED'}

#General Structure of layout which will be used by all the popups
def menu_layout_builder(self, yes_operator, process_type):
    layout = self.layout
    col = layout.column(align=True)
    col.scale_y = 1.2
    if process_type == "spectrum_save":
        col.label("Save a Color Palette", icon='FILE_TICK')
        col.label("(Palette will be synced if Sync Path is specified)")
        for i in range(1, 4):
            col.separator()
        col.prop(self, "name")
        col.separator()
        col.separator()
    elif process_type == "spectrum_publish":
        col.label("Publish a Color Palette", icon='WORLD')
        col.label("Are you sure you want to publish this palette?")
        col.label("On Publishing, all Kaleidoscope users will be able")
        col.label("to access your palette")
        col.label()
        col.label("This will be added to Community Online Palettes list")
        col.label("Make Sure your palette looks nice otherwise it")
        col.label("will get DELETED")
        for i in range(1, 4):
            col.separator()
    elif process_type == "spectrum_remove":
        col.label("Are you sure you want to", icon="ERROR")
        col.label("delete the current saved palette?")
        col.label()

    elif process_type == "intensity_save":
        col.label("Save a Value", icon='FILE_TICK')
        col.label("(Value will be synced if Sync Path is specified)")
        for i in range(1, 4):
            col.separator()
        col.prop(self, "name")
        col.separator()
        col.separator()
    elif process_type == "intensity_remove":
        col.label("Are you sure you want to", icon="ERROR")
        col.label("delete the current saved value?")
        col.label()

        row = layout.row(align = False)
        row.scale_y = 1.2
        for i in range(1, 8):
            row.separator()

    row = layout.row(align = False)
    row.scale_y = 1.2
    for i in range(1, 13):
        row.separator()
    row.alert = False
    row.separator()
    row.operator(yes_operator, text="Yes")
    """
    row.alert = False
    row.operator(CancelProcess.bl_idname, text="Cancel")"""

class SavePaletteMenu(bpy.types.Operator):
    """Save the current Palette for future use"""
    bl_idname = "spectrum.save_palette"
    bl_label = "Save Spectrum Palette"

    def set_name(self, context):
        kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
        kaleidoscope_spectrum_props.save_palette_name = self.name
        return None

    name = bpy.props.StringProperty(name="Palette Name", description="Enter the Name for the Palette", default="My Palette", update=set_name)

    def draw(self, context):
        menu_layout_builder(self, SavePaletteYes.bl_idname, "spectrum_save")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

class SavePaletteYes(bpy.types.Operator):
    """Save the Current Color Palette with the above name and sync it too"""
    bl_idname = "spectrum.save_palette_yes"
    bl_label = "Save Yes"

    def execute(self, context):
        try:
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE)
        except AttributeError:
            pass
        kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
        global palette_export
        name = kaleidoscope_spectrum_props.save_palette_name
        temp_name = name
        name = name.title()
        name = name.replace('_', ' ')
        kaleidoscope_spectrum_props.save_palette_name = name
        palette_export[kaleidoscope_spectrum_props.save_palette_name] = OrderedDict([
            ("palette_name", kaleidoscope_spectrum_props.save_palette_name),
            ("color1", spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color1)),
            ("color2", spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color2)),
            ("color3", spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color3)),
            ("color4", spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color4)),
            ("color5", spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color5))
        ])
        name = kaleidoscope_spectrum_props.save_palette_name
        name = name.lower()
        kaleidoscope_spectrum_props.save_palette_name = name.replace(' ', '_')
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "palettes")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "palettes"))
        path = os.path.join(os.path.dirname(__file__), "palettes", kaleidoscope_spectrum_props.save_palette_name+".json")
        s = json.dumps(palette_export, sort_keys=True)
        with open(path, "w") as f:
            f.write(s)

        if bpy.context.scene.kaleidoscope_props.sync_path != '':
            path = os.path.join(bpy.context.scene.kaleidoscope_props.sync_path, "palettes", kaleidoscope_spectrum_props.save_palette_name+".json")
            s = json.dumps(palette_export, sort_keys=True)
            with open(path, 'w') as f:
                f.write(s)
        temp_name = temp_name.title().replace("_", " ")
        self.report({'INFO'}, temp_name+" palette was saved successfully")
        return{'FINISHED'}

class PublishPaletteMenu(bpy.types.Operator):
    """Publish the current Palette"""
    bl_idname = "spectrum.publish_palette"
    bl_label = "Publish Spectrum Palette"

    def draw(self, context):
        menu_layout_builder(self, PublishPaletteYes.bl_idname, "spectrum_publish")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)


class PublishPaletteYes(bpy.types.Operator):
    """Publish the Current Color Palette"""
    bl_idname = "spectrum.publish_palette_yes"
    bl_label = "Publish Yes"

    def compare_colors(self, color1, color2):
        return math.pow((color1[0]-color2[0]), 2) + math.pow((color1[1]-color2[1]), 2) + math.pow((color1[2]-color2[2]), 2) # based on https://en.wikipedia.org/wiki/Color_difference

    def execute(self, context):
        try:
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE)
        except AttributeError:
            pass
        duplicate = False
        kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props

        community_palette_file = None
        if kaleidoscope_spectrum_props.new_community_file != 0:
            community_palette_file = str(urllib.request.urlopen("http://blskl.cf/kalcommunitypal").read(), 'UTF-8')
            if community_palette_file == "Off":
                spectrum.community_maintain = True
            else:
                kaleidoscope_spectrum_props.new_community_file = 0
                spectrum.community_palette = json.loads(community_palette_file)
                spectrum.community_maintain = False

        if community_palette_file != "Off":
            for palettes in spectrum.community_palette['Palettes']:
                col1 = spectrum.hex_to_real_rgb(spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color1))
                col2 = spectrum.hex_to_real_rgb(spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color2))
                col3 = spectrum.hex_to_real_rgb(spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color3))
                col4 = spectrum.hex_to_real_rgb(spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color4))
                col5 = spectrum.hex_to_real_rgb(spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color5))

                onl_col1 = spectrum.hex_to_real_rgb(palettes['Color_1'].rstrip('t'))
                onl_col2 = spectrum.hex_to_real_rgb(palettes['Color_2'].rstrip('t'))
                onl_col3 = spectrum.hex_to_real_rgb(palettes['Color_3'].rstrip('t'))
                onl_col4 = spectrum.hex_to_real_rgb(palettes['Color_4'].rstrip('t'))
                onl_col5 = spectrum.hex_to_real_rgb(palettes['Color_5'].rstrip('t'))

                comp1 = self.compare_colors(color1 = col1, color2 = onl_col1)
                comp2 = self.compare_colors(color1 = col2, color2 = onl_col2)
                comp3 = self.compare_colors(color1 = col3, color2 = onl_col3)
                comp4 = self.compare_colors(color1 = col4, color2 = onl_col4)
                comp5 = self.compare_colors(color1 = col5, color2 = onl_col5)

                if comp1 <= 3 and comp2 <= 3 and comp3 <= 3 and comp4 <= 3 and comp5 <= 3:
                    duplicate = True
                    break
                else:
                    duplicate = False
        else:
            self.report({'INFO'}, "Community Palettes Database is going through maintenance, check later")

        if duplicate == False:
            post_url = str("https://docs.google.com/forms/d/e/1FAIpQLSdVOWNzUeDwudMBcPNHfMRbDCMmNbQAK8A8DbX26u1w8oSYOA/formResponse?entry.737918241="+spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color1).lstrip('#')+"t"+"&entry.552637366="+spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color2).lstrip('#')+"t"+"&entry.1897395291="+spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color3).lstrip('#')+"t"+"&entry.1035475240="+spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color4).lstrip('#')+"t"+"&entry.577277592="+spectrum.rgb_to_hex(kaleidoscope_spectrum_props.color5).lstrip('#')+"t")
            out = requests.post(post_url)
            if out.status_code == 200:
                self.report({'INFO'}, 'Palette Successfully Published, Shift+Click \'Refresh\' to reload the Community Palettes')
            else:
                self.report({'WARNING'}, 'There was a Problem. Try again Later')
        else:
            self.report({'WARNING'}, 'A Palette of those colors already exists')
        return{'FINISHED'}

class DeletePaletteMenu(bpy.types.Operator):
    """Delete the Current Selected Palette"""
    bl_idname = "spectrum.save_palette_remove"
    bl_label = "Delete"

    def draw(self, context):
        menu_layout_builder(self, DeletePaletteYes.bl_idname, "spectrum_remove")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

class DeletePaletteYes(bpy.types.Operator):
    """Delete the Current Selected Palette"""
    bl_idname = "spectrum.save_palette_remove_yes"
    bl_label = "Delete Yes"

    def execute(self, context):
        try:
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE)
        except AttributeError:
            pass
        local_error = False
        global_error = False
        kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
        name = kaleidoscope_spectrum_props.saved_palettes
        temp_name = name
        name = name.lower()
        name = name.replace(' ', '_')
        path = os.path.join(os.path.dirname(__file__), "palettes", name+".json")
        try:
            os.remove(path)
        except:
            local_error = True

        if bpy.context.scene.kaleidoscope_props.sync_path != '':
            try:
                path = os.path.join(bpy.context.scene.kaleidoscope_props.sync_path, "palettes", name+".json")
                os.remove(path)
            except:
                global_error = True

        if local_error == False or global_error == False:
            self.report({'INFO'}, temp_name+" palette was successfully deleted")
        else:
            self.report({'WARNING'}, temp_name+" palette could not be deleted")
        return{'CANCELLED'}

#Intensity Node
class SaveValueMenu(bpy.types.Operator):
    """Save the current Value for future use"""
    bl_idname = "intensity.save_value"
    bl_label = "Save Intensity Value"

    def set_name(self, context):
        SaveValueMenu.pass_name = (self.name.replace(' ', '_')).lower()
        return None

    pass_name = None
    name = bpy.props.StringProperty(name="Value Name", description="Enter the Name for the Value", default="My Value", update=set_name)

    def draw(self, context):
        menu_layout_builder(self, SaveValueYes.bl_idname, "intensity_save")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

class SaveValueYes(bpy.types.Operator):
    """Save the current Value with the above name and sync it too"""
    bl_idname = "intensity.save_value_yes"
    bl_label = "Save Yes"

    def execute(self, context):
        try:
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE)
        except AttributeError:
            pass
        kaleidoscope_props = bpy.context.scene.kaleidoscope_props
        name = SaveValueMenu.pass_name
        temp_name = name
        name = name.title()
        name = name.replace('_', ' ')
        value_export = OrderedDict([
            ("value_name", name),
            ("Value", float(intensity.IntensityNode.num_val))
        ])
        name = SaveValueMenu.pass_name
        name = name.lower()
        SaveValueMenu.pass_name = name.replace(' ', '_')
        if kaleidoscope_props.sync_path != '':
            if not os.path.exists(os.path.join(kaleidoscope_props.sync_path, "values")):
                os.makedirs(os.path.join(kaleidoscope_props.sync_path, "values"))

        if not os.path.exists(os.path.join(os.path.dirname(__file__), "values")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "values"))
        path = os.path.join(os.path.dirname(__file__), "values", SaveValueMenu.pass_name+".json")
        s = json.dumps(value_export, sort_keys=True)
        with open(path, "w") as f:
            f.write(s)

        if kaleidoscope_props.sync_path != '':
            path = os.path.join(kaleidoscope_props.sync_path, "values", SaveValueMenu.pass_name+".json")
            s = json.dumps(value_export, sort_keys=True)
            with open(path, 'w') as f:
                f.write(s)
        intensity.IntensityNode.get_custom_vals(self, context)
        temp_name = temp_name.title().replace('_', " ")
        self.report({'INFO'}, temp_name+" value was saved successfully")
        return{'FINISHED'}

class DeleteValueMenu(bpy.types.Operator):
    """Remove this Value from the list"""
    bl_idname = "intensity.remove_value"
    bl_label = "Remove Intensity Value"

    def draw(self, context):
        menu_layout_builder(self, DeleteValueYes.bl_idname, "intensity_remove")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

class DeleteValueYes(bpy.types.Operator):
    """Remove this Value from the list"""
    bl_idname = "intensity.remove_value_yes"
    bl_label = "Delete Yes"

    def execute(self, context):
        try:
            VK_ESCAPE = 0x1B
            ctypes.windll.user32.keybd_event(VK_ESCAPE)
        except AttributeError:
            pass
        kaleidoscope_props=bpy.context.scene.kaleidoscope_props
        local_error = False
        global_error = False
        name = intensity.IntensityNode.active_custom_preset
        temp_name = name
        name = name.lower().replace(' ', '_')+".json"
        path = os.path.join(os.path.dirname(__file__), "values", name)
        try:
            os.remove(path)
        except:
            local_error = True
        try:
            if kaleidoscope_props.sync_path != '':
                path = os.path.join(kaleidoscope_props.sync_path, "values", name)
                try:
                    os.remove(path)
                except:
                    self.report({'INFO'}, "Custom Value is not Selected")
        except:
            global_error = True

        if local_error == False or global_error == False:
            self.report({'INFO'}, temp_name+" value was successfully deleted")
        else:
            self.report({'WARNING'}, temp_name+" value could not be deleted")
        return{'FINISHED'}

def register():
    pass

def unregister():
    pass
