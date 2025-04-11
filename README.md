# BlenderLightFriends

**BlenderLightFriends** is a lighting plugin designed for efficient surface lighting setup, inspired by KeyShot's lighting workflow. It focuses on animation rendering and flexibility. Key features include:  
- **Object Tracking**  
  Each light can be set to track a target object. The "Constraint Offset" allows adjusting the target position offset.  
- **Create Lights**  
  Preset parameters can be customized when creating new lights. Selecting a target object before clicking "Create" will automatically bind the light to track the target.  
- **"Point-and-Shoot" Mode** 🎯  
  A modal operator enables intuitive "point-and-shoot" functionality. When activated:  
  - Hold the left mouse button and drag to cast a raycast that updates the light's constraint offset to the clicked surface position.  
  - If "Normal Tracking" is enabled, the light's latitude/longitude (distance remains fixed) will align with the surface normal of the hit point.  

---

## Installation

1. Package the project into a ZIP file or directly download the plugin Python file (`BlenderLightFriends.py`).  
2. Open Blender, go to **Edit > Preferences > Add-ons**, click **Install** and select the ZIP or Python file.  
3. Enable the plugin in the add-ons list. The plugin panel will appear under the **[ 光 ]** tab in the 3D Viewport sidebar.  

---

## Usage Guide

1. **Set Preset Parameters**  
   Adjust global settings at the top of the panel: light shape, size, height, spread, default distance, and power.  

2. **Create a Surface Light**  
   Select the target object you want to track, then click the **+** button to create a new light.  

3. **Edit Light Properties**  
   Modify physical attributes (size, power, color) and orbital parameters (latitude/longitude, distance, constraint offset) in the detailed settings area.  

4. **"Point-and-Shoot" Mode**  
   - Click the **"Point-and-Shoot"** button in the detailed settings to enter modal mode.  
   - Press and drag the left mouse button to cast a raycast. The plugin updates the constraint offset to the clicked surface position.  
   - If "Normal Tracking" is enabled, the light's latitude/longitude will align with the surface normal (distance remains fixed).  
   - Release the mouse button to exit the mode.  

5. **Delete a Light**  
   Click the trash bin icon next to each light entry in the UI list to remove the light and its associated empty object.  

---

## Future Updates

- Optimize UI/UX.  
- Save preset parameters.  
- Add more light types: Point Lights, Emission Materials.  
- Gradient lighting support.  

---

## Compatibility

- The plugin requires no external dependencies.  
- Tested and verified on **Blender 3.6 and above**.  
- For issues, contact the author or leave a message via GitHub Issues.  

---

## Give it a ⭐ if you like this project!

---

<details>
  <summary>🇨 查看中文版说明 (Click to view Chinese version) 🎉</summary>

## 简介

**BlenderLightFriends** 是一个打光插件，具有高效的面光添加功能，参考了keyshot的打光模式，更侧重动画渲染与灵活性。  
主要功能包括：  
- **对象跟踪** 
  每个灯光可以选择跟踪目标，可通过调整“约束偏移”实现灯光目标点的偏移。
- **新建灯光**   
  新建灯光可以调整预设生成，选择目标后再点新建将会自动绑定跟踪对象。
- **“指哪打哪”模式** ️  
  通过一个模态操作符，实现“指哪打哪”功能。进入该模式后，按住鼠标左键拖动，插件将利用射线投射获取光标所在的目标表面位置，并更新灯光的约束偏移；
  若勾选“法线跟踪”，则根据击中的表面法线自动更新灯光的经纬度（距离保持不变）。

## 安装

1. 将整个项目打包成 ZIP 文件，或者直接下载插件python文件（ `BlenderLightFriends.py`）。
2. 打开 Blender，进入 **编辑 > 首选项 > 插件**，点击 **安装** 按钮并选择下载的 ZIP 或 Python 文件。
3. 安装后在插件列表中启用本插件。启用后插件面板会显示在 3D 视图侧边栏的 **[ 光 ]** 标签中。

## 使用说明

1. **设置预设参数**   
   在面板顶部调整全局预设参数：面光形状、尺寸、高度、扩散度、默认距离和功率。

2. **新建面光**   
   选中需要进行灯光跟踪的对象，点击 **+** 按钮新建一个面光对象。。

3. **编辑灯光参数**   
   在详细设置区域修改面光的物理属性（尺寸、功率、颜色等）以及环绕参数（经纬度、距离、约束偏移）。

4. **指哪打哪模式**   
   - 在详细设置区域点击 **“指哪打哪”** 按钮进入模态操作模式。
   - 按下鼠标左键后拖动，插件使用射线检测光标位置并更新约束偏移，使空对象移动到目标位置；若启用了“法线跟踪”，则根据击中表面的法线更新经纬度（距离保持不变）。
   - 松开鼠标左键结束操作。

5. **删除面光**   
   在 UI 列表中，每个面光项右侧都有删除按钮（垃圾桶图标），点击即可删除对应的面光及其相关空对象。

## 未来更新方向

- 优化界面UI。
- 预设参数保存。
- 更多灯光类型：点光源，自发光材质。
- 渐变灯光。

## 有关兼容性

- 直接导入插件即可，无需额外安装第三方库。  
- 已在 Blender 3.6 及以上版本中测试通过。
- 如有问题，请联系作者或者在 GitHub Issues 中留言反馈。

## 喜欢本项目请给我点个⭐️吧~
---

Feel free to contribute, report issues, or suggest improvements!
</details>
