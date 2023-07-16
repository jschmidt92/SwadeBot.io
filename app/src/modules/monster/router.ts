import type { RouteRecordRaw } from 'vue-router'

import MonstersModule from './Module.vue'
import MonsterCreate from './views/Create.vue'
import MonsterDetails from './views/View.vue'
import MonsterList from './views/List.vue'
import MonsterUpdate from './views/Update.vue'


const monsterRoutes: Array<RouteRecordRaw> = [
  {
    path: '/monsters',
    component: MonstersModule,
    children: [
      {
        path: '',
        name: 'MonsterList',
        component: MonsterList
      },
      {
        path: 'create',
        name: 'MonsterCreate',
        component: MonsterCreate,
        props: true
      },
      {
        path: ':id',
        name: 'MonsterDetails',
        component: MonsterDetails,
        props: true
      },
      {
        path: 'update',
        name: 'MonsterUpdate',
        component: MonsterUpdate
      }
    ]
  }
]

export default monsterRoutes
