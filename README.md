# GreebleGenerator
A Blender add-on generates Greebles.

This is my Graduation Project. 


## Dependencies
- Stable Diffusion Web UI by Automatic1111 should be installed locally. (https://github.com/AUTOMATIC1111/stable-diffusion-webui)
- Blender(3.0 or higher; recommend 3.5)


## Installation
1. Download this repository as zip file and open Blender.
2. Navigate to Edit->Preferences->Add-ons->Install and select zip file you downloaded.
3. Make sure "Greeble Generator" is enabled and restart Blender.
4. Navigate to Stable Diffusion Web UI installed folder and edit webui-user.bat.
5. Add "--api" to "COMMANDLINE_ARGS"


## Run
1. Navigate to Stable Diffusion Web UI installed folder and run webui-user.bat.
2. Open Blender in administrator mode.
3. Select desired face in face mode and press "Take Snapshot" in N Panel(Press N to activate).
4. Press "Apply Greeble Texture".


## Credits and Licenses

- Stable Diffusion - https://github.com/CompVis/stable-diffusion, https://github.com/CompVis/taming-transformers
- Stable Diffusion Web UI by Automatic1111 - https://github.com/AUTOMATIC1111/stable-diffusion-webui
- Blender by Blender - https://github.com/blender/blender
- ControlNet for Stable Diffusion WebUI by Mikubill - https://github.com/Mikubill/sd-webui-controlnet
