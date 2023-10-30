import bpy

class GreebleGeneratorPanel(bpy.types.Panel):
    bl_label = "Greeble Generator"
    bl_idname = "OBJECT_PT_greeble_generator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Greeble'

    def draw(self, context):
        layout = self.layout

        # Button for Snapshot Operator
        layout.operator("object.snapshot_operator", text="Take Snapshot")

        # Button for Apply Greeble Texture Operator
        layout.operator("object.apply_greeble_texture", text="Apply Greeble Texture")

def register():
    bpy.utils.register_class(GreebleGeneratorPanel)

def unregister():
    bpy.utils.unregister_class(GreebleGeneratorPanel)

if __name__ == "__main__":
    register()
