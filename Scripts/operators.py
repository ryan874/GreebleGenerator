import bpy
import bmesh
import mathutils
import os
from datetime import datetime
from mathutils import Vector
from .apihandler import send_prompt_to_stable_diffusion
from .apihandler import get_depth_map

addon_dir = os.path.dirname(__file__)

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

        # Align camera to face and set distance
        camera.rotation_euler = normal.rotation_difference(mathutils.Vector((0, 0, -1))).to_euler()
        camera_offset = max_edge_length  # Distance from the face
        camera.location = center + normal * camera_offset

        # Set orthographic scale
        camera.data.ortho_scale = max_edge_length

        # Set camera resolution to 1:1 aspect ratio
        render = bpy.context.scene.render
        render.resolution_x = 512
        render.resolution_y = 512

        # Add a light source at the camera's position
        bpy.ops.object.light_add(type='POINT', location=camera.location)
        light = context.object

        # Set the camera as active and render the scene
        bpy.context.scene.camera = camera
        bpy.ops.render.render(write_still=True)

        # Save the image
        snapshot_path = os.path.join(addon_dir, "snapshot.png")
        bpy.data.images['Render Result'].save_render(filepath=snapshot_path)

        # Store the path for later use
        context.scene.greeble_generator_snapshot_path = snapshot_path

        # Clean up: delete the camera and light
        bpy.data.objects.remove(camera)
        bpy.data.objects.remove(light)

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
        prompt = context.scene.greeble_generator_prompt
        send_prompt_to_stable_diffusion(prompt, steps=10)

        # Load the texture image
        addon_dir = os.path.dirname(__file__)
        image_path = os.path.join(addon_dir, "output.png")
        image = bpy.data.images.load(image_path)

        # Create a new material
        mat = bpy.data.materials.new(name="GreebleTextureMaterial")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes["Principled BSDF"]
        tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image.image = image
        mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])

        # Apply material to selected faces
        self.apply_material_to_selected_faces(context, mat)

        return {'FINISHED'}

    @staticmethod
    def apply_material_to_selected_faces(context, mat):
        obj = context.active_object
        if mat.name not in obj.data.materials:
            obj.data.materials.append(mat)

        # Ensure the object has UV mapping
        if not obj.data.uv_layers:
            obj.data.uv_layers.new()

        # Get the index of the material
        mat_index = obj.data.materials.find(mat.name)

        # Get selected faces
        bpy.ops.object.mode_set(mode='EDIT')
        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()
        selected_faces = [f for f in bm.faces if f.select]

        # Assign the material to the selected faces
        for face in selected_faces:
            face.material_index = mat_index

        # Update the mesh and return to Object Mode
        bmesh.update_edit_mesh(obj.data)
        bpy.ops.object.mode_set(mode='OBJECT')



class ApplyDepthMapOperator(bpy.types.Operator):
    bl_idname = "object.apply_depth_map"
    bl_label = "Apply Depth Map"

    def execute(self, context):

	# Send Output image to Stable Diffusion
        get_depth_map("", steps=10)

        # Load the depth map image
        addon_dir = os.path.dirname(__file__)
        depth_image_path = os.path.join(addon_dir, "depth.png")
        depth_image = bpy.data.images.load(depth_image_path)

        # Get the material
        mat = bpy.data.materials.get("GreebleTextureMaterial")
        if not mat:
            self.report({'ERROR'}, "GreebleTextureMaterial not found!")
            return {'CANCELLED'}

        # Add a displacement node and connect the depth map
        self.apply_depth_map_to_material(mat, depth_image)

        # Check if depth map exists
        if not os.path.exists(depth_image_path):
            self.report({'WARNING'}, "Depth map image not found. Skipping depth map application.")
            return {'FINISHED'}

        return {'FINISHED'}


    @staticmethod
    def apply_depth_map_to_material(mat, depth_image):
        mat.use_nodes = True
        displacement_node = mat.node_tree.nodes.new('ShaderNodeDisplacement')
        tex_image_depth = mat.node_tree.nodes.new('ShaderNodeTexImage')
        tex_image_depth.image = depth_image

        # Connect the depth map to the Displacement input of the Material Output node
        material_output = mat.node_tree.nodes.get('Material Output')
        mat.node_tree.links.new(displacement_node.inputs['Height'], tex_image_depth.outputs['Color'])
        mat.node_tree.links.new(material_output.inputs['Displacement'], displacement_node.outputs['Displacement'])


class ScaleUVOperator(bpy.types.Operator):
    bl_idname = "object.scale_uv_operator"
    bl_label = "Scale UV of Selected Faces"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'MESH' and context.mode == 'EDIT_MESH'

    def execute(self, context):
        scale_factor = context.scene.greeble_texture_scale
        self.scale_uv(context, scale_factor)
        return {'FINISHED'}

    def scale_uv(self, context, scale_factor):
        obj = context.active_object

        if not obj or not obj.data.uv_layers:
            self.report({'ERROR'}, "No active object with UV map found.")
            return

        bm = bmesh.from_edit_mesh(obj.data)
        uv_layer = bm.loops.layers.uv.active

        for face in bm.faces:
            if face.select:
                for loop in face.loops:
                    loop_uv = loop[uv_layer]
                    # Scale around the center (0.5, 0.5)
                    loop_uv.uv = ((loop_uv.uv - Vector((0.5, 0.5))) * scale_factor) + Vector((0.5, 0.5))

        bmesh.update_edit_mesh(obj.data)


class SaveTexturesOperator(bpy.types.Operator):
    bl_idname = "object.save_textures_operator"
    bl_label = "Save Textures with Unique Names"

    def execute(self, context):
        # Save the textures and get the new file paths
        addon_dir = os.path.dirname(__file__)
        image_path = os.path.join(addon_dir, "output.png")
        depth_image_path = os.path.join(addon_dir, "depth.png")
        new_output_path = self.save_texture_with_unique_name(image_path, "output")
        new_depth_path = self.save_texture_with_unique_name(depth_image_path, "depth")

        # Update the material with new image paths
        self.update_material_image_paths(context, new_output_path, new_depth_path)

        bpy.context.view_layer.update()

        return {'FINISHED'}

    def save_texture_with_unique_name(self, filepath, base_name):
        # Generate a unique timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create a new file name with the base name and timestamp
        new_filename = f"{base_name}_{timestamp}.png"
        new_filepath = os.path.join(addon_dir, new_filename)

        # Save the file with the new name
        bpy.data.images.load(filepath).save_render(new_filepath)

        return new_filepath

    def update_material_image_paths(self, context, new_output_path, new_depth_path):
        # Update the material to use the new image paths
        mat = bpy.data.materials.get("GreebleTextureMaterial")
        if mat:
            nodes = mat.node_tree.nodes
            for node in nodes:
                if node.type == 'TEX_IMAGE':
                    if "output.png" in node.image.filepath:
                        node.image.filepath = new_output_path
                    elif "depth.png" in node.image.filepath:
                        node.image.filepath = new_depth_path
