<template>
  <div class="chart-container">
    <v-chart 
      :option="chartOption" 
      :autoresize="true"
      style="height: 400px;"
    />
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  PieChart,
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
    default: 'Распределение тональности'
  }
})

const chartOption = computed(() => {
  // Подсчитываем статистику
  const stats = {}
  props.data.forEach(item => {
    const label = item.label || 'unknown'
    stats[label] = (stats[label] || 0) + 1
  })

  // Преобразуем в формат для диаграммы
  const chartData = Object.entries(stats).map(([name, value]) => ({
    name: getLabelText(name),
    value: value,
    itemStyle: {
      color: getLabelColor(name)
    }
  }))

  return {
    title: {
      text: props.title,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold'
      }
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center'
    },
    series: [
      {
        name: 'Тональность',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}: {d}%'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: chartData
      }
    ]
  }
})

const getLabelText = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive') || labelLower === 'positive') return 'Положительная'
  if (labelLower.includes('negative') || labelLower === 'negative') return 'Отрицательная'
  if (labelLower.includes('neutral') || labelLower === 'neutral') return 'Нейтральная'
  return label
}

const getLabelColor = (label) => {
  const labelLower = label?.toLowerCase() || ''
  if (labelLower.includes('positive')) return '#67c23a'
  if (labelLower.includes('negative')) return '#f56c6c'
  if (labelLower.includes('neutral')) return '#909399'
  return '#409EFF'
}
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

