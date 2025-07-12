<template>
  <div class="h-[90vh] bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- 背景装饰 - 进一步缩小高度 -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-10 -right-10 w-32 h-32 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
      <div class="absolute -bottom-10 -left-10 w-32 h-32 bg-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
      <div class="absolute top-10 left-10 w-32 h-32 bg-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
    </div>

    <div class="relative z-10 container mx-auto px-2 py-2">
      <!-- 标题区域 - 恢复大小 -->
      <div class="text-center mb-2">
        <div class="inline-flex items-center justify-center w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg mb-1 shadow-lg">
          <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
          </svg>
        </div>
        <h1 class="text-lg font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-0.5">
          智能对话Agent
        </h1>
        <p class="text-gray-600 dark:text-gray-400 text-xs">
          基于DeepSeek API的智能对话助手
        </p>
        <div class="flex items-center justify-center space-x-2 mt-0.5">
          <div class="w-1 h-1 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-xs text-gray-500 dark:text-gray-400">AI助手在线</span>
        </div>
      </div>

      <!-- 聊天容器 - 设置为580px -->
      <div class="max-w-5xl mx-auto">
        <div class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-xl rounded-xl shadow-lg border border-white/20 dark:border-gray-700/50 overflow-hidden">
          <!-- 聊天消息区域 - 580px高度 -->
          <div 
            ref="chatContainer"
            class="h-[580px] overflow-y-auto p-4 space-y-3 scroll-smooth"
          >
            <!-- 欢迎消息 - 恢复大小 -->
            <div v-if="messages.length === 0" class="text-center py-8">
              <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                </svg>
              </div>
              <h3 class="text-xl font-semibold text-gray-800 dark:text-white mb-2">欢迎使用智能对话助手</h3>
              <p class="text-gray-600 dark:text-gray-400 mb-6 text-sm">我可以帮助您解答问题、编写代码、分析数据等</p>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-2xl mx-auto">
                <div class="bg-gradient-to-r from-blue-50 to-blue-100 dark:from-blue-900/50 dark:to-blue-800/50 p-5 rounded-xl border border-blue-200 dark:border-blue-700 shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105 min-h-[120px] flex flex-col items-center justify-center text-center">
                  <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center mb-3">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
                    </svg>
                  </div>
                  <h4 class="font-semibold text-gray-800 dark:text-white text-sm mb-1">代码编写</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Python、JavaScript等</p>
                </div>
                <div class="bg-gradient-to-r from-purple-50 to-purple-100 dark:from-purple-900/50 dark:to-purple-800/50 p-5 rounded-xl border border-purple-200 dark:border-purple-700 shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105 min-h-[120px] flex flex-col items-center justify-center text-center">
                  <div class="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center mb-3">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                  </div>
                  <h4 class="font-semibold text-gray-800 dark:text-white text-sm mb-1">数据分析</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">图表、统计等</p>
                </div>
                <div class="bg-gradient-to-r from-green-50 to-green-100 dark:from-green-900/50 dark:to-green-800/50 p-5 rounded-xl border border-green-200 dark:border-green-700 shadow-md hover:shadow-lg transition-all duration-200 transform hover:scale-105 min-h-[120px] flex flex-col items-center justify-center text-center">
                  <div class="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center mb-3">
                    <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <h4 class="font-semibold text-gray-800 dark:text-white text-sm mb-1">问题解答</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">知识问答等</p>
                </div>
              </div>
            </div>

            <div 
              v-for="(message, index) in messages" 
              :key="index"
              class="flex animate-fade-in"
              :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
            >
              <!-- 用户消息 -->
              <div v-if="message.role === 'user'" class="flex items-start space-x-2 max-w-2xl flex-row-reverse">
                <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center shadow-md">
                  <span class="text-white text-xs font-medium">U</span>
                </div>
                <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-xl rounded-tr-sm shadow-md">
                  <p class="text-sm whitespace-pre-wrap">{{ message.content }}</p>
                </div>
              </div>
              
              <!-- AI回复 -->
              <div v-else class="flex items-start space-x-2 max-w-2xl">
                <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center shadow-md">
                  <span class="text-white text-xs font-medium">AI</span>
                </div>
                <div class="bg-white dark:bg-gray-700 text-gray-800 dark:text-white px-4 py-2 rounded-xl rounded-tl-sm shadow-md border border-gray-100 dark:border-gray-600">
                  <div class="text-sm markdown-content" v-html="renderMarkdown(message.content)"></div>
                </div>
              </div>
            </div>
            
            <!-- 加载状态 -->
            <div v-if="loading" class="flex justify-start animate-fade-in">
              <div class="flex items-start space-x-2">
                <div class="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center shadow-md">
                  <span class="text-white text-xs font-medium">AI</span>
                </div>
                <div class="bg-white dark:bg-gray-700 px-4 py-2 rounded-xl rounded-tl-sm shadow-md border border-gray-100 dark:border-gray-600">
                  <div class="flex space-x-1">
                    <div class="w-1 h-1 bg-blue-500 rounded-full animate-bounce"></div>
                    <div class="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                    <div class="w-1 h-1 bg-blue-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="border-t border-gray-200 dark:border-gray-700 p-3 bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700">
            <div class="flex space-x-2">
              <div class="flex-1 relative">
                <input
                  v-model="inputMessage"
                  @keyup.enter="sendMessage"
                  type="text"
                  placeholder="输入您的消息..."
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white text-sm bg-white dark:bg-gray-700 shadow-sm transition-all duration-200"
                  :disabled="loading"
                />
                <div class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                </div>
              </div>
              <button
                @click="sendMessage"
                :disabled="!inputMessage.trim() || loading"
                class="px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:scale-105"
              >
                {{ loading ? '发送中...' : '发送' }}
              </button>
              <button
                @click="clearChat"
                class="px-3 py-2 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-lg hover:from-gray-600 hover:to-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 transition-all duration-200 text-sm font-medium shadow-md hover:shadow-lg transform hover:scale-105"
              >
                清空
              </button>
            </div>
            <div class="mt-1 text-xs text-gray-500 dark:text-gray-400 text-center">
              按 Enter 发送消息 • 支持 Markdown 格式
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
/* 动画效果 */
@keyframes blob {
  0% {
    transform: translate(0px, 0px) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
  100% {
    transform: translate(0px, 0px) scale(1);
  }
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}

/* Markdown样式 - 美化版本 */
.markdown-content {
  line-height: 1.5;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(h1) {
  font-size: 1.2em;
  font-weight: 700;
  margin: 0.7em 0 0.3em 0;
  color: inherit;
  border-bottom: 2px solid #e5e7eb;
  padding-bottom: 0.2em;
  text-align: left;
}

.markdown-content :deep(h2) {
  font-size: 1em;
  font-weight: 600;
  margin: 0.6em 0 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(h3) {
  font-size: 0.9em;
  font-weight: 600;
  margin: 0.5em 0 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(h4) {
  font-size: 0.8em;
  font-weight: 600;
  margin: 0.4em 0 0.3em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(p) {
  margin: 0.4em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(ul), .markdown-content :deep(ol) {
  margin: 0.4em 0;
  padding-left: 1.2em;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(li) {
  margin: 0.2em 0;
  color: inherit;
  text-align: left;
}

.markdown-content :deep(blockquote) {
  border-left: 3px solid #3b82f6;
  padding-left: 0.8em;
  margin: 0.6em 0;
  color: #6b7280;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, rgba(147, 51, 234, 0.05) 100%);
  padding: 0.6em 0.8em;
  border-radius: 0.5em;
  text-align: left;
  position: relative;
}

.markdown-content :deep(blockquote::before) {
  content: '"';
  position: absolute;
  top: 0.2em;
  left: 0.2em;
  font-size: 1.2em;
  color: #3b82f6;
  opacity: 0.3;
}

.markdown-content :deep(code) {
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.05) 0%, rgba(0, 0, 0, 0.1) 100%);
  padding: 0.15em 0.3em;
  border-radius: 0.25em;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace;
  font-size: 0.8em;
  color: #e11d48;
  border: 1px solid rgba(0, 0, 0, 0.1);
  text-align: left;
}

.markdown-content :deep(pre) {
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  color: #e2e8f0;
  padding: 0.8em;
  border-radius: 0.6em;
  overflow-x: auto;
  margin: 0.6em 0;
  border: 1px solid #475569;
  position: relative;
  text-align: left;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.markdown-content :deep(pre::before) {
  content: attr(data-language);
  position: absolute;
  top: 0;
  right: 0.8em;
  background: linear-gradient(135deg, #475569 0%, #64748b 100%);
  color: #e2e8f0;
  padding: 0.15em 0.5em;
  border-radius: 0 0 0.5em 0.5em;
  font-size: 0.65em;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
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
  font-weight: 700;
  color: inherit;
}

.markdown-content :deep(em) {
  font-style: italic;
  color: inherit;
}

.markdown-content :deep(a) {
  color: #3b82f6;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
  padding-bottom: 1px;
}

.markdown-content :deep(a:hover) {
  border-bottom-color: #3b82f6;
  color: #2563eb;
}

.markdown-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin: 0.6em 0;
  border: 1px solid #e5e7eb;
  border-radius: 0.5em;
  overflow: hidden;
  box-shadow: 0 3px 5px rgba(0, 0, 0, 0.05);
}

.markdown-content :deep(th), .markdown-content :deep(td) {
  border: 1px solid #e5e7eb;
  padding: 0.6em;
  text-align: left;
  color: inherit;
}

.markdown-content :deep(th) {
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  font-weight: 700;
  color: #374151;
}

.markdown-content :deep(hr) {
  border: none;
  border-top: 2px solid #e5e7eb;
  margin: 1.2em 0;
  position: relative;
}

.markdown-content :deep(hr::after) {
  content: '';
  position: absolute;
  top: -1px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 1px;
}

/* 深色模式适配 */
.dark .markdown-content :deep(blockquote) {
  border-left-color: #60a5fa;
  color: #9ca3af;
  background: linear-gradient(135deg, rgba(96, 165, 250, 0.1) 0%, rgba(168, 85, 247, 0.1) 100%);
}

.dark .markdown-content :deep(code) {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.15) 100%);
  color: #f87171;
  border-color: rgba(255, 255, 255, 0.2);
}

.dark .markdown-content :deep(pre) {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  border-color: #334155;
}

.dark .markdown-content :deep(pre::before) {
  background: linear-gradient(135deg, #334155 0%, #475569 100%);
  color: #e2e8f0;
}

.dark .markdown-content :deep(table) {
  border-color: #374151;
}

.dark .markdown-content :deep(th), .dark .markdown-content :deep(td) {
  border-color: #374151;
}

.dark .markdown-content :deep(th) {
  background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
  color: #d1d5db;
}

.dark .markdown-content :deep(hr) {
  border-top-color: #374151;
}

/* 滚动条样式 */
.chat-container::-webkit-scrollbar {
  width: 4px;
}

.chat-container::-webkit-scrollbar-track {
  background: transparent;
}

.chat-container::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #d1d5db 0%, #9ca3af 100%);
  border-radius: 2px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #9ca3af 0%, #6b7280 100%);
}

.dark .chat-container::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #4b5563 0%, #6b7280 100%);
}

.dark .chat-container::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
}
</style> 