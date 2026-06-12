from prompts_data import PROMPTS

cards_html = ""
for item in PROMPTS:
    cards_html += f"""
            <div class="prompt-card">
                <p class="prompt-text">{item['text']}</p>
            </div>
    """

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Prompt Log - The Lyrical Time Capsule</title>
    
    <link rel="stylesheet" href="style/theme.css">
    <link rel="stylesheet" href="style/style.css">
    <link rel="stylesheet" href="style/prompts.css">
</head>
<body>
    <article>
        <a href="article.html" class="nav-link">← Back to the Article</a>
        <header>
            <h1>Prompt Log</h1>
            <p class="subtitle">A transparent record of the human-AI collaboration behind this project.</p>
        </header>
        <p>In the interest of full transparency, below is a curated log of the actual prompts used to guide the Artificial Intelligence during the creation of this project.</p>
        
        <div class="prompt-list">
{cards_html}
        </div>

        <footer>
            <hr>
            <p>
                © 2026 Sven Betschart. An interactive data storytelling project.
            </p>
        </footer>
    </article>
</body>
</html>
"""

with open('prompts.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("prompts.html successfully generated from prompts.json!")