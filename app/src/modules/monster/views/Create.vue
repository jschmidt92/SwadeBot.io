<script setup lang="ts">
import { ComputedRef, computed, reactive, ref, Ref } from 'vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseListBox from '@/components/BaseListBox.vue'
import { useMonsterStore, type MonsterCreate } from '../monster.store'

interface Dictionary {
  name: string
  value: string
}

interface FormMonsterCreate extends Omit<MonsterCreate, 'attributes' | 'skills' | 'gear' | 'powers' | 'weapons' | 'damage'> {
  attributes: Record<string, string>
  skills: Record<string, string>
  gear: string
  powers: string
  weapons: string
  damage: string
}

const form = reactive<FormMonsterCreate>({
  monster_name: '',
  race: '',
  gender: '',
  charisma: 0,
  pace: 0,
  parry: 0,
  toughness: 0,
  attributes: {},
  skills: {},
  gear: '[]',
  hindrances: '',
  edges: '',
  powers: '[]',
  weapons: '[]',
  damage: '{"Wounds": 0, "Fatigue": 0, "Inc": "No"}',
  ammo: 0,
  money: 0
})

const monsterStore = useMonsterStore()
const error = ref<string | null>(null)
const isLoading = ref(false)

const attribute = reactive({
  name: '',
  value: '',
  items: [] as Dictionary[]
})

const skill = reactive({
  name: '',
  value: '',
  items: [] as Dictionary[]
})

const genders = [
  {label: "Male", value: "male"},
  {label: "Female", value: "female"}
]

const races = [
  {label: "Android", value: "android"},
  {label: "Anklebiter", value: "anklebiter"},
  {label: "Angler", value: "angler"},
  {label: "A-Pex", value: "apex"},
  {label: "Aquarian", value: "aquarian"},
  {label: "Aurax", value: "aurax"},
  {label: "Avion", value: "avion"},
  {label: "Behemoth", value: "behemoth"},
  {label: "Bloodwing", value: "bloodwing"},
  {label: "Boomer", value: "boomer"},
  {label: "Colemata", value: "colemata"},
  {label: "Construct", value: "construct"},
  {label: "Deader", value: "deader"},
  {label: "Death Crawler (Swarm)", value: "deathcrawler"},
  {label: "Drake", value: "drake"},
  {label: "Dwarf", value: "dwarf"},
  {label: "Elf", value: "elf"},
  {label: "Floran", value: "floran"},
  {label: "Half-Elve", value: "halfelve"},
  {label: "Half-Folk", value: "halffolk"},
  {label: "Human", value: "human"},
  {label: "Hunter", value: "hunter"},
  {label: "Insectoid", value: "insectoid"},
  {label: "Kalian", value: "kalian"},
  {label: "Krok", value: "krok"},
  {label: "Krok, Giant", value: "krokgiant"},
  {label: "Lightning Darter (Swarm)", value: "lightningdarter"},
  {label: "Lacerauns", value: "lacerauns"},
  {label: "Mauler", value: "mauler"},
  {label: "Rakashan", value: "rakashan"},
  {label: "Ravager", value: "ravager"},
  {label: "Robot", value: "robot"},
  {label: "Sailfin", value: "sailfin"},
  {label: "Saurian", value: "saurian"},
  {label: "Scrat", value: "scrat"},
  {label: "Scute Boar", value: "scuteboar"},
  {label: "Serran", value: "serran"},
  {label: "Scylla", value: "scylla"},
  {label: "Scylla, Giant", value: "scyllagiant"},
  {label: "Siren Creeper", value: "sirencreeper"},
  {label: "Spitter", value: "spitter"},
  {label: "Yeti", value: "yeti"}
]

function jsonFormat(data: Ref<Dictionary[]>): ComputedRef<Record<string, string>> {
  return computed(() => {
    const json: Record<string, string> = {};

    for (const item of data.value) {
      json[item.name] = item.value;
    }

    return json;
  });
}

const jsonFormatAttributes = jsonFormat(ref(attribute.items));
const jsonFormatSkills = jsonFormat(ref(skill.items));

function addAttribute() {
  form.attributes[attribute.name] = attribute.value
  attribute.items.push({ name: attribute.name, value: attribute.value })
  attribute.name = ''
  attribute.value = ''
}

const updateAttribute = (index: number): void => {
  const updatedAttribute = attribute.items[index];

  if (updatedAttribute) {
    updatedAttribute.name = updatedAttribute.name.trim();
    updatedAttribute.value = updatedAttribute.value.trim();
  }
}

const deleteAttribute = (index: number): void => {
  attribute.items.splice(index, 1);
}

function addSkill() {
  form.skills[skill.name] = skill.value
  skill.items.push({ name: skill.name, value: skill.value })
  skill.name = ''
  skill.value = ''
}

