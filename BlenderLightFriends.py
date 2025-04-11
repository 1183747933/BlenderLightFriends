bl_info = {
    "name": "BlenderLightFriends",
    "author": "Your Name",
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

# ------------------------- 属性组定义 -------------------------
class LightPreset(bpy.types.PropertyGroup):
    shape: bpy.props.EnumProperty(
        name="形状",
        items=[('RECTANGLE', '长方形', ''), ('ELLIPSE', '椭圆', '')],
        default='RECTANGLE'
    )
    size: bpy.props.FloatProperty(
        name="宽度",
        default=2.0,
        min=0.1,
        max=50.0
    )
    height: bpy.props.FloatProperty(
        name="高度",
        default=1.0,
        min=0.1,
        max=50.0
    )
    spread: bpy.props.FloatProperty(
        name="扩散度",
        default=0.2,
        min=0.0,
        max=1.0,
        subtype='FACTOR'
    )
    distance: bpy.props.FloatProperty(
        name="默认距离",
        default=10.0,
        min=0.1,
        max=100.0
    )
    power: bpy.props.FloatProperty(
        name="功率",
        default=500.0,
        min=0.0,
        soft_max=2000.0
    )

class LightItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="名称")
    light_obj: bpy.props.PointerProperty(type=bpy.types.Object)

    longitude: bpy.props.FloatProperty(
        name="经度",
        default=0.0,
        min=-180.0,
        max=180.0,
        update=lambda self, context: self.update_geo_position()
    )
    latitude: bpy.props.FloatProperty(
        name="纬度",
        default=45.0,
        min=-89.9,
        max=89.9,
        update=lambda self, context: self.update_geo_position()
    )
    distance: bpy.props.FloatProperty(
        name="距离",
        default=10.0,
        min=0.1,
        max=100.0,
        update=lambda self, context: self.update_geo_position()
    )
    # “约束偏移”：调整空对象在跟踪目标内的局部坐标，修改时仅更新空对象位置，不改变角度与距离
    track_offset: bpy.props.FloatVectorProperty(
        name="约束偏移",
        subtype='TRANSLATION',
        default=(0.0, 0.0, 0.0),
        update=lambda self, context: self.update_geo_position()
    )
    # 灯光物理属性
    size: bpy.props.FloatProperty(
        name="宽度",
        default=2.0,
        min=0.1,
        max=50.0,
        update=lambda self, context: self.update_light_data()
    )
    height: bpy.props.FloatProperty(
        name="高度",
        default=1.0,
        min=0.1,
        max=50.0,
        update=lambda self, context: self.update_light_data()
    )
    spread: bpy.props.FloatProperty(
        name="扩散度",
        default=0.2,
        min=0.0,
        max=1.0,
        subtype='FACTOR',
        update=lambda self, context: self.update_light_data()
    )
    power: bpy.props.FloatProperty(
        name="功率",
        default=500.0,
        min=0.0,
        soft_max=2000.0,
        update=lambda self, context: self.update_light_data()
    )
    color: bpy.props.FloatVectorProperty(
        name="颜色",
        subtype='COLOR',
        default=(1.0, 1.0, 1.0),
        min=0.0,
        max=1.0,
        update=lambda self, context: self.update_light_data()
    )
    # 新增：法线跟踪选项
    normal_tracking: bpy.props.BoolProperty(
        name="法线跟踪",
        default=False
    )
    # 跟踪设置，必须指定一个跟踪目标
    track_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="跟踪目标",
        update=lambda self, context: self.setup_constraints()
    )
    # 内部使用的空对象，用作跟踪约束目标
    offset_obj: bpy.props.PointerProperty(
        name="约束空对象",
        type=bpy.types.Object
    )

    def update_geo_position(self):
        """更新灯光位置与旋转。"""
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
        """更新灯光的物理属性。"""
        if self.light_obj and self.light_obj.data:
            light = self.light_obj.data
            light.size = self.size
            light.size_y = self.height
            light.spread = self.spread
            light.energy = self.power
            light.color = self.color

    def setup_constraints(self):
        """设置灯光追踪约束，将空对象作为追踪目标。"""
        if not self.light_obj or not self.track_target:
            return
        if not self.offset_obj:
            empty_name = f"空_{self.light_obj.name}"
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

