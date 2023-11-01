import bpy
import subprocess
import sys
import os


def install_pillow():
    try:
        # Attempt to import Pillow
        import PIL
    except ImportError:
        # Pillow not installed, install it
        # Find Blender's Python executable
        python_exe = sys.executable
        # Ensure pip is installed and then install Pillow
        subprocess.call([python_exe, "-m", "ensurepip"])
        subprocess.call([python_exe, "-m", "pip", "install", "Pillow"])


# Call the install function before importing other modules
install_pillow()


# Now import other modules that might depend on Pillow
from .operators import SnapshotOperator, ApplyGreebleTextureOperator
from .ui import GreebleGeneratorPanel
from bpy.props import StringProperty

bl_info = {
    "name": "Greeble Generator",
    "author": "2014312728",
    "version": (1, 0),
    "blender": (3, 5, 0),
    "location": "View3D > N Panel > Greeble Tab",
    "description": "Generates greebles using Stable Diffusion",
    "category": "Object",
}

def register():
    bpy.utils.register_class(SnapshotOperator)
    bpy.utils.register_class(ApplyGreebleTextureOperator)
    bpy.utils.register_class(GreebleGeneratorPanel)
    bpy.types.Scene.greeble_generator_snapshot_path = StringProperty(
        name="Snapshot Path",
        description="Path to the snapshot image",
        default=""
    )
    bpy.types.Scene.greeble_generator_prompt = bpy.props.StringProperty(
        name="Greeble Prompt",
        description="Enter the prompt for the Greeble Generator",
        default="grb, mechanical parts, mechanical pistons and parts, hard surface, rigorous detail, precise detail, ultra realistic, highly detailed, sophisticated Generate a high-resolution, detailed texture-like image filled with intricate greebles and sci-fi details. The image should showcase a complex array of mechanical and futuristic elements, with a focus on metallic textures, interlocking geometric shapes, and a monochromatic color scheme with hints of neon blue. The overall mood is futuristic and high-tech, resembling the surface of a sci-fi spaceship or machinery, with a fine balance of shadows and light to enhance the 3D effect of the greebles."
    )

def unregister():
    bpy.utils.unregister_class(SnapshotOperator)
    bpy.utils.unregister_class(ApplyGreebleTextureOperator)
    bpy.utils.unregister_class(GreebleGeneratorPanel)
    del bpy.types.Scene.greeble_generator_snapshot_path
    del bpy.types.Scene.greeble_generator_prompt

if __name__ == "__main__":
    register()
