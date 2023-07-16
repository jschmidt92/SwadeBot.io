import type { RouteRecordRaw } from 'vue-router'

import CharactersModule from './Module.vue'
import CharacterCreate from './views/Create.vue'
import CharacterDetails from './views/View.vue'
import CharacterList from './views/List.vue'
import CharacterUpdate from './views/Update.vue'


const characterRoutes: Array<RouteRecordRaw> = [
  {
    path: '/characters',
    component: CharactersModule,
    children: [
      {
        path: '',
        name: 'CharacterList',
        component: CharacterList
      },
      {
        path: 'create',
        name: 'CharacterCreate',
        component: CharacterCreate,
        props: true
      },
      {
        path: ':id',
        name: 'CharacterDetails',
        component: CharacterDetails,
        props: true
      },
      {
        path: 'update',
        name: 'CharacterUpdate',
        component: CharacterUpdate
      }
    ]
  }
]

export default characterRoutes
