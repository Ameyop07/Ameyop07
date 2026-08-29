from PIL import Image, ImageOps, ImageEnhance

def image_to_ascii(image_path, output_width=92, aspect_ratio_correction=0.55):
    img = Image.open(image_path)
    
    # Crop to focus on Amey's head and shoulders (center-right of the landscape image)
    # The image is 1362 x 768. Let's crop:
    # X: 360 to 960 (600px wide)
    # Y: 60 to 660 (600px high)
    left = 360
    top = 60
    right = 960
    bottom = 660
    
    img = img.crop((left, top, right, bottom))
    
    # Convert to grayscale
    img = ImageOps.grayscale(img)
    
    # Enhance contrast to make the outlines pop
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.4)  # boost contrast by 40%
    
    # Enhance brightness slightly to clear up background noise
    brightness = ImageEnhance.Brightness(img)
    img = brightness.enhance(1.1)
    
    # Calculate aspect-corrected height
    cropped_w, cropped_h = img.size
    img_ratio = cropped_h / cropped_w
    output_height = int(output_width * img_ratio * aspect_ratio_correction)
    
    img = img.resize((output_width, output_height), Image.Resampling.LANCZOS)
    
    # Since we want dark sections (hair, suit, sunglasses) to render as lines/pixels
    # and light sections (sky, bright backgrounds) to render as thin dots or spaces,
    # we INVERT the grayscale pixels (255 - pixel)
    ASCII_CHARS = [" ", ".", ":", "-", "=", "+", "*", "%"]
    num_chars = len(ASCII_CHARS)
    
    ascii_str = []
    for y in range(output_height):
        line = ""
        for x in range(output_width):
            pixel = img.getpixel((x, y))
            # Invert the pixel value
            inverted_pixel = 255 - pixel
            char_idx = int((inverted_pixel / 255.0) * (num_chars - 1))
            line += ASCII_CHARS[char_idx]
        ascii_str.append(line)
        
    return ascii_str

if __name__ == "__main__":
    image_path = "profile-photo.jpeg"
    ascii_rows = image_to_ascii(image_path, output_width=92, aspect_ratio_correction=0.55)
    
    with open("portrait.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(ascii_rows))
        
    print(f"Generated portrait.txt with {len(ascii_rows)} lines of inverted ASCII art.")
