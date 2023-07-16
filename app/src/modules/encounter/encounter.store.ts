import { defineStore } from 'pinia'

export interface EncounterCreate {
  [key: string]: any
  name: string
  notes: string
}

export interface EncountersList {
  id: number
  name: string
}

export interface EncounterUpdate {
  id?: number
  name?: string
  notes?: string
}

export interface EncounterView {
  name: string
  notes: string
}

const BASE_URL = 'http://135.135.196.140/api'
// const BASE_URL = 'http://swadebot.api:8000/api'

export const useEncounterStore = defineStore('encounter', {
  state: () => ({
    encounter: null as EncounterView | null,
    encounters: [] as EncountersList[],
    error: null as string | null
  }),
  actions: {
    async createEncounter(encounter: EncounterCreate) {
      try {
        const response = await fetch(`${BASE_URL}/encounters`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(encounter)
        })
        if (!response.ok) {
          throw Error('Could not create encounter')
        }
        const newEncounter = await response.json()
        this.encounters.push(newEncounter)
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    },
    async getEncounters() {
      try {
        let data = await fetch(`${BASE_URL}/encounters`)
        if (!data.ok) {
          throw Error('No data available')
        }
        this.encounters = await data.json()
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    },
    async getEncounter(id: any) {
      try {
        let data = await fetch(`${BASE_URL}/encounters/` + id)
        if (!data.ok) {
          throw Error('Encounter does not exist')
        }
        this.encounter = await data.json()
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    },
    async updateEncounter(encounter: EncounterUpdate) {
      try {
        const response = await fetch(`${BASE_URL}/encounters/${encounter.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(encounter)
        })
        if (!response.ok) {
          throw Error('Could not update encounter')
        }
        const updatedEncounter = await response.json()
        const index = this.encounters.findIndex(c => c.id === updatedEncounter.id)
        if (index !== -1) {
          this.encounters.splice(index, 1, updatedEncounter)
        }
      } catch (err: any) {
        this.error = err.message
        console.log(this.error)
      }
    }
  }
})
