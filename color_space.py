import bpy


class ImageTextureColorSpace(bpy.types.Operator):
    """Checks the current material node tree and sets the Color Space of Image Textures accordingly"""
    bl_idname = "kaleidoscope.texture_color_space"
    bl_label = "Set Color Space"

    def execute(self, context):
        self.color_space(bpy.context.object.active_material.node_tree)
        return {'FINISHED'}

    def color_space(self, node_tree):
        for node in node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                links = node.outputs[0].links
                if links:
                    if (links[0].to_socket.type == 'RGBA' or links[0].to_socket.type == 'RGB') and links[0].to_node.type != 'NORMAL_MAP':
                        node.color_space = 'COLOR'
                    else:
                        node.color_space = 'NONE'
            elif node.type == 'GROUP':
                self.color_space(node.node_tree)

        return None

def colorSpacePanel(self, context):
    layout = self.layout

    if context.object.active_material.node_tree.nodes.active.type == 'TEX_IMAGE':
        column = layout.column()
        column.scale_y = 1.5
        column.operator(ImageTextureColorSpace.bl_idname, text='Set Color Spaces', icon='COLOR');


def register():
    pass

def unregister():
    pass
