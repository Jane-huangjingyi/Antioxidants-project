import fs from "node:fs/promises";
import path from "node:path";
import {createRequire} from "node:module";
import {fileURLToPath, pathToFileURL} from "node:url";
const home = path.dirname(fileURLToPath(import.meta.url));
const out = process.argv[2] || home;
let pkg = "@oai/artifact-tool";
if (process.env.CODEX_SPREADSHEET_MODULES) {
  const resolver = createRequire(path.join(process.env.CODEX_SPREADSHEET_MODULES, "..", "resolver.cjs"));
  pkg = pathToFileURL(resolver.resolve(pkg)).href;
}
const {Workbook, SpreadsheetFile} = await import(pkg);
const book = await Workbook.fromCSV(await fs.readFile(path.join(out,"Table1.csv"), "utf8"), {sheetName:"Candidate priorities"});
const sheet = book.worksheets.getItemAt(0);
const full = sheet.getUsedRange();
sheet.showGridLines = false;
sheet.freezePanes.freezeRows(1);
const header = sheet.getRange("A1:Q1");
header.format.fill = "#174369";
header.format.font.color = "#FFFFFF";
header.format.font.bold = true;
full.format.wrapText = true;
header.format.rowHeight = 32;
full.format.columnWidth = 24;
for (const col of ["E","M","N","P"]) sheet.getRange(col+"1:"+col+"25").format.columnWidth = 43;
for (const col of ["H", "K"]) {
  const range = sheet.getRange(col+"2:"+col+"25");
  range.values = range.values.map(([v]) => [v === null || v === "" ? null : Number(v)]);
}
sheet.getRange("A2:Q25").format.rowHeight = 52;
const file = await SpreadsheetFile.exportXlsx(book);
await file.save(path.join(out, "Table1.xlsx"));
const diagnostic = path.join(out, "Table1.xlsx.inspect.ndjson");
try {
  await fs.copyFile(diagnostic, path.resolve(home, "../../download_raw/Results1_Table1.inspect.ndjson"));
  await fs.unlink(diagnostic);
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
const preview = await book.render({sheetName:sheet.name, range:"A1:F7", format:"png"});
await fs.writeFile(path.resolve(home, "../../download_raw/Results1_Table1_preview.png"), new Uint8Array(await preview.arrayBuffer()));
