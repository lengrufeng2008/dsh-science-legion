import test from 'node:test'
import assert from 'node:assert/strict'
import { execFileSync } from 'node:child_process'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)))
const SCRIPT = join(ROOT, 'scripts', 'estimate-campaign.mjs')

function estimate(args) {
  const out = execFileSync(process.execPath, [SCRIPT, ...args, '--json'], { encoding: 'utf8' })
  return JSON.parse(out)
}

test('six-agent estimate reproduces the measured pilot cost', () => {
  const result = estimate(['--agents', '6'])
  assert.equal(result.request.coordination, 0)
  assert.equal(result.estimate.costCny, 1.45431996)
})

test('larger tiers add an explicit coordination overhead and warnings', () => {
  const result = estimate(['--agents', '24'])
  assert.equal(result.request.coordination, 0.25)
  assert.ok(result.estimate.costCny > result.pilot.costCny * 4)
  assert.ok(result.warnings.some((line) => line.includes('Coordination')))
})

test('rejects impossible agent counts', () => {
  assert.throws(() => estimate(['--agents', '0']))
  assert.throws(() => estimate(['--agents', '1001']))
})
