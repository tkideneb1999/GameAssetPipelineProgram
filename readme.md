# Game Asset Pipeline Automation
## Main Application Installation
1. Install Python
2. Run the Install.bat file
3. **Run the Start.bat file at least once** before using add-ons

## Blender Addon Installation
1. Navigate to the BlenderAddon folder of the downloaded files
2. Open the `__init__.py` file
3. Change the `pyQt_path` variable to point to the site packages folder of the Main Application
4. Create a zip archive from the files in the BlenderAddon folder called GAPA
5. Install the add-on as you would with any other Blender add-on

## Substance Painter Addon Installation
1. Make sure the `PROGRAM_NAME` variable in the `__init__.py` file matches the name of the Painter executable file
2. Open Substance Painter and click on Python/Plugins Folder
3. navigate to the plugins folder
4. create a folder called GAPA
5. copy all files in the SubstancePainterAddon Directory of the downloaded files to this location.

To remove any data the program generates, delete the GAPASettings folder in the Documents Directory.

## Functionality
Set the current project in the File Menu to provide Access for the add-ons to it
### Registering Programs
1. Add the exe of the program
2. Start the program after registration at least once, to activate the add-on correctly
![grafik](https://user-images.githubusercontent.com/13368962/151027992-8ee00ab7-7987-40f2-aceb-d33df4258ca1.png)

### Pipeline Configurator
- Add at least one Pipeline before adding new assets
- Pipeline Steps can be added via the `Add Step` Button, removed via right-click and `Delete`
- If Configs are used, do not add or delete any inputs and outputs
![grafik](https://user-images.githubusercontent.com/13368962/151027781-143d3791-c304-4c39-84a9-08e7f82d6e65.png)

### Asset Browser
- Asset removal not implemented
- Run plugins by right-clicking on a step and choose `Run Plugin...`
- Open the folder containing the files of a step by right-clicking and selecting `Open In Explorer` (only works on windows)
![grafik](https://user-images.githubusercontent.com/13368962/151027548-150bb62f-f999-43ba-b800-a17cedfe4bfe.png)

### Import / Export
![grafik](https://user-images.githubusercontent.com/13368962/151029251-79f483c8-118a-4cb5-9c3f-fdeb3860534e.png)

## Known Issues
- Step selection highlight in Pipeline Overview not working
- Do not modify the pipeline after using it in any assets!
- Texture sets that have different outputs are not supported
- No Position Map Baker available
