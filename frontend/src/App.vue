<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="container mx-auto px-4 py-6">
      <!-- 标题 -->
      <div class="text-center mb-6">
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white mb-2">
          智能对话Agent
        </h1>
        <p class="text-gray-600 dark:text-gray-400">
          基于DeepSeek API的智能对话助手
        </p>
      </div>

      <!-- 聊天容器 -->
      <div class="max-w-4xl mx-auto">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
          <!-- 聊天消息区域 -->
          <div 
            ref="chatContainer"
            class="h-[600px] overflow-y-auto p-6 space-y-6"
          >
            <div 
              v-for="(message, index) in messages" 
              :key="index"
              class="flex"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <!-- 用户消息 -->
              <div v-if="message.role === 'user'" class="flex items-start space-x-3 max-w-2xl flex-row-reverse">
                <div class="flex-shrink-0 w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">U</span>
                </div>
                <div class="bg-blue-500 text-white px-4 py-3 rounded-2xl rounded-tl-sm">
                  <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
                </div>
              </div>
              
              <!-- AI回复 -->
              <div v-else class="flex items-start space-x-3 max-w-2xl">
                <div class="flex-shrink-0 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">AI</span>
                </div>
                <div class="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white px-4 py-3 rounded-2xl rounded-tl-sm">
                  <div class="text-sm markdown-content" v-html="renderMarkdown(message.content)"></div>
                </div>
              </div>
            </div>
            
            <!-- 加载状态 -->
            <div v-if="loading" class="flex justify-start">
              <div class="flex items-start space-x-3">
                <div class="flex-shrink-0 w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">AI</span>
                </div>
                <div class="bg-gray-100 dark:bg-gray-700 px-4 py-3 rounded-2xl rounded-tl-sm">
                  <div class="flex space-x-1">
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800">
            <div class="flex space-x-3">
              <input
                v-model="inputMessage"
                @keyup.enter="sendMessage"
                type="text"
                placeholder="输入您的消息..."
                class="flex-1 px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white text-sm"
                :disabled="loading"
              />
              <button
                @click="sendMessage"
                :disabled="!inputMessage.trim() || loading"
                class="px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
              >
                {{ loading ? '发送中...' : '发送' }}
              </button>
              <button
                @click="clearChat"
                class="px-4 py-3 bg-gray-500 text-white rounded-xl hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-colors text-sm font-medium"
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
import { marked } from 'marked'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const messages = ref<Message[]>([])
const inputMessage = ref('')
const loading = ref(false)
const chatContainer = ref<HTMLElement>()

const API_BASE_URL = 'http://localhost:8000'

// 渲染Markdown
const renderMarkdown = (content: string): string => {
  try {
    const result = marked.parse(content)
    let html = typeof result === 'string' ? result : content
    
    // 简单处理代码块，添加语言标签
    html = html.replace(
      /<pre><code class="language-(\w+)">/g,
      '<pre data-language="$1"><code>'
    )
    html = html.replace(
      /<pre><code>/g,
      '<pre data-language="text"><code>'
    )
    
    return html
  } catch (error) {
    console.error('Markdown渲染错误:', error)
    return content
  }
}

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

<style scoped>
/* Markdown样式 - DeepSeek风格 */
.markdown-content {
  line-height: 1.6;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(h1) {
  font-size: 1.4em;
  font-weight: 600;
  margin: 0.8em 0 0.4em 0;
  color: inherit;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.3em;
  text-align: left;
}

.markdown-content :deep(h2) {
  font-size: 1.2em;
  font-weight: 600;
  margin: 0.7em 0 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(h3) {
  font-size: 1.1em;
  font-weight: 600;
  margin: 0.6em 0 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(h4) {
  font-size: 1em;
  font-weight: 600;
  margin: 0.5em 0 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(p) {
  margin: 0.5em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  margin: 0.5em 0;
  padding-left: 1.5em;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(li) {
  margin: 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid #3b82f6;
  padding-left: 1em;
  margin: 0.8em 0;
  color: #6b7280;
  background-color: rgba(59, 130, 246, 0.05);
  padding: 0.8em 1em;
  border-radius: 0.5em;
  text-align: left;
}

.markdown-content :deep(code) {
  background-color: rgba(0, 0, 0, 0.08);
  padding: 0.2em 0.4em;
  border-radius: 0.25em;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace;
  font-size: 0.9em;
  color: #e11d48;
  border: 1px solid rgba(0, 0, 0, 0.1);
  text-align: left;
}

.markdown-content :deep(pre) {
  background-color: #1e293b;
  color: #e2e8f0;
  padding: 1em;
  border-radius: 0.75em;
  overflow-x: auto;
  margin: 0.8em 0;
  border: 1px solid #334155;
  position: relative;
  text-align: left;
}

.markdown-content :deep(pre::before) {
  content: attr(data-language);
  position: absolute;
  top: 0;
  right: 1em;
  background-color: #475569;
  color: #e2e8f0;
  padding: 0.2em 0.6em;
  border-radius: 0 0.5em 0 0.5em;
  font-size: 0.75em;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.markdown-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
  border-radius: 0;
  color: inherit;
  border: none;
  text-align: left;
}

.markdown-content :deep(strong) {
  font-weight: 600;
  color: inherit;
}

.markdown-content :deep(em) {
  font-style: italic;
  color: inherit;
}

.markdown-content :deep(a) {
  color: #3b82f6;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.markdown-content :deep(a:hover) {
  border-bottom-color: #3b82f6;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 0.8em 0;
  border: 1px solid #e5e7eb;
  border-radius: 0.5em;
  overflow: hidden;
}

.markdown-content :deep(th), .markdown-content :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.75em;
  text-align: left;
  color: inherit;
}

.markdown-content :deep(th) {
  background-color: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 1px solid #e5e7eb;
  margin: 1.5em 0;
}

/* 深色模式适配 */
.dark .markdown-content :deep(blockquote) {
  border-left-color: #60a5fa;
  color: #9ca3af;
  background-color: rgba(96, 165, 250, 0.1);
}

.dark .markdown-content :deep(code) {
  background-color: rgba(255, 255, 255, 0.1);
  color: #f87171;
  border-color: rgba(255, 255, 255, 0.2);
}

.dark .markdown-content :deep(pre) {
  background-color: #0f172a;
  color: #e2e8f0;
  border-color: #1e293b;
}

.dark .markdown-content :deep(pre::before) {
  background-color: #334155;
  color: #e2e8f0;
}

.dark .markdown-content :deep(table) {
  border-color: #374151;
}

.dark .markdown-content :deep(th), .dark .markdown-content :deep(td) {
  border-color: #374151;
}

.dark .markdown-content :deep(th) {
  background-color: #1f2937;
  color: #d1d5db;
}

.dark .markdown-content :deep(hr) {
  border-top-color: #374151;
}

/* 滚动条样式 */
.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: transparent;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

.dark .chat-container::-webkit-scrollbar-thumb {
  background: #4b5563;
}

.dark .chat-container::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style> 