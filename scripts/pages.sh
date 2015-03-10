echo + [$(date "+%Y-%m-%d-%Hh%Mm%Ss")] $(pdfinfo swiatlow_thesis.pdf | grep Pages | tr -d "Pages: ") $(texcount -sum -total -merge swiatlow_thesis.tex  | grep "Sum count:" | tr -d "Sum count: ") >> pages.md
python scripts/plot_pages.py

