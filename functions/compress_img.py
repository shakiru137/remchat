import tinify

# Image compression function
def compress_img(image):
    """
    Compresses an image using the Tinify API.

    This function takes an image file, compresses it using the Tinify 
    service, and returns the compressed image in a buffer format.

    Args:
        image (file-like object): The image file to be compressed.

    Returns:
        bytes or None: The compressed image data as bytes if successful; 
                        None if compression fails.
    """
    tinify.key = "CgCQJfMMzMrZwRlrGQXsm1qWJf0J5br6"  # Set Tinify API key
    try:
        return tinify.Source.from_buffer(image.read()).to_buffer()
    except Exception as e:
        print(f"Compression error: {e} 😒")  # Log the error
        return None
