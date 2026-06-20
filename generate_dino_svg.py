import os

# Define the Dino Sprites (pixels: '#' is filled, '.' is transparent/eye, ' ' is transparent)
DINO_SPRITES = {
    'run1': [
        "            ########",
        "           ##########",
        "           ##.#######",
        "           ##########",
        "           ######",
        "           ####",
        " #         ######",
        " ##       #####",
        " ###     #########",
        " ####   ##########",
        " ##### ###########",
        " ################",
        "  ##############",
        "   ############",
        "    ##########",
        "     ########",
        "      ######",
        "       ## ##",
        "       ##",
        "       ##",
    ],
    'run2': [
        "            ########",
        "           ##########",
        "           ##.####",
        "           ##      ##",
        "           ########",
        "           ####",
        " #         ######",
        " ##       #####",
        " ###     #########",
        " ####   ##########",
        " ##### ###########",
        " ################",
        "  ##############",
        "   ############",
        "    ##########",
        "     ########",
        "      ######",
        "       ## ##",
        "          ##",
        "          ##",
    ],
    'jump': [
        "            ########",
        "           ##########",
        "           ##.####",
        "           ##      ##",
        "           ########",
        "           ####",
        " #         ######",
        " ##       #####",
        " ###     #########",
        " ####   ##########",
        " ##### ###########",
        " ################",
        "  ##############",
        "   ############",
        "    ##########",
        "     ########",
        "      ######",
        "       ## ##",
        "       ## ##",
        "       #   #",
    ]
}

# 7x5 Retro font for TRUNGVI
LETTER_SPRITES = {
    'T': [
        "#####",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  "
    ],
    'R': [
        "#### ",
        "#   #",
        "#   #",
        "#### ",
        "#  # ",
        "#   #",
        "#   #"
    ],
    'U': [
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        " ### "
    ],
    'N': [
        "#   #",
        "##  #",
        "# # #",
        "#  ##",
        "#   #",
        "#   #",
        "#   #"
    ],
    'G': [
        " ### ",
        "#   #",
        "#    ",
        "# ###",
        "#   #",
        "#   #",
        " ### "
    ],
    'V': [
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        " # # ",
        "  #  "
    ],
    'I': [
        "#####",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "#####"
    ]
}

# Helper to convert sprite to SVG path
def sprite_to_path_d(sprite, pixel_size=2):
    path_parts = []
    for r_idx, row in enumerate(sprite):
        for c_idx, char in enumerate(row):
            if char == '#':
                x = c_idx * pixel_size
                y = r_idx * pixel_size
                path_parts.append(f"M {x} {y} h {pixel_size} v {pixel_size} h {-pixel_size} Z")
    return " ".join(path_parts)

