import test from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)))

test('the package surface passes the local DSH-Store preflight', () => {
  const out = execFileSync(process.execPath, [join(ROOT, 'scripts/preflight-package.mjs'), '--json'], { cwd: ROOT, encoding: 'utf8' })
  const report = JSON.parse(out)
  assert.deepEqual(report.issues, [])
  assert.ok(report.files > 0)
})
