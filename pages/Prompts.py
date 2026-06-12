import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(layout="wide", page_title="AI Prompt Log", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        .block-container { padding: 0rem !important; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

try:
    with open("prompts.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    with open("style/theme.css", "r", encoding="utf-8") as f:
        theme_css = f.read()
    with open("style/style.css", "r", encoding="utf-8") as f:
        style_css = f.read()
        
    prompts_css = ""
    if os.path.exists("style/prompts.css"):
        with open("style/prompts.css", "r", encoding="utf-8") as f:
            prompts_css = f.read()
            
    import base64
    def get_base64_of_bin_file(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
        
    akira_path = "style/fonts/akira.otf"
    if os.path.exists(akira_path):
        b64_akira = get_base64_of_bin_file(akira_path)
        theme_css = theme_css.replace("url('fonts/akira.otf')", f"url('data:font/otf;base64,{b64_akira}')")
        theme_css = theme_css.replace("url(fonts/akira.otf)", f"url('data:font/otf;base64,{b64_akira}')")

    links_theme = ['<link rel="stylesheet" href="theme.css">', '<link rel="stylesheet" href="style/theme.css">']
    links_style = ['<link rel="stylesheet" href="style.css">', '<link rel="stylesheet" href="style/style.css">']
    links_prompts = ['<link rel="stylesheet" href="prompts.css">', '<link rel="stylesheet" href="style/prompts.css">']

    for link in links_theme:
        html_content = html_content.replace(link, f'<style>{theme_css}</style>')
    for link in links_style:
        html_content = html_content.replace(link, f'<style>{style_css}</style>')
    if prompts_css:
        for link in links_prompts:
            html_content = html_content.replace(link, f'<style>{prompts_css}</style>')

    html_content = html_content.replace('href="article.html"', 'href="/" target="_parent"')

    components.html(html_content, height=900, scrolling=True)

except FileNotFoundError as e:
    st.error(f"Fehler beim Laden einer Datei: {e}. Bitte checke, ob die Pfade stimmen.")