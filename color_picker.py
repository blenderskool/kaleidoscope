# Advnced ColorRamp Color Picker Tool

import bpy
import blf
import math
import bgl
from . import spectrum

node_tree_type = None
start_draw = False
x_loc = 0
y_loc = 0

def draw_call(self, context):
    global x_loc
    global y_loc

    width = 30
    height = 30

    """if start_draw == True:
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glLineWidth(4)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glColor4f(0.0, 0.0, 0.0, 0.75)
        for x, y in self.draw_mouse_path:
            bgl.glVertex2i(x, y)

        bgl.glEnd()"""

    bgl.glEnable(bgl.GL_BLEND)
    bgl.glColor4f(1.0, 1.0, 1.0, 0.98)
    font_id = 0

    #Info of the Modal
    blf.position(font_id, 25, 20, 0)
    blf.size(font_id, 20, 57)
    blf.draw(font_id, "Press Enter to Confirm")

    blf.position(font_id, 40, 7, 0)
    blf.size(font_id, 20, 40)
    blf.draw(font_id, "Kaleidoscope Modal 0.1")

    bgl.glBegin(bgl.GL_QUADS)
    bgl.glColor3f(c[0][0], c[0][1], c[0][2])
    bgl.glVertex3f(x_loc+20,y_loc+20,0)
    bgl.glVertex3f(x_loc+20+width,y_loc+20,0)
    bgl.glVertex3f(x_loc+20+width,y_loc+height+20,0)
    bgl.glVertex3f(x_loc+20,y_loc+height+20,0)
    bgl.glEnd()

    if c[0][0] < 0.1 and c[0][1] < 0.1 and c[0][2] < 0.1:
        bgl.glColor3f(1, 1, 1)
    else:
        bgl.glColor3f(0, 0, 0)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2f(x_loc+20-1, y_loc+20-1)
    bgl.glVertex2f(x_loc+20+width+1, y_loc+20-1)
    bgl.glVertex2f(x_loc+20+width, y_loc+20+height+1)
    bgl.glVertex2f(x_loc+20-1, y_loc+20+height)
    bgl.glVertex2f(x_loc+20-1, y_loc+20-1)
    bgl.glEnd()

c = bgl.Buffer(bgl.GL_FLOAT, [1,3])
selected_col = bgl.Buffer(bgl.GL_FLOAT, [1,3])
col_list = []

class ModalPickerOperator(bpy.types.Operator):
    """Kaleidoscope Color Picker Tool"""
    bl_idname = "kaleidoscope.color_picker"
    bl_label = "Kaleidoscope Color Picker Modal"

    def modal(self, context, event):
        context.area.tag_redraw()
        global start_draw

        if event.type == 'MOUSEMOVE':
            global x_loc
            global y_loc

            x_loc = event.mouse_region_x
            y_loc = event.mouse_region_y
            bgl.glReadPixels(event.mouse_x, event.mouse_y,1,1,bgl.GL_RGB,bgl.GL_FLOAT,c)
            if start_draw == True:
                self.draw_mouse_path.append((event.mouse_region_x, event.mouse_region_y))
                self.mouse_color_path.append((event.mouse_x, event.mouse_y))
            else:
                self.draw_mouse_path.clear()

        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                start_draw = True
            else:
                start_draw = False
                #if self.cursor_set:
                #context.window.cursor_modal_restore()
                #bpy.types.SpaceImageEditor.draw_handler_remove(self._handle, 'WINDOW')

                for x, y in self.mouse_color_path:
                    bgl.glReadPixels(x, y,1,1,bgl.GL_RGB,bgl.GL_FLOAT,selected_col)
                    col_list.append((selected_col[0][0], selected_col[0][1], selected_col[0][2]))
                total_colors = len(col_list)
                if total_colors > 32:
                    total_colors = 32
                if node_tree_type == 'OBJECT':
                    # Objects
                    if bpy.context.object.active_material.node_tree.nodes.active.type == 'VALTORGB':
                        node = bpy.context.object.active_material.node_tree.nodes.active
                elif node_tree_type == 'WORLD':
                    # World
                    if bpy.context.scene.world.node_tree.nodes.active.type == 'VALTORGB':
                        node = bpy.context.scene.world.node_tree.nodes.active
                elif node_tree_type == 'LAMP':
                    # Lamps
                    for lamp in bpy.data.lamps:
                        if lamp.name == bpy.context.active_object.name:
                            if lamp.node_tree.nodes.active.type == 'VALTORGB':
                                node = lamp.node_tree.nodes.active
                                break
                while len(node.color_ramp.elements) > 1:
                    node.color_ramp.elements.remove(node.color_ramp.elements[0])
                i=1
                color1 = None
                for color in col_list:
                    if i > 1:
                        color_rgb = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
                        res = math.pow((color_rgb[0]-color1[0]), 2) + math.pow((color_rgb[1]-color1[1]), 2) + math.pow((color_rgb[2]-color1[2]), 2)
                        if res > 10:
                            color = spectrum.hex_to_rgb(spectrum.real_rgb_to_hex(color_rgb))
                            try:
                                element = node.color_ramp.elements.new(i/total_colors)
                                element.color[0] = color[0]
                                element.color[1] = color[1]
                                element.color[2] = color[2]
                            except:
                                self.report({'INFO'}, 'ColorRamp limit exceed, some colors have been removed')
                            color1 = color_rgb
                            i=i+1
                        else:
                            i=i+1
                            continue
                    elif i == 1:
                        color1 = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
                        color = spectrum.hex_to_rgb(spectrum.real_rgb_to_hex(color1))
                        node.color_ramp.elements[0].position = i/total_colors
                        node.color_ramp.elements[0].color[0] = color[0]
                        node.color_ramp.elements[0].color[1] = color[1]
                        node.color_ramp.elements[0].color[2] = color[2]
                        i=i+1

        elif event.type == 'ESC':
            if self.cursor_set:
                col_list.clear()
                context.window.cursor_modal_restore()
                bpy.types.SpaceImageEditor.draw_handler_remove(self._handle, 'WINDOW')

            return {'CANCELLED'}
        elif event.type in {'RET', 'RIGHTMOUSE'}:
            if self.cursor_set:
                col_list.clear()
                context.window.cursor_modal_restore()
                bpy.types.SpaceImageEditor.draw_handler_remove(self._handle, 'WINDOW')

            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.cursor_set = False
        if context.area.type == 'IMAGE_EDITOR':
            self.cursor_set = False
            args = (self, context)
            self.draw_mouse_path = []
            self.mouse_color_path = []
            self._handle = bpy.types.SpaceImageEditor.draw_handler_add(draw_call, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            bpy.context.window.cursor_modal_set('EYEDROPPER')
            self.cursor_set = True
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "Image Editor not found, Color Picker will not run")
            return {'CANCELLED'}

