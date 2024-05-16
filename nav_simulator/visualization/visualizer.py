import pyglet
from pyglet import shapes
from pyglet.gl import glClearColor


class Visualizer(object):
    def __init__(self, window_width=500, window_height=500):
        # Initialize window
        self.window = pyglet.window.Window(window_width, window_height)

        # Initialize circle
        self.circle = shapes.Circle(x=window_width // 2, y=window_height // 2, radius=20, color=(50, 225, 30))

        # Set up the event handlers
        self.window.push_handlers(self.on_draw)

        # Schedule the update function to be called at regular intervals
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)  # Update at 60 Hz
    def on_draw(self):
        # Clear the window with a white background
        pyglet.gl.glClearColor(1, 1, 1, 1)
        self.window.clear()

        # Draw the circle
        self.circle.draw()

    def update(self, dt):
        # Update the position of the circle (sample movement)
        self.circle.x
        self.circle.y += 1

    def run(self):
        # Run the pyglet application
        pyglet.app.run()



