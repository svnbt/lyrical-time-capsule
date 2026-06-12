import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Full page config
st.set_page_config(layout="wide", page_title="The Lyrical Time Capsule", initial_sidebar_state="collapsed")

# Hide sides and header
st.markdown("""
    <style>
        .block-container { padding: 0rem !important; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

# Encode images in Base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load HTML, CSS and images
try:
    # Load HTML
    with open("article.html", "r", encoding="utf-8") as f:
        html_content = f.read()


    # Load CSS
    with open("style/theme.css", "r", encoding="utf-8") as f:
        theme_css = f.read()
    with open("style/style.css", "r", encoding="utf-8") as f:
        style_css = f.read()
    with open("style/animation.css", "r", encoding="utf-8") as f:
        animation_css = f.read()

    # Load font
    akira_path = "style/fonts/akira.otf"
    if os.path.exists(akira_path):
        b64_akira = get_base64_of_bin_file(akira_path)
        
        theme_css = theme_css.replace(
            "url('fonts/akira.otf')", 
            f"url('data:font/otf;base64,{b64_akira}')"
        )

    # Inject CSS directly into HTML
    alte_theme_links = ['<link rel="stylesheet" href="theme.css">', '<link rel="stylesheet" href="style/theme.css">']
    alte_style_links = ['<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style/style.css">']
    alte_animation_links = ['<link rel="stylesheet" href="animation.css">', '<link rel="stylesheet" href="style/animation.css">']
    
    for link in alte_theme_links:
        html_content = html_content.replace(link, f'<style>{theme_css}</style>')
    for link in alte_style_links:
        html_content = html_content.replace(link, f'<style>{style_css}</style>')
    for link in alte_animation_links:
        html_content = html_content.replace(link, f'<style>{animation_css}</style>')


    # Link to prompts
    html_content = html_content.replace('href="prompts.html"', 'href="Prompts" target="_parent"')
    html_content = html_content.replace('target="_blank" target="_parent"', 'target="_parent"')

    # Convert images to Base64 and replace in HTML
    charts = ["chart1.png", "chart2.png", "chart3.png", "chart4.png"]
    for chart in charts:
        img_path = f"chartsPNG/{chart}"
        if os.path.exists(img_path):
            b64 = get_base64_of_bin_file(img_path)
            html_content = html_content.replace(f'src="chartsPNG/{chart}"', f'src="data:image/png;base64,{b64}"')

    # Show the finished HTML in streamlit
    components.html(html_content, height=900, scrolling=True)

except FileNotFoundError as e:
    st.error(f"Fehler beim Laden einer Datei: {e}. Bitte stelle sicher, dass alle drei CSS-Dateien im 'style'-Ordner liegen.")