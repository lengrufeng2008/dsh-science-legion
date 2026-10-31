import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile, readdir } from 'node:fs/promises'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { apply, name, inject } from '../plugin/index.js'

const ROOT = dirname(dirname(fileURLToPath(import.meta.url)))
const MANIFEST = JSON.parse(await readFile(join(ROOT, 'manifest.json'), 'utf8'))

function frontmatter(text) {
  const match = text.match(/^---\n([\s\S]*?)\n---\n/)
  return match ? match[1] : ''
}

test('manifest is complete and every skill file exists', async () => {
  assert.equal(name, 'science-legion')
  assert.deepEqual(inject, ['skills'])
  assert.equal(MANIFEST.length, 8)
  assert.equal(new Set(MANIFEST.map((entry) => entry.name)).size, 8)
  for (const entry of MANIFEST) {
    assert.ok(entry.name && entry.dir && entry.description, entry.name)
    const text = await readFile(join(ROOT, 'skills', entry.dir, 'SKILL.md'), 'utf8')
    assert.match(frontmatter(text), new RegExp(`^name: ${entry.name}$`, 'm'))
    assert.ok(text.includes('#'), `${entry.name} has a body`)
  }
})

test('registers a six-skill provider and resolves content without frontmatter', async () => {
  let factory
  apply({ skills: { registerProvider(fn) { factory = fn } } })
  assert.equal(typeof factory, 'function')
  const provider = factory()
  assert.equal(provider.name, 'dsh-science-legion')
  const list = await provider.list()
  assert.equal(list.length, 8)
  assert.ok(list.every((entry) => entry.source === 'bundled' && entry.provider === 'dsh-science-legion'))
  assert.ok(list.every((entry) => entry.invocation.modelInvocable && entry.invocation.userInvocable))
  const math = await provider.get({ name: 'math-research' })
  assert.equal(math.name, 'math-research')
  assert.ok(math.content.trimStart().startsWith('# Mathematical research'))
  assert.ok(!math.content.startsWith('---'))
  assert.equal(await provider.get({ name: 'missing' }), undefined)
})

test('the doctrine carries tiers, verification, and budget gates', async () => {
  const legion = await readFile(join(ROOT, 'skills', 'legion-command', 'SKILL.md'), 'utf8')
  assert.match(legion, /Squad/)
  assert.match(legion, /Platoon/)
  assert.match(legion, /Company/)
  assert.match(legion, /Legion/)
  assert.match(legion, /Never start at Legion/)
  assert.match(legion, /Wolf pack/)
  assert.match(legion, /Flanking/)
  assert.match(legion, /Pincer/)
  assert.match(legion, /Retreat/)
  assert.match(legion, /COST\.json/)
  assert.match(legion, /token budget/i)
  assert.match(legion, /Verifier/)
  const router = await readFile(join(ROOT, 'skills', 'science-legion', 'SKILL.md'), 'utf8')
  assert.match(router, /math-research/)
  assert.match(router, /physics-research/)
  assert.match(router, /astronomy-research/)
  assert.match(router, /science-verify/)
  assert.match(router, /engineering-research/)
  assert.match(router, /biomedical-research/)
})

test('known-answer evals are present and never claim an open problem', async () => {
  const evals = JSON.parse(await readFile(join(ROOT, 'evals', 'problems.json'), 'utf8'))
  assert.ok(evals.length >= 10)
  const pilot = await readFile(join(ROOT, 'evals', 'pilot-pendulum', 'check.py'), 'utf8')
  assert.match(pilot, /Route A/)
  const independent = await readFile(join(ROOT, 'evals', 'pilot-pendulum', 'independent.py'), 'utf8')
  assert.match(independent, /AGM-only/)
  const fourth = await readFile(join(ROOT, 'evals', 'pilot-fourth-order', 'README.md'), 'utf8')
  assert.match(fourth, /1\.066080729/)
  const ledger = JSON.parse(await readFile(join(ROOT, 'evals', 'pilot-fourth-order', 'COST.json'), 'utf8'))
  assert.equal(ledger.costCny, 1.45431996)
  assert.equal(ledger.agents, 6)
  for (const item of evals) {
    assert.ok(item.id && item.domain && item.prompt && item.expected && item.verify)
    assert.equal(item.expected.toLowerCase().includes('open problem'), false)
  }
  const dirs = await readdir(join(ROOT, 'skills'))
  assert.deepEqual(dirs.sort(), MANIFEST.map((entry) => entry.dir).sort())
})
