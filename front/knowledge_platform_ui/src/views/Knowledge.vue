<template>
  <div class="knowledge-container">
    <div class="page-header">
      <h2>数控刀具知识库管理</h2>
      <p class="subtitle">上传并管理数控刀具知识文档</p>
    </div>

    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <span>文件上传</span>
        </div>
      </template>
      <div class="upload-area">
        <el-upload
          class="upload-demo"
          drag
          action=""
          :http-request="handleUpload"
          multiple
          :show-file-list="false"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            Drop file here or <em>click to upload</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              Supported files: .txt, .md, .pdf (if supported by backend)
            </div>
          </template>
        </el-upload>
      </div>
    </el-card>

    <div v-if="uploadHistory.length > 0" class="history-section">
      <h3>上传记录</h3>
      <el-table :data="uploadHistory" style="width: 100%" :row-class-name="tableRowClassName">
        <el-table-column prop="fileName" label="文件名" width="280" />
        <el-table-column prop="chunks" label="新增切片数" width="150" align="center" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="message" label="信息" />
        <el-table-column prop="time" label="时间" width="180" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadFile } from '@/api/knowledge'
import { ElMessage } from 'element-plus'

const uploadHistory = ref([])

const handleUpload = async (options) => {
  const { file } = options
  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await uploadFile(formData)
    uploadHistory.value.unshift({
      fileName: res.file_name,
      chunks: res.chunks_added,
      status: res.status,
      message: res.message,
      time: new Date().toLocaleString()
    })
    ElMessage.success(`File ${file.name} uploaded successfully`)
  } catch (error) {
    uploadHistory.value.unshift({
      fileName: file.name,
      chunks: 0,
      status: 'error',
      message: error.message || 'Upload failed',
      time: new Date().toLocaleString()
    })
    ElMessage.error(`Upload failed for ${file.name}`)
  }
}

const tableRowClassName = ({ rowIndex }) => {
  if (rowIndex === 0) {
    return 'success-row'
  }
  return ''
}
</script>

<style lang="scss" scoped>
.knowledge-container {
  max-width: 1080px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 26px;
  h2 {
    color: #243d35;
    margin: 0 0 8px;
    font-size: 28px;
    letter-spacing: -.02em;
  }
  .subtitle {
    margin: 0;
    color: #7b8e87;
    font-size: 14px;
  }
}

.upload-card {
  background-color: #fff;
  border: 1px solid #e0e9e5;
  border-radius: 16px;
  color: #30463e;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(49,77,67,.05);

  :deep(.el-card__header) {
    padding: 17px 20px;
    border-bottom: 1px solid #edf2ef;
  }
}

.upload-area {
  padding: 8px;
  
  :deep(.el-upload-dragger) {
    padding: 46px 20px;
    background-color: #f8fbf9;
    border-color: #d9e7e0;
    border-radius: 13px;
    
    &:hover {
      border-color: #73ae99;
      background-color: #f2f8f5;
    }
    
    .el-icon--upload {
      color: #54a083;
    }
    
    .el-upload__text {
      color: #71867e;
      em {
        color: #2f8f72;
      }
    }
  }
}

.history-section {
  h3 {
    color: #2b443c;
    margin-bottom: 16px;
  }
  
  :deep(.el-table) {
    overflow: hidden;
    background-color: #fff;
    color: #43574f;
    border: 1px solid #e2eae6;
    border-radius: 14px;
    --el-table-border-color: #edf2ef;
    --el-table-header-bg-color: #f7faf8;
    --el-table-row-hover-bg-color: #f3f8f5;
    
    th, tr {
      background-color: #fff;
    }
    
    .success-row {
      background-color: #f4faf6;
    }
  }
}
</style>
