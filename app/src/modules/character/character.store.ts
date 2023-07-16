import { defineStore } from 'pinia'

export interface CharacterCreate {
  [key: string]: any
  user_id: string | null
  character_name: string
  race: string
  gender: string
  charisma: number
  pace: number
  parry: number
  toughness: number
  attributes: string | Record<string, any>
  skills: string | Record<string, any>
  gear?: string | any[]
  hindrances: string
  edges: string
  powers?: string | any[]
  weapons?: string | any[]
  damage: string | Record<string, any>
  ammo: number
  money: number
}

export interface CharactersList {
  id: number
  character_name: string
}

export interface CharacterUpdate {
  id?: number
  character_name?: string
  race?: string
  gender?: string
  charisma?: number
  pace?: number
  parry?: number
  toughness?: number
  attributes?: string | Record<string, any>
  skills?: string | Record<string, any>
  gear?: string | any[]
  hindrances?: string
  edges?: string
  powers?: string | any[]
  weapons?: string | any[]
  damage?: string | Record<string, any>
  ammo?: number
  money?: number
}

export interface CharacterView {
  character_name: string
  race: string
  gender: string
  charisma: number
  pace: number
  parry: number
  toughness: number
  attributes: string | Record<string, any>
  skills: string | Record<string, any>
  gear: Gear[]
  hindrances: string
  edges: string
  powers: Power[]
  weapons: Weapon[]
  damage: string | Record<string, any>
  ammo: number
  money: number
}

export interface Gear {
  id: number
  name: string
  min_str: string
  wt: number
  cost: number
  notes: string
}

export interface Power {
  id: number
  name: string
  pp: string
  range: string
  duration: string
  effect: string
  notes: string
}

export interface Weapon {
  id: number
  name: string
  range: string
  damage: string
  rof: number
  shots: number
  min_str: string
  wt: number
  cost: number
  notes: string
}

const BASE_URL = 'http://135.135.196.140/api'
// const BASE_URL = 'http://swadebot.api:8000/api'

export const useCharacterStore = defineStore('character', {
  state: () => ({
    character: null as CharacterView | null,
    characters: [] as CharactersList[],
    error: null as string | null
  }),
  actions: {
    async createCharacter(character: CharacterCreate) {
      try {
        const response = await fetch(`${BASE_URL}/characters`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(character)
        })
        if (!response.ok) {
          throw Error('Could not create character')
        }
        const newCharacter = await response.json()
        this.characters.push(newCharacter)
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    },
    async getCharacters() {
      try {
        let data = await fetch(`${BASE_URL}/characters`)
        if (!data.ok) {
          throw Error('No data available')
        }
        this.characters = await data.json()
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    },
    async getCharacter(id: any) {
      try {
        let data = await fetch(`${BASE_URL}/characters/` + id)
        if (!data.ok) {
          throw Error('Character does not exist')
        }
        this.character = await data.json()
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    },
    async updateCharacter(character: CharacterUpdate) {
      try {
        const response = await fetch(`${BASE_URL}/characters/${character.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(character)
        })
        if (!response.ok) {
          throw Error('Could not update character')
        }
        const updatedCharacter = await response.json()
        const index = this.characters.findIndex(c => c.id === updatedCharacter.id)
        if (index !== -1) {
          this.characters.splice(index, 1, updatedCharacter)
        }
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    }
  }
})
