#!/usr/bin/env node
/**
 * Planning estimate for a Science Legion campaign.
 *
 * It scales the measured six-agent pilot linearly per agent and adds a coordination
 * overhead. That is a planning number, not a quote: coordination, retries, and
 * verification can grow faster than linearly. Never use it as proof a large run fits.
 */
import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'

const args = process.argv.slice(2)
function option(name, fallback) {
  const i = args.indexOf(name)
  if (i === -1) return fallback
  const v = args[i + 1]
  if (v === undefined) throw new Error(`${name} needs a value`)
  return v
}
function numberOption(name, fallback) {
  const v = Number(option(name, fallback))
  if (!Number.isFinite(v)) throw new Error(`${name} must be a finite number`)
  return v
}

const json = args.includes('--json')
const agents = Math.floor(numberOption('--agents', 6))
const coordination = numberOption('--coordination', agents > 6 ? 0.25 : 0)
if (agents < 1 || agents > 1000) throw new Error('--agents must be between 1 and 1000')
if (coordination < 0 || coordination > 2) throw new Error('--coordination must be between 0 and 2')

const pilotPath = new URL('../evals/pilot-fourth-order/COST.json', import.meta.url)
const pilot = JSON.parse(await readFile(pilotPath, 'utf8'))
const pilotAgents = Number(pilot.agents)
const scale = agents / pilotAgents
const factor = scale * (1 + coordination)
const tokens = {
  cacheRead: Math.round(Number(pilot.tokens.cacheRead) * factor),
  uncachedInput: Math.round(Number(pilot.tokens.input) * factor),
  output: Math.round(Number(pilot.tokens.output) * factor),
}
const costCny = Number(pilot.costCny) * factor
const perAgent = {
  cacheRead: Math.round(Number(pilot.tokens.cacheRead) / pilotAgents),
  uncachedInput: Math.round(Number(pilot.tokens.input) / pilotAgents),
  output: Math.round(Number(pilot.tokens.output) / pilotAgents),
  costCny: Number(pilot.costCny) / pilotAgents,
}
const result = {
  source: 'linear scaling of the measured six-agent pilot; planning estimate only',
  pilot: { agents: pilotAgents, costCny: pilot.costCny },
  request: { agents, coordination },
  perAgent,
  estimate: { tokens, costCny, costPerAgentCny: costCny / agents },
  warnings: [
    'Coordination and verification can grow faster than linearly.',
    agents >= 96 ? 'At 96+ agents, measure a smaller tier first and set a hard cap.' : 'Start at the smallest tier that can answer the question.',
    'This is not a provider quote; peak/idle pricing and retries change the bill.',
  ],
}
if (json) {
  console.log(JSON.stringify(result, null, 2))
} else {
  console.log(`Science Legion planning estimate — ${agents} agents, coordination +${(coordination * 100).toFixed(0)}%`)
  console.log(`  cache-read input: ${result.estimate.tokens.cacheRead.toLocaleString()}`)
  console.log(`  uncached input:   ${result.estimate.tokens.uncachedInput.toLocaleString()}`)
  console.log(`  output:           ${result.estimate.tokens.output.toLocaleString()}`)
  console.log(`  cost:             ¥${result.estimate.costCny.toFixed(2)}`)
  console.log(`  per agent:        ¥${result.estimate.costPerAgentCny.toFixed(4)}`)
  console.log('')
  for (const warning of result.warnings) console.log(`  ! ${warning}`)
}
