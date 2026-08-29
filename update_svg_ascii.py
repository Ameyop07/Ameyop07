import re

def update_svg_with_ascii(svg_path, ascii_path):
    with open(ascii_path, "r", encoding="utf-8") as f:
        ascii_lines = f.read().splitlines()
    
    # Generate the tspans
    # Start y at 70 to match the vertical positioning nicely
    start_y = 52.0
    line_spacing = 7.55
    
    tspan_blocks = []
    for idx, line in enumerate(ascii_lines):
        y_val = round(start_y + (idx * line_spacing), 2)
        # Ensure xml:space="preserve" is set so spaces aren't collapsed by browser
        tspan_blocks.append(f'<tspan x="30" y="{y_val}" xml:space="preserve">{line}</tspan>')
        
    new_ascii_block = "\n".join(tspan_blocks)
    
    # Read the SVG file
    with open(svg_path, "r", encoding="utf-8") as f:
        svg_content = f.read()
        
    # Regex to replace the text inside <text x="30" y="0" class="ascii">...</text>
    # Note: Use DOTALL to match newlines
    pattern = r'(<text x="30" y="0" class="ascii">).*?(</text>)'
    replacement = r'\1\n' + new_ascii_block + r'\n  \2'
    
    updated_content = re.sub(pattern, replacement, svg_content, flags=re.DOTALL)
    
    # If the user list is a bit longer or shorter, let's write it back
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
        
    print(f"Updated {svg_path} with {len(ascii_lines)} lines of ASCII art.")

if __name__ == "__main__":
    update_svg_with_ascii("dark.svg", "portrait.txt")
    update_svg_with_ascii("light.svg", "portrait.txt")
