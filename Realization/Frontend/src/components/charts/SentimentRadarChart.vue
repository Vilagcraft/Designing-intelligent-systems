<template>
  <div class="chart-container">
    <v-chart 
      :option="chartOption" 
      :autoresize="true"
      style="height: 450px;"
    />
  </div>
</template>

<script setup>
import { computed, inject, ref } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'Многомерный анализ тональности'
  }
})

// Получаем информацию о текущей теме
const isDark = inject('isDark', ref(false))

const chartOption = computed(() => {
  // Статистика
  const total = props.data.length
  const stats = {
    positive: 0,
    negative: 0,
    neutral: 0
  }
  
  let totalConfidence = 0
  let totalLength = 0
  
  props.data.forEach(item => {
    const label = item.label?.toLowerCase() || ''
    if (label.includes('positive')) stats.positive++
    else if (label.includes('negative')) stats.negative++
    else if (label.includes('neutral')) stats.neutral++
    
    // Получаем уверенность
    let confidence = 0
    if (item.confidence !== undefined) {
      confidence = item.confidence
    } else if (item.probs && Array.isArray(item.probs) && item.probs.length > 0) {
      confidence = Math.max(...item.probs)
    }
    totalConfidence += confidence
    totalLength += item.text?.length || 0
  })
  
  const avgConfidence = total > 0 ? (totalConfidence / total * 100) : 0
  const avgLength = total > 0 ? (totalLength / total) : 0
  
  // Нормализуем для radar chart
  const maxLength = 500 // предполагаемая максимальная длина
  
  // Динамические цвета в зависимости от темы
  const textColor = isDark.value ? '#e0e0e0' : '#303133'
  const axisLineColor = isDark.value ? '#666' : '#dcdfe6'
  const splitLineColor = isDark.value ? '#444' : '#e4e7ed'
  
  return {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: textColor
      }
    },
    tooltip: {
      trigger: 'item'
    },
    legend: {
      data: ['Метрики'],
      bottom: 0,
      textStyle: {
        color: textColor
      }
    },
    radar: {
      indicator: [
        { name: 'Положительные (%)', max: 100 },
        { name: 'Отрицательные (%)', max: 100 },
        { name: 'Нейтральные (%)', max: 100 },
        { name: 'Средняя уверенность (%)', max: 100 },
        { name: 'Средняя длина', max: maxLength }
      ],
      radius: '65%',
      axisName: {
        color: textColor
      },
      axisLine: {
        lineStyle: {
          color: axisLineColor
        }
      },
      splitLine: {
        lineStyle: {
          color: splitLineColor
        }
      },
      splitArea: {
        areaStyle: {
          color: isDark.value ? ['rgba(255, 255, 255, 0.05)', 'rgba(255, 255, 255, 0.1)'] : ['rgba(114,172,209,0.2)', 'rgba(114,172,209,0.4)']
        }
      }
    },
    series: [
      {
        name: 'Метрики',
        type: 'radar',
        data: [
          {
            value: [
              ((stats.positive / total) * 100).toFixed(1),
              ((stats.negative / total) * 100).toFixed(1),
              ((stats.neutral / total) * 100).toFixed(1),
              avgConfidence.toFixed(1),
              avgLength.toFixed(0)
            ],
            name: 'Метрики',
            areaStyle: {
              color: 'rgba(64, 158, 255, 0.3)'
            },
            lineStyle: {
              color: '#409EFF',
              width: 2
            },
            itemStyle: {
              color: '#409EFF'
            }
          }
        ]
      }
    ]
  }
})
</script>

<style scoped>
.chart-container {
  width: 100%;
  padding: 20px;
  background: var(--el-bg-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>

