import pyglet
from pyglet import shapes
from functools import partial


class MySimulation:
    def __init__(self, window_width, window_height):
        # Initialize window
        self.window = pyglet.window.Window(window_width, window_height)

        # Initialize circle
        self.circle = shapes.Circle(x=window_width // 2, y=window_height // 2, radius=20, color=(50, 225, 30))

        # Set up the event handlers
        self.window.push_handlers(self.on_draw)

        # Schedule the update function to be called at regular intervals
        pyglet.clock.schedule_interval(partial(self.update, new_x=0, new_y=0), 1 / 60.0)  # Update at 60 Hz

    def on_draw(self):
        # Clear the window with a white background
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.window.clear()

        # Draw the circle
        self.circle.draw()

    def update(self, dt, new_x, new_y):
        # Update the position of the circle based on new_x and new_y
        self.circle.x = new_x
        self.circle.y = new_y

    def run(self):
        # Run the pyglet application
        pyglet.app.run()

# Example usage
simulation = MySimulation(window_width=500, window_height=500)
simulation.run()

# Example loop to update the position of the circle
for i in range(10):
    print(i)
    new_x = i * 50  # Example calculation for new x position
    new_y = 250     # Example y position remains constant
    pyglet.clock.tick()  # Ensure the update is processed
    simulation.update(0, new_x, new_y)  # Call the update method with the new position

