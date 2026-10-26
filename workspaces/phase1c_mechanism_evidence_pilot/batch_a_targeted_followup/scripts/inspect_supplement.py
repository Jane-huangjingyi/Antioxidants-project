import io,json,pathlib,zipfile
from pypdf import PdfReader
ROOT=pathlib.Path(__file__).resolve().parents[1]
with zipfile.ZipFile(ROOT/'local_sources/HDAC1_EPMC_supplement.zip') as outer:
 data=outer.read('biology-15-00206-s001.zip')
with zipfile.ZipFile(io.BytesIO(data)) as inner:
 print('SUPPLEMENT_MEMBERS',[(i.filename,i.file_size) for i in inner.infolist()])
 entries=[]
 for i in inner.infolist():
  if i.is_dir():continue
  if i.file_size>15_000_000:continue
  # Extract individual byte payloads under a fixed local name, never trust archive paths.
  suffix=pathlib.PurePosixPath(i.filename).suffix
  p=ROOT/'local_sources'/('HDAC1_supplement_member_'+str(len(entries))+suffix)
  p.write_bytes(inner.read(i.filename))
  item={'member':i.filename,'local_path':'local_sources/'+p.name,'bytes':i.file_size}
  if suffix.lower()=='.pdf':
   reader=PdfReader(p);item['pages']=len(reader.pages)
   text='\n'.join('PDF_PAGE '+str(n+1)+'\n'+page.extract_text() for n,page in enumerate(reader.pages))
   (p.with_suffix('.txt')).write_text(text,encoding='utf-8')
   print('PDF_TEXT',text[:10000])
  entries.append(item)
(ROOT/'qc/HDAC1_Supplement_Inventory.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
