<template>
  <div class="chat-container">
    <div class="chat-box">
      <div class="messages" ref="messagesRef">
        <div v-if="messages.length === 0" class="empty-state">
          <el-icon :size="60" color="#30363d"><ChatDotRound /></el-icon>
          <p>开始您的提问，我将基于知识库为您解答。</p>
        </div>
        
        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          class="message-item"
          :class="msg.role"
        >
          <div class="avatar">
            <el-avatar :icon="msg.role === 'user' ? 'User' : 'Service'" :style="{ backgroundColor: msg.role === 'user' ? '#2f8f72' : '#8bbba9' }" />
          </div>
          <div class="content">
            <div class="bubble">
              <div v-if="msg.loading" class="typing-indicator">
                <span></span><span></span><span></span>
              </div>
              <div v-else v-html="formatContent(msg.content)"></div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="input-area">
        <el-input
          v-model="input"
          placeholder="请输入您的问题..."
          :rows="3"
          type="textarea"
          resize="none"
          @keydown.enter.prevent="handleSend"
        />
        <el-button type="primary" class="send-btn" @click="handleSend" :loading="loading" :disabled="!input.trim()">
          <el-icon><Position /></el-icon> 发送
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { queryKnowledge } from '@/api/knowledge'
import { User, Service, Position, ChatDotRound } from '@element-plus/icons-vue'
import { marked } from 'marked'

const input = ref('')
const loading = ref(false)
const messages = ref([])
const messagesRef = ref(null)

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

const formatContent = (text) => {
  return marked(text)
}

const handleSend = async () => {
  if (!input.value.trim() || loading.value) return
  
  const question = input.value
  input.value = ''
  
  messages.value.push({
    role: 'user',
    content: question
  })
  scrollToBottom()
  
  loading.value = true
  messages.value.push({
    role: 'assistant',
    content: '',
    loading: true
  })
  scrollToBottom()
  
  try {
    const res = await queryKnowledge({ question })
    const botMsg = messages.value[messages.value.length - 1]
    botMsg.loading = false
    botMsg.content = res.answer
  } catch (error) {
    const botMsg = messages.value[messages.value.length - 1]
    botMsg.loading = false
    botMsg.content = '抱歉，查询出错，请稍后重试。'
  } finally {
    loading.value = false
    scrollToBottom()
  }
}
</script>

<style lang="scss" scoped>
.chat-container {
  height: calc(100vh - 56px);
  max-width: 1080px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.chat-box {
  flex: 1;
  background-color: #fff;
  border: 1px solid #e0e9e5;
  border-radius: 18px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 12px 36px rgba(49,77,67,.06);
}

.messages {
  flex: 1;
  padding: 28px;
  overflow-y: auto;
  
  .empty-state {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #82938d;
    
    p {
      margin-top: 20px;
    }
  }
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  
  &.user {
    flex-direction: row-reverse;
    
    .content {
      align-items: flex-end;
      
      .bubble {
        background-color: #2f8f72;
        color: #fff;
        border-top-right-radius: 0;
      }
    }
    
    .avatar {
      margin-left: 10px;
      margin-right: 0;
    }
  }
  
  &.assistant {
    .content {
      align-items: flex-start;
      
      .bubble {
        background-color: #f7faf8;
        color: #344a42;
        border: 1px solid #e7eeea;
        border-top-left-radius: 0;
      }
    }
    
    .avatar {
      margin-right: 10px;
    }
  }
}

.content {
  display: flex;
  flex-direction: column;
  max-width: 70%;
  
  .bubble {
    padding: 12px 16px;
    border-radius: 15px;
    line-height: 1.65;
    font-size: 15px;
    word-break: break-word;

    

    :deep(p) {
      margin: 0 0 10px 0;
      &:last-child {
        margin-bottom: 0;
      }
    }

    :deep(a) {
      color: #2f8f72;
      text-decoration: none;
      &:hover {
        text-decoration: underline;
      }
    }
    
    :deep(ul), :deep(ol) {
      padding-left: 20px;
      margin: 5px 0;
    }
    
    :deep(code) {
      color: #26755d;
      background-color: #eaf3ef;
      padding: 0.2em 0.4em;
      border-radius: 6px;
      font-family: monospace;
    }
    
    :deep(pre) {
      background-color: #f0f5f2;
      padding: 10px;
      border-radius: 6px;
      overflow-x: auto;
      
      code {
        background-color: transparent;
        padding: 0;
      }
    }
    
    :deep(img) {
      max-width: 100%;
      border-radius: 6px;
      margin: 10px 0;
    }
  }
}

.input-area {
  padding: 18px 20px;
  background-color: #fbfcfb;
  border-top: 1px solid #edf2ef;
  display: flex;
  gap: 10px;
  align-items: flex-end;
  
  :deep(.el-textarea__inner) {
    min-height: 66px !important;
    padding: 14px 16px;
    background-color: #fff;
    color: #31473f;
    border-radius: 13px;
    box-shadow: 0 0 0 1px #dbe6e1 inset;
    
    &:focus {
      box-shadow: 0 0 0 1px #68a890 inset, 0 0 0 3px rgba(47,143,114,.08);
    }
  }
  
  .send-btn {
    height: 44px;
    padding: 0 20px;
    background: #2f8f72;
    border: 0;
    border-radius: 11px;
  }
}

.typing-indicator {
  span {
    display: inline-block;
    width: 6px;
    height: 6px;
    background-color: #72a391;
    border-radius: 50%;
    margin: 0 2px;
    animation: bounce 1.4s infinite ease-in-out both;
    
    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
  }
}

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}
</style>
