from ursina import *
from ursina.prefabs.dropdown_menu import DropdownMenu, DropdownMenuButton
import pandas as pd

import parse_files

#Load the atomic data from the csv file PubChemElements_all.csv
atomicData = pd.read_csv("dataFiles/PubChemElements_all.csv")
# print(atomicData.loc[atomicData["Symbol"] == "H"]["AtomicRadius"])

# create a window
app = Ursina(title="3Dvis", borderless=False, editor_ui_enabled=False, development_mode=False, fullscreen=False)

# Set initial variables
# initialCameraPosition = camera.position
initialCameraPosition = (0, 0, -20)

#Read data from file
atoms, uniqueSpecies = parse_files.parse_XYZ("testFiles/pyridine.xyz")
selectionColours = [color.random_color() for _ in range(len(uniqueSpecies))]
print(selectionColours)

# UI text and buttons
rotText = Text(text='Rotation: OFF', position=window.bottom_right, origin=(+0.5, -0.5))
selectionTxt = Text(text='No atom selected', position=window.bottom_left, origin=(-0.5, -0.5))

DropdownMenu('Settings', buttons=(
    DropdownMenu('Atomic size', buttons=(
        DropdownMenuButton('From file', on_click=lambda: print('From file')),
        DropdownMenuButton('From table', on_click=lambda: print('From table')),
    )),
))

# Class entities
class Atom(Entity):
    atomSelected = False
    atomPosition = (0,0,0)

    def __init__(self, position=(0,0,0), scale=(1,1,1), color=color.orange, **kwargs):
        super().__init__()
        self.model = 'sphere'
        self.color = color
        self.scale = (1, 1, 1)
        self.collider = 'sphere'
        self.world_position = position
        self.scale = scale

    def update(self):
        if self.hovered:
            self.color = color.tint(self.color, .1)
            selectionTxt.text = f"{self.name}: {self.atomPosition}"
        else:
            self.color = selectionColours[uniqueSpecies.index(self.name)]

# create app contents
spheres = []
for atom in atoms:
    scale = atomicData.loc[atomicData["Symbol"] == atom['element']]["AtomicRadius"] / 100.0
    sphere = Atom(position=(atom['x'], atom['y'], atom['z']), color=selectionColours[uniqueSpecies.index(atom['element'])], scale=(scale, scale, scale))
    sphere.name = atom['element']
    sphere.atomPosition = (atom['x'], atom['y'], atom['z'])

    spheres.append(sphere)

# b = Button(text='hello world!', color=color.azure, scale=.25, highlight_scale=1.1)
# b.tooltip = Tooltip('test')

rotToggled = False
def input(key):
    if key == 'escape': # close the app when pressing escape
        application.quit()
    
    if key == "r":
        global rotToggled
        rotToggled = not rotToggled
        if rotToggled:
            rotText.text = 'Rotation: ON'
        else:
            rotText.text = 'Rotation: OFF'

# update function
def update():
    if held_keys['c']: # reset camera
        camera.position = initialCameraPosition
        camera.rotation = (0, 0, 0)

    # camera movement   
    camera.position += camera.forward * time.dt * 10 * held_keys['w']
    camera.position -= camera.forward * time.dt * 10 * held_keys['s']
    camera.position += camera.right * time.dt * 10 * held_keys['d']
    camera.position -= camera.right * time.dt * 10 * held_keys['a']

    # camera rotation
    if rotToggled:
        camera.world_rotation_y += held_keys['d'] * 1
        camera.world_rotation_y -= held_keys['a'] * 1
        camera.world_rotation_x -= held_keys['w'] * 1
        camera.world_rotation_x += held_keys['s'] * 1

    if mouse.hovered_entity == None:
        selectionTxt.text = 'No atom selected'

# start running the app
app.run()