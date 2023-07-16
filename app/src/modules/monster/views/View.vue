<script lang="ts" setup>
import { onMounted } from 'vue'
import { useMonsterStore } from '../monster.store'
import DiceRoller from '@/components/DiceRoller.vue'

const props = defineProps({ id: String })
const monsterStore = useMonsterStore()
const webhook = "https://discord.com/api/webhooks/1128793925461737742/6ecKxmLAYFcNapF_sjA32Uq14zU_ScPIrYEJIftDWYGuUDb7tG4W50pbhmKvofKxVsDW"

onMounted(async () => {
  await monsterStore.getMonster(props.id)
})
</script>

<template>
  <div v-if="monsterStore.error">{{ monsterStore.error }}</div>
  <div class="col-6 offset-md-3" v-else-if="monsterStore.monster" style="padding-bottom: 1em;">
    <h1>{{ monsterStore.monster.monster_name }}</h1>
    <ul class="list-group border rounded-0">
      <li class="list-group-item border-0 pt-2 pb-0">Race: <span class="fw-semibold">{{ monsterStore.monster.race }}</span></li>
      <li class="list-group-item border-0 py-0">Gender: <span class="fw-semibold">{{ monsterStore.monster.gender }}</span></li>
      <li class="list-group-item border-0 py-0">Charisma: <span class="fw-semibold">{{ monsterStore.monster.charisma }}</span></li>
      <li class="list-group-item border-0 py-0">Pace: <span class="fw-semibold">{{ monsterStore.monster.pace }}</span></li>
      <li class="list-group-item border-0 py-0">Parry: <span class="fw-semibold">{{ monsterStore.monster.parry }}</span></li>
      <li class="list-group-item border-0 py-0">Toughness: <span class="fw-semibold">{{ monsterStore.monster.toughness }}</span></li>
      <li class="list-group-item border-0 py-0">Attributes:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="(value, key) in monsterStore.monster.attributes" :key="key">{{ key }}: <span class="fw-semibold">{{ value }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Skills:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="(value, key) in monsterStore.monster.skills" :key="key">{{ key }}: <span class="fw-semibold">{{ value }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Hindrances:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="hindrance in monsterStore.monster.hindrances.split(',')" :key="hindrance">{{ hindrance.trim() }}</li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Edges:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="edge in monsterStore.monster.edges.split(',')" :key="edge">{{ edge.trim() }}</li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Damage:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="(value, key) in monsterStore.monster.damage" :key="key">{{ key }}: <span class="fw-semibold">{{ value }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Powers:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="power in monsterStore.monster.powers" :key="power.name">{{ power.name }}</li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Weapons:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="weapon in monsterStore.monster.weapons" :key="weapon.name"><span class="fw-semibold">{{ weapon.name }}</span> Damage: <span class="fw-semibold">{{ weapon.damage }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Gear:
        <ul>
          <li class="list-group-item border-0 py-0" v-for="gear in monsterStore.monster.gear" :key="gear.name"><span class="fw-semibold">{{ gear.name }}</span></li>
        </ul>
      </li>
      <li class="list-group-item border-0 py-0">Ammo: <span class="fw-semibold">{{ monsterStore.monster.ammo }}</span></li>
      <li class="list-group-item border-0 pt-0 pb-2">Money: <span class="fw-semibold">{{ monsterStore.monster.money }}</span></li>
    </ul>
  </div>
  <div v-else>
    <p>Loading Monster...</p>
  </div>
  <DiceRoller :webhook="webhook" />
</template>
../monster.store