import markdown
from pathlib import Path

# Chemins
BASE_DIR = Path(__file__).resolve().parent
md_file = BASE_DIR / "markdown.md"
html_file = BASE_DIR / "markdown.html"

# Lecture du Markdown
with open(md_file, "r", encoding="utf-8") as f:
    md_content = f.read()

# Conversion Markdown -> HTML
html_content = markdown.markdown(
    md_content,
    extensions=["tables"]
)

# Écriture du HTML final
with open(html_file, "w", encoding="utf-8") as f:
    f.write(f"""
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>SAE 1.05</title>
</head>
<body>
{html_content}
</body>
</html>
""")

print("Fichier HTML généré avec succès.")
