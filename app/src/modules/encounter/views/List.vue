<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useEncounterStore } from '../encounter.store'

const encounterStore = useEncounterStore()
const encounters = ref<{ id: number; name: string; }[]>([])

onMounted(async () => {
  await encounterStore.getEncounters()
  encounters.value = encounterStore.encounters
})
</script>

<template>
  <div class="col-md-6 offset-md-3">
    <template v-if="encounters.length">
      <div class="row">
        <div class="col-md-12">
          <ul class="list-group">
            <li class="list-group-item" v-for="encounter in encounters" :key="encounter.id">
              <router-link :to="{ name: 'EncounterDetails', params: { id: encounter.id} }" :name="encounter.name">{{ encounter.name }}</router-link>
            </li>
          </ul>
        </div>
      </div>
    </template>
    <p v-else>Loading Encounters...</p>
  </div>
</template>