class ColorPickerButton(bpy.types.Operator):
    """Use the Kaleidoscope Color Picker to Sample an Image for colors"""
    bl_idname = "kaleidoscope.color_picker_button"
    bl_label = "Color Picker Button"

    def execute(self, context):
        for area in bpy.context.screen.areas:
            if area.type == 'IMAGE_EDITOR':
                image_editor = True
                override = {'area': area, 'region': area.regions[-1]}
                bpy.ops.kaleidoscope.color_picker(override, 'INVOKE_SCREEN')
                break

        return{'FINISHED'}

def color_picker_button_ui(self, context):
    global node_tree_type
    layout = self.layout
    layout.separator()
    box = layout.box()
    box.label("Kaleidoscope Picker", icon='COLOR')
    row = box.row(align=True)
    if bpy.context.space_data.shader_type == 'OBJECT' and bpy.context.active_object.type != 'LAMP':
        # Object
        node_tree_type = 'OBJECT'
        if bpy.context.object.active_material.node_tree.nodes.active.type == 'VALTORGB':
            row.enabled = True
        else:
            row.enabled = False

    elif bpy.context.space_data.shader_type == 'WORLD':
        # World
        node_tree_type = 'WORLD'
        if bpy.context.scene.world.node_tree.nodes.active.type == 'VALTORGB':
            row.enabled = True
        else:
            row.enabled = False
    else:
        # Lamps
        for lamp in bpy.data.lamps:
            if lamp.name == bpy.context.active_object.name:
                node_tree_type = 'LAMP'
                if bpy.context.scene.world.node_tree.nodes.active.type == 'VALTORGB':
                    row.enabled = True
                else:
                    row.enabled = False
                break
    row.scale_y = 1.2
    row.operator(ColorPickerButton.bl_idname, text='Use Color Picker', icon='EYEDROPPER')
    if bpy.context.space_data.shader_type == 'OBJECT' and bpy.context.active_object.type != 'LAMP':
        # Object
        if bpy.context.object.active_material.node_tree.nodes.active.type != 'VALTORGB':
            col = box.column(align=True)
            col.label("Active Node is not")
            col.label("a valid ColorRamp node.")
    elif bpy.context.space_data.shader_type == 'WORLD':
        # World
        if bpy.context.scene.world.node_tree.nodes.active.type != 'VALTORGB':
            col = box.column(align=True)
            col.label("Active Node is not")
            col.label("a valid ColorRamp node.")
    else:
        # Lamps
        for lamp in bpy.data.lamps:
            if lamp.name == bpy.context.active_object.name:
                if bpy.context.scene.world.node_tree.nodes.active.type != 'VALTORGB':
                    col = box.column(align=True)
                    col.label("Active Node is not")
                    col.label("a valid ColorRamp node.")
                    break
