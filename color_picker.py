# Advnced ColorRamp Color Picker Tool

import bpy
import blf
import math
import bgl
from . import spectrum
from bpy.app.handlers import persistent

click_area_x = None
click_area_y = None
width = None
height = None
start_draw = False
ui = None
x_loc = 0
y_loc = 0

class BGLWidget:
    handle = None

    def __init__(self, op, context, areatype):

        # Calculate scroller width, dpi and pixelsize dependent
        self.pixel_size = context.user_preferences.system.pixel_size
        self.dpi = context.user_preferences.system.dpi
        self.dpi_fac = self.pixel_size * self.dpi / 72
        # A normal widget unit is 20, but the scroller is apparently 16
        self.scroller_width = 16 * self.dpi_fac

        self.op = op
        self.areatype = areatype

        self.handle = self.create_handle(context)
        theme = context.user_preferences.themes[0]
        self.theme = theme

    def create_handle(self, context):
        handle = self.areatype.draw_handler_add(
            self.draw_region,
            (context,),'WINDOW', 'POST_PIXEL')
        return handle

    def remove_handle(self):
        if self.handle:
            self.areatype.draw_handler_remove(self.handle, 'WINDOW')
            self.handle = None

    def draw_region(self, context):
        # check validity
        self.visualise(context)

    def draw_box(self, x, y, w, h, color=(0.0, 0.0, 0.0, 1.0)):
        global click_area_x
        global click_area_y
        global width
        global height

        click_area_x = x
        click_area_y = y
        width = w
        height = h

        try:
            if bpy.context.object.active_material.node_tree.nodes.active.type == 'VALTORGB':
                bgl.glEnable(bgl.GL_BLEND)
                bgl.glBegin(bgl.GL_POLYGON)
                bgl.glColor4f(0.0,0.33,0.49, 0.8)
                bgl.glVertex2f(x,y+h)

                bgl.glVertex2f(x,y)

                bgl.glColor4f(0.23,0.63,0.49, 0.6)
                bgl.glVertex2f(x+w-5,y)

                bgl.glVertex2f(x+w-5, y+h)

                bgl.glEnd()

                bgl.glBegin(bgl.GL_LINES)
                bgl.glColor3f(0.0,0.0,0.0)
                bgl.glVertex2f(x,y)
                bgl.glVertex2f(x,y+h)

                bgl.glVertex2f(x,y)
                bgl.glVertex2f(x+w-5,y)

                bgl.glVertex2f(x,y+h)
                bgl.glVertex2f(x+w-5,y+h)

                bgl.glVertex2f(x+w-5,y)
                bgl.glVertex2f(x+w-5,y+h+1)
                bgl.glEnd()

                bgl.glEnable(bgl.GL_LINES)
                bgl.glColor4f(1.0, 1.0, 1.0, 0.8)

                font_id = 0  # XXX, need to find out how best to get this.

                # draw some text
                blf.position(font_id, x+w/2-39, y+h/2+4, 0)
                blf.size(font_id, 20, 43)
                blf.draw(font_id, "Kaleidoscope")

                blf.position(font_id, x+w/2-43, y+h/2-12, 0)
                blf.size(font_id, 20, 55)
                blf.draw(font_id, "Color Picker")
                bgl.glEnd()

                bgl.glFlush()
        except:
            pass

    def visualise(self, context):
        # used to draw override in class def
        pass

class Button:
    def __init__(self, x, y, w, h, color=(1,1,1,1)):
        #draw a box
        self.x = 0
        self.y = 0
        self.w = w
        self.h = h
        self.color = color

    def __str__(self):
        return "Button %s" % str(self.color)

    def __repr__(self):
        return "Button %d %d color(%s)" % (self.x, self.y, str(self.color))

    def in_box(self, x, y):
        return (self.x < x < self.x + self.w and self.y < y < self.y + self.h)


class ButtonWidget(BGLWidget):
    help_screen = -1
    buttons = []
    screen_buttons = {}
    def button(self, w, h):
        # add a new button
        b = Button(0, 0, w, h)
        self.buttons.append(b)
        return b

    def visualise(self, context):
        for b in self.buttons:
            self.draw_button(b, context)

    def draw_button(self, box, context):
        m = [i for i, a in enumerate(context.screen.areas) if a == context.area]
        if not len(m):
            return None
        key = "area%d" % m[0]
        b = self.screen_buttons.setdefault(key, Button(box.x, box.y, box.w, box.h, color=box.color))
        b.x = context.region.width - b.w - self.scroller_width
        b.y = context.region.height - b.h - self.scroller_width
        self.draw_box(b.x, b.y, b.w, b.h, color=b.color)

