import Vue from 'vue'
import Router from 'vue-router'
import Miner from '@/components/Miner'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Miner',
      component: Miner
    }
  ]
})
