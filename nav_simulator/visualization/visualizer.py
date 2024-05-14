import pyglet
from pyglet import shapes


class Visualizer(object):
    def __init__(self, window_width=500, window_height=500):
        # Initialize window
        self.window = pyglet.window.Window(window_width, window_height)

        # Initialize circle
        self.circle = shapes.Circle(x=50, y=50, radius=20, color=(50, 225, 30))
        self.batch = pyglet.graphics.Batch()
        self.circle.batch = self.batch

        # Set up the event handlers
        self.window.push_handlers(self.on_draw)

        # Set an initial flag for the simulation running state
        self.simulation_running = True

    def on_draw(self):
        # Clear the window and draw the circle
        self.window.clear()
        self.batch.draw()

    def update(self):
        # Update the position of the circle
        self.circle.x += 1
        self.circle.y += 1
        # Redraw the window to reflect the updated position
        self.window.clear()
        self.batch.draw()


    def run(self):
        # Run the pyglet application
        pyglet.app.run()



