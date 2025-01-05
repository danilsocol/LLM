<template>
  <div class="document-form">
    <h2>{{ isEditMode ? 'Редактировать документ' : 'Добавить документ' }}</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label for="title">Заголовок:</label>
        <input type="text" id="title" v-model="documentTitle" required>
      </div>
      <div>
        <label for="content">Содержимое:</label>
        <textarea id="content" v-model="documentContent" required></textarea>
      </div>
      <button type="submit">{{ isEditMode ? 'Сохранить' : 'Добавить' }}</button>
      <button type="button" @click="goBack" class="cancel-button">Отмена</button>
    </form>
  </div>
</template>

<script>
import {Document, User} from "@/models/models.js";
import {getCurrentUser} from "@/services/api.js";
export default {
  props: {
    document: {
      type: Object,
      default: null
    },
    isEditMode: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      documentTitle: '',
      documentContent: '',
      user: User,
    };
  },
  async mounted() {
    this.user = await getCurrentUser();
    if (this.document && this.isEditMode) {
      this.documentTitle = this.document.title;
      this.documentContent = this.document.content;
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    submitForm() {
      if (this.documentTitle && this.documentContent) {
        const newDocumentData = {
          title: this.documentTitle,
          content: this.documentContent,
          organizationId: parseInt(this.$route.params.organizationId),
          modifiedById: this.user.id
        };
        if (this.isEditMode && this.document) {
          this.$emit('document-updated', {
            ...newDocumentData,
            id: this.document.id
          });
        } else {
          this.$emit('document-added', newDocumentData);
        }
      } else {
        alert("Пожалуйста, заполните все поля.");
      }
    }
  }
}
</script>

<style scoped>
.document-form {
  padding: 20px;
  background-color: #f4f4f4;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  color: #333;
}

form div {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #555;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 16px;
}

textarea {
  min-height: 150px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  margin-right: 10px;
}

button:hover {
  background-color: #0056b3;
}

.cancel-button {
  background-color: #dc3545;
}

.cancel-button:hover {
  background-color: #c82333;
}
</style>