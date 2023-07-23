<script lang="ts" setup>
import { onMounted } from 'vue'
import { useEncounterStore } from '../encounter.store'
import DiceRoller from '@/components/DiceRoller.vue'

const props = defineProps({ id: String })
const encounterStore = useEncounterStore()
const webhook = 'https://discord.com/api/webhooks/1129538520214683739/bYEVm_ar3DwJCqKrWn_pcvbTZleCXxZShbBghL6nkmRajbXiAfmoZljU3R5_silFtAcC'

onMounted(async () => {
  await encounterStore.getEncounter(props.id)
})
</script>

<template>
  <div v-if="encounterStore.error">{{ encounterStore.error }}</div>
  <div class="col-md-6 offset-md-3" v-else-if="encounterStore.encounter" style="padding-bottom: 1em;">
    <h1>{{ encounterStore.encounter.name }}</h1>
    <ul class="list-group border rounded-0">
      <li class="list-group-item border-0 py-0">Notes: <span class="fw-semibold">{{ encounterStore.encounter.notes }}</span></li>
    </ul>
  </div>
  <div v-else>
    <p>Loading Encounter...</p>
  </div>
  <DiceRoller :webhook="webhook" />
</template>
