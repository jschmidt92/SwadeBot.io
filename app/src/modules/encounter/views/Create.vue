<script setup lang="ts">
import { reactive, ref } from 'vue'
import BaseInput from '@/components/BaseInput.vue'
import { useEncounterStore, type EncounterCreate } from '../encounter.store'

const form = reactive<EncounterCreate>({
  name: '',
  notes: ''
})

const encounterStore = useEncounterStore()
const error = ref<string | null>(null)
const isLoading = ref(false)

const create = async() => {
  if (!form.name) {
    error.value = 'Please fill in all required fields.'
    return
  }

  const { ...otherFields } = form
  console.log(form)

  const encounterData: EncounterCreate = {
    ...otherFields
  } as EncounterCreate

  isLoading.value = true
  try {
    await encounterStore.createEncounter(encounterData)
  } catch (e) {
    error.value = 'An error occurred while creating the encounter.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="col-md-6 offset-md-3">
    <form class="mb-3" @submit.prevent="create">
      <BaseInput v-model="form.name" label="Encounter Name:" type="text" class="mb-3" />
      <BaseInput v-model="form.notes" label="Hindrances:" type="text" class="mb-3" />

      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-outline-success rounded-0">Create</button>
      </div>
      <p v-if="error">{{ error }}</p>
    </form>
  </div>
</template>