def main():
    # Output file
    output_path = r"C:\Users\HP\.gemini\antigravity\scratch\github-profile\dino-trungvi.svg"
    
    # Grid parameters
    dino_pixel_size = 2 # 20 rows * 2 = 40px height, 20 cols * 2 = 40px width
    letter_pixel_size = 4 # 7 rows * 4 = 28px height, 5 cols * 4 = 20px width
    
    # Convert sprites to path data
    dino_run1_d = sprite_to_path_d(DINO_SPRITES['run1'], dino_pixel_size)
    dino_run2_d = sprite_to_path_d(DINO_SPRITES['run2'], dino_pixel_size)
    dino_jump_d = sprite_to_path_d(DINO_SPRITES['jump'], dino_pixel_size)
    
    letters_d = {}
    for letter, sprite in LETTER_SPRITES.items():
        letters_d[letter] = sprite_to_path_d(sprite, letter_pixel_size)
        
    # Letter Positions
    # Center of SVG is 400.
    letters = ['T', 'R', 'U', 'N', 'G', 'V', 'I']
    letter_x_coords = [200, 265, 330, 395, 460, 525, 590]
    
    # Ground details
    # We will generate a retro ground with some cracks/bumps
    ground_y = 150
    ground_path_d = f"M 0 {ground_y} H 800"
    
    # Add some retro pixel ground decorations (like dots or small horizontal lines)
    ground_decorations = [
        "M 50 155 h 6 M 52 157 h 2",
        "M 180 154 h 4",
        "M 310 156 h 8 M 312 158 h 3",
        "M 450 155 h 5",
        "M 620 154 h 3 M 622 156 h 5",
        "M 750 157 h 4"
    ]
    ground_decor_d = " ".join(ground_decorations)

    # Jump Timing and Keyframes
    # Loop duration: 12 seconds
    # Speed: 920px in 12s => 76.67px/s
    # Dino X: -60 to 860
    jumps = [
        (2.76, 3.26),  # T (peak at 3.01)
        (3.61, 4.11),  # R (peak at 3.86)
        (4.46, 4.96),  # U (peak at 4.71)
        (5.31, 5.81),  # N (peak at 5.56)
        (6.15, 6.65),  # G (peak at 6.40)
        (7.00, 7.50),  # V (peak at 7.25)
        (7.85, 8.35)   # I (peak at 8.10)
    ]
    
    def is_jumping(t):
        for start, end in jumps:
            if start <= t <= end:
                return True
        return False

    # Generate step-based leg animations
    fps = 20 # 0.05s steps
    total_time = 12.0
    num_steps = int(total_time * fps) + 1
    
    keyframes_run1 = []
    keyframes_run2 = []
    keyframes_jump = []
    
    for i in range(num_steps):
        t = i / fps
        pct = (t / total_time) * 100
        if pct > 100.0: pct = 100.0
        
        if is_jumping(t):
            state = 'jump'
        else:
            state = 'run1' if (int(t / 0.12) % 2 == 0) else 'run2'
            
        opacity_run1 = 1 if state == 'run1' else 0
        opacity_run2 = 1 if state == 'run2' else 0
        opacity_jump = 1 if state == 'jump' else 0
        
        keyframes_run1.append(f"      {pct:.2f}% {{ opacity: {opacity_run1}; }}")
        keyframes_run2.append(f"      {pct:.2f}% {{ opacity: {opacity_run2}; }}")
        keyframes_jump.append(f"      {pct:.2f}% {{ opacity: {opacity_jump}; }}")
        
    run1_css = "\n".join(keyframes_run1)
    run2_css = "\n".join(keyframes_run2)
    jump_css = "\n".join(keyframes_jump)

    # Let's generate the Letter bounce CSS keyframes
    letter_animations_css = []
    for idx, letter in enumerate(letters):
        peak_t = jumps[idx][0] + 0.25 # peak of jump
        peak_pct = (peak_t / total_time) * 100
        
        start_pct = ((jumps[idx][0] - 0.1) / total_time) * 100
        end_pct = ((jumps[idx][1] + 0.2) / total_time) * 100
        mid_pct = ((jumps[idx][1]) / total_time) * 100
        
        letter_animations_css.append(f"""
    @keyframes bounce-{letter.lower()} {{
      0% {{ transform: scale(1); }}
      {start_pct:.2f}% {{ transform: scale(1); }}
      {peak_pct:.2f}% {{ transform: scale(1.3, 0.7); }} /* Squished as Dino jumps over */
      {mid_pct:.2f}% {{ transform: scale(0.8, 1.2); }}  /* Rebound stretch */
      {end_pct:.2f}% {{ transform: scale(1); }}
      100% {{ transform: scale(1); }}
    }}
    .letter-{letter.lower()} {{
      animation: bounce-{letter.lower()} 12s infinite ease-in-out;
      transform-box: fill-box;
      transform-origin: center bottom;
    }}""")

    letter_animations_block = "\n".join(letter_animations_css)

    # Compile the SVG
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" width="100%" height="100%">
  <style>
    /* Theme color adaptation */
    :root {{
      --bg-color: transparent;
      --dino-color: #39ff14;
      --ground-color: #30363d;
      --decor-color: #21262d;
      
      /* Rainbow letters - Dark Theme */
      --color-t: #ff7b72;
      --color-r: #f0883e;
      --color-u: #ffeb3b;
      --color-n: #39ff14;
      --color-g: #58a6ff;
      --color-v: #bc8cff;
      --color-i: #ff79c6;
    }}
    
    @media (prefers-color-scheme: light) {{
      :root {{
        --dino-color: #24292f;
        --ground-color: #d0d7de;
        --decor-color: #afb8c1;
        
        /* Rainbow letters - Light Theme */
        --color-t: #cf222e;
        --color-r: #bc4c00;
        --color-u: #8250df;
        --color-n: #1a7f37;
        --color-g: #0969da;
        --color-v: #8250df;
        --color-i: #bf3989;
      }}
    }}

    .dino-color {{ fill: var(--dino-color); }}
    .ground-color {{ stroke: var(--ground-color); stroke-width: 2; fill: none; }}
    .decor-color {{ fill: var(--decor-color); }}
    
    /* Letter colors */
    .color-t {{ fill: var(--color-t); }}
    .color-r {{ fill: var(--color-r); }}
    .color-u {{ fill: var(--color-u); }}
    .color-n {{ fill: var(--color-n); }}
    .color-g {{ fill: var(--color-g); }}
    .color-v {{ fill: var(--color-v); }}
    .color-i {{ fill: var(--color-i); }}

    /* Base layouts */
    .letters-group {{
      display: flex;
    }}

    /* Dino movement path */
    .dino-container {{
      animation: move-x 12s linear infinite;
    }}
    
    .dino-y {{
      animation: jump 12s linear infinite;
    }}

    @keyframes move-x {{
      0% {{ transform: translateX(-60px); }}
      100% {{ transform: translateX(860px); }}
    }}

    @keyframes jump {{
      0% {{ transform: translateY(0); }}
      23.00% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      25.10% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      27.20% {{ transform: translateY(0); }}
      30.10% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      32.20% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      34.20% {{ transform: translateY(0); }}
      37.20% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      39.20% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      41.30% {{ transform: translateY(0); }}
      44.20% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      46.30% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      48.40% {{ transform: translateY(0); }}
      51.25% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      53.30% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      55.40% {{ transform: translateY(0); }}
      58.30% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      60.40% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      62.50% {{ transform: translateY(0); }}
      65.40% {{ transform: translateY(0); animation-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }}
      67.50% {{ transform: translateY(-60px); animation-timing-function: cubic-bezier(0.55, 0.085, 0.68, 0.53); }}
      69.60% {{ transform: translateY(0); }}
      100% {{ transform: translateY(0); }}
    }}

    /* Dino leg frame switches */
    @keyframes run1 {{
{run1_css}
    }}

    @keyframes run2 {{
{run2_css}
    }}

    @keyframes jump-frame {{
{jump_css}
    }}

    .dino-run1 {{ animation: run1 12s step-end infinite; }}
    .dino-run2 {{ animation: run2 12s step-end infinite; }}
    .dino-jump {{ animation: jump-frame 12s step-end infinite; }}
    
