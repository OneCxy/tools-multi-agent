<template>
  <div class="app-container">
    

    <div v-if="!isLoggedIn" class="login-container">
      <div class="login-form">
        <div class="app-logo login-logo">
            <img src="/cutting-tool-logo.svg" alt="数控刀具系统图标" width="60" height="60"/>
          </div>
        <h1 class="login-title">数控刀具智能问询系统</h1>
        <div class="login-input-group">
          <label for="username">用户名</label>
          <input 
            id="username"
            v-model="username"
            type="text"
            placeholder="请输入用户名"
            @keyup.enter="handleLogin"
          />
        </div>
        <div class="login-input-group">
          <label for="password">密码</label>
          <input 
            id="password"
            v-model="password"
            type="password"
            placeholder="请输入密码"
            @keyup.enter="handleLogin"
          />
        </div>
        <div v-if="loginError" class="login-error">
          {{ loginError }}
        </div>
        <button class="login-button btn-primary" @click="handleLogin">
          登录
        </button>
        <div class="login-hint">
          <p>测试用户：root1, root2, root3</p>
          <p>密码：123456</p>
        </div>
      </div>
    </div>
    
    

    <template v-else>
      

      
      <div class="main-content">
        

        <div class="sidebar-wrapper">
          

          <div class="sidebar-content" :class="{ 'expanded': isSidebarExpanded }">
            

            <div class="app-branding">
              

              <div class="app-logo">
                <img src="/cutting-tool-logo.svg" alt="数控刀具系统图标" width="40" height="40"/>
              </div>
              <div v-show="isSidebarExpanded" class="sidebar-text-content">
                <strong class="brand-name">数控刀具智能问询系统</strong>
              </div>
              
              

              <button 
                class="toggle-sidebar-btn" 
                @click="toggleSidebar"
                :title="isSidebarExpanded ? '收起侧边栏' : '展开侧边栏'"
              >
                {{ isSidebarExpanded ? '‹' : '›' }}
              </button>
            </div>
            
            

            <div class="session-button-container" v-show="isSidebarExpanded">
              <a href="/" class="new-chat-btn" @click.prevent="createNewSession">
                <span class="icon">
                  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" role="img" style="" width="20" height="20" viewBox="0 0 1024 1024" name="AddConversation" class="iconify new-icon" data-v-9f34fd85="">
                    <path d="M475.136 561.152v89.74336c0 20.56192 16.50688 37.23264 36.864 37.23264s36.864-16.67072 36.864-37.23264v-89.7024h89.7024c20.60288 0 37.2736-16.54784 37.2736-36.864 0-20.39808-16.67072-36.864-37.2736-36.864H548.864V397.63968A37.0688 37.0688 0 0 0 512 360.448c-20.35712 0-36.864 16.67072-36.864 37.2736v89.7024H385.4336a37.0688 37.0688 0 0 0-37.2736 36.864c0 20.35712 16.67072 36.864 37.2736 36.864h89.7024z" fill="currentColor"></path>
                    <path d="M512 118.784c-223.96928 0-405.504 181.57568-405.504 405.504 0 78.76608 22.44608 152.3712 61.35808 214.6304l-44.27776 105.6768a61.44 61.44 0 0 0 56.68864 85.1968H512c223.92832 0 405.504-181.53472 405.504-405.504 0-223.92832-181.57568-405.504-405.504-405.504z m-331.776 405.504a331.776 331.776 0 1 1 331.73504 331.776H198.656l52.59264-125.5424-11.59168-16.62976A330.09664 330.09664 0 0 1 180.224 524.288z" fill="currentColor"></path>
                  </svg>
                </span>
                <span class="text">新建会话</span>
                <span class="shortcut">
                  <span class="key">Ctrl</span>
                  <span>+</span>
                  <span class="key">K</span>
                </span>
              </a>
            </div>
            
            

            <div class="navigation-container" v-show="isSidebarExpanded">
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'knowledge' }" @click="handleCuttingToolConsultation">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="nav-icon">
                  <path fill="currentColor" fill-rule="evenodd" d="M3.75 7h16.563c0 .48-.007 1.933-.016 3.685.703.172 1.36.458 1.953.837V5.937a2 2 0 0 0-2-2h-6.227a3 3 0 0 1-1.015-.176L9.992 2.677A3 3 0 0 0 8.979 2.5h-5.23a2 2 0 0 0-1.999 2v14.548a2 2 0 0 0 2 2h10.31a6.5 6.5 0 0 1-1.312-2H3.75S3.742 8.5 3.75 7m15.002 14.5a.514.514 0 0 0 .512-.454c.24-1.433.451-2.169.907-2.625.454-.455 1.186-.666 2.611-.907a.513.513 0 0 0-.002-1.026c-1.423-.241-2.155-.453-2.61-.908-.455-.457-.666-1.191-.906-2.622a.514.514 0 0 0-.512-.458.52.52 0 0 0-.515.456c-.24 1.432-.452 2.167-.907 2.624-.454.455-1.185.667-2.607.909a.514.514 0 0 0-.473.513.52.52 0 0 0 .47.512c1.425.24 2.157.447 2.61.9.455.454.666 1.19.907 2.634a.52.52 0 0 0 .515.452" clip-rule="evenodd"></path>
                </svg>
                <span class="nav-text">刀具技术咨询</span>
              </div>
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'sales' }" @click="handleSalesOrder">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="nav-icon">
                  <path fill="currentColor" fill-rule="evenodd" d="M12 20.571a8.5 8.5 0 0 1 2.5-6.08c1.43-1.429 3.5-2.49 6.071-2.491-2.571.002-4.617-1.075-6.05-2.508S12 6 12 3.428C12 6 10.954 8.095 9.517 9.532 8.081 10.968 6 12 3.428 12a8.52 8.52 0 0 1 6.082 2.516c1.43 1.43 2.487 3.484 2.49 6.055m-9.853-7.314c3.485.588 5.053 1.331 6.163 2.44s1.847 2.667 2.435 6.198c.105.627.603 1.105 1.26 1.105.664 0 1.156-.479 1.25-1.11.588-3.502 1.329-5.085 2.441-6.2 1.111-1.114 2.677-1.845 6.16-2.433.638-.075 1.144-.586 1.144-1.253 0-.668-.5-1.188-1.147-1.254-3.481-.59-5.026-1.347-6.137-2.46-1.112-1.115-1.872-2.674-2.46-6.171C13.16 1.482 12.671 1 12.003 1c-.66 0-1.155.481-1.259 1.114-.588 3.5-1.323 5.087-2.435 6.203C7.2 9.43 5.632 10.159 2.156 10.75 1.503 10.816 1 11.333 1 12.004c0 .68.52 1.17 1.147 1.253" clip-rule="evenodd"></path>
                </svg>
                <span class="nav-text">销售报价与订单</span>
              </div>
              <div class="navigation-item" :class="{ 'selected': selectedNavItem === 'supplier' }" @click="handleSupplierLocator">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24" class="nav-icon">
                  <path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5Z"></path>
                </svg>
                <span class="nav-text">附近刀具供应商</span>
              </div>
              

            </div>

            

            <div v-show="isSidebarExpanded" class="sidebar-main">
              <div class="navigation-item" @click="toggleSessions">
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 1024 1024" class="nav-icon">
                  <path d="M512 81.066667c-233.301333 0-422.4 189.098667-422.4 422.4s189.098667 422.4 422.4 422.4 422.4-189.098667 422.4-422.4-189.098667-422.4-422.4-422.4z m-345.6 422.4a345.6 345.6 0 1 1 691.2 0 345.6 345.6 0 1 1-691.2 0z m379.733333-174.933334a38.4 38.4 0 0 0-76.8 0v187.733334a38.4 38.4 0 0 0 11.264 27.136l93.866667 93.866666a38.4 38.4 0 1 0 54.272-54.272L546.133333 500.352V328.533333z" fill="currentColor"></path>
                </svg>
                <span class="nav-text">历史会话</span>
              </div>
              <div class="sessions-list" v-show="showSessions">
                <div v-if="isLoadingSessions" class="loading-sessions">
                  加载历史对话中...
                </div>
                <div v-else-if="sessions.length === 0" class="no-sessions">
                  暂无历史对话
                </div>
                <div
                  v-for="session in sessions"
                  :key="session.session_id"
                  :class="['session-item', { 'selected': session.session_id === selectedSessionId }]"
                  @click="selectSession(session.session_id)"
                >
                  <div class="session-info">
                    <div style="display: flex; align-items: center; gap: 8px;">
                      <span class="session-icon" aria-hidden="true">◷</span>
                      <div class="session-preview">{{ session.memory[0]?.content || '空对话' }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          

        </div>
        
        

        <div class="main-container">
          

          <div class="result-container" :class="{ 'processing': isProcessing }">
            

            <div class="top-user-section">
              

              <div class="user-avatar-container" ref="avatarContainerRef">
                

                <button
                  type="button"
                  class="user-avatar"
                  aria-label="打开用户菜单"
                  @click="toggleUserInfo"
                >{{ currentUser ? currentUser.slice(0, 1).toUpperCase() : 'U' }}</button>
                
                

                <div class="user-info-dropdown" v-show="showUserInfo">
                  <template v-if="currentUser">
                    <span class="user-name">{{ currentUser }}</span>
                    <button data-testid="setup_logout" class="btn-tertiary" style="width: 100%; justify-content: flex-start;" @click="handleLogout"><span role="img" class="semi-icon semi-icon-default text-16"><svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" fill="none" viewBox="0 0 24 24"><path fill="currentColor" fill-rule="evenodd" d="M14 3H4.5v18H14v-5h2v5a2 2 0 0 1-2 2H4.5a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2H14a2 2 0 0 1 2 2v5h-2zm5.207 4.793a1 1 0 1 0-1.414 1.414L19.586 11H10.5a1 1 0 1 0 0 2h9.086l-1.793 1.793a1 1 0 0 0 1.414 1.414l3.5-3.5a1 1 0 0 0 0-1.414z" clip-rule="evenodd"></path></svg></span>退出登录</button>
                  </template>
                  <template v-else>
                    <span class="user-name">当前未登录</span>
                    <button class="login-button btn-primary" @click="goToLogin">请登录</button>
                  </template>
                </div>
              </div>
            </div>

          
            
            

            <div class="chat-message-container" ref="processContent">
              <div v-if="chatMessages.length === 0" class="welcome-state">
                <div class="welcome-mark">✦</div>
                <span class="welcome-eyebrow">数控刀具智能问询系统</span>
                <h2>今天想了解哪类刀具问题？</h2>
                <p>从选型、切削参数到供应商查询，我会结合知识库给出清晰、可执行的建议。</p>
                <div class="quick-prompts">
                  <button type="button" @click="userInput = '帮我推荐适合 45 钢精加工的刀具'">45 钢精加工选型</button>
                  <button type="button" @click="userInput = '如何设置合理的切削速度和进给量？'">切削参数建议</button>
                  <button type="button" @click="userInput = '分析一下刀具磨损过快的常见原因'">刀具磨损分析</button>
                </div>
              </div>
              <div v-for="(msg, index) in chatMessages" :key="index" :class="['message-wrapper', msg.type]">
                 

                 <div class="message-role-label" v-if="msg.type === 'THINKING'" @click="toggleThinking(index)">
                   <div class="thinking-header">
                     <span class="thinking-text">{{ isProcessing && index === chatMessages.length - 1 ? '思考中...' : '思考过程' }}</span>
                     <svg 
                       xmlns="http://www.w3.org/2000/svg" 
                       width="16" 
                       height="16" 
                       viewBox="0 0 24 24" 
                       fill="none" 
                       stroke="currentColor" 
                       stroke-width="2" 
                       stroke-linecap="round" 
                       stroke-linejoin="round"
                       class="thinking-icon"
                       :class="{ 'collapsed': msg.collapsed }"
                     >
                       <polyline points="6 9 12 15 18 9"></polyline>
                     </svg>
                   </div>
                 </div>
                 
                 

                 <div class="message-content" v-show="msg.type !== 'THINKING' || !msg.collapsed">
                   <div class="markdown-body" v-html="renderMarkdown(msg.content)"></div>
                 </div>
              </div>
            </div>
              
              

              <div class="input-container">
                <div class="textarea-with-button">
                  <textarea
                    v-model="userInput"
                    placeholder="请输入您的请求..."
                    @keyup.enter.exact="handleSend($event)"
                    :disabled="isProcessing"
                  ></textarea>
                  <button 
                    class="send-button btn-primary"
                    :class="{ 'cancel-button': isProcessing, 'disabled': !userInput.trim() && !isProcessing }"
                    :disabled="!userInput.trim() && !isProcessing"
                    @click="isProcessing ? handleCancel() : handleSend()"
                  >
                    {{ isProcessing ? '■' : '发送' }}
                  </button>
                </div>
              </div>
          </div>
        </div>
      </div>
      </template>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue';
import { marked } from 'marked';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

marked.setOptions({
  breaks: true, // Enable line breaks
  gfm: true,    // Enable GitHub Flavored Markdown
});

const renderMarkdown = (text) => {
  if (!text) return '';
  try {
    return marked.parse(text);
  } catch (e) {
    console.error('Markdown parsing error:', e);
    return text;
  }
};

export default {
  name: 'App',
  setup() {
    const isLoggedIn = ref(true);
    const isSidebarExpanded = ref(true);
    const username = ref('');
    const password = ref('');
    const currentUser = ref('');
    const loginError = ref('');
    const showUserInfo = ref(false);
    const avatarContainerRef = ref(null);
    
    const toggleUserInfo = () => {
      showUserInfo.value = !showUserInfo.value;
    };

    const handleClickOutside = (event) => {
      if (showUserInfo.value && avatarContainerRef.value && !avatarContainerRef.value.contains(event.target)) {
        showUserInfo.value = false;
      }
      

    };
    
    onMounted(() => {
      document.addEventListener('click', handleClickOutside);
    });
    
    onUnmounted(() => {
      document.removeEventListener('click', handleClickOutside);
    });
    
    const savedUserId = localStorage.getItem('currentUserId');
    if (savedUserId) {
      const validUsers = [
        { username: 'root1', password: '123456', userId: 'root1' },
        { username: 'root2', password: '123456', userId: 'root2' },
        { username: 'root3', password: '123456', userId: 'root3' }
      ];
      
      const savedUser = validUsers.find(u => u.userId === savedUserId);
      if (savedUser) {
        currentUser.value = savedUser.username;
      }
    }
    
    const userInput = ref('');
    const chatMessages = ref([]); // Unified chat history: { type: 'user'|'assistant'|'THINKING'|'PROCESS', content: string }
    const processMessages = ref([]); // Deprecated, kept for safety
    const answerText = ref(''); // Deprecated, kept for safety
    const processContent = ref(null);
    const isProcessing = ref(false); // 标记是否正在处理请求
    let reader = null; // 保存读取器引用，用于取消请求
    
    const selectedNavItem = ref('');
    


    const toggleThinking = (index) => {
      const msg = chatMessages.value[index];
      if (msg && msg.type === 'THINKING') {
        msg.collapsed = !msg.collapsed;
      }
    };
    
    

    
    const handleCuttingToolConsultation = () => {
      console.log('打开刀具技术咨询');
      processMessages.value = [];
      answerText.value = '';
      processContent.value = null;
      selectedNavItem.value = 'knowledge';
      selectedSessionId.value = '';
    };
    
    const handleSalesOrder = () => {
      console.log('打开销售报价与订单');
      processMessages.value = [];
      answerText.value = '';
      processContent.value = null;
      selectedNavItem.value = 'sales';
      selectedSessionId.value = '';
    };

    const handleSupplierLocator = () => {
      console.log('打开附近刀具供应商查询');
      processMessages.value = [];
      answerText.value = '';
      processContent.value = null;
      selectedNavItem.value = 'supplier';
      selectedSessionId.value = '';
    };
    
    const sessions = ref([]);
    const selectedSessionId = ref('');
    const isLoadingSessions = ref(false);
    const showSessions = ref(true); // 控制历史会话的显示/隐藏
    
    const toggleSessions = () => {
      showSessions.value = !showSessions.value;
    };

    const handleLogin = () => {
      loginError.value = '';
      
      const validUsers = [
        { username: 'root1', password: '123456', userId: 'root1' },
        { username: 'root2', password: '123456', userId: 'root2' },
        { username: 'root3', password: '123456', userId: 'root3' }
      ];
      
      const user = validUsers.find(u => u.username === username.value && u.password === password.value);
      
      if (user) {
        isLoggedIn.value = true;
        currentUser.value = user.username;
        localStorage.setItem('currentUserId', user.userId);
        window.scrollTo(0, 0);
        username.value = '';
        password.value = '';
      } else {
        loginError.value = '用户名或密码错误';
      }
    };

    const fetchUserSessions = async () => {
      if (!currentUser.value) return;
      
      isLoadingSessions.value = true;
      try {
        const response = await fetch(`${API_BASE_URL}/api/user_sessions`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({"user_id": currentUser.value})
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        if (data.success && data.sessions) {
          sessions.value = data.sessions;
          if (data.sessions.length > 0 && !selectedSessionId.value) {
            selectSession(data.sessions[0].session_id);
          }
        }
      } catch (error) {
        console.error('Error fetching sessions:', error);
      } finally {
        isLoadingSessions.value = false;
        scrollToBottom();
      }
    };


    
    const createNewSession = () => {
      const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      
      const newSession = {
        session_id: newSessionId,
        create_time: new Date().toISOString(),
        memory: [],
        total_messages: 0
      };
      
      sessions.value.unshift(newSession);
      
      processMessages.value = [];
      answerText.value = '';
      userInput.value = '';
      
      selectSession(newSessionId);
    };
    
    const selectSession = (sessionId) => {
      selectedSessionId.value = sessionId;
      selectedNavItem.value = '';
      const session = sessions.value.find(s => s.session_id === sessionId);
      
      chatMessages.value = [];
      processMessages.value = [];
      answerText.value = '';
      
      if (session && session.memory && Array.isArray(session.memory) && session.memory.length > 0) {
        let lastType = null;
        
        session.memory.forEach(msg => {
          if (!msg || !msg.content) return;
          
          let type = msg.role;
          if (type === 'process') type = 'THINKING';
          
          if (type === 'THINKING' && lastType === 'THINKING') {
            const lastMsg = chatMessages.value[chatMessages.value.length - 1];
            lastMsg.content += '\n' + msg.content;
          } else {
            chatMessages.value.push({
              type: type, // 'user', 'assistant', 'THINKING'
              content: msg.content
            });
          }
          lastType = type;
        });
        
        nextTick(() => {
          scrollToBottom();
        });
      }
    };
    
    const handleLogout = () => {
      isLoggedIn.value = false;
      currentUser.value = '';
      localStorage.removeItem('currentUserId');
      processMessages.value = [];
      answerText.value = '';
      userInput.value = '';
      sessions.value = [];
      selectedSessionId.value = '';
    };
    
    const goToLogin = () => {
      isLoggedIn.value = false;
      currentUser.value = '';
      localStorage.removeItem('currentUserId');
    };
    
      const handleSend = async (event) => {
        if (event) {
          event.preventDefault();
        }
        if (!userInput.value.trim()) return;
        
        window.scrollTo(0, 0);
        
        const userId = localStorage.getItem('currentUserId');
        if (!userId) {
          isLoggedIn.value = false;
          return;
        }
        
        isProcessing.value = true;
        
        chatMessages.value.forEach(msg => {
          if (msg.type === 'THINKING') {
            msg.collapsed = true;
          }
        });
        
        processMessages.value = [];
        
        chatMessages.value.push({
          type: 'user',
          content: userInput.value.trim()
        });
        
        const userMessage = `<div class="user-message">${userInput.value.trim()}</div>\n\n`;
        if (selectedSessionId.value && answerText.value) {
          answerText.value += userMessage;
        } else {
          answerText.value = userMessage;
        }
        
        const finalUserId = userId || currentUser.value;
        
        scrollToBottom();
        
        const requestData = {
          query: userInput.value.trim(),
          context: { 
            user_id: finalUserId,
            session_id: selectedSessionId.value || ''
          }
        };
        

        
        console.log('发送请求，会话ID:', selectedSessionId.value);
        
        console.log('发送请求，用户ID:', finalUserId);
        
        try {
          const response = await fetch(`${API_BASE_URL}/api/query`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
          });
          
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          
        reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
          const { done, value } = await reader.read();
          
          if (done) {
              if (buffer.trim()) {
                processSSEData(buffer);
                buffer = ''; // 清空缓冲区
              }
              break;
            }
          
          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;
          
          const lines = buffer.split('\n');
          
          for (let i = 0; i < lines.length - 1; i++) {
            const line = lines[i];
            if (line.trim()) {
              processSSEData(line);
            }
          }
          
          buffer = lines[lines.length - 1];
        }
          
        } catch (error) {
          if (!error.name || error.name !== 'AbortError') {
            const errorMsg = `请求失败: ${error.message}`;
            streamTextToProcess(errorMsg + '\n');
            processMessages.value.push({
              type: 'PROCESS',
              text: errorMsg
            });
            console.error('Error:', error);
          }
        } finally {
          isProcessing.value = false;
          reader = null;
          
          scrollToBottom();

          
          fetchUserSessions();
        }
        
        userInput.value = '';
      };
      
    const processSSEData = (data) => {
      try {
        if (typeof data !== 'string') return;

        if (data.startsWith('data:')) {
          const jsonStr = data.substring(5).trim();

          if (jsonStr) {
            try {
              const parsedData = JSON.parse(jsonStr);

              let kind; // 变量名改为 kind
              let text;

              if (parsedData.content && typeof parsedData.content === 'object') {
                text = parsedData.content.text;

                if (parsedData.content.kind) {
                  kind = parsedData.content.kind;
                } else if (parsedData.content.type) {
                  kind = parsedData.content.type;
                }

                if (parsedData.status === 'FINISHED' || parsedData.content.contentType === 'sagegpt/finish') {
                   return;
                }
              }

              else if (parsedData.type && parsedData.content) {
                kind = parsedData.type;
                text = parsedData.content;
              }

              if (kind && text) {

                switch (kind) {
                  case 'ANSWER':
                    stopThinkingAnimation();
                    streamTextToAnswer(text);
                    break;

                  case 'THINKING':
                    streamTextToProcess(text);
                    break;

                  case 'PROCESS':
                    streamTextToProcess(text + '\n');
                    processMessages.value = [...processMessages.value, {
                      type: 'PROCESS', // 前端内部状态可以暂时保留叫 type，或者你也想改成 kind？建议暂时不动内部状态
                      text: text
                    }];
                    scrollToBottom();
                    break;

                  default:
                    console.log('Unknown content kind:', kind);
                    streamTextToProcess(text + '\n');
                }
              }
            } catch (jsonError) {
              console.error('JSON parse error:', jsonError);
            }
          }
        }
      } catch (error) {
        console.error('Error processing SSE data:', error);
      }
    };
      
      const handleCancel = () => {
        if (reader) {
          reader.cancel();
          reader = null;
        }
        isProcessing.value = false;
        stopThinkingAnimation();
        
        streamTextToProcess('请求已取消\n');
        processMessages.value.push({
          type: 'PROCESS',
          text: '请求已取消'
        });
      };


    const streamTextToAnswer = (text) => {
      const lastMsg = chatMessages.value[chatMessages.value.length - 1];
      if ((!text || !text.trim()) && lastMsg && lastMsg.type !== 'assistant') {
        return;
      }

      text = text
      .replace(/ +/g, ' ')  // 将多个连续空白字符（包括空格、制表符等）替换为单个空格
      .replace(/\n+/g, '\n'); // 将多个连续换行符替换为单个换行符
      
      if (lastMsg && lastMsg.type === 'assistant') {
        lastMsg.content += text;
      } else {
        chatMessages.value.push({ type: 'assistant', content: text });
      }
      chatMessages.value = [...chatMessages.value]; // Trigger reactivity
      
      answerText.value += text;
      
      scrollToBottom();
    };
    
    const streamTextToProcess = (text) => {
      const lastMsg = chatMessages.value[chatMessages.value.length - 1];
      if (lastMsg && lastMsg.type === 'THINKING') {
        lastMsg.content += text;
        if (isProcessing.value && lastMsg.collapsed === undefined) {
           lastMsg.collapsed = false;
        }
      } else {
        chatMessages.value.push({ 
          type: 'THINKING', 
          content: text,
          collapsed: false // 默认为展开状态
        });
      }
      chatMessages.value = [...chatMessages.value];
      
      const lastProcessMsg = processMessages.value[processMessages.value.length - 1];
      if (lastProcessMsg && lastProcessMsg.type === 'THINKING') {
        lastProcessMsg.text += text;
        processMessages.value = [...processMessages.value];
      } else {
        processMessages.value = [...processMessages.value, {
          type: 'THINKING',
          text: text
        }];
      }
      
      scrollToBottom();
    };
    
    const startThinkingAnimation = () => {
    };
    
    const stopThinkingAnimation = () => {
    };
    
      
      const handleResponseData = (data) => {
        if (data.type === 'ANSWER') {
          stopThinkingAnimation();
          streamTextToAnswer(data.content);
        } else if (data.type === 'THINKING') {
          streamTextToProcess(data.content);
        } else if (data.type === 'PROCESS') {
          stopThinkingAnimation();
          processMessages.value.push({ type: 'PROCESS', text: data.content });
          scrollToBottom();
        }
      };

    const scrollToBottom = () => {
      setTimeout(() => {
        const chatContainer = document.querySelector('.chat-message-container');
        if (chatContainer) {
          chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        window.scrollTo(0, 0);
      }, 0);
    };

    watch(isLoggedIn, (newVal) => {
      if (newVal && currentUser.value) {
        fetchUserSessions();
      }
    });
    
    onMounted(() => {
      if (isLoggedIn.value && currentUser.value) {
        fetchUserSessions();

        nextTick(() => {
          scrollToBottom();
        });
      }
      
      document.addEventListener('keydown', handleKeyDown);
    });
    
    onUnmounted(() => {
      document.removeEventListener('keydown', handleKeyDown);
    });
    
    const handleKeyDown = (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        createNewSession();
      }
    };
    
    const toggleSidebar = () => {
      isSidebarExpanded.value = !isSidebarExpanded.value;
      console.log('侧边栏状态:', isSidebarExpanded.value ? '展开' : '收起');
    };
    
    return {
      isLoggedIn,
      username,
      password,
      currentUser,
      loginError,
      showUserInfo,
      toggleUserInfo,
      avatarContainerRef,
      handleLogin,
      handleLogout,
      goToLogin,
      userInput,
      chatMessages,
      processMessages,
      answerText,
      processContent,
      isProcessing,
      handleSend,
      handleCancel,
      renderMarkdown,
      sessions,
      selectedSessionId,
      isLoadingSessions,
      showSessions,
      toggleSessions,
      selectedNavItem,
  handleCuttingToolConsultation,
  handleSalesOrder,
  handleSupplierLocator,
      selectSession,
      fetchUserSessions,
      createNewSession,

      isSidebarExpanded,
      toggleSidebar,
      toggleThinking
    };
  }
};
</script>

