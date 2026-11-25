// main.ts — entrypoint for the news-image-20261125 entry.
// The front page is drawn at build time by draw.py (Pillow) and shipped
// in this repository as entry.png. This program only copies that file
// into the grader's output directory, using the Node 22 standard
// library only: no network, no dependencies, byte-identical every run.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The repository root is the directory holding this file.
const here = dirname(fileURLToPath(import.meta.url));
const source = resolve(here, "entry.png");

// The grader sets MAKEFUN_OUTPUT_DIR; fall back to /output, then ./out.
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const target = join(outDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts: ${source}`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(source, target);

const bytes = statSync(target).size;
const sourceBytes = statSync(source).size;
if (bytes !== sourceBytes) {
  throw new Error(`copy mismatch: wrote ${bytes} bytes, source is ${sourceBytes}`);
}

// Byte-identical copy: the hash of what was written must match the source.
const digest = (path: string) =>
  createHash("sha256").update(readFileSync(path)).digest("hex");
const sourceHash = digest(source);
const targetHash = digest(target);
if (sourceHash !== targetHash) {
  throw new Error(`copy mismatch: sha256 ${targetHash} != ${sourceHash}`);
}

console.log(`wrote ${target} (${bytes} bytes, sha256 ${targetHash})`);
