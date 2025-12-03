<template>
  <el-card class="predict-single-card">
    <template #header>
      <div class="card-header">
        <span>Анализ тональности текста</span>
      </div>
    </template>

    <el-form>
      <el-form-item label="Введите текст для анализа:">
        <el-input
          v-model="inputText"
          type="textarea"
          :rows="6"
          placeholder="Введите текст на русском языке..."
          :disabled="loading"
        />
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          @click="handlePredict"
          :loading="loading"
          :disabled="!inputText.trim()"
        >
          <el-icon class="el-icon--left"><Search /></el-icon>
          Анализировать
        </el-button>
        <el-button @click="handleClear" :disabled="loading">
          Очистить
        </el-button>
      </el-form-item>
    </el-form>

    <!-- Результаты -->
    <el-divider v-if="result || error" />

    <el-alert
      v-if="error"
      title="Ошибка"
      type="error"
      :description="error"
      show-icon
      :closable="false"
    />

    <div v-if="result" class="result-container">
      <h3>Результат анализа:</h3>
      <div class="result-content">
        <el-row :gutter="20">
          <el-col :xs="24" :md="12">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="Текст">
                {{ inputText }}
              </el-descriptions-item>
              <el-descriptions-item label="Тональность">
                <el-tag :type="getTagType(result.label)" size="large">
                  {{ getLabelText(result.label) }}
                </el-tag>
              </el-descriptions-item>
              <el-descriptions-item v-if="result.confidence" label="Уверенность">
                <el-progress
                  :percentage="Math.round(result.confidence * 100)"
                  :color="getProgressColor(result.confidence)"
                />
              </el-descriptions-item>
              <el-descriptions-item v-if="result.probs" label="Распределение вероятностей">
                <div class="probs-list">
                  <div v-for="(prob, index) in result.probs" :key="index" class="prob-item">
                    <span>Класс {{ index }}: </span>
                    <el-tag size="small">{{ (prob * 100).toFixed(2) }}%</el-tag>
                  </div>
                </div>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
          <el-col :xs="24" :md="12">
            <SentimentGaugeChart 
              v-if="hasConfidence"
              :value="getConfidenceValue()"
              title="Уверенность модели"
            />
            <el-empty v-else description="Данные об уверенности недоступны" />
          </el-col>
        </el-row>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElNotification } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import api from '../api/client'
import SentimentGaugeChart from './charts/SentimentGaugeChart.vue'

const inputText = ref('')
const result = ref(null)
const error = ref(null)
const loading = ref(false)

const hasConfidence = computed(() => {
  if (!result.value) return false
  return result.value.confidence !== undefined || 
         (result.value.probs && Array.isArray(result.value.probs) && result.value.probs.length > 0)
})

const getConfidenceValue = () => {
  if (!result.value) return 0
  if (result.value.confidence !== undefined) {
    return result.value.confidence
  }
  if (result.value.probs && Array.isArray(result.value.probs) && result.value.probs.length > 0) {
    return Math.max(...result.value.probs)
  }
  return 0
}

const handlePredict = async () => {
  if (!inputText.value.trim()) return

  loading.value = true
  error.value = null
  result.value = null

  try {
    const response = await api.predictSingle(inputText.value.trim())
    result.value = response
    
    ElNotification({
      title: 'Успешно',
      message: 'Анализ завершен',
      type: 'success',
      duration: 2000
    })
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Произошла ошибка при анализе'
    
    ElNotification({
      title: 'Ошибка',
      message: error.value,
      type: 'error',
      duration: 3000
    })
  } finally {
    loading.value = false
  }
}

const handleClear = () => {
  inputText.value = ''
  result.value = null
  error.value = null
}

const getTagType = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive') || labelLower.includes('положительн')) return 'success'
  if (labelLower.includes('negative') || labelLower.includes('отрицательн')) return 'danger'
  return 'info'
}

const getLabelText = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive')) return 'Положительная'
  if (labelLower.includes('negative')) return 'Отрицательная'
  if (labelLower.includes('neutral')) return 'Нейтральная'
  return label
}

const getProgressColor = (confidence) => {
  if (confidence > 0.8) return '#67c23a'
  if (confidence > 0.6) return '#e6a23c'
  return '#f56c6c'
}
</script>

<style scoped>
.predict-single-card {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.result-container {
  margin-top: 20px;
}

.result-content {
  margin-top: 15px;
}

h3 {
  margin: 0 0 15px 0;
  color: var(--el-text-color-primary);
}

.probs-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.prob-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

