import base64
import re

def embed_photo_in_svg(svg_path, image_path):
    # Read the image and convert to base64
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    # Read the SVG file
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        
    # Define the clip path and image element to inject
    clip_path_def = '<clipPath id="photoClip"><rect x="24" y="36" width="468" height="448" rx="10" /></clipPath>'
    image_element = f'<image x="24" y="36" width="468" height="448" href="data:image/jpeg;base64,{encoded_string}" clip-path="url(#photoClip)" preserveAspectRatio="xMidYMid slice" />'
    
    # 1. Inject clipPath definition into <defs> if not already present
    if '<clipPath id="photoClip">' not in svg_content:
        # Search for index of </defs>
        defs_end = svg_content.find('</defs>')
        if defs_end != -1:
            svg_content = svg_content[:defs_end] + "  " + clip_path_def + "\n" + svg_content[defs_end:]
            
    # 2. Replace the ASCII text element inside the mask block
    # Remove any existing ASCII text element or show mask block and replace
    pattern = r'<g mask="url\(#revealMask\)">.*?</g>'
    
    # We replace the entire mask group with our direct image tag
    # The image will load instantly and naturally inside the panel
    updated_content = re.sub(pattern, image_element, svg_content, flags=re.DOTALL)
    
    # Write the updated Content back to the SVG
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"Successfully embedded {image_path} inside {svg_path}.")

if __name__ == "__main__":
    embed_photo_in_svg("dark.svg", "profile-photo.jpeg")
    embed_photo_in_svg("light.svg", "profile-photo.jpeg")
