<template>
  <el-row :gutter="20">
    <el-col :xs="24" :sm="24" :md="12">
      <el-card class="training-card">
        <template #header>
          <div class="card-header">
            <span>Управление обучением</span>
            <el-icon><Setting /></el-icon>
          </div>
        </template>

        <el-form label-position="top">
          <el-alert
            title="Информация"
            type="info"
            :closable="false"
            style="margin-bottom: 20px"
          >
            Обучение модели может занять продолжительное время. 
            Используйте опции ниже для настройки процесса обучения.
          </el-alert>

          <el-form-item>
            <el-checkbox v-model="forceTraining" :disabled="training">
              <strong>Force</strong> - Принудительное переобучение
            </el-checkbox>
            <div class="checkbox-description">
              Запустить обучение даже если модель уже существует
            </div>
          </el-form-item>

          <el-form-item>
            <el-checkbox v-model="useSpark" :disabled="training">
              <strong>Use Spark</strong> - Использовать Apache Spark
            </el-checkbox>
            <div class="checkbox-description">
              Использовать Spark для обработки больших объемов данных
            </div>
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              @click="handleStartTraining"
              :loading="training"
              :disabled="training"
              size="large"
              style="width: 100%"
            >
              <el-icon class="el-icon--left"><VideoPlay /></el-icon>
              {{ training ? 'Обучение запущено...' : 'Запустить обучение' }}
            </el-button>
          </el-form-item>

          <el-divider />

          <el-form-item>
            <el-button
              @click="handleCheckStatus"
              :loading="loadingStatus"
              style="width: 100%"
            >
              <el-icon class="el-icon--left"><Refresh /></el-icon>
              Обновить статус
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </el-col>

    <el-col :xs="24" :sm="24" :md="12">
      <el-card class="status-card">
        <template #header>
          <div class="card-header">
            <span>Статус обучения</span>
            <el-icon><DataAnalysis /></el-icon>
          </div>
        </template>

        <div v-if="!statusData && !statusError" class="empty-state">
          <el-empty description="Нажмите 'Обновить статус' для получения информации" />
        </div>

        <el-alert
          v-if="statusError"
          title="Ошибка"
          type="error"
          :description="statusError"
          show-icon
          :closable="false"
        />

        <div v-if="statusData" class="status-content">
          <el-descriptions :column="1" border>
            <el-descriptions-item label="Состояние">
              <el-tag :type="getStatusType(statusData.status)">
                {{ getStatusText(statusData.status) }}
              </el-tag>
            </el-descriptions-item>
            
            <el-descriptions-item v-if="statusData.message" label="Сообщение">
              {{ statusData.message }}
            </el-descriptions-item>
            
            <el-descriptions-item v-if="statusData.train_count !== undefined" label="Количество обучений">
              {{ statusData.train_count }}
            </el-descriptions-item>
            
            <el-descriptions-item v-if="statusData.last_trained" label="Последнее обучение">
              {{ formatDate(statusData.last_trained) }}
            </el-descriptions-item>
            
            <el-descriptions-item v-if="statusData.progress !== undefined" label="Прогресс">
              <el-progress
                :percentage="statusData.progress"
                :status="statusData.progress === 100 ? 'success' : undefined"
              />
            </el-descriptions-item>
          </el-descriptions>

          <!-- Детали обучения -->
          <div v-if="statusData.details" style="margin-top: 20px">
            <el-divider content-position="left">Детали</el-divider>
            <pre class="details-pre">{{ JSON.stringify(statusData.details, null, 2) }}</pre>
          </div>
        </div>
      </el-card>
    </el-col>
  </el-row>
</template>

<script setup>
import { ref } from 'vue'
import { ElNotification, ElMessageBox } from 'element-plus'
import { Setting, VideoPlay, Refresh, DataAnalysis } from '@element-plus/icons-vue'
import api from '../api/client'

const forceTraining = ref(false)
const useSpark = ref(false)
const training = ref(false)
const loadingStatus = ref(false)
const statusData = ref(null)
const statusError = ref(null)

const handleStartTraining = async () => {
  try {
    await ElMessageBox.confirm(
      'Вы уверены, что хотите запустить обучение модели? Это может занять продолжительное время.',
      'Подтверждение',
      {
        confirmButtonText: 'Запустить',
        cancelButtonText: 'Отмена',
        type: 'warning',
      }
    )

    training.value = true
    
    const response = await api.startTraining(forceTraining.value, useSpark.value)
    
    ElNotification({
      title: 'Успешно',
      message: response.message || 'Обучение успешно запущено',
      type: 'success',
      duration: 3000
    })
    
    // Автоматически обновляем статус после запуска
    setTimeout(() => {
      handleCheckStatus()
      training.value = false
    }, 2000)
    
  } catch (err) {
    if (err !== 'cancel') {
      ElNotification({
        title: 'Ошибка',
        message: err.response?.data?.detail || err.message || 'Не удалось запустить обучение',
        type: 'error',
        duration: 3000
      })
      training.value = false
    } else {
      training.value = false
    }
  }
}

const handleCheckStatus = async () => {
  loadingStatus.value = true
  statusError.value = null
  
  try {
    const response = await api.getTrainingStatus()
    statusData.value = response
    
    ElNotification({
      title: 'Обновлено',
      message: 'Статус обучения обновлен',
      type: 'success',
      duration: 1500
    })
  } catch (err) {
    statusError.value = err.response?.data?.detail || err.message || 'Не удалось получить статус'
    
    ElNotification({
      title: 'Ошибка',
      message: statusError.value,
      type: 'error',
      duration: 3000
    })
  } finally {
    loadingStatus.value = false
  }
}

const getStatusType = (status) => {
  const statusLower = status?.toLowerCase() || ''
  if (statusLower.includes('success') || statusLower.includes('complete')) return 'success'
  if (statusLower.includes('running') || statusLower.includes('training')) return 'warning'
  if (statusLower.includes('error') || statusLower.includes('failed')) return 'danger'
  return 'info'
}

const getStatusText = (status) => {
  const statusLower = status?.toLowerCase() || ''
  if (statusLower.includes('success') || statusLower.includes('complete')) return 'Завершено'
  if (statusLower.includes('running') || statusLower.includes('training')) return 'Выполняется'
  if (statusLower.includes('error') || statusLower.includes('failed')) return 'Ошибка'
  if (statusLower.includes('not')) return 'Не обучена'
  return status
}

const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  try {
    return new Date(dateString).toLocaleString('ru-RU')
  } catch {
    return dateString
  }
}
</script>

<style scoped>
.training-card,
.status-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.checkbox-description {
  margin-left: 24px;
  margin-top: 5px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.empty-state {
  padding: 40px 0;
}

.status-content {
  margin-top: 10px;
}

.details-pre {
  background-color: var(--el-fill-color-light);
  padding: 15px;
  border-radius: 4px;
  font-size: 12px;
  overflow-x: auto;
  max-height: 300px;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .status-card {
    margin-top: 20px;
  }
}
</style>