<style scoped>


.thinking-header {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  user-select: none;
  transition: color 0.2s;
}

.thinking-header:hover {
  color: var(--tech-text-main);
}

.thinking-text {
  font-weight: 500;
}

.thinking-icon {
  transition: transform 0.3s ease;
  opacity: 0.7;
}

.thinking-icon.collapsed {
  transform: rotate(-90deg);
}

.app-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 5px;
  padding-bottom: 10px; 

  box-sizing: border-box;
  min-height: 100vh;
  overflow: hidden; 

}



.main-content {
  display: flex;
  flex: 1;
  gap: 20px;
  overflow: hidden;
}



.sessions-sidebar {
  width: 300px;
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.sidebar-header {
  padding: 15px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.refresh-button {
  padding: 6px 12px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.refresh-button:hover:not(:disabled) {
  background-color: #1976D2;
}

.refresh-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.sessions-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}





.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
  padding: 20px;
}

.login-form {
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.login-logo {
  margin: 0 auto 20px;
}

.login-title {
  margin: 0 0 30px;
  font-size: 28px;
  font-weight: 700;
  color: #333;
  background: linear-gradient(90deg, #4CAF50, #2196F3);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.login-input-group {
  margin-bottom: 20px;
  text-align: left;
}

.login-input-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.login-input-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
  box-sizing: border-box;
}

.login-input-group input:focus {
  outline: none;
  border-color: #2196F3;
  box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
}

.login-error {
  color: #f44336;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #ffebee;
  border-radius: 4px;
}

.login-button {
    width: 100%;
    padding: 14px;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .login-button:hover {
    background-color: #1976D2;
  }

.login-hint {
  margin-top: 20px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 6px;
  font-size: 14px;
  color: #666;
}

.login-hint p {
  margin: 5px 0;
}



.user-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.current-user {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  white-space: nowrap;
}

.logout-button {
  padding: 8px 10.67px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.logout-button:hover {
  background-color: #d32f2f;
}



.app-header {
  background-color: white;
  border-radius: 8px;
  padding: 10px 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-branding {
  display: flex;
  align-items: center;
  gap: 15px;
}



.app-logo {
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-logo svg {
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.1));
}



.app-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  letter-spacing: 1px;
  font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
  text-transform: uppercase;
  

  background: linear-gradient(90deg, #2196F3, #90CAF9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-fill-color: transparent;
}

.display-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  margin-top: 5px;
  margin-bottom: 5px;
  min-height: 500px; 

}

.result-container {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
  

  overflow: visible;
  height: auto;
  box-sizing: border-box;
  border-radius: 8px;
  border: 1px solid #fff; 

}



.result-container.processing {
  animation: gradient-pulse 1.5s infinite ease-in-out;
}

@keyframes gradient-pulse {
  0% {
    border-color: #fff;
  }
  50% {
    border-color: #2196F3; 

  }
  100% {
    border-color: #fff;
  }
}




.process-container {
  width: 100%;
  max-height: 30%; 

  min-height: 100px;
  margin: 0 0 15px 0; 

  padding: 10px;
  background-color: #f8f9fa; 
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-sizing: border-box;
}

.process-container h3,
.result-container h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
  font-weight: 600;
  display: flex;
  align-items: center;
}



.process-container h3::before {
  content: '';
  display: inline-block;
  width: 4px;
  height: 16px;
  background-color: #2196F3;
  margin-right: 8px;
  border-radius: 2px;
}

.process-content {
    flex: 1;
    overflow-y: auto;
    padding: 5px;
    background-color: white;
    border-radius: 4px;
    font-size: 13px;
    border: 1px solid #eee;
  }

.result-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 10px 10px 10px; 

  background-color: white;
  border-radius: 4px;
  white-space: pre-wrap;
  text-align: left;
  font-size: 14px;
  margin-top: 0; 

}

.message-item {
    margin-bottom: 8px;
    padding: 5px;
    border-radius: 4px;
    text-align: left;
    line-height: 1.5;
    word-wrap: break-word;
    font-size: 16px !important;
  }

  

  .markdown {
    font-size: 16px !important;
    line-height: 1.6 !important;
  }

  .markdown .paragraph {
    margin-bottom: 16px !important;
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: #333 !important;
  }
  
  

  .result-content {
    font-size: 16px !important;
  }
  
  

  .result-content p {
    font-size: 16px !important;
    line-height: 1.8 !important;
    margin-bottom: 1px !important;
    margin-top: 1px !important;
    color: #333 !important;
    display: inline-block !important;
  }
  
  

  .result-content > div {
    font-size: 16px !important;
    line-height: 1.8 !important;
  }
  
  

  .result-content * {
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: #333 !important;
  }
  
  

  :deep(.result-content) {
    font-size: 16px !important;
  }
  
  :deep(.result-content) * {
    font-size: 16px !important;
    line-height: 1.8 !important;
    color: #333 !important;
  }
  
  

  :deep(.result-content p) {
    font-size: 16px !important;
    line-height: 1.8 !important;
    margin-bottom: 1px !important;
    margin-top: 1px !important;
    color: #333 !important;
    display: inline-block !important;
  }

  

  

  :deep(.result-content) {
    position: relative;
  }
  
  :deep(.result-content) [v-pre] {
    white-space: pre-wrap;
    word-break: break-word;
  }
  
  

  :deep(.result-content) [v-pre] {
    line-height: 1.6;
  }
  
  

  :deep(.result-content) [v-pre] {
    

    font-size: 14px;
  }
  
  

  :deep(.result-content) .user-message {
    background-color: #f5f5f5; 

    color: #1565c0;
    display: inline-block; 

    text-align: left; 

    margin-left: auto;
    margin-right: 0;
    max-width: 66.6%; 

    border-radius: 8px;
    padding: 10px 15px;
    margin-bottom: 8px;
    word-break: break-word;
    line-height: 1.6;
    white-space: pre-wrap;
  }
  
  

  :deep(.result-content) .user-message {
    text-align: left;
  }

  

  :deep(.result-content) {
    text-align: left;
  }
  
  

  :deep(.result-content) .assistant-message {
    text-align: left;
    display: block;
  }
  
  :deep(.result-content) .assistant-message {
    background-color: #ffffff; 

    color: #333;
    text-align: left;
    margin-left: 0;
    margin-right: auto;
    max-width: 100%;
    padding: 10px 15px;
    margin-bottom: 8px;
    word-break: break-word;
    line-height: 1.6;
  }
  
  

  .message-item.user {
    background-color: #e3f2fd;
    color: #1565c0;
    text-align: right;
    margin-left: auto;
    max-width: 66.6%; 

    border-radius: 8px;
    padding: 10px;
  }

  .message-item.THINKING {
    background-color: #f0f7ff;
    color: #0066cc;
    white-space: pre-wrap; 

    word-break: break-all; 

  }

  .message-item.PROCESS {
    background-color: #f0f7ff;
    color: #0066cc;
    


  }

  

  :deep(h1) {
    font-size: 24px;
    margin: 16px 0 8px;
    color: #333;
  }

  :deep(h2) {
    font-size: 20px;
    margin: 14px 0 7px;
    color: #444;
  }

  :deep(h3) {
    font-size: 18px;
    margin: 12px 0 6px;
    color: #555;
  }

  :deep(p) {
    margin: 8px 0;
    line-height: 1.6;
  }

  :deep(ul), :deep(ol) {
    margin: 8px 0;
    padding-left: 24px;
  }

  :deep(li) {
    margin: 4px 0;
  }

  :deep(pre) {
    background-color: #f5f5f5;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    font-family: 'Courier New', monospace;
  }

  :deep(code) {
    background-color: #f5f5f5;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'Courier New', monospace;
  }

  :deep(strong) {
    font-weight: bold;
  }

  :deep(em) {
    font-style: italic;
  }

  :deep(a) {
    color: #2196f3;
    text-decoration: none;
  }

  :deep(a:hover) {
    text-decoration: underline;
  }

.input-container {
  padding: 0;
  margin-top: auto;
}

.textarea-with-button {
  position: relative;
  display: inline-block;
  width: 100%;
  max-width: 50vw;
}

.textarea-with-button textarea {
  width: 100%;
  padding: 12px 48px 12px 12px;
  border: 1px solid #ccc;
  border-radius: 12px;
  resize: none;
  height: 100px;
  font-size: 16px;
  font-family: inherit;
}

.textarea-with-button .send-button {
  position: absolute;
  bottom: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background-color: #4CAF50;
  color: white;
  font-size: 12px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

  .textarea-with-button textarea:focus {
    outline: none;
    border-color: #4CAF50;
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
  }
  
  


  .textarea-with-button textarea:disabled {
    background-color: #f5f5f5;
    cursor: not-allowed;
  }

  .input-container button {
    padding: 12px 24px;
    background-color: #2196F3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    transition: background-color 0.3s ease;
  }

  .input-container button:hover {
    background-color: #1976D2;
  }

  .input-container button:active {
    background-color: #1565C0;
  }

  .input-container button.cancel-button {
    background-color: #f44336;
    width: 40px;
    padding: 12px;
    font-size: 16px;
    line-height: 1;
  }

  .input-container button.cancel-button:hover {
    background-color: #d32f2f;
  }



.process-content::-webkit-scrollbar {
  width: 0;
  position: absolute;
  right: 0;
  transition: width 0.2s ease;
}

.process-content::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 4px;
}

.process-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.process-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}



