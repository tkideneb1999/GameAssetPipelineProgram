# Game Asset Pipeline Automation
## Main Application Installation
1. Install Python
2. Run the Install.bat file
3. **Run the Start.bat file at least once** before using add-ons

## Blender Addon Installation
Works for Blender 2.93 to 3.00, 3.1 and above not supported because Python was upgraded from 3.9 to 3.10
1. Navigate to the BlenderAddon folder of the downloaded files
2. Put the Files from the Blender Addon Folder in a folder called GAPA, then put this in a zip Archive with the same name
3. Install the add-on as you would with any other Blender add-on

## Substance Painter Addon Installation
Works for Substance Painter 2021
1. Make sure the `PROGRAM_NAME` variable in the `__init__.py` file matches the name of the Painter executable file
2. Open Substance Painter and click on Python/Plugins Folder
3. navigate to the plugins folder
4. create a folder called GAPA
5. copy all files in the SubstancePainterAddon Directory of the downloaded files to this location.

To remove any data the program generates, delete the GAPASettings folder in the Documents Directory.

## Functionality
Set the current project in the File Menu to provide Access for the add-ons to it
### Registering Programs
Start the Pipeline Tool at least once to initiate some settings.
After Add-on installation enabling the Add-on automatically registers it.
![grafik](https://user-images.githubusercontent.com/13368962/151027992-8ee00ab7-7987-40f2-aceb-d33df4258ca1.png)

### Pipeline Configurator
- Add at least one Pipeline before adding new assets
- Pipeline Steps can be added by pressing Tab and selecting a step
- Inputs and outputs can be wrangled like in any other nodegraph
- Images inputs/outputs are generally marked with a square, 3D meshes with a triangle, any other with a circle. This is only an indication and they can still be connected to each other
- Pipelines can be saved and published by right-clicking anywhere in the viewport and respectively selecting Save or Publish
- !! The Nodegraph is work in progress and still needs refinement
![grafik](https://user-images.githubusercontent.com/13368962/177412819-28b10f97-a977-4008-96c0-929aa6716731.png)

### Asset Browser
- Asset removal not implemented
- Run plugins by right-clicking on a step and choose `Run Plugin...`
- Open the folder containing the files of a step by right-clicking and selecting `Open In Explorer` (only works on windows)
![grafik](https://user-images.githubusercontent.com/13368962/151027548-150bb62f-f999-43ba-b800-a17cedfe4bfe.png)

### Import / Export
![grafik](https://user-images.githubusercontent.com/13368962/151029251-79f483c8-118a-4cb5-9c3f-fdeb3860534e.png)

## Known Issues
- Do not modify the pipeline after using it in any assets!
- Texture sets that have different outputs are not supported
- No Position Map Baker available

## Future Plans
- Asset Dependencies
- Substance Designer Add-On
- Meshroom Add-On or Plug-In
- Pipeline File/Asset Imports
