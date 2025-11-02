import numpy as np
import matplotlib.pyplot as plt


def load_raw_image(filepath, width=2560, height=3072):
    """
    Load a raw image file from CsI/Gadox x-ray detector.
    
    Parameters:
    -----------
    filepath : str
        Path to the .raw file
    width : int
        Image width in pixels (default: 2560)
    height : int
        Image height in pixels (default: 3072)
    
    Returns:
    --------
    numpy.ndarray
        2D array of shape (height, width) containing the image data
    """
    # Read binary data as 16-bit unsigned integers, little-endian
    data = np.fromfile(filepath, dtype=np.uint16)
    
    # Reshape to (height, width)
    image = data.reshape((height, width))
    
    return image


def create_master_flat(flat_field_files):
    """
    Create a master flat field by combining multiple flat field images.
    
    Parameters:
    -----------
    flat_field_files : list of str
        List of paths to flat field .raw files
    
    Returns:
    --------
    numpy.ndarray
        Master flat field image (median of all input images)
    """
    print(f"Loading {len(flat_field_files)} flat field images...")
    
    # Load all flat field images
    flat_fields = []
    for i, filepath in enumerate(flat_field_files, 1):
        print(f"  Loading {filepath}...")
        img = load_raw_image(filepath)
        flat_fields.append(img)
    
    # Stack images along a new axis (shape: num_images, height, width)
    flat_stack = np.stack(flat_fields, axis=0)
    print(f"Stacked shape: {flat_stack.shape}")
    
    # Compute median to reject outliers
    print("Computing median...")
    master_flat = np.median(flat_stack, axis=0)
    
    print(f"Master flat field created:")
    print(f"  Shape: {master_flat.shape}")
    print(f"  Min: {master_flat.min():.2f}")
    print(f"  Max: {master_flat.max():.2f}")
    print(f"  Mean: {master_flat.mean():.2f}")
    
    return master_flat


# Test the function
if __name__ == "__main__":
    # Create master flat field from ff1-ff5
    flat_field_files = [
        'for_flat_field_correction/ff1.raw',
        'for_flat_field_correction/ff2.raw',
        'for_flat_field_correction/ff3.raw',
        'for_flat_field_correction/ff4.raw',
        'for_flat_field_correction/ff5.raw'
    ]
    
    master_flat = create_master_flat(flat_field_files)
    
    # Visualize the master flat field
    plt.figure(figsize=(10, 12))
    plt.imshow(master_flat, cmap='gray')
    plt.colorbar(label='Pixel Intensity')
    plt.title('Master Flat Field (Median of ff1-ff5)')
    plt.xlabel('Width (pixels)')
    plt.ylabel('Height (pixels)')
    plt.tight_layout()
    plt.show()