.process-content:hover::-webkit-scrollbar {
  width: 8px;
}



.result-content::-webkit-scrollbar {
  width: 0;
  position: absolute;
  right: 0;
  transition: width 0.2s ease;
}

.result-content:hover::-webkit-scrollbar {
  width: 8px;
}

.result-content::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 4px;
}

.result-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.result-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}



@media (max-width: 768px) {
  .app-container {
    padding: 8px;
    gap: 8px;
  }
  
  .display-container {
    flex-direction: column;
    gap: 15px;
  }
  
  .process-container,
  .result-container {
    min-height: 180px;
  }
  
  .input-container textarea {
    height: 80px;
    font-size: 14px;
  }
  
  

  .login-form {
    padding: 30px 20px;
  }
  
  .login-title {
    font-size: 24px;
  }
  
  

  .app-header {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
  
  .user-info {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .app-container {
    padding: 10px;
    gap: 10px;
  }
  
  .process-container h3,
  .result-container h3 {
    font-size: 16px;
  }
  
  .input-container {
    flex-direction: column;
  }
  
  .input-container button {
    align-self: flex-end;
    padding: 10px 20px;
  }
  
  

  .login-form {
    padding: 20px 15px;
  }
  
  .login-logo svg {
    width: 50px;
    height: 50px;
  }
}
.model-down {
     padding-left: 50px;
     margin-top: 10px;
}



.app-container { gap: 0; padding: 0; color: #20352f; background: #f5f8f6; }
.main-content { gap: 0; background: #f5f8f6; }
.sidebar-content { width: 72px; background: #edf6f1; border-right: 1px solid #dce9e2; box-shadow: none; backdrop-filter: none; }
.sidebar-content.expanded { width: 272px; }
.app-branding { min-height: 76px; padding: 14px 16px; gap: 11px; background: transparent; border-bottom: 0; box-sizing: border-box; }
.app-logo { flex: 0 0 auto; }
.app-logo img { display: block; width: 40px; height: 40px; }
.sidebar-text-content { min-width: 0; flex: 1; display: flex; flex-direction: column; line-height: 1.25; }
.brand-name { color: #1f4036; font-size: 13px; white-space: nowrap; }
.brand-caption { margin-top: 4px; color: #82948e; font-size: 11px; white-space: nowrap; }
.toggle-sidebar-btn { width: 30px; height: 30px; padding: 0; border: 1px solid #d8e6df; border-radius: 9px; color: #668078; background: rgba(255,255,255,.75); box-shadow: none; }
.toggle-sidebar-btn:hover { color: #24785f; background: #fff; border-color: #bdd8cb; transform: none; }
.session-button-container { padding: 4px 14px 12px; }
.new-chat-btn { display: flex; align-items: center; gap: 10px; min-height: 42px; padding: 0 12px; color: #fff; background: #2f8f72; border: 0; border-radius: 12px; box-shadow: 0 6px 16px rgba(47,143,114,.16); text-decoration: none; }
.new-chat-btn:hover { color: #fff; background: #287c63; text-shadow: none; transform: translateY(-1px); }
.new-chat-btn .text { flex: 1; }
.new-chat-btn .shortcut { display: flex; align-items: center; gap: 3px; color: rgba(255,255,255,.72); font-size: 10px; }
.new-chat-btn .key { padding: 1px 4px; border: 1px solid rgba(255,255,255,.25); border-radius: 4px; }
.navigation-container, .sidebar-main { padding: 4px 12px; }
.sidebar-main { min-height: 0; margin-top: 10px; padding-top: 12px; border-top: 1px solid #ddeae3; }
.navigation-item { min-height: 42px; margin: 3px 0; padding: 0 12px; gap: 11px; color: #657b74; border-radius: 11px; }
.navigation-item:hover { color: #245d4d; background: rgba(255,255,255,.7); }
.navigation-item.selected { color: #257b61; background: #fff; box-shadow: 0 3px 12px rgba(39,92,74,.06); }
.nav-icon { font-size: 19px; }
.nav-text { font-size: 14px; font-weight: 500; }
.sessions-list { padding: 4px 0 0; }
.session-item { margin: 3px 0; padding: 9px 10px; color: #6a7e78; border-radius: 10px; }
.session-item:hover, .session-item.selected { color: #285e4f; background: rgba(255,255,255,.8); }
.session-icon { width: 24px; height: 24px; display: grid; place-items: center; flex: 0 0 auto; color: #59917f; background: #deeee6; border-radius: 7px; font-size: 14px; }
.loading-sessions, .no-sessions { padding: 18px 8px; color: #90a09b; font-size: 12px; text-align: center; }
.main-container { padding: 18px; background: #f5f8f6; }
.result-container { position: relative; height: 100%; padding: 0; background: #fff; border: 1px solid #e2ebe7; border-radius: 20px; box-shadow: 0 12px 36px rgba(49,77,67,.06); overflow: hidden; }
.result-container.processing { animation: none; border-color: #aad1c1; }
.top-user-section { top: 18px; right: 22px; margin: 0; }
.user-avatar { width: 38px; height: 38px; padding: 0; display: grid; place-items: center; border: 0; border-radius: 12px; color: #276a56; background: #e2f2ea; box-shadow: none; font-size: 14px; font-weight: 700; }
.user-avatar:hover { color: #fff; background: #2f8f72; border: 0; box-shadow: none; transform: none; }
.user-info-dropdown { margin-top: 9px; padding: 10px; background: #fff; border: 1px solid #e0e9e5; border-radius: 13px; box-shadow: 0 14px 35px rgba(35,61,52,.12); backdrop-filter: none; }
.user-name { color: #29453c; border-color: #edf1ef; }
.chat-message-container { width: min(900px, calc(100% - 48px)); margin: 0 auto; padding: 72px 8px 150px; box-sizing: border-box; }
.welcome-state { min-height: calc(100vh - 285px); max-width: 680px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }
.welcome-mark { width: 48px; height: 48px; margin-bottom: 16px; display: grid; place-items: center; color: #2f8f72; background: #e5f4ed; border-radius: 16px; font-size: 22px; }
.welcome-eyebrow { color: #58907e; font-size: 12px; font-weight: 700; letter-spacing: .12em; }
.welcome-state h2 { margin: 10px 0 8px; color: #203a32; font-size: clamp(25px,3vw,36px); font-weight: 650; letter-spacing: -.03em; }
.welcome-state p { max-width: 570px; margin: 0; color: #788b85; line-height: 1.75; }
.quick-prompts { display: flex; flex-wrap: wrap; justify-content: center; gap: 9px; margin-top: 25px; }
.quick-prompts button { padding: 9px 14px; color: #557169; background: #f7faf8; border: 1px solid #e1ebe6; border-radius: 999px; font-size: 13px; }
.quick-prompts button:hover { color: #27755d; background: #edf7f2; border-color: #c6dfd3; transform: translateY(-1px); }
.message-wrapper { margin-bottom: 18px; }
.message-wrapper.user .message-content { padding: 11px 15px; color: #24483d; background: #eaf5f0; border: 0; border-radius: 16px 16px 4px 16px; box-shadow: none; }
.message-wrapper.assistant .message-content { padding: 8px 2px; color: #30433d; line-height: 1.75; }
.message-role-label { color: #6f847d; background: #f7faf8; border: 1px solid #e6eeea; border-radius: 10px; }
.message-role-label::before { background: #6eaa96; }
.message-wrapper.THINKING .message-content { color: #687d76; background: #fafcfb; border-left: 2px solid #c9ddd4; }
.input-container { bottom: 24px; width: min(760px, calc(100% - 48px)); max-width: none; }
.textarea-with-button { width: 100%; max-width: none; display: block; background: #fff; border: 1px solid #dce8e2; border-radius: 17px; box-shadow: 0 10px 30px rgba(40,72,61,.10); backdrop-filter: none; }
.textarea-with-button:focus-within { border-color: #78b39e; box-shadow: 0 10px 32px rgba(40,111,87,.13), 0 0 0 3px rgba(47,143,114,.08); }
.textarea-with-button textarea { height: auto; min-height: 60px; max-height: 160px; padding: 18px 100px 17px 18px; color: #29453c; background: transparent !important; font-size: 15px; }
.textarea-with-button textarea::placeholder { color: #a0aea9; }
.textarea-with-button .send-button { right: 9px; bottom: 9px; width: auto; height: 42px; min-width: 70px; padding: 0 16px; color: #fff; background: #2f8f72; border: 0; border-radius: 11px; box-shadow: none; font-size: 14px; }
.textarea-with-button .send-button:hover { color: #fff; background: #287c63; box-shadow: none; transform: none; }
.textarea-with-button .send-button:disabled { color: #a7b3af; background: #edf1ef; border: 0; }
.markdown-body, :deep(.markdown-body) { color: #30433d !important; background: transparent !important; }
:deep(.markdown-body pre) { background: #f6f8f7 !important; border: 1px solid #e2e9e6; border-radius: 10px; }
:deep(.markdown-body code) { color: #24765d !important; background: #edf5f1 !important; }
:deep(.tech-process-card) { color: #40564f; background: #fff; border: 1px solid #e1eae6; border-left: 3px solid #5aa087; border-radius: 10px; box-shadow: 0 3px 12px rgba(42,72,61,.05); backdrop-filter: none; font-family: inherit; }
:deep(.tech-process-card:hover) { background: #fff; border-color: #cbded5; box-shadow: 0 5px 16px rgba(42,72,61,.07); }
:deep(.tech-process-card.agent-update) { border-left-color: #8caeeb; }
:deep(.tech-process-card.agent-update .tech-node.target),
:deep(.tech-process-card.agent-update .highlight) { color: #5278bd; text-shadow: none; }

@media (max-width: 768px) {
  .app-container { padding: 0; }
  .sidebar-content { width: 58px; }
  .sidebar-content.expanded { width: 220px; position: absolute; z-index: 20; box-shadow: 12px 0 32px rgba(39,75,62,.12); }
  .app-branding { min-height: 64px; padding: 10px 9px; }
  .main-container { padding: 8px; }
  .result-container { border-radius: 14px; }
  .chat-message-container { width: calc(100% - 24px); padding: 65px 0 130px; }
  .welcome-state { min-height: calc(100vh - 240px); }
  .welcome-state p { font-size: 14px; }
  .quick-prompts { gap: 7px; }
  .input-container { bottom: 14px; width: calc(100% - 24px); }
  .top-user-section { top: 13px; right: 14px; }
}
</style>
