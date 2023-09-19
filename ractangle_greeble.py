import bpy
import bmesh
import random

def divide_face_with_random_rectangles(obj, face_index, num_rectangles):
    """
    Divide a face of a given object with random rectangles.
    
    Parameters:
    - obj: The mesh object.
    - face_index: The index of the face to be divided.
    - num_rectangles: Number of random rectangles to add.
    """
    # Ensure the object is in edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    
    # Create a bmesh from the object
    bm = bmesh.from_edit_mesh(obj.data)
    
    # Ensure the lookup table is updated
    bm.faces.ensure_lookup_table()
    
    # Get the face
    face = bm.faces[face_index]
    
    # Get the bounding box of the face
    min_x = min([v.co.x for v in face.verts])
    max_x = max([v.co.x for v in face.verts])
    min_y = min([v.co.y for v in face.verts])
    max_y = max([v.co.y for v in face.verts])
    z = face.verts[0].co.z  # Assuming the face is flat
    
    for _ in range(num_rectangles):
        # Randomly determine the coordinates for the rectangle
        x1 = random.uniform(min_x, max_x)
        x2 = random.uniform(x1, max_x)
        y1 = random.uniform(min_y, max_y)
        y2 = random.uniform(y1, max_y)
        
        # Create vertices for the rectangle
        v1 = bm.verts.new((x1, y1, z))
        v2 = bm.verts.new((x2, y1, z))
        v3 = bm.verts.new((x2, y2, z))
        v4 = bm.verts.new((x1, y2, z))
        
        # Ensure the lookup table is updated after adding new vertices
        bm.verts.ensure_lookup_table()
        
        # Create the rectangle face
        bm.faces.new([v1, v2, v3, v4])
        
    # Update the mesh
    bmesh.update_edit_mesh(obj.data)

# Example usage:
obj = bpy.context.active_object
divide_face_with_random_rectangles(obj, face_index=0, num_rectangles=5)
