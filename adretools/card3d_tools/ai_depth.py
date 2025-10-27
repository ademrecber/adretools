import cv2
import numpy as np
from PIL import Image

def generate_depth_map(image):
    """AI ile depth map oluştur"""
    try:
        # MiDaS AI model kullanmayı dene
        from transformers import pipeline
        depth_estimator = pipeline('depth-estimation', model='Intel/dpt-large')
        depth_result = depth_estimator(image)
        return depth_result['depth']
    except:
        # Fallback: OpenCV ile basit depth
        img_array = np.array(image.convert('RGB'))
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        
        # Edge detection ile fake depth
        edges = cv2.Canny(gray, 50, 150)
        depth = cv2.GaussianBlur(edges, (15, 15), 0)
        
        # Normalize
        depth = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX)
        return Image.fromarray(depth)

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