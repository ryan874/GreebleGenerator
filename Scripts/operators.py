import bpy
import bmesh
import mathutils
import os
from .apihandler import send_prompt_to_stable_diffusion

class SnapshotOperator(bpy.types.Operator):
    bl_idname = "object.snapshot_operator"
    bl_label = "Snapshot Selected Face"

    def execute(self, context):
        obj = context.active_object

        # Store current mode and switch to edit mode to access face data
        current_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        # Store indices of initially selected faces
        initially_selected_faces_indices = [f.index for f in bm.faces if f.select]

        if not initially_selected_faces_indices:
            self.report({'ERROR'}, "No faces selected!")
            return {'CANCELLED'}

        face = bm.faces[initially_selected_faces_indices[0]]
        normal = face.normal.copy()
        center = face.calc_center_median().copy()

        # Calculate the maximum edge length for orthographic scale
        max_edge_length = max([edge.calc_length() for edge in face.edges])

        # Switch back to object mode before adding the camera
        bpy.ops.object.mode_set(mode='OBJECT')

        # Create a new camera
        bpy.ops.object.camera_add()
        camera = context.object
        camera.data.type = 'ORTHO'

        # Align camera to face
        camera.location = center
        camera.rotation_euler = normal.rotation_difference(mathutils.Vector((0, 0, 1))).to_euler()

        # Set orthographic scale
        camera.data.ortho_scale = max_edge_length

        # Set the camera as active and render the scene
        bpy.context.scene.camera = camera
        bpy.ops.render.render(write_still=True)

        # Save the image
        snapshot_dir = "C:\\tmp"
        os.makedirs(snapshot_dir, exist_ok=True)
        snapshot_path = os.path.join(snapshot_dir, "snapshot.png")
        bpy.data.images['Render Result'].save_render(filepath=snapshot_path)

        # Store the path for later use
        context.scene.greeble_generator_snapshot_path = snapshot_path

        # Clean up: delete the camera
        bpy.data.objects.remove(camera)

        # Reactivate the original object and restore initial selection
        context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)  # Re-acquire BMesh data
        bm.faces.ensure_lookup_table()  # Update the internal index table
        for face_index in initially_selected_faces_indices:
            bm.faces[face_index].select = True
        bpy.ops.object.mode_set(mode=current_mode)

        return {'FINISHED'}


class ApplyGreebleTextureOperator(bpy.types.Operator):
    bl_idname = "object.apply_greeble_texture"
    bl_label = "Apply Greeble Texture"

    def execute(self, context):
        snapshot_path = context.scene.greeble_generator_snapshot_path

        # Send the snapshot to Stable Diffusion
        prompt = "Add greebles to this image"
        send_prompt_to_stable_diffusion(prompt, steps=5)

        # Logic to apply the returned image as a texture
        # ...

        return {'FINISHED'}
