import os
import time
from PIL import Image, ImageDraw, ImageFont

# 1. Setup Configuration
OUTPUT_GIF = "assets/demo.gif"
SCRIPT_FILE = "demo_script.txt"
FONT_SIZE = 14
WIDTH, HEIGHT = 700, 450
BG_COLOR = (43, 43, 43)       # Monokai dark grey
TEXT_COLOR = (248, 248, 242)   # Crisp white
PROMPT_COLOR = (166, 226, 46)  # Monokai green

os.makedirs("assets", exist_ok=True)

# Try to grab a default clean monospaced font
try:
    font = ImageFont.truetype("consola.ttf", FONT_SIZE) # Windows Console font
except IOError:
    font = ImageFont.load_default()

frames = []
lines_to_render = []

def add_frame():
    # Draws a fresh terminal frame based on current text lines
    img = Image.new("RGB", (WIDTH, HEIGHT), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw simple mock terminal window top bar
    draw.rectangle([0, 0, WIDTH, 30], fill=(33, 33, 33))
    draw.ellipse([15, 10, 23, 18], fill=(255, 95, 86))   # Red close button
    draw.ellipse([30, 10, 38, 18], fill=(255, 189, 46))  # Yellow minimize
    draw.ellipse([45, 10, 53, 18], fill=(39, 201, 63))   # Green maximize
    
    # Render terminal lines
    y_offset = 45
    for line, is_prompt in lines_to_render:
        color = PROMPT_COLOR if is_prompt else TEXT_COLOR
        draw.text((20, y_offset), line, fill=color, font=font)
        y_offset += 22
    frames.append(img)

# 2. Parse script and simulate real typing loops
if not os.path.exists(SCRIPT_FILE):
    with open(SCRIPT_FILE, "w") as f:
        f.write('& python -m chessforge.cli --mode human-ai --depth 3\ne2e4\ng1f3\nd2d4\nquit')

with open(SCRIPT_FILE, "r") as f:
    commands = f.read().splitlines()

print("Generating showcase frames...")
lines_to_render.append(("PS C:\\Users\\shehe\\chessforge> ", True))
add_frame()

for cmd in commands:
    # Simulate keystroke-by-keystroke typing animation
    current_prompt = lines_to_render[-1][0]
    for i in range(len(cmd) + 1):
        lines_to_render[-1] = (current_prompt + cmd[:i] + "█", True)
        add_frame()
    
    # Remove cursor character, freeze line
    lines_to_render[-1] = (current_prompt + cmd, True)
    add_frame()
    
    # Simulate engine response outputs
    if cmd.startswith("& python"):
        lines_to_render.append(("8  r n b q k b n r", False))
        lines_to_render.append(("7  p p p p p p p p", False))
        lines_to_render.append(("2  P P P P P P P P", False))
        lines_to_render.append(("1  R N B Q K B N R", False))
        lines_to_render.append(("   a b c d e f g h", False))
        lines_to_render.append(("White to move.", False))
    elif cmd == "quit":
        lines_to_render.append(("Process exited cleanly.", False))
    elif cmd:
        lines_to_render.append((f"[Engine calculating deep-dive search tree at depth 3...]", False))
        lines_to_render.append((f"Engine played response move.", False))
        
    lines_to_render.append(("White> ", True))
    add_frame()

# Save out the compiled frames as a high-quality looping GIF
print(f"Compiling frames into high-resolution asset: {OUTPUT_GIF}")
frames[0].save(
    OUTPUT_GIF,
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=80, # milliseconds per frame
    loop=0
)
print("Success! Open assets/demo.gif to view your new engine showcase.")