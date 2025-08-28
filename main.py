from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import io
import webcolors
from typing import List, Dict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title = "Color recognition API",
    description="Upload an image and get dominant colors in RGB, HEX, and name.",
    version="1.0.0",
)

def closest_color(requested_color):
    """
    Find the closest named CSS3 color using Euclidean distance.
    Uses webcolors 24.8.0+ API.
    """
    r, g, b = requested_color
    min_distance = float('inf')
    closest_name = None

    # Get all CSS3 color names
    for name in webcolors.names("css3"):
        try:
            rgb = webcolors.name_to_rgb(name)  # Returns an RGB named tuple
            c_r, c_g, c_b = rgb.red, rgb.green, rgb.blue
        except Exception:
            continue  # Skip any that fail

        distance = (c_r - r) ** 2 + (c_g - g) ** 2 + (c_b - b) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name or "Unknown Color"

def get_dominant_colors(image: np.ndarray, num_colors: int = 5) -> List[Dict]:
    """
    Extract dominant colors using K-Means clustering.
    Returns list of dicts with RGB, HEX, and color name.
    """
    pixels = image.reshape(-1, 3)
    if pixels.shape[0] == 0:
        raise ValueError("Image has no pixels to process.")

    # Limit number of clusters based on pixel count
    num_colors = min(num_colors, len(pixels) // 100 or 1, 10)
    num_colors = max(num_colors, 1)

    kmeans = KMeans(n_clusters=num_colors, n_init=10, random_state=42)
    kmeans.fit(pixels)
    
    colors = kmeans.cluster_centers_.astype(int)
    labels = kmeans.labels_
    counts = np.bincount(labels)
    sorted_indices = np.argsort(counts)[::-1]
    sorted_colors = colors[sorted_indices]
    
    result = []
    for color in sorted_colors:
        hex_color = '#{:02x}{:02x}{:02x}'.format(color[0], color[1], color[2])
        name = closest_color(color)
        result.append({
            "rgb": color.tolist(),
            "hex": hex_color,
            "name": name.title()
        })
    return result

@app.post("/api/color-recognition", response_model=Dict)
async def color_recognition(
    image: UploadFile = File(..., description="Upload an image file"),
    num_colors: int = Form(5, ge=1, le=10, description='Number of dominant colors to extract (1-10)')
):
    """
    Upload an image and get the dominant colors.
    
    - **image**: JPEG, PNG, etc.
    - **num_colors**: Optional, default is 5 (max 10)
    
    Returns: JSON with list of dominant colors (RGB, HEX, name).
    """
    logger.info(f"Received file image {image.filename}, num_colors: {num_colors}")

    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image.")
    
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        pil_image = pil_image.convert("RGB")
        image_np = np.array(pil_image)

        dominant_colors = get_dominant_colors(image_np, num_colors)

        return {
            "success": True,
            "filename": image.filename,
            "num_colors": len(dominant_colors),
            "colors": dominant_colors
        }
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.get("/healt")
def healt_check():
    """
    Health check endpoint.
    """
    return {"status": "OK", "message": "Color recognition API is running!"}



