<template>
  <div class="app-wrapper">
    <div class="sidebar">
      <div class="logo">
        <span class="logo-mark">K</span>
        <span><strong>数控刀具知识库</strong><small>KNOWLEDGE CENTER</small></span>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="el-menu-vertical"
      >
        <el-menu-item index="/knowledge">
          <el-icon><Files /></el-icon>
          <span>知识库管理</span>
        </el-menu-item>
        <el-menu-item index="/chat">
          <el-icon><ChatDotRound /></el-icon>
          <span>智能问答</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="main-container">
      <router-view v-slot="{ Component }">
        <transition name="fade-transform" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const activeMenu = computed(() => route.path)
</script>

<style lang="scss" scoped>
.app-wrapper {
  display: flex;
  height: 100vh;
  width: 100%;
  background-color: #f5f8f6;
  color: #273c35;
}

.sidebar {
  width: 248px;
  padding: 0 12px;
  background-color: #edf6f1;
  border-right: 1px solid #dce9e2;
  display: flex;
  flex-direction: column;
  box-shadow: none;
  z-index: 10;

  .logo {
    height: 76px;
    padding: 0 10px;
    display: flex;
    align-items: center;
    gap: 11px;
    color: #23483c;

    .logo-mark {
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      color: #fff;
      background: #2f8f72;
      border-radius: 12px;
      font-size: 17px;
      font-weight: 700;
    }

    span:last-child { display: flex; flex-direction: column; gap: 3px; }
    strong { font-size: 15px; }
    small { color: #869890; font-size: 9px; letter-spacing: .12em; }
  }
  
  .el-menu-vertical {
    border-right: none;
    background: transparent;

    :deep(.el-menu-item) {
      height: 44px;
      margin: 4px 0;
      color: #657b74;
      border-radius: 11px;
    }

    :deep(.el-menu-item:hover) { color: #286b57; background: rgba(255,255,255,.7); }
    :deep(.el-menu-item.is-active) { color: #267b61; background: #fff; box-shadow: 0 3px 12px rgba(39,92,74,.06); }
  }
}

.main-container {
  flex: 1;
  padding: 28px 36px;
  overflow-y: auto;
  background: #f5f8f6;
}

.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all 0.4s ease;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

@media (max-width: 760px) {
  .sidebar { width: 72px; padding: 0 8px; }
  .logo { justify-content: center; padding: 0 !important; }
  .logo > span:last-child, :deep(.el-menu-item span) { display: none !important; }
  .main-container { padding: 14px; }
}
</style>
