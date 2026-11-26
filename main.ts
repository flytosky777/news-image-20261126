// News-image entry for make.fun (Node 22, standard library only).
// The image is the entry.png beside this file; the program copies it to
// /output/entry.png (or $MAKEFUN_OUTPUT_DIR), unchanged, every run.
//
// Run it outside the grader with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFile, mkdir, readFile, stat } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_MIB = 1048576;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const JPEG_MAGIC = Buffer.from([0xff, 0xd8, 0xff]);

async function run() {
  const repoDir = path.dirname(fileURLToPath(import.meta.url));
  const source = path.join(repoDir, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = path.join(outDir, "entry.png");

  const info = await stat(source);
  if (info.size > ONE_MIB) {
    throw new Error(`entry.png is ${info.size} bytes, over the 1 MiB cap`);
  }
  const bytes = await readFile(source);
  const isPng = bytes.subarray(0, 8).equals(PNG_MAGIC);
  const isJpeg = bytes.subarray(0, 3).equals(JPEG_MAGIC);
  if (!isPng && !isJpeg) {
    throw new Error("entry.png is neither a PNG nor a JPEG");
  }
  if (isPng) {
    // PNG IHDR: width and height are big-endian uint32 at bytes 16 and 20.
    const width = bytes.readUInt32BE(16);
    const height = bytes.readUInt32BE(20);
    if (width > 1024 || height > 1024) {
      throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
    }
  }
  await mkdir(outDir, { recursive: true });
  await copyFile(source, target);
  const written = await readFile(target);
  if (written.length !== info.size) {
    throw new Error(`copied ${written.length} bytes, expected ${info.size}`);
  }
  const digest = createHash("sha256").update(written).digest("hex");
  console.log(`wrote ${target} (${info.size} bytes) sha256 ${digest}`);
}

await run();
