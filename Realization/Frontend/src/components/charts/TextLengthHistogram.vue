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
import { computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  BarChart,
  TitleComponent,
  TooltipComponent,
  GridComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'Распределение длины текстов'
  }
})

const chartOption = computed(() => {
  // Подсчитываем длину каждого текста
  const lengths = props.data.map(item => item.text?.length || 0)
  
  // Создаем интервалы (bins)
  const maxLength = Math.max(...lengths)
  const binSize = Math.ceil(maxLength / 10)
  const bins = {}
  
  lengths.forEach(length => {
    const bin = Math.floor(length / binSize) * binSize
    bins[bin] = (bins[bin] || 0) + 1
  })
  
  const categories = Object.keys(bins).sort((a, b) => a - b).map(b => `${b}-${parseInt(b) + binSize}`)
  const values = Object.keys(bins).sort((a, b) => a - b).map(k => bins[k])

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
      trigger: 'axis',
      formatter: '{b}<br/>Количество: {c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      name: 'Длина текста (символы)',
      axisLabel: {
        interval: 0,
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: 'Количество текстов'
    },
    series: [
      {
        name: 'Количество',
        type: 'bar',
        data: values,
        itemStyle: {
          color: '#409EFF'
        },
        label: {
          show: true,
          position: 'top'
        }
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

