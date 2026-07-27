"""
Create a simple test image for the Detection Agent
"""
from PIL import Image, ImageDraw, ImageFont
import random

def create_test_image():
    """Create a simulated drone image with random colored shapes"""
    
    # Create a 1920x1080 image (like a drone photo)
    img = Image.new('RGB', (1920, 1080), color=(50, 120, 200))  # Blue-ish sky/water
    
    draw = ImageDraw.Draw(img)
    
    # Draw some "flood water" patches (blue/dark areas)
    for _ in range(random.randint(5, 15)):
        x = random.randint(0, 1920)
        y = random.randint(0, 1080)
        w = random.randint(50, 300)
        h = random.randint(50, 200)
        draw.rectangle([x, y, x+w, y+h], fill=(30, 80, 160))
    
    # Draw some "buildings" (gray rectangles)
    for _ in range(random.randint(3, 8)):
        x = random.randint(100, 1820)
        y = random.randint(100, 980)
        w = random.randint(40, 80)
        h = random.randint(60, 120)
        draw.rectangle([x, y, x+w, y+h], fill=(150, 150, 150))
        # Windows
        for wx in range(x+10, x+w-10, 15):
            for wy in range(y+15, y+h-15, 20):
                draw.rectangle([wx, wy, wx+8, wy+12], fill=(255, 255, 200))
    
    # Draw some "people" (small colored dots) - representing detected people
    for _ in range(random.randint(10, 30)):
        x = random.randint(100, 1820)
        y = random.randint(100, 980)
        # Draw person as a small colored circle
        color = random.choice([(255, 50, 50), (255, 100, 50), (255, 150, 50)])  # Red/orange
        draw.ellipse([x-5, y-10, x+5, y+10], fill=color)
        # Small head
        draw.ellipse([x-3, y-15, x+3, y-8], fill=(255, 200, 150))
    
    # Draw some "trees" (green circles)
    for _ in range(random.randint(5, 12)):
        x = random.randint(100, 1820)
        y = random.randint(100, 980)
        draw.ellipse([x-15, y-20, x+15, y+20], fill=(30, 120, 30))
        draw.rectangle([x-3, y+10, x+3, y+25], fill=(100, 80, 50))
    
    # Save image
    img.save("test_drone_image.jpg")
    print("✅ Created test_drone_image.jpg")
    return "test_drone_image.jpg"

if __name__ == "__main__":
    create_test_image()