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


def apply_flat_field_correction(raw_image, master_flat):
    """
    Apply flat field correction to a raw image.
    
    Parameters:
    -----------
    raw_image : numpy.ndarray
        Raw image to be corrected
    master_flat : numpy.ndarray
        Master flat field image
    
    Returns:
    --------
    numpy.ndarray
        Flat field corrected image
    """
    # Avoid division by zero by setting a minimum threshold
    # Use a small positive value where master_flat is very low
    master_flat_safe = np.where(master_flat > 0, master_flat, 1)
    
    # Apply correction: corrected = (raw / master_flat) * mean(master_flat)
    mean_flat = np.mean(master_flat)
    corrected_image = (raw_image.astype(np.float32) / master_flat_safe) * mean_flat
    
    print(f"Flat field correction applied:")
    print(f"  Original range: [{raw_image.min()}, {raw_image.max()}]")
    print(f"  Corrected range: [{corrected_image.min():.2f}, {corrected_image.max():.2f}]")
    print(f"  Mean flat value: {mean_flat:.2f}")
    
    return corrected_image


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
    
    # Load ff6.raw
    print("\nLoading ff6.raw...")
    ff6 = load_raw_image('ff6.raw')
    print(f"ff6 loaded: shape={ff6.shape}, min={ff6.min()}, max={ff6.max()}, mean={ff6.mean():.2f}")
    
    # Apply flat field correction
    print("\nApplying flat field correction...")
    ff6_corrected = apply_flat_field_correction(ff6, master_flat)
    
    # Visualize original and corrected images side by side
    fig, axes = plt.subplots(1, 2, figsize=(20, 12))
    
    # Original ff6
    im1 = axes[0].imshow(ff6, cmap='gray')
    axes[0].set_title('Original ff6')
    axes[0].set_xlabel('Width (pixels)')
    axes[0].set_ylabel('Height (pixels)')
    plt.colorbar(im1, ax=axes[0], label='Pixel Intensity')
    
    # Corrected ff6
    im2 = axes[1].imshow(ff6_corrected, cmap='gray')
    axes[1].set_title('Corrected ff6 (Flat Field Applied)')
    axes[1].set_xlabel('Width (pixels)')
    axes[1].set_ylabel('Height (pixels)')
    plt.colorbar(im2, ax=axes[1], label='Pixel Intensity')
    
    plt.tight_layout()
    plt.show()
    
    # Load reference corrected image
    print("\nLoading reference corrected image...")
    ff_corrected_ref = load_raw_image('reference/ff_corrected.raw')
    print(f"Reference loaded: shape={ff_corrected_ref.shape}, min={ff_corrected_ref.min()}, max={ff_corrected_ref.max()}, mean={ff_corrected_ref.mean():.2f}")
    
    # Compare histograms of corrected ff6 and reference
    print("\nComparing histograms...")
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    # Histogram of our corrected ff6
    axes[0].hist(ff6_corrected.flatten(), bins=256, color='blue', alpha=0.7, edgecolor='black')
    axes[0].set_title('Histogram of Corrected ff6')
    axes[0].set_xlabel('Pixel Intensity')
    axes[0].set_ylabel('Frequency')
    axes[0].grid(True, alpha=0.3)
    axes[0].text(0.02, 0.98, f'Mean: {ff6_corrected.mean():.2f}\nStd: {ff6_corrected.std():.2f}', 
                 transform=axes[0].transAxes, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # Histogram of reference corrected image
    axes[1].hist(ff_corrected_ref.flatten(), bins=256, color='green', alpha=0.7, edgecolor='black')
    axes[1].set_title('Histogram of Reference ff_corrected')
    axes[1].set_xlabel('Pixel Intensity')
    axes[1].set_ylabel('Frequency')
    axes[1].grid(True, alpha=0.3)
    axes[1].text(0.02, 0.98, f'Mean: {ff_corrected_ref.mean():.2f}\nStd: {ff_corrected_ref.std():.2f}', 
                 transform=axes[1].transAxes, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.show()
    
    # Overlay histograms for direct comparison
    plt.figure(figsize=(12, 6))
    plt.hist(ff6_corrected.flatten(), bins=256, color='blue', alpha=0.5, label='Corrected ff6', edgecolor='black')
    plt.hist(ff_corrected_ref.flatten(), bins=256, color='green', alpha=0.5, label='Reference ff_corrected', edgecolor='black')
    plt.title('Histogram Comparison: Correction vs Reference')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

