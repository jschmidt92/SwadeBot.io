<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth.store'

import d4 from '@/assets/d4.png'
import d6 from '@/assets/d6.png'
import d8 from '@/assets/d8.png'
import d10 from '@/assets/d10.png'
import d12 from '@/assets/d12.png'
import d20 from '@/assets/d20.png'

const authStore = useAuthStore()

let timer: number | null = null

const startTimer = () => {
  timer = window.setTimeout(hideDice, 1000)
}

const checkHoldTime = () => {
  if (timer) {
    window.clearTimeout(timer)
    timer = null
  }
}


const hideDice = (event: MouseEvent) => {
  event.preventDefault()
  showDice.value = false
}

const diceOptions = [
  { value: 20, icon: d20 },
  { value: 12, icon: d12 },
  { value: 10, icon: d10 },
  { value: 8, icon: d8 },
  { value: 6, icon: d6 },
  { value: 4, icon: d4 }
]

const getUsername = async () => {
  const username = await authStore.getUsername()
  return username
}

const selectedDice = reactive<Record<number, number>>({})
const results = ref<Array<{ dice: string; result: string }>>([])
const result = ref<number | null>(null)
const showDice = ref(false)

const selectDice = (dice: any) => {
  if (selectedDice[dice.value]) {
    selectedDice[dice.value]++
  } else {
    selectedDice[dice.value] = 1
  }
}

const deselectDice = (dice: any, event: MouseEvent) => {
  event.preventDefault()
  if (selectedDice[dice.value]) {
    selectedDice[dice.value]--
  }
}

const props = defineProps<{ webhook: string }>()

const DISCORD_WEBHOOK_URL = props.webhook

function capitalizeWords(str: string) {
  return str.split(' ').map(word => 
    word.split('.').map(capitalize).join('.')
  ).join(' ')
}

function capitalize(str: string) {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

const sendRollResultsToDiscord = async () => {
  const discordId = localStorage.getItem('discordId')

  if (!discordId) {
    console.error('No Discord ID found in local storage.')
    return
  }

  const rollResults = results.value.map(roll => `${roll.dice}(${roll.result})`).join(', ')
  const rollTotal = result.value

  const username = await getUsername()
  const capitalizedUsername = username ? capitalizeWords(username) : 'unknown user'

  const payload = {
    content: `Player ${capitalizedUsername} rolled ${rollResults} for a total of ${rollTotal}.`,
  }

  const response = await fetch(DISCORD_WEBHOOK_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    console.error('Failed to send message to Discord:', response)
  }
}

const rollDice = () => {
  results.value = []
  result.value = null
  showDice.value = true

  let total = 0
  let diceResults: Record<string, number[]> = {}

  for (const [diceValue, count] of Object.entries(selectedDice)) {
    if (count > 0) {
      const sides = Number(diceValue)
      diceResults[sides] = []
      for (let i = 0; i < count; i++) {
        const roll = Math.floor(Math.random() * sides) + 1
        diceResults[sides].push(roll)
        total += roll
      }
    }
  }

  for (const [diceValue, rolls] of Object.entries(diceResults)) {
    if (rolls.length > 0) {
      results.value.push({ dice: `${rolls.length}d${diceValue}`, result: rolls.join(', ') })
    }
  }

  result.value = total

  for (const diceValue in selectedDice) {
    selectedDice[diceValue] = 0
  }

  if (result.value > 0) {
    sendRollResultsToDiscord()
    showDice.value = false
  }
}

</script>

<template>
  <div class="dice-roller position-fixed bottom-0 start-0 w-100 p-2">
    <div class="row" v-if="showDice">
      <div class="col-md-1">
        <div class="position-relative mb-1" role="button" v-for="dice in diceOptions" :key="dice.value">
          <img class="img img-fluid bg-dark rounded-circle" :src="dice.icon" @mousedown="startTimer" @mouseup="checkHoldTime" @click="selectDice(dice)" @contextmenu="deselectDice(dice, $event)" style="width: 4em; height: 4em" />
          <p class="position-absolute top-0 text-danger fs-4 badge">{{selectedDice[dice.value] || 0}}</p>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-1">
        <div class="d-grid gap-2">
          <button class="btn btn-dark rounded-circle bg-danger" @contextmenu.prevent="hideDice" @click="rollDice" style="width: 4em; height: 4em;">Roll</button>
        </div>
      </div>
    </div>
    <div class="row">
      <div class="col-md-2">
        <p class="h6 mb-0" v-if="results.length">Results: <span class="fs-5">{{ results.map(roll => `${roll.dice}(${roll.result})`).join(', ') }}</span></p>
        <p class="h6 mt-0" v-if="result !== null && result !== 0">Total: <span class="fs-5">{{ result }}</span></p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dice-roller {
  width: 200px;
}

.badge {
  font-size: 0.75em;
  padding: 0.25em;
}
</style>
