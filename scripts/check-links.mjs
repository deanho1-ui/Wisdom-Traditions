// Checks every external link in index.html and lists the ones that fail.
import { readFileSync } from "node:fs";

const html = readFileSync(new URL("../index.html", import.meta.url), "utf8");
const urls = [...new Set(html.match(/https:\/\/[^"'\s<>)\\]+/g))]
  .filter(u => !/fonts\.(googleapis|gstatic)\.com|github\.io/.test(u));

const failed = [];
for (const url of urls) {
  let status = 0;
  for (let attempt = 0; attempt < 2 && !(status >= 200 && status < 400); attempt++) {
    try {
      const res = await fetch(url, { redirect: "follow", headers: { "user-agent": "Mozilla/5.0 (link check)" }, signal: AbortSignal.timeout(20000) });
      status = res.status;
    } catch { status = 0; }
    if (!(status >= 200 && status < 400)) await new Promise(r => setTimeout(r, 1500));
  }
  if (!(status >= 200 && status < 400)) failed.push(`${status} ${url}`);
  await new Promise(r => setTimeout(r, 250));
}

console.log(`Checked ${urls.length} links, ${failed.length} failed.`);
for (const f of failed) console.log("FAILED " + f);
process.exit(failed.length ? 1 : 0);
