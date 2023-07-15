def center_window(width, height, root):
    """
    Centers the window on the screen based on the specified width and height.
    
    Args:
        width (int): The width of the window.
        height (int): The height of the window.
        root: The root Tkinter window object.

    Returns:
        None
    """
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
