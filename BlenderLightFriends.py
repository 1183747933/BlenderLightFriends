bl_info = {
    "name": "BlenderLightFriends",
    "author": "LITTLE_HOUSE_STUDIO",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "View3D > Sidebar > [ 光 ]",
    "description": "one",
    "category": "Lighting",
}

import bpy
import math
from mathutils import Vector
import bpy_extras.view3d_utils

class LightPreset(bpy.types.PropertyGroup):
    shape: bpy.props.EnumProperty(
        name="Shape",
        items=[('RECTANGLE', 'Rectangle', ''), ('ELLIPSE', 'Ellipse', '')],
        default='RECTANGLE'
    )
    size: bpy.props.FloatProperty(
        name="Width",
        default=2.0,
        min=0.1,
        max=50.0
    )
    height: bpy.props.FloatProperty(
        name="Height",
        default=1.0,
        min=0.1,
        max=50.0
    )
    spread: bpy.props.FloatProperty(
        name="Spread",
        default=0.2,
        min=0.0,
        max=1.0,
        subtype='FACTOR'
    )
    distance: bpy.props.FloatProperty(
        name="Default Distance",
        default=10.0,
        min=0.1,
        max=100.0
    )
    power: bpy.props.FloatProperty(
        name="Power",
        default=500.0,
        min=0.0,
        soft_max=2000.0
    )

class LightItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Name")
    light_obj: bpy.props.PointerProperty(type=bpy.types.Object)

    longitude: bpy.props.FloatProperty(
        name="Longitude",
        default=0.0,
        min=-180.0,
        max=180.0,
        update=lambda self, context: self.update_geo_position()
    )
    latitude: bpy.props.FloatProperty(
        name="Latitude",
        default=45.0,
        min=-89.9,
        max=89.9,
        update=lambda self, context: self.update_geo_position()
    )
    distance: bpy.props.FloatProperty(
        name="Distance",
        default=10.0,
        min=0.1,
        max=100.0,
        update=lambda self, context: self.update_geo_position()
    )
    track_offset: bpy.props.FloatVectorProperty(
        name="Constraint Offset",
        subtype='TRANSLATION',
        default=(0.0, 0.0, 0.0),
        update=lambda self, context: self.update_geo_position()
    )
    size: bpy.props.FloatProperty(
        name="Width",
        default=2.0,
        min=0.1,
        max=50.0,
        update=lambda self, context: self.update_light_data()
    )
    height: bpy.props.FloatProperty(
        name="Height",
        default=1.0,
        min=0.1,
        max=50.0,
        update=lambda self, context: self.update_light_data()
    )
    spread: bpy.props.FloatProperty(
        name="Spread",
        default=0.2,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
        update=lambda self, context: self.update_light_data()
    )
    power: bpy.props.FloatProperty(
        name="Power",
        default=500.0,
        min=0.0,
        soft_max=2000.0,
        update=lambda self, context: self.update_light_data()
    )
    color: bpy.props.FloatVectorProperty(
        name="Color",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        update=lambda self, context: self.update_light_data()
    )
    normal_tracking: bpy.props.BoolProperty(
        name="Normal Tracking",
        default=False
    )
    track_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Tracking Target",
        update=lambda self, context: self.setup_constraints()
    )
    offset_obj: bpy.props.PointerProperty(
        name="Constraint Empty",
        type=bpy.types.Object
    )

    def update_geo_position(self):
        if not self.light_obj or not self.track_target:
            return
        if self.offset_obj:
            self.offset_obj.location = Vector(self.track_offset)
            base = self.offset_obj.matrix_world.to_translation()
        else:
            base = self.track_target.location + Vector(self.track_offset)
        theta = math.radians(90 - self.latitude)
        phi = math.radians(self.longitude)
        x = self.distance * math.sin(theta) * math.cos(phi)
        y = self.distance * math.sin(theta) * math.sin(phi)
        z = self.distance * math.cos(theta)
        new_location = base + Vector((x, y, z))
        self.light_obj.location = new_location
        self.light_obj.rotation_euler = (
            math.radians(self.latitude),
            0,
            math.radians(self.longitude) + math.pi / 2
        )

    def update_light_data(self):
        if self.light_obj and self.light_obj.data:
            light = self.light_obj.data
            light.size = self.size
            light.size_y = self.height
            light.spread = self.spread
            light.energy = self.power
            light.color = self.color

    def setup_constraints(self):
        if not self.light_obj or not self.track_target:
            return
        if not self.offset_obj:
            empty_name = f"Empty_{self.light_obj.name}"
            empty = bpy.data.objects.new(empty_name, None)
            empty.empty_display_size = 0.5
            empty.empty_display_type = 'ARROWS'
            bpy.context.scene.collection.objects.link(empty)
            empty.parent = self.track_target
            empty.location = self.track_offset
            self.offset_obj = empty
        else:
            if self.offset_obj.parent != self.track_target:
                self.offset_obj.parent = self.track_target
            self.offset_obj.location = self.track_offset
        for c in self.light_obj.constraints:
            if c.type == 'TRACK_TO':
                self.light_obj.constraints.remove(c)
        track_constraint = self.light_obj.constraints.new('TRACK_TO')
        track_constraint.target = self.offset_obj
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'

