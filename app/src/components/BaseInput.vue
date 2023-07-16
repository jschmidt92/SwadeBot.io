<script setup lang="ts">
defineProps({
  label: {
    type: String,
    default: ''
  },
  modelValue: {
    type: [String, Number],
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  }
})

const updateValue = (e: Event) => {
  const value = (e.target as HTMLInputElement).value
  emit('input', value)
  emit('update:modelValue', value)
}

const emit = defineEmits<{
  (e: 'input', value: string): void
  (e: 'update:modelValue', value: string): void
}>()
</script>

<template>
  <div class="form-floating small">
    <input class="form-control rounded-0" :type="type" :placeholder="label" :value="modelValue" @input="updateValue" v-bind="$attrs">
    <label>{{ label }}</label>
  </div>
</template>
