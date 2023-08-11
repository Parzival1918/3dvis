from ursina import *

import parse_files

# create a window
app = Ursina(title="3Dvis")

window.borderless = False # show a border

# Set initial variables
# initialCameraPosition = camera.position
initialCameraPosition = (0, 0, -20)

#Read data from file
atoms = parse_files.parse_XYZ("testFiles/pyridine.xyz")

# Class entities
class Atom(Entity):
    def __init__(self, position=(0,0,0), scale=(1,1,1), **kwargs):
        super().__init__()
        self.model = 'sphere'
        self.color = color.orange
        self.scale = (1, 1, 1)
        self.collider = 'sphere'
        self.world_position = position
        self.scale = scale

    def update(self):
        if self.hovered:
            self.color = color.tint(self.color, .1)
        else:
            self.color = color.orange

# create app contents
spheres = []
for atom in atoms:
    sphere = Atom(position=(atom['x'], atom['y'], atom['z']))
    sphere.name = atom['element']

    spheres.append(sphere)

# b = Button(text='hello world!', color=color.azure, scale=.25, highlight_scale=1.1)
# b.on_click = application.quit # assign a function to the button.
# b.tooltip = Tooltip('exit')

# UI text and buttons
rotText = Text(text='Rotation: OFF', position=window.top_left)

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

# start running the app
app.run()