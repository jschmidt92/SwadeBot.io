<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useCharacterStore } from '../character.store'
import CharacterCard from '@/components/CharacterCard.vue';

const characterStore = useCharacterStore()
const characters = ref<{ id: number; character_name: string; }[]>([])

onMounted(async () => {
  await characterStore.getCharacters()
  characters.value = characterStore.characters
})
</script>

<template>
  <div class="col-md-6 offset-md-3">
    <template v-if="characters.length">
      <div class="row">
        <div class="col-md-12" v-for="character in characters" :key="character.id">
          <CharacterCard :to="{ name: 'CharacterDetails', params: { id: character.id} }" :name="character.character_name" />
        </div>
      </div>
    </template>
    <p v-else>Loading Characters...</p>
  </div>
</template>