# ------------------------- Modal 指哪打哪 操作符 -------------------------
class LIGHT_OT_PointAndShoot(bpy.types.Operator):
    bl_idname = "light.point_and_shoot"
    bl_label = "指哪打哪"
    bl_options = {'REGISTER', 'UNDO'}

    _light_item = None
    is_tracking = False

    def modal(self, context, event):
        # 退出条件：右键或 ESC 取消
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.report({'INFO'}, "指哪打哪取消")
            return {'CANCELLED'}
        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                self.is_tracking = True
            elif event.value == 'RELEASE':
                self.report({'INFO'}, "指哪打哪结束")
                return {'FINISHED'}
        # 只有在左键按下后才进行更新
        if self.is_tracking and event.type == 'MOUSEMOVE':
            region = context.region
            rv3d = context.space_data.region_3d
            coord = (event.mouse_region_x, event.mouse_region_y)
            view_vector = bpy_extras.view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
            ray_origin = bpy_extras.view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
            result, location, normal, index, obj, matrix = context.scene.ray_cast(context.view_layer.depsgraph, ray_origin, view_vector)
            if result:
                # 指哪打哪：计算新 track_offset 使空对象移至击中点
                new_track_offset = location - self._light_item.track_target.location
                self._light_item.track_offset = new_track_offset
                # 如果勾选了法线跟踪，则根据 hit normal 更新经纬度
                if self._light_item.normal_tracking:
                    n = normal.normalized()
                    theta = math.acos(n.z)  # 与 Z 轴夹角
                    new_latitude = 90 - math.degrees(theta)
                    new_longitude = math.degrees(math.atan2(n.y, n.x))
                    self._light_item.latitude = new_latitude
                    self._light_item.longitude = new_longitude
                # 调用更新，注意：距离保持不变
                self._light_item.update_geo_position()
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        idx = context.scene.light_index
        if idx < 0:
            self.report({'ERROR'}, "未选中面光对象")
            return {'CANCELLED'}
        self._light_item = context.scene.light_items[idx]
        self.is_tracking = False
        context.window_manager.modal_handler_add(self)
        self.report({'INFO'}, "请按下左键后拖动鼠标选择目标位置，然后松开结束")
        return {'RUNNING_MODAL'}

# ------------------------- UI 列表 -------------------------
class LIGHT_UL_LightList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        # 在默认布局下仅显示名称和右侧的删除按钮
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row(align=True)
            row.label(text=item.name, icon='LIGHT')
            row.operator("light.remove_light", text="", icon="TRASH").item_name = item.name
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon='LIGHT')

# ------------------------- 主面板 -------------------------
class LIGHT_PT_MainPanel(bpy.types.Panel):
    bl_label = "BlenderLightFriends"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = '[ 光 ]'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # 全局预设
        box = layout.box()
        box.label(text="预设参数")
        box.prop(scene.light_preset, "shape")
        box.prop(scene.light_preset, "size")
        box.prop(scene.light_preset, "height")
        box.prop(scene.light_preset, "spread")
        box.prop(scene.light_preset, "distance")
        box.prop(scene.light_preset, "power")

        # 灯光列表管理：新建按钮使用 “+” 图标
        layout.separator()
        row = layout.row(align=True)
        row.operator("light.add_light", icon='ADD')
        layout.template_list("LIGHT_UL_LightList", "", scene, "light_items", scene, "light_index")

        # 单个灯光详细设置
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
                box.label(text="环绕参数:")
                col = box.column()
                col.prop(item, "longitude", slider=True, text="经度")
                col.prop(item, "latitude", slider=True, text="纬度")
                col.prop(item, "distance")
                col.prop(item, "track_offset", text="约束偏移")
                box.separator()
                # 新增“法线跟踪”复选框
                box.prop(item, "normal_tracking", text="法线跟踪")
                box.separator()
                # 新增“指哪打哪”按钮，图标使用 HAND（手形）
                box.operator("light.point_and_shoot", text="指哪打哪", icon='HAND')

# ------------------------- 新建/删除操作符 -------------------------
class LIGHT_OT_AddLight(bpy.types.Operator):
    bl_idname = "light.add_light"
    bl_label = "新建面光"

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
        new_light.name = f"面光_{len(context.scene.light_items) + 1}"
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
    bl_label = "删除面光"
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

# ------------------------- 帧变化处理器 -------------------------
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

# ------------------------- 更新 active index 回调 -------------------------
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

# ------------------------- 注册/注销 -------------------------
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
