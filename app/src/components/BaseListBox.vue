<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  options: {
    type: Array as () => { label: string; value: string }[],
    default: () => []
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Select an Option'
  }
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string | number): void
}>()

const selectedOption = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
});
</script>

<template>
  <select class="form-select" v-model="selectedOption">
    <option disabled value="">{{ placeholder }}</option>
    <option v-for="option in props.options" :key="option.value" :value="option.value">{{ option.label }}</option>
  </select>
</template>
