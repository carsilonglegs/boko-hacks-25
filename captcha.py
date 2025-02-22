from PIL import Image, ImageDraw, ImageFont
import random
import string

def generate_captcha(text: str, width: int = 200, height: int = 100) -> Image:
    image = Image.new('RGB', (width, height), (255, 255, 255))
    font = ImageFont.load_default()
    draw = ImageDraw.Draw(image)
    
    # Draw text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
    
    return image

def main() -> None:
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    image = generate_captcha(captcha_text)
    image.save('out.png')

if __name__ == "__main__":
    main()