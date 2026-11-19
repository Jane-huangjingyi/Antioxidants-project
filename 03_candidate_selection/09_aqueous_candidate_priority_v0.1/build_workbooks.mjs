import fs from "node:fs/promises";
import {createRequire} from "node:module";
import path from "node:path";
import {fileURLToPath,pathToFileURL} from "node:url";

const folder = path.dirname(fileURLToPath(import.meta.url));
const packageName = "@oai/artifact-tool";
let entry = packageName;
if (process.env.CODEX_SPREADSHEET_MODULES) {
  const require = createRequire(path.join(process.env.CODEX_SPREADSHEET_MODULES, "..", "resolver.cjs"));
  entry = pathToFileURL(require.resolve(packageName)).href;
}
const {Workbook, SpreadsheetFile} = await import(entry);
const local = path.resolve(folder, "..", "..", "download_raw");
const data = JSON.parse(await fs.readFile(path.join(local, "antioxidants_priority_v01.json"), "utf8"));
function add(book, name, records) {
  const sheet = book.worksheets.add(name);
  sheet.showGridLines = false;
  const keys = Object.keys(records[0]);
  const values = [keys.map(key => key.replaceAll("_", " ")), ...records.map(row => keys.map(key => row[key] ?? null))];
  const full = sheet.getRangeByIndexes(0, 0, values.length, keys.length);
  full.values = values;
  full.format.font.name = "Calibri";
  full.format.font.size = 11;
  const header = sheet.getRangeByIndexes(0, 0, 1, keys.length);
  header.format.fill = "#174369";
  header.format.font.color = "#FFFFFF";
  header.format.font.bold = true;
  header.format.wrapText = true;
  header.format.rowHeight = 35;
  for (const [index, key] of keys.entries()) {
    const column = sheet.getRangeByIndexes(0, index, values.length, 1);
    const verbose = /source_DOIs|locator|unresolved|rationale|gate|interpretation|protocol|disposition|food_occurrence/.test(key);
    column.format.columnWidth = verbose ? 42 : /compound|unit|material|status|doi|source|quality|inchi|scope/i.test(key) ? 28 : 16;
    if (verbose) column.format.wrapText = true;
  }
  sheet.freezePanes.freezeRows(1);
  if (records.length < 80) sheet.getRangeByIndexes(1, 0, records.length, keys.length).format.rowHeight = 42;
  else sheet.getRangeByIndexes(1, 0, records.length, keys.length).format.rowHeight = 44;
}
async function emit(name, sheets) {
  const book = Workbook.create();
  for (const [sheetName, records] of sheets) add(book, sheetName, records);
  const file = await SpreadsheetFile.exportXlsx(book);
  await file.save(path.join(folder, name + ".xlsx"));
  for (const [sheetName] of sheets) {
    try {
      const preview = await book.render({sheetName, range: "A1:F5", scale: 1, format: "png"});
      await fs.writeFile(path.join(local, "antiox-" + sheetName + ".png"), new Uint8Array(await preview.arrayBuffer()));
    } catch (error) {
      console.warn("Preview unavailable for", sheetName, error.message);
    }
  }
}
await emit("Assay_Specific_Rankings", [
  ["Method coverage", data.methods], ["Comparison blocks", data.blocks],
  ["Within block ranks", data.rankings], ["Original observations", data.observations]
]);
await emit("Aqueous_Antioxidant_Candidate_Priority", [
  ["Candidate priority", data.panel],
  ["How to read", [
    {item:"A", meaning:"First to qualify experimentally after identity, food and bench gates"},
    {item:"B", meaning:"Explore after source or assay gate resolves"},
    {item:"C", meaning:"Defer while substantial interference or material barrier remains"},
    {item:"Queue position", meaning:"Work order for review, with no global efficacy score"},
    {item:"Prior FL position", meaning:"Historical diagnostic within 51-compound component, with no absorbance prediction"},
    {item:"DOI counts", meaning:"Distinct report counts. Independent experiment count awaits review"}
  ]]
]);
