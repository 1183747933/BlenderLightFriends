<p align="right">
    <b>Language:</b> <a href="README.md">中文</a> | <a href="README_EN.md">English</a>
</p>

# BlenderLightFriends Quick Guide

## Introduction

**BlenderLightFriends** is a lighting management add-on for Blender. It allows you to quickly add, manage, control, and animate lights in your 3D scene. It supports studio-style lighting layouts, lets you place lights around a target using longitude, latitude, and distance, supports keyframe animation, and features a "Point and Shoot" tool.

---

## Installation & Activation

1. Save the script as `blender_light_friends.py`.
2. In Blender, go to **Edit > Preferences > Add-ons**, click **Install**, select this file and enable the add-on.
3. In the 3D View's **right sidebar (press N)**, you'll find a new tab **[ 光 ]** where the add-on panel is located.

---

## Feature Overview

### 1. Preset Parameters

- **Shape**: Choose between Rectangle or Ellipse for the light.
- **Width/Height**: Set the size of the light panel.
- **Spread**: Control the spread angle of the light.
- **Default Distance**: Default distance of the new light from the target.
- **Power**: The intensity/brightness of the light.

**Each parameter can be keyframed for animation using the button to the right.**

---

### 2. Light List & Management

- Click the **Add Light** button to add a new Area Light using the preset parameters above.
- The add-on will automatically place the new light around the selected object (or inherit the previous light's target if none is selected).
- Each light is listed and can be deleted with a single click (trash icon).

---

### 3. Light Details

- Select a light from the list to access its detailed adjustable parameters:
  - **Width/Height/Spread/Power/Color**: All can be adjusted and keyframed.
  - **Tracking Target**: Choose the object the light orbits.
- When a tracking target is set, **Orbit Parameters** will appear:
  - **Longitude/Latitude**: Control the light's orbit position around the target (spherical coordinates).
  - **Distance**: Distance from the light to the target.
  - **Constraint Offset**: Fine-tune the light's offset from the target.
  - **Normal Tracking**: If enabled, the light will adjust its orientation to match the surface normal.

---

### 4. Point and Shoot

- Click the **Point and Shoot** button, hold and drag with the left mouse button in the 3D View to aim at the desired spot. Release to move and aim the light at that point.
- **ESC or right mouse button** cancels the operation.

---

### 5. Animation Support

- All parameters can be keyframed using the keyframe button for easy light animation.

---

## Additional Notes

- The add-on auto-syncs lights and targets, updating light positions and parameters on frame changes.
- When deleting a light, related helper empties are also removed to keep the scene clean.
- Supports managing multiple lights for complex lighting setups.

---

## FAQ

**Q1: How do I specify the target for a new light?**  
A: Select an object (e.g., your character or prop) and click "Add Light". The light will automatically orbit the selected object.

**Q2: How can I animate a light orbiting its target?**  
A: Adjust the longitude, latitude, and distance parameters and insert keyframes to create orbiting animation.

**Q3: Point and Shoot not working?**  
A: Make sure you have selected a light and set its tracking target before using Point and Shoot.

---

## Quick Workflow Example

1. Select the object you want the light to orbit.
2. Set up the preset parameters and click "Add Light".
3. Select the light in the list, tweak the parameters, or use Point and Shoot for quick positioning.
4. For animation, click the keyframe button next to the parameter.
5. For multiple lights, repeat the above steps for efficient complex lighting.

---
