#Client System for the Spectrum and Intensity Node
#Used for Saving, Deleting Files by Kaleidoscope
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
        col.label(text="Save a Color Palette", icon='FILE_TICK')
        for i in range(1, 4):
            col.separator()
        col.prop(self, "name")
        col.separator()
        col.separator()
    elif process_type == "spectrum_remove":
        col.label(text="Are you sure you want to", icon="ERROR")
        col.label(text="delete the current saved palette?")
        col.label()

    elif process_type == "intensity_save":
        col.label(text="Save a Value", icon='FILE_TICK')
        for i in range(1, 4):
            col.separator()
        col.prop(self, "name")
        col.separator()
        col.separator()
    elif process_type == "intensity_remove":
        col.label(text="Are you sure you want to", icon="ERROR")
        col.label(text="delete the current saved value?")
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

class SavePaletteMenu(bpy.types.Operator):
    """Save the current Palette for future use"""
    bl_idname = "spectrum.save_palette"
    bl_label = "Save Spectrum Palette"

    def set_name(self, context):
        kaleidoscope_spectrum_props=bpy.context.scene.kaleidoscope_spectrum_props
        kaleidoscope_spectrum_props.save_palette_name = self.name
        return None

    name: bpy.props.StringProperty(name="Palette Name", description="Enter the Name for the Palette", default="My Palette", update=set_name)

    def draw(self, context):
        menu_layout_builder(self, SavePaletteYes.bl_idname, "spectrum_save")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

class SavePaletteYes(bpy.types.Operator):
    """Save the Current Color Palette with the above name"""
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

        temp_name = temp_name.title().replace("_", " ")
        self.report({'INFO'}, temp_name+" palette was saved successfully")
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

        if local_error == False:
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

    pass_name = None
    name: bpy.props.StringProperty(name="Value Name", description="Enter the Name for the Value", default="My Value", update=set_name)

    def draw(self, context):
        menu_layout_builder(self, SaveValueYes.bl_idname, "intensity_save")

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_popup(self)

class SaveValueYes(bpy.types.Operator):
    """Save the current Value with the above name"""
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

        if not os.path.exists(os.path.join(os.path.dirname(__file__), "values")):
            os.makedirs(os.path.join(os.path.dirname(__file__), "values"))
        path = os.path.join(os.path.dirname(__file__), "values", SaveValueMenu.pass_name+".json")
        s = json.dumps(value_export, sort_keys=True)
        with open(path, "w") as f:
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
        name = intensity.IntensityNode.active_custom_preset
        temp_name = name
        name = name.lower().replace(' ', '_')+".json"
        path = os.path.join(os.path.dirname(__file__), "values", name)
        try:
            os.remove(path)
        except:
            local_error = True

        if local_error == False:
            self.report({'INFO'}, temp_name+" value was successfully deleted")
        else:
            self.report({'WARNING'}, temp_name+" value could not be deleted")
        return{'FINISHED'}

def register():
    pass

def unregister():
    pass