{letter_animations_block}
  </style>

  <!-- Background (Optional / Transparent by default) -->
  <rect width="100%" height="100%" fill="var(--bg-color)" />

  <!-- Ground -->
  <path class="ground-color" d="{ground_path_d}" />
  <path class="decor-color" d="{ground_decor_d}" />

  <!-- Letters "TRUNGVI" -->
  <!-- Positioned at y = 122 (150 ground - 28 height) -->
  <g transform="translate({letter_x_coords[0]}, 122)">
    <g class="letter-t">
      <path class="color-t" d="{letters_d['T']}" />
    </g>
  </g>
  <g transform="translate({letter_x_coords[1]}, 122)">
    <g class="letter-r">
      <path class="color-r" d="{letters_d['R']}" />
    </g>
  </g>
  <g transform="translate({letter_x_coords[2]}, 122)">
    <g class="letter-u">
      <path class="color-u" d="{letters_d['U']}" />
    </g>
  </g>
  <g transform="translate({letter_x_coords[3]}, 122)">
    <g class="letter-n">
      <path class="color-n" d="{letters_d['N']}" />
    </g>
  </g>
  <g transform="translate({letter_x_coords[4]}, 122)">
    <g class="letter-g">
      <path class="color-g" d="{letters_d['G']}" />
    </g>
  </g>
  <g transform="translate({letter_x_coords[5]}, 122)">
    <g class="letter-v">
      <path class="color-v" d="{letters_d['V']}" />
    </g>
  </g>
  <g transform="translate({letter_x_coords[6]}, 122)">
    <g class="letter-i">
      <path class="color-i" d="{letters_d['I']}" />
    </g>
  </g>

  <!-- Animated Dino -->
  <!-- Base y offset puts Dino on the ground (150 ground - 40 dino height) -->
  <g class="dino-container">
    <g transform="translate(0, 110)">
      <g class="dino-y">
        <path class="dino-color dino-run1" d="{dino_run1_d}" />
        <path class="dino-color dino-run2" d="{dino_run2_d}" />
        <path class="dino-color dino-jump" d="{dino_jump_d}" />
      </g>
    </g>
  </g>
</svg>
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated pixel dinosaur SVG at {output_path}")

if __name__ == '__main__':
    main()
