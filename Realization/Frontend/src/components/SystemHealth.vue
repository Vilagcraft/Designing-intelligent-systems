<template>
  <el-card class="health-card">
    <template #header>
      <div class="card-header">
        <span>Статус системы</span>
        <el-icon><Monitor /></el-icon>
      </div>
    </template>

    <el-button
      type="primary"
      @click="handleCheckHealth"
      :loading="loading"
      style="width: 100%; margin-bottom: 20px"
    >
      <el-icon class="el-icon--left"><Refresh /></el-icon>
      {{ loading ? 'Проверка...' : 'Проверить статус' }}
    </el-button>

    <el-divider v-if="healthData || error" />

    <el-alert
      v-if="error"
      title="Ошибка подключения"
      type="error"
      :description="error"
      show-icon
      :closable="false"
    />

    <div v-if="healthData" class="health-content">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="8">
          <el-card shadow="hover" class="status-item">
            <div class="status-content">
              <div class="status-title">Общий статус</div>
              <div class="status-value">
                <el-icon :size="32" :color="getStatusColor(healthData.status === 'ok')">
                  <component :is="healthData.status === 'ok' ? 'CircleCheckFilled' : 'CircleCloseFilled'" />
                </el-icon>
              </div>
              <div class="status-tag">
                <el-tag :type="healthData.status === 'ok' ? 'success' : 'danger'" size="large">
                  {{ healthData.status === 'ok' ? 'OK' : 'ОШИБКА' }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="8">
          <el-card shadow="hover" class="status-item">
            <div class="status-content">
              <div class="status-title">Модель</div>
              <div class="status-value">
                <el-icon :size="32" :color="getStatusColor(healthData.model)">
                  <component :is="healthData.model ? 'CircleCheckFilled' : 'CircleCloseFilled'" />
                </el-icon>
              </div>
              <div class="status-tag">
                <el-tag :type="healthData.model ? 'success' : 'danger'" size="large">
                  {{ healthData.model ? 'Загружена' : 'Не найдена' }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>

        <el-col :xs="24" :sm="8">
          <el-card shadow="hover" class="status-item">
            <div class="status-content">
              <div class="status-title">Словарь</div>
              <div class="status-value">
                <el-icon :size="32" :color="getStatusColor(healthData.vocab)">
                  <component :is="healthData.vocab ? 'CircleCheckFilled' : 'CircleCloseFilled'" />
                </el-icon>
              </div>
              <div class="status-tag">
                <el-tag :type="healthData.vocab ? 'success' : 'danger'" size="large">
                  {{ healthData.vocab ? 'Загружен' : 'Не найден' }}
                </el-tag>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-divider content-position="left">Детальная информация</el-divider>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="Backend URL">
          <el-link type="primary" href="http://localhost:8000" target="_blank">
            http://localhost:8000
          </el-link>
        </el-descriptions-item>
        
        <el-descriptions-item label="API Docs">
          <el-link type="primary" href="http://localhost:8000/docs" target="_blank">
            http://localhost:8000/docs
          </el-link>
        </el-descriptions-item>
        
        <el-descriptions-item label="Время проверки">
          {{ lastCheckTime }}
        </el-descriptions-item>
      </el-descriptions>

      <!-- Действия -->
      <div class="actions-section">
        <el-divider content-position="left">Действия</el-divider>
        
        <el-space wrap>
          <el-button
            type="success"
            :disabled="!healthData.model"
            @click="handleDownload('model')"
          >
            <el-icon class="el-icon--left"><Download /></el-icon>
            Скачать модель
          </el-button>
          
          <el-button
            type="success"
            :disabled="!healthData.vocab"
            @click="handleDownload('vocab')"
          >
            <el-icon class="el-icon--left"><Download /></el-icon>
            Скачать словарь
          </el-button>
        </el-space>
      </div>

      <!-- Рекомендации -->
      <div v-if="!healthData.model || !healthData.vocab" class="recommendations">
        <el-divider content-position="left">Рекомендации</el-divider>
        <el-alert
          title="Требуется обучение"
          type="warning"
          :closable="false"
        >
          <template #default>
            <p>Модель или словарь не найдены. Для начала работы необходимо:</p>
            <ol>
              <li>Перейти на вкладку "Обучение"</li>
              <li>Запустить процесс обучения модели</li>
              <li>Дождаться завершения обучения</li>
              <li>Вернуться сюда и проверить статус снова</li>
            </ol>
          </template>
        </el-alert>
      </div>
    </div>

    <div v-if="!healthData && !error && !loading" class="empty-state">
      <el-empty description="Нажмите кнопку выше для проверки статуса системы" />
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import { Monitor, Refresh, Download, CircleCheckFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import api from '../api/client'

const healthData = ref(null)
const error = ref(null)
const loading = ref(false)
const lastCheckTime = ref(null)

const handleCheckHealth = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await api.checkHealth()
    healthData.value = response
    lastCheckTime.value = new Date().toLocaleString('ru-RU')
    
    const allOk = response.model && response.vocab && response.status === 'ok'
    
    ElNotification({
      title: allOk ? 'Система в норме' : 'Требуется внимание',
      message: allOk 
        ? 'Все компоненты системы работают корректно' 
        : 'Некоторые компоненты недоступны',
      type: allOk ? 'success' : 'warning',
      duration: 3000
    })
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Не удалось подключиться к серверу'
    
    ElNotification({
      title: 'Ошибка подключения',
      message: 'Backend сервер недоступен. Убедитесь, что он запущен.',
      type: 'error',
      duration: 4000
    })
  } finally {
    loading.value = false
  }
}

const getStatusColor = (isOk) => {
  return isOk ? '#67c23a' : '#f56c6c'
}

const handleDownload = async (type) => {
  try {
    const blob = type === 'model' 
      ? await api.downloadModel()
      : await api.downloadVocab()
    
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = type === 'model' ? 'model.pt' : 'vocab.json'
    link.click()
    window.URL.revokeObjectURL(url)
    
    ElNotification({
      title: 'Скачивание',
      message: `${type === 'model' ? 'Модель' : 'Словарь'} успешно скачан`,
      type: 'success',
      duration: 2000
    })
  } catch (err) {
    ElNotification({
      title: 'Ошибка',
      message: err.response?.data?.detail || err.message || 'Не удалось скачать файл',
      type: 'error',
      duration: 3000
    })
  }
}
</script>

<style scoped>
.health-card {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.health-content {
  margin-top: 10px;
}

.status-item {
  margin-bottom: 10px;
}

.status-content {
  text-align: center;
  padding: 10px;
}

.status-title {
  font-size: 14px;
  color: var(--el-text-color-secondary);
  margin-bottom: 15px;
  font-weight: 500;
}

.status-value {
  margin: 15px 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.status-tag {
  margin-top: 15px;
}

.actions-section {
  margin-top: 20px;
}

.recommendations {
  margin-top: 20px;
}

.recommendations ol {
  margin: 10px 0 0 0;
  padding-left: 20px;
}

.recommendations li {
  margin: 5px 0;
}

.empty-state {
  padding: 60px 0;
}

@media (max-width: 768px) {
  .status-item {
    margin-bottom: 15px;
  }
}
</style>

