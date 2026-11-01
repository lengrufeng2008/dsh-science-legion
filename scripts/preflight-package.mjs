#!/usr/bin/env node
// Local approximation of the DSH-Store package surface checks.
// It does not replace the store's security review; it catches unsupported artifacts early.
import { readFile, stat, readdir } from 'node:fs/promises'
import { join, relative, basename } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = fileURLToPath(new URL('..', import.meta.url))
const pkg = JSON.parse(await readFile(join(ROOT, 'package.json'), 'utf8'))
const issues = []
const files = new Set(['package.json'])
const allowed = /\.(?:[cm]?[jt]sx?|mmd|jsonl?|ya?ml|sh|bash|py|html?|vue|svelte|md|txt|rst|png|jpe?g|webp|gif|ico|svg|css|woff2?|ttf|otf|map|webmanifest|xml)$|(?:^|\/)(?:licen[cs]e|readme|copying|notice)(?:\.[^/]*)?$/i

async function walk(path) {
  const info = await stat(path)
  if (info.isFile()) { files.add(relative(ROOT, path).split('\\').join('/')); return }
  for (const entry of await readdir(path, { withFileTypes: true })) {
    const child = join(path, entry.name)
    if (entry.isDirectory()) await walk(child)
    else files.add(relative(ROOT, child).split('\\').join('/'))
  }
}

for (const entry of pkg.files ?? []) {
  if (entry.includes('*')) {
    const folder = join(ROOT, entry.slice(0, entry.lastIndexOf('/')))
    const suffix = entry.slice(entry.lastIndexOf('*') + 1)
    for (const name of await readdir(folder)) {
      if (name.endsWith(suffix)) files.add(relative(ROOT, join(folder, name)).split('\\').join('/'))
    }
  } else {
    await walk(join(ROOT, entry))
  }
}

for (const file of [...files].sort()) {
  if (!allowed.test(file)) issues.push(`unsupported artifact: ${file}`)
  const info = await stat(join(ROOT, file))
  if (info.size > 4 * 1024 * 1024) issues.push(`file over 4 MiB: ${file}`)
}
const total = (await Promise.all([...files].map(file => stat(join(ROOT, file))))).reduce((sum, info) => sum + info.size, 0)
if (total > 8 * 1024 * 1024) issues.push(`package surface over 8 MiB: ${total} bytes`)
if (files.size > 512) issues.push(`too many files: ${files.size}`)
for (const script of ['preinstall', 'install', 'postinstall', 'prepare']) {
  if (pkg.scripts?.[script]) issues.push(`lifecycle script present: ${script}`)
}
if (!pkg.license) issues.push('package.json has no license')
if (!pkg.dsh?.bundle?.patch) issues.push('package.json has no dsh.bundle.patch')
else {
  try { await stat(join(ROOT, pkg.dsh.bundle.patch)) } catch { issues.push(`missing bundle patch: ${pkg.dsh.bundle.patch}`) }
}
const report = { files: files.size, totalBytes: total, issues }
if (process.argv.includes('--json')) console.log(JSON.stringify(report, null, 2))
else {
  console.log(`package preflight: ${files.size} files, ${total} bytes`)
  for (const issue of issues) console.log(`  ! ${issue}`)
  if (!issues.length) console.log('  ok')
}
process.exitCode = issues.length ? 1 : 0