class LIGHT_OT_PointAndShoot(bpy.types.Operator):
    bl_idname = "light.point_and_shoot"
    bl_label = "Point and Shoot"
    bl_options = {'REGISTER', 'UNDO'}

    _light_item = None
    is_tracking = False

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.report({'INFO'}, "Point and Shoot canceled")
            return {'CANCELLED'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.is_tracking = True
            elif event.value == 'RELEASE':
                self.report({'INFO'}, "Point and Shoot finished")
                return {'FINISHED'}
        if self.is_tracking and event.type == 'MOUSEMOVE':
            region = context.region
            rv3d = context.space_data.region_3d
            coord = (event.mouse_region_x, event.mouse_region_y)
            view_vector = bpy_extras.view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
            result, location, normal, index, obj, matrix = context.scene.ray_cast(context.view_layer.depsgraph, ray_origin, view_vector)
            if result:
                new_track_offset = location - self._light_item.track_target.location
                self._light_item.track_offset = new_track_offset
                if self._light_item.normal_tracking:
                    n = normal.normalized()
                    theta = math.acos(n.z)
                    new_latitude = 90 - math.degrees(theta)
                    new_longitude = math.degrees(math.atan2(n.y, n.x))
                    self._light_item.latitude = new_latitude
                    self._light_item.longitude = new_longitude
                self._light_item.update_geo_position()
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        idx = context.scene.light_index
        if idx < 0:
            self.report({'ERROR'}, "No light selected")
            return {'CANCELLED'}
        self._light_item = context.scene.light_items[idx]
        self.is_tracking = False
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "Press left mouse button and drag to select target position, then release to finish")
        return {'RUNNING_MODAL'}

class LIGHT_UL_LightList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text=item.name, icon='LIGHT')
            row.operator("light.remove_light", text="", icon="TRASH").item_name = item.name
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='LIGHT')

class LIGHT_PT_MainPanel(bpy.types.Panel):
    bl_label = "BlenderLightFriends"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "[ 光 ]"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        box = layout.box()
        box.label(text="Preset Parameters")
        box.prop(scene.light_preset, "shape")
        box.prop(scene.light_preset, "size")
        box.prop(scene.light_preset, "height")
        box.prop(scene.light_preset, "spread")
        box.prop(scene.light_preset, "distance")
        box.prop(scene.light_preset, "power")
        layout.separator()
        row = layout.row(align=True)
        row.operator("light.add_light", icon='ADD')
        layout.template_list("LIGHT_UL_LightList", "", scene, "light_items", scene, "light_index")
        if scene.light_index >= 0:
            item = scene.light_items[scene.light_index]
            box = layout.box()
            col = box.column()
            col.prop(item, "size")
            col.prop(item, "height")
            col.prop(item, "spread")
            col.prop(item, "power")
            col.prop(item, "color")
            box.separator()
            box.prop(item, "track_target")
            if item.track_target:
                box.separator()
                box.label(text="Surround Parameters:")
                col = box.column()
                col.prop(item, "longitude", slider=True, text="Longitude")
                col.prop(item, "latitude", slider=True, text="Latitude")
                col.prop(item, "distance")
                col.prop(item, "track_offset", text="Constraint Offset")
                box.separator()
                box.prop(item, "normal_tracking", text="Normal Tracking")
                box.separator()
                box.operator("light.point_and_shoot", text="Point and Shoot", icon='HAND')

