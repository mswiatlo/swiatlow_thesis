echo + [$(date "+%Y-%m-%d-%Hh%Mm%Ss")] $(pdfinfo swiatlow_thesis.pdf | grep Pages | tr -d "Pages: ") >> pages.md
python scripts/plot_pages.py

