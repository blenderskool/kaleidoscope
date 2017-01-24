import os
import bpy
import bpy.utils.previews

icons_dict = {}
icons_check = False

def load_icons():
    global icons_dict
    global icons_check

    if icons_check:
        return icons_dict["main"]

    ka_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    ka_icons.load("ka_PUBLISH", os.path.join(icons_dir, "publish.png"), 'IMAGE')
    ka_icons.load("ka_SAVE", os.path.join(icons_dir, "save.png"), 'IMAGE')

    icons_dict["main"] = ka_icons
    icons_check = True

    return icons_dict["main"]

def clear_icons():
    global icons_check
    for icon in icons_dict.values():
        bpy.utils.previews.remove(icon)
    icons_dict.clear()
    icons_check = False
