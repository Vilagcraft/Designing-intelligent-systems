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
import { LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  GridComponent,
  LegendComponent,
  DataZoomComponent
])

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  title: {
    type: String,
    default: 'График уверенности модели'
  }
})

const chartOption = computed(() => {
  const confidenceData = props.data.map((item, index) => {
    // Получаем уверенность из разных источников
    let confidence = 0
    if (item.confidence !== undefined) {
      confidence = item.confidence
    } else if (item.probs && Array.isArray(item.probs) && item.probs.length > 0) {
      confidence = Math.max(...item.probs)
    }
    return {
      index: index + 1,
      confidence: (confidence * 100).toFixed(2),
      label: item.label
    }
  })

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
      formatter: function(params) {
        const data = params[0]
        return `Текст #${data.name}<br/>Уверенность: ${data.value}%`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: confidenceData.map(d => d.index),
      name: 'Номер текста'
    },
    yAxis: {
      type: 'value',
      name: 'Уверенность (%)',
      min: 0,
      max: 100
    },
    dataZoom: [
      {
        type: 'slider',
        start: 0,
        end: 100
      }
    ],
    visualMap: {
      show: false,
      dimension: 1,
      pieces: [
        { lte: 50, color: '#f56c6c' },
        { gt: 50, lte: 75, color: '#e6a23c' },
        { gt: 75, color: '#67c23a' }
      ]
    },
    series: [
      {
        name: 'Уверенность',
        type: 'line',
        data: confidenceData.map(d => d.confidence),
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 2
        },
        areaStyle: {
          opacity: 0.3
        },
        emphasis: {
          focus: 'series',
          itemStyle: {
            borderWidth: 3
          }
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

