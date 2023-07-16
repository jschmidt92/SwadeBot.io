import type { RouteRecordRaw } from 'vue-router'

import EncountersModule from './Module.vue'
import EncounterCreate from './views/Create.vue'
import EncounterDetails from './views/View.vue'
import EncounterList from './views/List.vue'
import EncounterUpdate from './views/Update.vue'


const encounterRoutes: Array<RouteRecordRaw> = [
  {
    path: '/encounters',
    component: EncountersModule,
    children: [
      {
        path: '',
        name: 'EncounterList',
        component: EncounterList
      },
      {
        path: 'create',
        name: 'EncounterCreate',
        component: EncounterCreate,
        props: true
      },
      {
        path: ':id',
        name: 'EncounterDetails',
        component: EncounterDetails,
        props: true
      },
      {
        path: 'update',
        name: 'EncounterUpdate',
        component: EncounterUpdate
      }
    ]
  }
]

export default encounterRoutes
