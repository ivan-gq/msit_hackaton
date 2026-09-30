import pyfiglet

text = "Python"

for font in pyfiglet.FigletFont.getFonts()[:5]:  # Preview first 5 fonts
    print(f"--- Font: {font} ---")
    print(pyfiglet.figlet_format(text, font=font))