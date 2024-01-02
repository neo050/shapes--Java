import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Pallet class as you provided...

class ImageViewer:
    def __init__(self, pallets, pallet_width, pallet_height):
        self.pallets = pallets
        self.pallet_width = pallet_width
        self.pallet_height = pallet_height
        self.fig, self.ax = plt.subplots()
        self.idx = 0
        self.show_pallet(self.idx)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)

    def show_pallet(self, idx):
        self.ax.clear()
        pallet = self.pallets[idx]
        self.ax.add_patch(patches.Rectangle((0, 0), self.pallet_width, self.pallet_height, fill=None, edgecolor='red'))
        for _, (x, y, shape) in enumerate(pallet.placed_shapes):
            self.ax.add_patch(patches.Rectangle((x, y), shape[0], shape[1], edgecolor='blue', facecolor='blue', alpha=0.5))
            plt.text(x + shape[0]/2, y + shape[1]/2, str(_), color='white', ha='center', va='center')
        self.ax.set_xlim(0, self.pallet_width)
        self.ax.set_ylim(0, self.pallet_height)
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_title(f'Pallet {idx + 1}/{len(self.pallets)}')
        self.fig.canvas.draw()

    def on_key(self, event):
        if event.key == 'right':
            self.idx = (self.idx + 1) % len(self.pallets)
        elif event.key == 'left':
            self.idx = (self.idx - 1) % len(self.pallets)
        self.show_pallet(self.idx)

def visualize_packing(pallet_width, pallet_height, placed_shapes, save=False, file_prefix='pallet_layout'):
    fig, ax = plt.subplots()
    ax.add_patch(patches.Rectangle((0, 0), pallet_width, pallet_height, fill=None, edgecolor='red'))
    for i, (x, y, shape) in enumerate(placed_shapes):
        ax.add_patch(patches.Rectangle((x, y), shape[0], shape[1], edgecolor='blue', facecolor='blue', alpha=0.5))
        plt.text(x + shape[0]/2, y + shape[1]/2, str(i), color='white', ha='center', va='center')
    ax.set_xlim(0, pallet_width)
    ax.set_ylim(0, pallet_height)
    ax.set_aspect('equal', adjustable='box')
    if save:
        plt.savefig(f'{file_prefix}.png')
    else:
        plt.show()

def get_shape_dimensions(message, limit):
    while True:
        dimensions_input = input(message)
        if dimensions_input.lower() == 'cancel':
            return None
        try:
            width, height = map(int, dimensions_input.split())
            if width > 0 and height > 0 and width <= limit[0] and height <= limit[1]:
                return width, height
            else:
                print(f"Error: Shape dimensions must be positive and not exceed the pallet size of {limit}. Try again or type 'cancel'.")
        except ValueError:
            print("Invalid input. Enter two integer values separated by a space or 'cancel' to skip.")

def get_pallet_dimensions():
    while True:
        dimensions_input = input("Enter the pallet width and height, separated by a space (e.g., '100 100'): ")
        try:
            width, height = map(int, dimensions_input.split())
            if width > 0 and height > 0:
                return width, height
            else:
                print("Error: Pallet dimensions must be positive integers. Please try again.")
        except ValueError:
            print("Invalid input. Please enter two integer values separated by a space.")

