<script lang="ts" setup>
import { onMounted } from 'vue'
import { useCharacterStore } from '../character.store'
import DiceRoller from '@/components/DiceRoller.vue'

const props = defineProps({ id: String })
const characterStore = useCharacterStore()
const webhook = "https://discord.com/api/webhooks/1128793925461737742/6ecKxmLAYFcNapF_sjA32Uq14zU_ScPIrYEJIftDWYGuUDb7tG4W50pbhmKvofKxVsDW"

onMounted(async () => {
  await characterStore.getCharacter(props.id)
})
</script>

<template>
  <div v-if="characterStore.error">{{ characterStore.error }}</div>
  <div class="col-md-6 offset-md-3" v-else-if="characterStore.character" style="padding-bottom: 1em;">
    <h1>{{ characterStore.character.character_name }}</h1>
    <ul class="list-group border rounded-0">
      <li class="list-group-item border-0 pt-2 pb-0">Race: <span class="fw-semibold">{{ characterStore.character.race }}</span></li>
      <li class="list-group-item border-0 py-0">Gender: <span class="fw-semibold">{{ characterStore.character.gender }}</span></li>
      <li class="list-group-item border-0 py-0">Charisma: <span class="fw-semibold">{{ characterStore.character.charisma }}</span></li>
      <li class="list-group-item border-0 py-0">Pace: <span class="fw-semibold">{{ characterStore.character.pace }}</span></li>
      <li class="list-group-item border-0 py-0">Parry: <span class="fw-semibold">{{ characterStore.character.parry }}</span></li>
      <li class="list-group-item border-0 py-0">Toughness: <span class="fw-semibold">{{ characterStore.character.toughness }}</span></li>
      <li class="list-group-item border-0 py-0">Attributes:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="(value, key) in characterStore.character.attributes" :key="key">{{ key }}: <span class="fw-semibold">{{ value }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Skills:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="(value, key) in characterStore.character.skills" :key="key">{{ key }}: <span class="fw-semibold">{{ value }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Hindrances:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="hindrance in characterStore.character.hindrances.split(',')" :key="hindrance">{{ hindrance.trim() }}</li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Edges:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="edge in characterStore.character.edges.split(',')" :key="edge">{{ edge.trim() }}</li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Damage:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="(value, key) in characterStore.character.damage" :key="key">{{ key }}: <span class="fw-semibold">{{ value }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Powers:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="power in characterStore.character.powers" :key="power.name">{{ power.name }}</li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Weapons:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="weapon in characterStore.character.weapons" :key="weapon.name"><span class="fw-semibold">{{ weapon.name }}</span> Damage: <span class="fw-semibold">{{ weapon.damage }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Gear:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="gear in characterStore.character.gear" :key="gear.name"><span class="fw-semibold">{{ gear.name }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Ammo: <span class="fw-semibold">{{ characterStore.character.ammo }}</span></li>
      <li class="list-group-item border-0 pt-0 pb-2">Money: <span class="fw-semibold">{{ characterStore.character.money }}</span></li>
    </ul>
  </div>
  <div v-else>
    <p>Loading Character...</p>
  </div>
  <DiceRoller :webhook="webhook" />
</template>
