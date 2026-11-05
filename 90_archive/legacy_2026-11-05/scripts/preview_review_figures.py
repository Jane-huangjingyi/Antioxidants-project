"""Temporary visual-QA thumbnails only; scientific outputs are all generated in R."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
root=Path(__file__).resolve().parents[1];dest=root/'workspaces/repository_review_20261030/previews';dest.mkdir(exist_ok=True)
files=sorted((root/'figures/editable').rglob('*.png'))
for start in range(0,len(files),9):
 canvas=Image.new('RGB',(1800,1350),'#dddddd');draw=ImageDraw.Draw(canvas)
 for i,p in enumerate(files[start:start+9]):
  im=Image.open(p).convert('RGB');im.thumbnail((590,410))
  x=(i%3)*600;y=(i//3)*450;canvas.paste(im,(x+(600-im.width)//2,y+25));draw.text((x+8,y+5),p.stem[:72],fill='black')
 canvas.save(dest/f'figures_contact_{start//9+1}.png')
print('QA contact sheets:',(len(files)+8)//9)
