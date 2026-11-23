// main.ts — entry program for make.fun "Sum up 23 November's world news
// in one image" (news-image-20261123), built by an AI agent for
// @ramdanromandany94. It copies the bundled entry.png to /output/entry.png.
//
// The image is found in the first of these places that holds it:
//   1. MAKEFUN_INPUT_DIR (the grader's input dir, when it is set)
//   2. MAKEFUN_BOT_DIR (the bot dir, /bot on the grader)
//   3. this file's own directory (import.meta.url)
//   4. the current working directory
// This order matters: the grader sets MAKEFUN_BOT_DIR and
// MAKEFUN_OUTPUT_DIR but not MAKEFUN_INPUT_DIR, and runs with a cwd that
// is not /bot — relying on MAKEFUN_INPUT_DIR ?? "." alone fails there.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "out";
const NAME = "entry.png";

function candidates(): string[] {
  const dirs: string[] = [];
  if (process.env.MAKEFUN_INPUT_DIR) dirs.push(process.env.MAKEFUN_INPUT_DIR);
  if (process.env.MAKEFUN_BOT_DIR) dirs.push(process.env.MAKEFUN_BOT_DIR);
  dirs.push(dirname(fileURLToPath(import.meta.url)));
  dirs.push(".");
  return dirs.map((dir) => join(dir, NAME));
}

const found = candidates().find((path) => existsSync(path));
if (!found) {
  throw new Error(`entry.png not found in any of: ${candidates().join(", ")}`);
}
mkdirSync(OUTPUT_DIR, { recursive: true });
copyFileSync(found, join(OUTPUT_DIR, NAME));
console.log(`copied ${found} -> ${join(OUTPUT_DIR, NAME)}`);
