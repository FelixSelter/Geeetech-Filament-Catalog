import requests
from bs4 import BeautifulSoup
from pathlib import Path
import re

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

FIGURE_TEMPLATE = r"""
\begin{figure}[H]
    SUBFIGURES
\end{figure}
""".strip()

SUBFIGURE_TEMPLATE = r"""
\begin{minipage}{0.25\textwidth}
    \centering
    \includegraphics[keepaspectratio, width=\linewidth, height=3.5cm]{FILE_PATH}
    \caption*{CAPTION}
\end{minipage}\hfill
""".strip()

urls = {"pla": "https://www.geeetech.com/filament-pla-c-83_111.html",
        "petg": "https://www.geeetech.com/filament-petg-c-83_124.html",
        "pla-silk": "https://www.geeetech.com/filament-silksilk-dual-tricolor-c-83_113.html",
        "pla-matte": "https://www.geeetech.com/filament-matte-pla-c-83_142.html",
        "pla-woodmarble": "https://www.geeetech.com/filament-like-marble-wood-c-83_157.html",
        "pla-luminous": "https://www.geeetech.com/filament-luminous-pla-c-83_146.html",
        "pla-highspeed": "https://www.geeetech.com/filament-high-speed-pla-c-83_149.html",
        "asa": "https://www.geeetech.com/filament-asa-c-83_180.html",
        "abs": "https://www.geeetech.com/filament-abs-c-83_175.html",
        "tpu": "https://www.geeetech.com/filament-tpu-c-83_130.html"
        }

results = {}

for filament, url in urls.items():
    print(filament)
    html_doc = requests.get(url).text
    html = BeautifulSoup(html_doc, 'html.parser')

    for product in html.find_all("div", {"class": "products-list-item"}):
        img = product.find("img", {"class": "listingProductImage"})
        name = product.find(
            "div", {"class": "products-list-item-name"}).text.strip()

        if "Vacuum Bag" in name:
            continue

        print(f"\tName: {name}; Image: {img['src']}")
        img_response = requests.get(f"https://www.geeetech.com/{img['src']}")
        url_path = Path(img['src'])
        file_path = Path(
            re.sub(r'_+', '_', f"images/{filament}/{name.replace(' ', '_').replace('/', '_')}{url_path.suffix}"))
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(img_response.content)

        if filament not in results:
            results[filament] = []
        name = name.replace(' 3D printer Filament 1.75mm 1kg/roll', '')
        name = name.replace('  3D Printer Filament 1.75mm 1kg/roll', '')
        name = name.replace(' 3D Printer Filament 1.75mm 1kg/roll', '')
        name = name.replace(' 3D Printer Filament  1.75mm 1kg/roll', '')
        results[filament].append(SUBFIGURE_TEMPLATE.replace("FILE_PATH", str(file_path)).replace("CAPTION", name))

with open("template.tex", "r") as f:
    template = f.read()

    for filament, subfigures in results.items():
        figures = []
        for group in chunks(subfigures, 3):
            figures.append(FIGURE_TEMPLATE.replace("SUBFIGURES", "\n".join(group)))

        replacement = "\n\n".join(figures)
        marker = f"% TEMPLATE {filament}"

        if marker not in template:
            raise ValueError(f"Marker not found: {marker}")

        template = template.replace(marker, replacement, 1)

    with open("generated.tex", "w") as f:
        f.write(template)