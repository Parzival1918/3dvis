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
prevMousePos = None

#Read data from file
atoms, uniqueSpecies = parse_files.parse_XYZ("testFiles/pyridine.xyz")
selectionColours = []

# UI text and buttons
rotText = Text(text='Rotation: OFF', position=window.bottom_right, origin=(+0.5, -0.5))
selectionTxt = Text(text='No atom selected', position=window.bottom_left, origin=(-0.5, -0.5))

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
            global selectionColours
            self.color = selectionColours[uniqueSpecies.index(self.name)]

# create app contents
spheres = []
for atom in atoms:
    sphere = Atom(position=(atom['x'], atom['y'], atom['z']))
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

    if mouse.left and mouse.moving:
        global prevMousePos
        if prevMousePos == None:
            prevMousePos = mouse.position
        else:
            deltaMousePos = [mouse.position[0] - prevMousePos[0], mouse.position[1] - prevMousePos[1]]
            speed = 0.5
            if abs(deltaMousePos[0]) >= 0.02:
                if deltaMousePos[0] > 0:
                    camera.world_rotation_y += speed
                else:
                    camera.world_rotation_y -= speed
            if abs(deltaMousePos[1]) >= 0.02:
                if deltaMousePos[1] > 0:
                    camera.world_rotation_x -= speed
                else:
                    camera.world_rotation_x += speed
        print(mouse.position)

def atomic_size_from_table():
    print("Atomic size from table")

    for sphere in spheres:
        scale = atomicData.loc[atomicData["Symbol"] == sphere.name]["AtomicRadius"] / 100.0
        sphere.scale = (scale, scale, scale)

def atomic_size_equal():
    print("Atomic size constant")

    for sphere in spheres:
        sphere.scale = (1, 1, 1)

def colour_random():
    print("Colour random")

    global selectionColours
    selectionColours = [color.random_color() for _ in range(len(uniqueSpecies))]
    for sphere in spheres:
        sphere.color = color.random_color()

DropdownMenu('Settings', buttons=(
    DropdownMenu('Atomic size', buttons=(
        DropdownMenuButton('From file', on_click=lambda: print('From file')),
        DropdownMenuButton('From table', on_click=lambda: atomic_size_from_table(), tooltip=Tooltip('Set atomic size from table')),
        DropdownMenuButton('Equal', on_click=lambda: atomic_size_equal()),
    )),
    DropdownMenu('Colour', buttons=(
        DropdownMenuButton('Random', on_click=lambda: colour_random()),
    ))
))

atomic_size_from_table() # Set atomic size from table as default
colour_random() # Set random colours as default

# start running the app
app.run()