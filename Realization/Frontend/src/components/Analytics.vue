<template>
  <el-card class="analytics-card">
    <template #header>
      <div class="card-header">
        <span>📊 Аналитика и визуализация</span>
        <el-tag type="info">{{ results.length }} текст(ов)</el-tag>
      </div>
    </template>

    <el-empty v-if="results.length === 0" description="Нет данных для отображения">
      <el-button type="primary" @click="$emit('analyze')">
        Начать анализ
      </el-button>
    </el-empty>

    <div v-else class="analytics-content">
      <!-- Основная статистика -->
      <el-row :gutter="20" class="stats-row">
        <el-col :xs="12" :sm="6">
          <el-statistic title="Всего текстов" :value="results.length">
            <template #prefix>
              <el-icon><Document /></el-icon>
            </template>
          </el-statistic>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-statistic 
            title="Положительных" 
            :value="positiveCount"
            :value-style="{ color: '#67c23a' }"
          >
            <template #prefix>
              <el-icon><CircleCheck /></el-icon>
            </template>
          </el-statistic>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-statistic 
            title="Отрицательных" 
            :value="negativeCount"
            :value-style="{ color: '#f56c6c' }"
          >
            <template #prefix>
              <el-icon><CircleClose /></el-icon>
            </template>
          </el-statistic>
        </el-col>
        <el-col :xs="12" :sm="6">
          <el-statistic 
            title="Нейтральных" 
            :value="neutralCount"
            :value-style="{ color: '#909399' }"
          >
            <template #prefix>
              <el-icon><Minus /></el-icon>
            </template>
          </el-statistic>
        </el-col>
      </el-row>

      <el-divider />

      <!-- Графики первого ряда -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="8">
          <SentimentGaugeChart 
            :value="averageConfidence"
            title="Средняя уверенность"
          />
        </el-col>
        <el-col :xs="24" :md="16">
          <SentimentPieChart 
            :data="results"
            title="Распределение тональности"
          />
        </el-col>
      </el-row>

      <el-divider />

      <!-- Графики второго ряда -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <SentimentBarChart 
            :data="results"
            title="Количество по категориям"
          />
        </el-col>
        <el-col :xs="24" :md="12">
          <TextLengthHistogram 
            :data="results"
            title="Распределение длины текстов"
          />
        </el-col>
      </el-row>

      <el-divider />

      <!-- Графики третьего ряда -->
      <el-row :gutter="20">
        <el-col :xs="24" :md="12">
          <ConfidenceChart 
            :data="results"
            title="График уверенности модели"
          />
        </el-col>
        <el-col :xs="24" :md="12">
          <SentimentRadarChart 
            :data="results"
            title="Многомерный анализ"
          />
        </el-col>
      </el-row>

      <!-- Детальная таблица статистики -->
      <el-divider content-position="left">Детальная статистика</el-divider>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="Всего проанализировано">
          {{ results.length }} текстов
        </el-descriptions-item>
        <el-descriptions-item label="Успешных анализов">
          {{ successCount }} ({{ successRate }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Средняя длина текста">
          {{ averageLength }} символов
        </el-descriptions-item>
        <el-descriptions-item label="Средняя уверенность">
          {{ (averageConfidence * 100).toFixed(2) }}%
        </el-descriptions-item>
        <el-descriptions-item label="Положительных">
          {{ positiveCount }} ({{ positivePercent }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Отрицательных">
          {{ negativeCount }} ({{ negativePercent }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Нейтральных">
          {{ neutralCount }} ({{ neutralPercent }}%)
        </el-descriptions-item>
        <el-descriptions-item label="Преобладающая тональность">
          <el-tag :type="dominantSentimentType">
            {{ dominantSentiment }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </el-card>
</template>

<script setup>
import { computed } from 'vue'
import { Document, CircleCheck, CircleClose, Minus } from '@element-plus/icons-vue'
import SentimentPieChart from './charts/SentimentPieChart.vue'
import SentimentBarChart from './charts/SentimentBarChart.vue'
import ConfidenceChart from './charts/ConfidenceChart.vue'
import TextLengthHistogram from './charts/TextLengthHistogram.vue'
import SentimentRadarChart from './charts/SentimentRadarChart.vue'
import SentimentGaugeChart from './charts/SentimentGaugeChart.vue'

const props = defineProps({
  results: {
    type: Array,
    default: () => []
  }
})

const positiveCount = computed(() => {
  return props.results.filter(r => 
    r.label?.toLowerCase().includes('positive')
  ).length
})

const negativeCount = computed(() => {
  return props.results.filter(r => 
    r.label?.toLowerCase().includes('negative')
  ).length
})

const neutralCount = computed(() => {
  return props.results.filter(r => 
    r.label?.toLowerCase().includes('neutral')
  ).length
})

const successCount = computed(() => {
  return props.results.filter(r => r.label && !r.error).length
})

const successRate = computed(() => {
  if (props.results.length === 0) return 0
  return ((successCount.value / props.results.length) * 100).toFixed(1)
})

const averageLength = computed(() => {
  if (props.results.length === 0) return 0
  const total = props.results.reduce((sum, r) => sum + (r.text?.length || 0), 0)
  return Math.round(total / props.results.length)
})

const averageConfidence = computed(() => {
  if (successCount.value === 0) return 0
  const total = props.results.reduce((sum, r) => {
    if (r.label && !r.error) {
      // Пытаемся получить уверенность из разных источников
      let confidence = 0
      if (r.confidence !== undefined) {
        confidence = r.confidence
      } else if (r.probs && Array.isArray(r.probs) && r.probs.length > 0) {
        confidence = Math.max(...r.probs)
      }
      return sum + confidence
    }
    return sum
  }, 0)
  return successCount.value > 0 ? total / successCount.value : 0
})

const positivePercent = computed(() => {
  if (props.results.length === 0) return 0
  return ((positiveCount.value / props.results.length) * 100).toFixed(1)
})

const negativePercent = computed(() => {
  if (props.results.length === 0) return 0
  return ((negativeCount.value / props.results.length) * 100).toFixed(1)
})

const neutralPercent = computed(() => {
  if (props.results.length === 0) return 0
  return ((neutralCount.value / props.results.length) * 100).toFixed(1)
})

const dominantSentiment = computed(() => {
  const max = Math.max(positiveCount.value, negativeCount.value, neutralCount.value)
  if (max === positiveCount.value) return 'Положительная'
  if (max === negativeCount.value) return 'Отрицательная'
  return 'Нейтральная'
})

const dominantSentimentType = computed(() => {
  const max = Math.max(positiveCount.value, negativeCount.value, neutralCount.value)
  if (max === positiveCount.value) return 'success'
  if (max === negativeCount.value) return 'danger'
  return 'info'
})
</script>

<style scoped>
.analytics-card {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.analytics-content {
  padding: 10px 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stats-row :deep(.el-statistic) {
  text-align: center;
  padding: 15px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
}

.el-row {
  margin-bottom: 20px;
}

.el-col {
  margin-bottom: 20px;
}
</style>

