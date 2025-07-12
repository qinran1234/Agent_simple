<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="container mx-auto px-4 py-8">
      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-800 dark:text-white mb-2">
          智能对话Agent
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          基于DeepSeek API的智能对话助手
        </p>
      </div>

      <!-- 聊天容器 -->
      <div class="max-w-4xl mx-auto">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
          <!-- 聊天消息区域 -->
          <div 
            ref="chatContainer"
            class="h-96 overflow-y-auto p-6 space-y-4"
          >
            <div 
              v-for="(message, index) in messages" 
              :key="index"
              class="flex"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <div 
                class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
                :class="message.role === 'user' 
                  ? 'bg-blue-500 text-white' 
                  : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-white'"
              >
                <p class="text-sm">{{ message.content }}</p>
              </div>
            </div>
            
            <!-- 加载状态 -->
            <div v-if="loading" class="flex justify-start">
              <div class="bg-gray-200 dark:bg-gray-700 px-4 py-2 rounded-lg">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="border-t border-gray-200 dark:border-gray-700 p-4">
            <div class="flex space-x-4">
              <input
                v-model="inputMessage"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="输入您的消息..."
                class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
                :disabled="loading"
              />
              <button
                @click="sendMessage"
                :disabled="!inputMessage.trim() || loading"
                class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {{ loading ? '发送中...' : '发送' }}
              </button>
              <button
                @click="clearChat"
                class="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors"
              >
                清空
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<Message[]>([])
const inputMessage = ref('')
const loading = ref(false)
const chatContainer = ref<HTMLElement>()

const API_BASE_URL = 'http://localhost:8000'

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || loading.value) return

  const userMessage = inputMessage.value.trim()
  messages.value.push({
    role: 'user',
    content: userMessage
  })

  inputMessage.value = ''
  loading.value = true

  try {
            const response = await axios.post(`${API_BASE_URL}/chat/`, {
          message: userMessage
        })

    messages.value.push({
      role: 'assistant',
      content: response.data.response
    })
  } catch (error) {
    console.error('发送消息失败:', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后重试。'
    })
  } finally {
    loading.value = false
    await scrollToBottom()
  }
}

const clearChat = async () => {
  try {
    await axios.post(`${API_BASE_URL}/chat/clear`)
    messages.value = []
  } catch (error) {
    console.error('清空对话失败:', error)
  }
}

onMounted(() => {
  scrollToBottom()
})
</script> 