class ColorPickerModalButton(bpy.types.Operator):
    bl_idname = "kaleidoscope.color_picker_button"
    bl_label = "Color Picker Button"

    def modal(self, context, event):
        def in_area(area, x, y):

            return (area.x < x < area.x + area.width and area.y < y < area.y + area.height)

        screen = context.screen
        mx = event.mouse_x
        my = event.mouse_y
        global click_area_x
        global click_area_y
        global width
        global height
        areas = [i for i, a in enumerate(screen.areas) if a.type.startswith('NODE_EDITOR') and in_area(a, mx, my)]

        for i in areas:
            a = screen.areas[i]
            region = a.regions[-1]
            x = mx - region.x
            y = my - region.y

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':

                if x >= click_area_x and x <= click_area_x+width:
                    if y >= click_area_y and y <= click_area_y+height:
                        try:
                            for a in bpy.context.screen.areas:
                                if a.type == 'IMAGE_EDITOR':
                                    override = {'area': a, 'region': a.regions[-1]}
                                    bpy.ops.kaleidoscope.color_picker(override, 'INVOKE_SCREEN')
                        except:
                            pass

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

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
    font_id = 0  # XXX, need to find out how best to get this.

    # draw some text
    blf.position(font_id, 25, 20, 0)
    blf.size(font_id, 20, 57)
    blf.draw(font_id, "Press Enter to Confirm")

    blf.position(font_id, 40, 7, 0)
    blf.size(font_id, 20, 40)
    blf.draw(font_id, "Kaleidoscope Modal 0.1")

    bgl.glBegin(bgl.GL_QUADS)
    bgl.glColor3f(c[0][0], c[0][1], c[0][2])
    bgl.glVertex3f(x_loc+10,y_loc+10,0)
    bgl.glVertex3f(x_loc+10+width,y_loc+10,0)
    bgl.glVertex3f(x_loc+10+width,y_loc+height+10,0)
    bgl.glVertex3f(x_loc+10,y_loc+height+10,0)
    bgl.glEnd()

    if c[0][0] < 0.1 and c[0][1] < 0.1 and c[0][2] < 0.1:
        bgl.glColor3f(1, 1, 1)
    else:
        bgl.glColor3f(0, 0, 0)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glLineWidth(1)
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2f(x_loc+10-1, y_loc+10-1)
    bgl.glVertex2f(x_loc+10+width+1, y_loc+10-1)
    bgl.glVertex2f(x_loc+10+width, y_loc+10+height+1)
    bgl.glVertex2f(x_loc+10-1, y_loc+10+height)
    bgl.glVertex2f(x_loc+10-1, y_loc+10-1)
    bgl.glEnd()

c = bgl.Buffer(bgl.GL_FLOAT, [1,3])
selected_col = bgl.Buffer(bgl.GL_FLOAT, [1,3])
col_list = []

class ModalPickerOperator(bpy.types.Operator):
    """Kaleidoscope Color Picker"""
    bl_idname = "kaleidoscope.color_picker"
    bl_label = "OpenGL Advanced Color Picker"

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
                if bpy.context.object.active_material.node_tree.nodes.active.type == 'VALTORGB':
                    node = bpy.context.object.active_material.node_tree.nodes.active
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
            bpy.context.window_manager.modal_handler_add(self)
            bpy.context.window.cursor_modal_set('EYEDROPPER')
            self._handle = bpy.types.SpaceImageEditor.draw_handler_add(draw_call, args, 'WINDOW', 'POST_PIXEL')
            self.cursor_set = True
            self.record = False
            context.area.tag_redraw()
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

@persistent
def set_modal(self):
    global ui
    try:
        bpy.app.handlers.scene_update_pre.remove(set_modal)
    except ValueError:
        pass
    context = bpy.context
    h = 35
    w = 100
    ui = ButtonWidget(None, context, bpy.types.SpaceNodeEditor)
    button = ui.button(w, h)
    for a in context.screen.areas:
        if a.type == 'NODE_EDITOR':
            a.tag_redraw()
    bpy.ops.kaleidoscope.color_picker_button('INVOKE_SCREEN')

def remove_modal():
    global ui
    ui.remove_handle()
