import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Pallet:
    def __init__(self, width, height, padding=0):
        self.width = width
        self.height = height
        self.padding = padding
        self.placed_shapes = []
        self.grid = [[False] * height for _ in range(width)]

    def fit_shape(self, shape):
        for rotated in [False, True]:
            current_shape = (shape[1], shape[0]) if rotated else shape
            padded_shape = (current_shape[0] + self.padding, current_shape[1] + self.padding)
            best_spot = None
            min_waste = float('inf')

            for x in range(self.width - padded_shape[0] + 1):
                for y in range(self.height - padded_shape[1] + 1):
                    if self.can_place_shape(padded_shape, x, y):
                        waste = self.calculate_waste(padded_shape, x, y)
                        if waste < min_waste:
                            min_waste = waste
                            best_spot = (x, y, rotated)

            if best_spot is not None:
                self.place_shape_on_grid(padded_shape, best_spot[0], best_spot[1])
                self.placed_shapes.append((best_spot[0], best_spot[1], current_shape))
                return True

        return False

    def can_place_shape(self, shape, x_pos, y_pos):
        for i in range(x_pos, x_pos + shape[0]):
            for j in range(y_pos, y_pos + shape[1]):
                if self.grid[i][j]:
                    return False
        return True

    def place_shape_on_grid(self, shape, x, y):
        for i in range(x, x + shape[0]):
            for j in range(y, y + shape[1]):
                self.grid[i][j] = True

    def calculate_waste(self, shape, x, y):
        waste_area = 0
        for i in range(x, x + shape[0]):
            for j in range(y, y + shape[1]):
                if not self.grid[i][j]:
                    waste_area += 1
        return waste_area
    
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

def main():
    pallet_width, pallet_height = get_pallet_dimensions()
    padding = int(input("Enter padding between shapes (0 for no padding): "))
    number_of_shapes = int(input("How many shapes do you want to place on the pallet? "))

    shapes_to_cut = []
    for i in range(1, number_of_shapes + 1):
        shape_dimensions = get_shape_dimensions(f"Enter the dimensions for shape {i} (width height), or type 'cancel' to skip this shape: ", (pallet_width, pallet_height))
        if shape_dimensions is None:
            print(f"Skipping shape {i}.")
            continue
        shapes_to_cut.append(shape_dimensions)

    shapes_to_cut.sort(key=lambda s: s[0] * s[1], reverse=True)

    pallets = [Pallet(pallet_width, pallet_height, padding)]
    for shape in shapes_to_cut:
        if not pallets[-1].fit_shape(shape):
            new_pallet = Pallet(pallet_width, pallet_height, padding)
            new_pallet.fit_shape(shape)
            pallets.append(new_pallet)

    action = input("Type 'view' to interactively view the pallet images or 'save' to save the images: ").strip().lower()
    if action == 'view':
        viewer = ImageViewer(pallets, pallet_width, pallet_height)
        plt.show()
    elif action == 'save':
        for idx, pallet in enumerate(pallets):
            visualize_packing(pallet_width, pallet_height, pallet.placed_shapes, save=True, file_prefix=f'pallet_layout_{idx}')
    else:
        print("Invalid action. Exiting the program.")

if __name__ == "__main__":
    main()
