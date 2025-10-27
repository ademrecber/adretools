import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def generate_depth_map(image):
    """Basit depth map oluştur"""
    # PIL ile basit depth detection
    img = image.convert('L')  # Grayscale
    
    # Edge detection
    edges = img.filter(ImageFilter.FIND_EDGES)
    
    # Blur for depth effect
    depth = edges.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(depth)
    depth = enhancer.enhance(2.0)
    
    return depth

def create_3d_layers(image, depth_map):
    """3D katmanlar oluştur"""
    import base64
    import io
    
    # Ana görsel
    main_layer = image.copy()
    
    # Depth map'i PIL Image'a çevir
    if not isinstance(depth_map, Image.Image):
        depth_array = np.array(depth_map)
        depth_map = Image.fromarray(depth_array).convert('L')
    
    # Boyutları eşitle
    depth_map = depth_map.resize(image.size)
    
    # Base64'e çevir
    main_b64 = image_to_base64(main_layer)
    depth_b64 = image_to_base64(depth_map)
    
    return {
        'main': main_b64,
        'depth': depth_b64,
        'width': image.width,
        'height': image.height
    }

def image_to_base64(image):
    """PIL Image'ı base64'e çevir"""
    import base64
    import io
    
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"