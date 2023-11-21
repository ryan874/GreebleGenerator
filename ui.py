import bpy

class GreebleGeneratorPanel(bpy.types.Panel):
    bl_label = "Greeble Generator"
    bl_idname = "OBJECT_PT_greeble_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Greeble'

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Button for Snapshot Operator
        layout.operator("object.snapshot_operator", text="Take Snapshot")

        # Textbox for the prompt
        row = layout.row()
        row.prop(scene, "greeble_generator_prompt")

        # Slider for CFG scale
        layout.prop(scene, "greeble_cfg_scale", slider=True)

        # Slider for denoising strength
        layout.prop(scene, "greeble_denoising_strength", slider=True)

        # Button for Apply Greeble Texture Operator
        layout.operator("object.apply_greeble_texture", text="Apply Greeble Texture")

        # Button for Apply Depth Map Operator
        layout.operator("object.apply_depth_map", text="Apply Depth Map")

        # Slider for texture scale
        layout.prop(scene, "greeble_texture_scale")
        layout.operator("object.scale_uv_operator", text="Scale UV")

        # Button for Save Textures Operator
        layout.operator("object.save_textures_operator", text="Save Textures")

