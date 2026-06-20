import os

# Define the Dino Sprites
# '#' is body (Cyan), '*' is spikes (Magenta), '.' is eye (Red), ' ' is transparent
DINO_SPRITES = {
    'run1': [
        "            ########",
        "           ##########",
        "           ##.#######",
        "           ##########",
        "           ######",
        "           ####",
        " *         ######",
        " **       #####",
        " ***     #########",
        " ****   ##########",
        " ***** ###########",
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
        " *         ######",
        " **       #####",
        " ***     #########",
        " ****   ##########",
        " ***** ###########",
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
        " *         ######",
        " **       #####",
        " ***     #########",
        " ****   ##########",
        " ***** ###########",
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

# 7x5 Stencil Tech font for TRUNGVI
LETTER_SPRITES = {
    'T': [
        "#####",
        "  #  ",
        "  #  ",
        "     ",  # Stencil gap
        "  #  ",
        "  #  ",
        "  #  "
    ],
    'R': [
        "#### ",
        "#   #",
        "#   #",
        "#### ",
        "     ",  # Stencil gap
        "#  # ",
        "#   #"
    ],
    'U': [
        "#   #",
        "#   #",
        "#   #",
        "     ",  # Stencil gap
        "#   #",
        "#   #",
        " ### "
    ],
    'N': [
        "#   #",
        "##  #",
        "# # #",
        "     ",  # Stencil gap
        "#  ##",
        "#   #",
        "#   #"
    ],
    'G': [
        " ### ",
        "#   #",
        "#    ",
        "     ",  # Stencil gap
        "# ###",
        "#   #",
        " ### "
    ],
    'V': [
        "#   #",
        "#   #",
        "#   #",
        "     ",  # Stencil gap
        "#   #",
        " # # ",
        "  #  "
    ],
    'I': [
        "#####",
        "  #  ",
        "  #  ",
        "     ",  # Stencil gap
        "  #  ",
        "  #  ",
        "#####"
    ]
}

# Helper to convert sprite to multiple paths based on character types
def sprite_to_paths(sprite, pixel_size=2):
    paths = {
        'body': [],
        'spikes': [],
        'eye': []
    }
    for r_idx, row in enumerate(sprite):
        for c_idx, char in enumerate(row):
            x = c_idx * pixel_size
            y = r_idx * pixel_size
            path_part = f"M {x} {y} h {pixel_size} v {pixel_size} h {-pixel_size} Z"
            if char == '#':
                paths['body'].append(path_part)
            elif char == '*':
                paths['spikes'].append(path_part)
            elif char == '.':
                paths['eye'].append(path_part)
    return {k: " ".join(v) for k, v in paths.items()}

def main():
    # Output file
    output_path = r"C:\Users\HP\.gemini\antigravity\scratch\github-profile\dino-trungvi.svg"
    
    # Grid parameters
    dino_pixel_size = 2 # 20 rows * 2 = 40px height, 20 cols * 2 = 40px width
    letter_pixel_size = 4 # 7 rows * 4 = 28px height, 5 cols * 4 = 20px width
    
    # Convert sprites to path data dictionaries
    dino_run1 = sprite_to_paths(DINO_SPRITES['run1'], dino_pixel_size)
    dino_run2 = sprite_to_paths(DINO_SPRITES['run2'], dino_pixel_size)
    dino_jump = sprite_to_paths(DINO_SPRITES['jump'], dino_pixel_size)
    
    letters_d = {}
    for letter, sprite in LETTER_SPRITES.items():
        # Letters only have '#' and ' ' (transparent)
        paths_dict = sprite_to_paths(sprite, letter_pixel_size)
        letters_d[letter] = paths_dict['body']
        
    # Letter Positions
    letters = ['T', 'R', 'U', 'N', 'G', 'V', 'I']
    letter_x_coords = [200, 265, 330, 395, 460, 525, 590]
    
    # Ground details - Glowing digital axis
    ground_y = 150
    ground_path_d = f"M 0 {ground_y} H 800"
    
    # Sci-fi ground tick marks
    ground_decorations = [
        "M 40 150 v 5 M 42 153 h 4",
        "M 120 150 v 3",
        "M 220 150 v 6 M 222 154 h 6",
        "M 340 150 v 4",
        "M 480 150 v 5 M 482 153 h 4",
        "M 600 150 v 3",
        "M 720 150 v 6 M 722 154 h 6"
    ]
    ground_decor_d = " ".join(ground_decorations)

    # Jump Timing and Keyframes (Loop duration: 12 seconds)
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
      {peak_pct:.2f}% {{ transform: scale(1.2, 0.8); }} /* Squished as Dino jumps over */
      {mid_pct:.2f}% {{ transform: scale(0.85, 1.15); }}  /* Rebound stretch */
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
      --dino-color: #00f0ff;
      --ground-color: rgba(0, 240, 255, 0.25);
      --decor-color: rgba(255, 0, 127, 0.2);
      
      /* Neon Cyber Colors */
      --color-t: #00f0ff;
      --color-r: #ff007f;
      --color-u: #00f0ff;
      --color-n: #ff007f;
      --color-g: #00f0ff;
      --color-v: #ff007f;
      --color-i: #00f0ff;
    }}
    
    @media (prefers-color-scheme: light) {{
      :root {{
        --dino-color: #080B10;
        --ground-color: rgba(0, 136, 204, 0.3);
        --decor-color: rgba(204, 0, 102, 0.25);
        
        --color-t: #0088cc;
        --color-r: #cc0066;
        --color-u: #0088cc;
        --color-n: #cc0066;
        --color-g: #0088cc;
        --color-v: #cc0066;
        --color-i: #0088cc;
      }}
    }}

    .dino-color {{ fill: var(--dino-color); }}
    .ground-color {{ stroke: var(--ground-color); stroke-width: 1.5; fill: none; }}
    .decor-color {{ fill: none; stroke: var(--decor-color); stroke-width: 1; }}
    
    /* Neon Glows */
    .glow-cyan {{ filter: drop-shadow(0 0 3px rgba(0, 240, 255, 0.6)); }}
    .glow-magenta {{ filter: drop-shadow(0 0 3px rgba(255, 0, 127, 0.6)); }}
    
    /* Letter colors */
    .color-t {{ fill: var(--color-t); filter: drop-shadow(0 0 3px rgba(0, 240, 255, 0.5)); }}
    .color-r {{ fill: var(--color-r); filter: drop-shadow(0 0 3px rgba(255, 0, 127, 0.5)); }}
    .color-u {{ fill: var(--color-u); filter: drop-shadow(0 0 3px rgba(0, 240, 255, 0.5)); }}
    .color-n {{ fill: var(--color-n); filter: drop-shadow(0 0 3px rgba(255, 0, 127, 0.5)); }}
    .color-g {{ fill: var(--color-g); filter: drop-shadow(0 0 3px rgba(0, 240, 255, 0.5)); }}
    .color-v {{ fill: var(--color-v); filter: drop-shadow(0 0 3px rgba(255, 0, 127, 0.5)); }}
    .color-i {{ fill: var(--color-i); filter: drop-shadow(0 0 3px rgba(0, 240, 255, 0.5)); }}

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

  <!-- Background -->
  <rect width="100%" height="100%" fill="var(--bg-color)" />

  <!-- Ground Axis -->
  <path class="ground-color" d="{ground_path_d}" />
  <path class="decor-color" d="{ground_decor_d}" />

  <!-- Letters "TRUNGVI" -->
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

  <!-- Animated Cyber-Dino -->
  <!-- Base y offset puts Dino on the ground (150 ground - 40 dino height) -->
  <g class="dino-container">
    <g transform="translate(0, 110)">
      <g class="dino-y">
        <!-- Body (Cyan) -->
        <path class="dino-color dino-run1 glow-cyan" d="{dino_run1['body']}" />
        <path class="dino-color dino-run2 glow-cyan" d="{dino_run2['body']}" />
        <path class="dino-color dino-jump glow-cyan" d="{dino_jump['body']}" />
        
        <!-- Spikes (Neon Pink) -->
        <path class="dino-run1 glow-magenta" d="{dino_run1['spikes']}" fill="#ff007f" />
        <path class="dino-run2 glow-magenta" d="{dino_run2['spikes']}" fill="#ff007f" />
        <path class="dino-jump glow-magenta" d="{dino_jump['spikes']}" fill="#ff007f" />
        
        <!-- Eye (Neon Red) -->
        <path class="dino-run1" d="{dino_run1['eye']}" fill="#ff0033" filter="drop-shadow(0 0 2px #ff0033)" />
        <path class="dino-run2" d="{dino_run2['eye']}" fill="#ff0033" filter="drop-shadow(0 0 2px #ff0033)" />
        <path class="dino-jump" d="{dino_jump['eye']}" fill="#ff0033" filter="drop-shadow(0 0 2px #ff0033)" />
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
