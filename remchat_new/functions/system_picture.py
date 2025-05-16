import os
import base64

def system_picture():
    """
    Reads an image file named 'picture.jpg' located in the same directory as the script,
    encodes it in Base64 format, and returns the encoded string.

    Returns:
        str: Base64 encoded string of the image if the file exists and is readable.
        None: If the image file is not found or cannot be opened.
    
    Exceptions:
        FileNotFoundError: Raised if the image file does not exist.
    
    Example:
        >>> system_picture()
        'iVBORw0KGgoAAAANSUhEUgAA...'
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(__file__)
    image = os.path.join(script_dir, 'picture.jpg')

    try:
        with open(image, 'rb') as dft_pic:
            if dft_pic:
                return base64.b64encode(dft_pic.read()).decode('utf-8')
            else:
                return None
    except FileNotFoundError as e:
        print(f"Error occurred while fetching image: {e} 😒")
        return None
