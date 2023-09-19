import bpy
import random
from mathutils import Vector

def create_greeble_on_face(face, obj):
    
    # Calculate the center of the face
    verts = [obj.data.vertices[i] for i in face.vertices]
    center = sum((obj.matrix_world @ v.co for v in verts), Vector()) / len(verts)
    
    # Calculate the size of the greeble based on the face size
    size = face.area * random.uniform(0.1, 0.5)
    
    # Create a cube greeble
    bpy.ops.mesh.primitive_cube_add(size=size, enter_editmode=False, align='WORLD', location=center)
    greeble = bpy.context.active_object

    # Join the greeble with the main object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    greeble.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.join()


def generate_greebles(obj_name):
    # Ensure the object is a mesh
    obj = bpy.data.objects[obj_name]
    if obj.type != 'MESH':
        print("Selected object is not a mesh!")
        return
    
    # Enter edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Deselect all faces
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Enter object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Iterate over faces and decide whether to add a greeble
    for face in obj.data.polygons:
        if random.random() < 0.2:  # 20% chance to add a greeble on a face
            create_greeble_on_face(face, obj)

# Use the function on the currently active object
generate_greebles(bpy.context.active_object.name)
