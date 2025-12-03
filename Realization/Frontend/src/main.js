import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import 'element-plus/theme-chalk/dark/css-vars.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import ECharts from 'vue-echarts'
import App from './App.vue'

const app = createApp(App)

app.use(ElementPlus)

// Регистрация всех иконок Element Plus
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// Регистрация ECharts глобально
app.component('v-chart', ECharts)

app.mount('#app')

