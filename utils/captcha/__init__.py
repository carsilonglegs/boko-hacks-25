from PIL import Image, ImageDraw, ImageFont
import random
import os

def generate_captcha(text: str, width: int = 200, height: int = 80) -> Image:
    """
    Generate a CAPTCHA image with the given text.
    
    Args:
        text (str): The text to display in the CAPTCHA
        width (int): Image width
        height (int): Image height
        
    Returns:
        PIL.Image: The generated CAPTCHA image
    """
    # Create image with white background
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    try:
        # Try to load Arial font if available
        font = ImageFont.truetype('arial.ttf', 36)
    except OSError:
        # Fallback to default font if Arial not available
        font = ImageFont.load_default()
    
    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Add noise (random dots)
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)))
    
    # Add random lines
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill=(random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)))
    
    # Draw text with slight random offset for each character
    x_offset = text_x
    for char in text:
        # Random slight vertical offset for each character
        y_offset = text_y + random.randint(-5, 5)
        draw.text((x_offset, y_offset), char, font=font, fill=(0, 0, 0))
        # Move x position with a slight random offset
        char_width = draw.textlength(char, font=font)
        x_offset += char_width + random.randint(-2, 2)
    
    return image