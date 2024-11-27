<template>
  <div class="organization-documents">
    <h1>Документы организации</h1>
    <div class="button-container">
      <button @click="goToAddDocument" class="add-document-btn">Добавить документ</button>
      <button @click="goBack">Назад</button>
    </div>
    <table>
      <thead>
      <tr>
        <th>Id</th>
        <th>Заголовок</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="document in documents" :key="document.id">
        <td>{{ document.id }}</td>
        <td>{{ document.title }}</td>
        <td>
          <button @click="goToEditDocument(document.id)" class="edit-btn">Редактировать</button>
          <button @click="deleteDocument(document.id)" class="delete-btn">Удалить</button>
        </td>
      </tr>
      </tbody>
    </table>
    <router-view v-slot="{ Component }">
      <component :is="Component"
                 v-if="showDocumentForm"
                 :document="getEditingDocument"
                 :isEditMode="isEditMode"
                 @document-added="addDocument"
                 @document-updated="updateDocument"
      />
    </router-view>
  </div>
</template>

<script>
import {
  getDocumentsByOrganization,
  addDocumentToOrganization,
  updateDocumentInOrganization,
  deleteDocumentFromOrganization
} from "@/services/api.js";
import { Document } from "@/models/models";
import { getUser } from "@/services/auth";
import DocumentForm from "@/components/DocumentForm.vue";

export default {
  components: {
    DocumentForm
  },
  data() {
    return {
      documents: [],
      showDocumentForm: false,
      editingDocumentId: null
    };
  },
  computed: {
    getEditingDocument() {
      if(this.editingDocumentId !== null) {
        return this.documents.find(doc => doc.id === this.editingDocumentId) || null;
      }
      return null;
    },
    isEditMode() {
      return this.$route.name === 'EditDocument';
    }
  },
  async mounted() {
    if (this.$route.params.organizationId) {
      await this.loadDocuments();
    }
    if (this.$route.name === 'AddDocument' || this.$route.name === 'EditDocument') {
      this.showDocumentForm = true;
      if(this.$route.name === 'EditDocument') {
        this.editingDocumentId = parseInt(this.$route.params.documentId);
      }
    }
  },
  watch: {
    '$route'(to) {
      this.showDocumentForm = to.name === 'AddDocument' || to.name === 'EditDocument';
      if (to.name === 'EditDocument') {
        this.editingDocumentId = parseInt(to.params.documentId);
      } else {
        this.editingDocumentId = null;
      }
    }
  },
  methods: {
    async loadDocuments() {
      try {
        const documentsData = await getDocumentsByOrganization(this.$route.params.organizationId);
        this.documents = documentsData.map(doc => new Document(doc.id, doc.title, doc.content, doc.organizationId, doc.modifiedById));
      } catch (error) {
        console.error("Ошибка при получении документов:", error);
        alert("Не удалось загрузить список документов.");
      }
    },
    goBack() {
      this.$router.go(-1);
    },
    goToAddDocument() {
      this.$router.push({ name: 'AddDocument', params: { organizationId: this.$route.params.organizationId } });
    },
    goToEditDocument(documentId) {
      this.$router.push({ name: 'EditDocument', params: { organizationId: this.$route.params.organizationId, documentId: documentId } });
    },
    async addDocument(newDocumentData) {
      try {
        const addedDocument = await addDocumentToOrganization(this.$route.params.organizationId, newDocumentData);
        this.documents.push(new Document(addedDocument.id, addedDocument.title, addedDocument.content, addedDocument.organization_id, addedDocument.modified_by_id)); // Используйте правильные поля из ответа
        alert("Документ успешно добавлен!");
        this.$router.push({ name: 'OrganizationDocuments', params: { organizationId: this.$route.params.organizationId } });
      } catch (error) {
        console.error("Ошибка при добавлении документа:", error);
        alert("Не удалось добавить документ. Попробуйте позже.");
      }
    },
    async updateDocument(updatedDocumentData) {
      try {
        await updateDocumentInOrganization(this.$route.params.organizationId, updatedDocumentData);
        const index = this.documents.findIndex(doc => doc.id === updatedDocumentData.id);
        if (index !== -1) {
          this.documents.splice(index, 1, new Document(updatedDocumentData.id, updatedDocumentData.title, updatedDocumentData.content, updatedDocumentData.organization_id, updatedDocumentData.modified_by_id));
        }
        alert("Документ успешно обновлен!");
        this.$router.push({ name: 'OrganizationDocuments', params: { organizationId: this.$route.params.organizationId } });
      } catch (error) {
        console.error("Ошибка при обновлении документа:", error);
        alert("Не удалось обновить документ. Попробуйте позже.");
      }
    },
    async deleteDocument(documentId) {
      if (confirm("Вы уверены, что хотите удалить этот документ?")) {
        try {
          await deleteDocumentFromOrganization(documentId); // Изменено: вызов функции
          this.documents = this.documents.filter(doc => doc.id !== documentId);
          alert("Документ успешно удален!");
        } catch (error) {
          console.error("Ошибка при удалении документа:", error);
          alert("Не удалось удалить документ. Попробуйте позже.");
        }
      }
    }
  }
};
</script>

<style scoped>
.organization-documents {
  padding: 20px;
  background-color: #f4f4f4;
  min-height: 100vh;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #007bff;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.button-container button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button-container button:hover {
  background-color: #0056b3;
}

.add-document-btn {
  background-color: #28a745;
}

.add-document-btn:hover {
  background-color: #218838;
}
.edit-btn {
  background-color: #ffc107;
  color: black;
  margin-right: 5px;
}

.edit-btn:hover {
  background-color: #e0a800;
}

.delete-btn {
  background-color: #dc3545;
}

.delete-btn:hover {
  background-color: #c82333;
}
</style>