class LIGHT_OT_AddLight(bpy.types.Operator):
    bl_idname = "light.add_light"
    bl_label = "Add Light"
    def execute(self, context):
        preset = context.scene.light_preset
        candidate = None
        if context.active_object is not None:
            candidate = context.active_object
        bpy.ops.object.light_add(
            type='AREA',
            radius=preset.size,
            location=context.scene.cursor.location
        )
        new_light = context.active_object
        new_light.name = f"Light_{len(context.scene.light_items) + 1}"
        light_data = new_light.data
        light_data.shape = preset.shape
        light_data.size = preset.size
        light_data.size_y = preset.height
        light_data.spread = preset.spread
        light_data.energy = preset.power
        new_light.select_set(True)
        context.view_layer.objects.active = new_light
        item = context.scene.light_items.add()
        item.name = new_light.name
        item.light_obj = new_light
        item.size = preset.size
        item.height = preset.height
        item.spread = preset.spread
        item.power = preset.power
        item.distance = preset.distance
        if candidate is not None and candidate != new_light:
            item.track_target = candidate
        elif len(context.scene.light_items) > 1:
            for prev_item in reversed(context.scene.light_items[:-1]):
                if prev_item.track_target:
                    item.track_target = prev_item.track_target
                    break
        if item.track_target:
            item.setup_constraints()
        item.update_geo_position()
        item.update_light_data()
        context.scene.light_index = len(context.scene.light_items) - 1
        return {'FINISHED'}

class LIGHT_OT_RemoveLight(bpy.types.Operator):
    bl_idname = "light.remove_light"
    bl_label = "Delete Light"
    item_name: bpy.props.StringProperty()
    def execute(self, context):
        scene = context.scene
        for i, item in enumerate(scene.light_items):
            if item.name == self.item_name:
                if item.light_obj:
                    bpy.data.objects.remove(item.light_obj, do_unlink=True)
                if item.offset_obj:
                    bpy.data.objects.remove(item.offset_obj, do_unlink=True)
                scene.light_items.remove(i)
                break
        scene.light_index = min(scene.light_index, len(scene.light_items) - 1)
        return {'FINISHED'}

def frame_change_handler(scene):
    active_index = scene.light_index
    for i, item in enumerate(scene.light_items):
        if item.light_obj and item.track_target:
            item.update_geo_position()
            item.update_light_data()
            if i == active_index:
                item.light_obj.select_set(True)
                scene.view_layer.objects.active = item.light_obj
            else:
                item.light_obj.select_set(False)
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.tag_redraw()

def update_light_index(self, context):
    idx = self.light_index
    for i, item in enumerate(self.light_items):
        if item.light_obj:
            if i == idx:
                item.light_obj.select_set(True)
                context.view_layer.objects.active = item.light_obj
            else:
                item.light_obj.select_set(False)

bpy.types.Scene.light_index = bpy.props.IntProperty(default=-1, update=update_light_index)

classes = (
    LightPreset,
    LightItem,
    LIGHT_UL_LightList,
    LIGHT_PT_MainPanel,
    LIGHT_OT_AddLight,
    LIGHT_OT_RemoveLight,
    LIGHT_OT_PointAndShoot,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.light_preset = bpy.props.PointerProperty(type=LightPreset)
    bpy.types.Scene.light_items = bpy.props.CollectionProperty(type=LightItem)
    if frame_change_handler not in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.append(frame_change_handler)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.light_preset
    del bpy.types.Scene.light_items
    del bpy.types.Scene.light_index
    if frame_change_handler in bpy.app.handlers.frame_change_post:
        bpy.app.handlers.frame_change_post.remove(frame_change_handler)

if __name__ == "__main__":
    register()
