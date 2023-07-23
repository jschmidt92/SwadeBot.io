<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useMonsterStore } from '../monster.store'
import MonsterCard from '@/components/CharacterCard.vue';

const monsterStore = useMonsterStore()
const monsters = ref<{ id: number; monster_name: string; }[]>([])

onMounted(async () => {
  await monsterStore.getMonsters()
  monsters.value = monsterStore.monsters
})
</script>

<template>
  <div class="col-md-6 offset-md-3">
    <template v-if="monsters.length">
      <div class="row">
        <div class="col-md-12" v-for="monster in monsters" :key="monster.id">
          <MonsterCard :to="{ name: 'MonsterDetails', params: { id: monster.id} }" :name="monster.monster_name" />
        </div>
      </div>
    </template>
    <p v-else>Loading Monsters...</p>
  </div>
</template>
../monster.store