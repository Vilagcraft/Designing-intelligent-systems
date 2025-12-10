<template>
  <div id="app">
    <el-container>
      <!-- Шапка приложения -->
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo-section">
            <el-icon :size="32" color="#409EFF">
              <DataAnalysis />
            </el-icon>
            <h1>Анализ тональности текста</h1>
          </div>
          <div class="header-actions">
            <el-tooltip content="Переключить тему" placement="bottom">
              <el-button 
                :icon="isDark ? 'Sunny' : 'Moon'" 
                circle 
                @click="toggleTheme"
              />
            </el-tooltip>
            <el-tooltip content="Документация API" placement="bottom">
              <el-button 
                icon="Document" 
                circle 
                @click="openApiDocs"
              />
            </el-tooltip>
          </div>
        </div>
      </el-header>

      <!-- Основной контент -->
      <el-main class="app-main">
        <el-tabs 
          v-model="activeTab" 
          type="border-card"
          class="main-tabs"
        >
          <el-tab-pane name="predict">
            <template #label>
              <span class="tab-label">
                <el-icon><ChatDotRound /></el-icon>
                <span>Предсказание</span>
              </span>
            </template>
            <PredictSingle />
          </el-tab-pane>

          <el-tab-pane name="batch">
            <template #label>
              <span class="tab-label">
                <el-icon><Files /></el-icon>
                <span>Batch предсказание</span>
              </span>
            </template>
            <PredictBatch />
          </el-tab-pane>

          <el-tab-pane name="dataset">
            <template #label>
              <span class="tab-label">
                <el-icon><FolderOpened /></el-icon>
                <span>Анализ датасета</span>
              </span>
            </template>
            <DatasetAnalysis />
          </el-tab-pane>

          <el-tab-pane name="training">
            <template #label>
              <span class="tab-label">
                <el-icon><Setting /></el-icon>
                <span>Обучение</span>
              </span>
            </template>
            <Training />
          </el-tab-pane>

          <el-tab-pane name="health">
            <template #label>
              <span class="tab-label">
                <el-icon><Monitor /></el-icon>
                <span>Статус системы</span>
              </span>
            </template>
            <SystemHealth />
          </el-tab-pane>
        </el-tabs>
      </el-main>

      <!-- Футер -->
      <el-footer class="app-footer">
        <div class="footer-content">
          <span>© 2024 Sentiment Analysis System</span>
          <el-space>
            <el-text type="info">Backend: 
              <el-link 
                type="primary" 
                href="http://localhost:8000" 
                target="_blank"
                :underline="false"
              >
                localhost:8000
              </el-link>
            </el-text>
            <el-divider direction="vertical" />
            <el-text type="info">Frontend: 
              <el-text type="primary">localhost:5173</el-text>
            </el-text>
          </el-space>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, provide } from 'vue'
import { DataAnalysis, ChatDotRound, Files, Setting, Monitor, FolderOpened } from '@element-plus/icons-vue'
import PredictSingle from './components/PredictSingle.vue'
import PredictBatch from './components/PredictBatch.vue'
import DatasetAnalysis from './components/DatasetAnalysis.vue'
import Training from './components/Training.vue'
import SystemHealth from './components/SystemHealth.vue'

const activeTab = ref('predict')
const isDark = ref(false)

// Предоставляем информацию о теме дочерним компонентам
provide('isDark', isDark)

// Проверяем сохраненную тему при загрузке
onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark') {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
})

const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const openApiDocs = () => {
  window.open('http://localhost:8000/docs', '_blank')
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  min-height: 100vh;
}

#app {
  min-height: 100vh;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.el-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Шапка */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  height: 70px !important;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logo-section h1 {
  font-size: 24px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* Основной контент */
.app-main {
  flex: 1;
  padding: 20px;
  background: var(--el-bg-color-page);
}

.main-tabs {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.main-tabs :deep(.el-tabs__content) {
  padding: 20px;
}

.tab-label {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-label .el-icon {
  font-size: 18px;
}

/* Футер */
.app-footer {
  background: var(--el-bg-color);
  border-top: 1px solid var(--el-border-color);
  display: flex;
  align-items: center;
  padding: 0 30px;
  height: 50px !important;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  font-size: 14px;
}

/* Темная тема */
.dark {
  color-scheme: dark;
}

/* Адаптивность */
@media (max-width: 768px) {
  .app-header {
    padding: 0 15px;
    height: auto !important;
    min-height: 70px;
  }

  .header-content {
    flex-direction: column;
    gap: 10px;
    padding: 10px 0;
  }

  .logo-section h1 {
    font-size: 18px;
  }

  .app-main {
    padding: 10px;
  }

  .main-tabs :deep(.el-tabs__content) {
    padding: 10px;
  }

  .footer-content {
    flex-direction: column;
    gap: 5px;
    font-size: 12px;
    padding: 10px 0;
  }

  .app-footer {
    height: auto !important;
    min-height: 50px;
    padding: 0 15px;
  }

  .tab-label span {
    display: none;
  }
}

@media (max-width: 480px) {
  .logo-section {
    gap: 10px;
  }

  .logo-section .el-icon {
    font-size: 24px !important;
  }

  .logo-section h1 {
    font-size: 16px;
  }
}

/* Скроллбар */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--el-fill-color-lighter);
}

::-webkit-scrollbar-thumb {
  background: var(--el-border-color-darker);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--el-border-color-dark);
}
</style>

