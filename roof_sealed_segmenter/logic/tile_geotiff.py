import rasterio
from rasterio.windows import Window
import os


def split_geotiff(self):

    input_geotiff = self.SelectTiffToTile.filePath()
    output_folder = self.SaveTiledResults.filePath()
    tile_size = self.spinBox.value()

    filename = os.path.basename(input_geotiff)
    tiff_name = os.path.splitext(filename)[0]

    with rasterio.open(input_geotiff) as src:
        # Get the dimensions of the original image
        width = src.width
        height = src.height

        # Calculate the number of tiles in both dimensions
        n_tiles_x = width // tile_size
        n_tiles_y = height // tile_size

        # Create the output directory if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through the tiles
        for i in range(n_tiles_x):
            for j in range(n_tiles_y):
                # Define the window (section of the image to read)
                window = Window(i * tile_size, j * tile_size, tile_size, tile_size)

                # Read the data in the window
                data = src.read(window=window)

                # Define the output filename
                output_filename = os.path.join(output_folder, f"{tiff_name}_{i}_{j}.tif")

                # Update the metadata for the new tile
                profile = src.profile
                profile.update({
                    'height': tile_size,
                    'width': tile_size,
                    'transform': src.window_transform(window)
                })

                # Write the tile to a new file
                with rasterio.open(output_filename, 'w', **profile) as dst:
                    dst.write(data)

                print(f"Saved tile: {output_filename}")

