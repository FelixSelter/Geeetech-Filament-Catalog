# Geeetech Filament Catalog

This project generates a **printable PDF catalog** of Geeetech 3D printer filaments.  
The catalog focuses on **minimal information**: just the filament names and images, so others can easily browse and choose what they want.

The catalog is intended to help you **show available filaments** to friends, clients, or colleagues. They can then select a filament for you to buy and print their file.

The catalog is automatically refreshed **every month** using GitHub Actions, ensuring it stays up-to-date with Geeetech's inventory.

---

## Requirements

- Python 3.12+ (previous versions will most likely also work)
- Python packages:
  - `requests`
  - `beautifulsoup4`
- LaTeX installation (TeX Live recommended with `latex-extra` packages)
- GitHub Actions (for automatic monthly refresh)

---

## Usage

#### 1. Clone the repository:

```bash
git clone https://https://github.com/FelixSelter/Geeetech-Filament-Catalog.git
cd Geeetech-Filament-Catalog
```

#### 2. Install Python dependencies:
```bash
pip install requests beautifulsoup4
```

#### 3. Run the script:
```bash
python main.py
```

#### 4. Compile the LaTeX document:
```bash
pdflatex -interaction=nonstopmode generated.tex
```

#### 5. Open generated.pdf to view the catalog.

## License

This project is for personal use and internal demonstration purposes.
All filament images and information are property of [Geeetech](https://www.geeetech.com/)