const updateSkill = (index: number): void => {
  const updatedSkill = skill.items[index];

  if (updatedSkill) {
    updatedSkill.name = updatedSkill.name.trim();
    updatedSkill.value = updatedSkill.value.trim();
  }
}

const deleteSkill = (index: number): void => {
  skill.items.splice(index, 1);
}

const create = async() => {
  if (!form.monster_name || !form.race || !form.gender || !form.charisma || !form.pace || !form.parry || !form.toughness || !form.hindrances || !form.edges) {
    error.value = 'Please fill in all required fields.'
    return
  }

  const jsonFields = ['damage', 'gear', 'powers', 'weapons']
  const parsedFields: Partial<MonsterCreate> = {}
  for (const field of jsonFields) {
    try {
      parsedFields[field] = JSON.parse(form[field])
    } catch (e) {
      error.value = `Invalid JSON in ${field} field`
      return
    }
  }

  const { attributes, skills, gear, damage, powers, weapons, ...otherFields } = form
  console.log(form)

  const monsterData: MonsterCreate = {
    ...otherFields,
    ...parsedFields,
    attributes: jsonFormatAttributes.value,
    skills: jsonFormatSkills.value
  } as MonsterCreate

  isLoading.value = true
  try {
    await monsterStore.createMonster(monsterData)
  } catch (e) {
    error.value = 'An error occurred while creating the monster.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="col-md-6 offset-md-3">
    <form class="mb-3" @submit.prevent="create">
      <BaseInput v-model="form.monster_name" label="Monster Name:" type="text" class="mb-3" />
      <BaseListBox v-model="form.race" :options="races" class="mb-3" />
      <BaseListBox v-model="form.gender" :options="genders" class="mb-3" />
      <BaseInput v-model="form.charisma" label="Charisma:" type="number" class="mb-3" />
      <BaseInput v-model="form.pace" label="Pace:" type="number" class="mb-3" />
      <BaseInput v-model="form.parry" label="Parry:" type="number" class="mb-3" />
      <BaseInput v-model="form.toughness" label="Toughness:" type="number" class="mb-3" />

      <div class="mb-3">
        <div class="input-group">
          <BaseInput v-model="attribute.name" label="Attribute Name:" type="text" />
          <BaseInput v-model="attribute.value" label="Attribute Value:" type="text" />
          <button type="button" class="btn btn-outline-dark rounded-0" @click.prevent="addAttribute">Add</button>
        </div>
        <div v-if="attribute.items.length">
          <ul class="list-group">
            <li class="list-group-item border border-0" style="background: none !important;" v-for="(item, index) in attribute.items" :key="index">
              <div class="input-group">
                <BaseInput v-model="item.name" label="Attribute Name:" :placeholder="`Attribute Name ${index + 1}`" type="text" />
                <BaseInput v-model="item.value" label="Attribute Value:" :placeholder="`Attribute Value ${index + 1}`" type="text" />
                <button type="button" class="btn btn-outline-warning rounded-0" @click.prevent="updateAttribute(index)">Update</button>
                <button type="button" class="btn btn-outline-danger rounded-0" @click.prevent="deleteAttribute(index)">Delete</button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No attributes have been added yet.</p>
        </div>
      </div>

      <div class="mb-3">
        <div class="input-group">
          <BaseInput v-model="skill.name" label="Skill Name:" type="text" />
          <BaseInput v-model="skill.value" label="Skill Value:" type="text" />
          <button type="button" class="btn btn-outline-dark rounded-0" @click.prevent="addSkill">Add</button>
        </div>
        <div v-if="skill.items.length">
          <ul class="list-group">
            <li class="list-group-item border border-0" style="background: none !important;" v-for="(item, index) in skill.items" :key="index">
              <div class="input-group">
                <BaseInput v-model="item.name" label="Skill Name:" :placeholder="`Skill Name ${index + 1}`" type="text" />
                <BaseInput v-model="item.value" label="Skill Value:" :placeholder="`Skill Value ${index + 1}`" type="text" />
                <button type="button" class="btn btn-outline-warning rounded-0" @click.prevent="updateSkill(index)">Update</button>
                <button type="button" class="btn btn-outline-danger rounded-0" @click.prevent="deleteSkill(index)">Delete</button>
              </div>
            </li>
          </ul>
        </div>
        <div v-else>
          <p>No skills have been added yet.</p>
        </div>
      </div>

      <BaseInput v-model="form.hindrances" label="Hindrances:" type="text" class="mb-3" />
      <BaseInput v-model="form.edges" label="Edges:" type="text" class="mb-3" />

      <div class="d-grid gap-2">
        <button type="submit" class="btn btn-outline-success rounded-0">Create</button>
      </div>
      <p v-if="error">{{ error }}</p>
    </form>
  </div>
</template>../monster.store