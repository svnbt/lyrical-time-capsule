import json

with open('config.json', 'r') as f:
    config = json.load(f)

colors = config["colors"]
fonts = config["fonts"]

css_content = f"""
/* AUTOMATICALLY GENERATED FROM config.json */
:root {{
    --bg-color: {colors['BG_COLOR']};
    --text-color: {colors['TEXT_COLOR']};
    --light-text-color: {colors['LIGHT_TEXT_COLOR']};
    --accent-color: {colors['US_COLOR']}; 
    --muted-text: #B0B3B8;
    --grid-color: {colors['GRID_COLOR']};
}}

@font-face {{
    font-family: '{fonts['title_font_name']}';
    src: url('{fonts['title_font_path']}');
}}

@font-face {{
    font-family: '{fonts['main_font_name']}';
    src: url('{fonts['main_font_path']}');
}}

body {{
    font-family: '{fonts['main_font_name']}', sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
}}

h1 {{
    font-family: '{fonts['title_font_name']}', sans-serif;
}}

h2 {{
    font-family: '{fonts['title_font_name']}', sans-serif;
}}
"""

with open('style/theme.css', 'w', encoding='utf-8') as f:
    f.write(css_content)

print("theme.css was generated successfully!")