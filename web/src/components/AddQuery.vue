<template>
  <div class="add-query-container">
    <h1>Создать запрос</h1>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="documentId">Документ (ID - необязательно):</label>
        <input type="number" id="documentId" v-model.number="documentId">
      </div>
      <div class="form-group">
        <label for="question">Ваш вопрос:</label>
        <textarea id="question" v-model="question" required></textarea>
      </div>
      <button type="submit">Отправить запрос</button>
    </form>
    <button @click="goBack">Назад</button>

  </div>
</template>

<script>
import {addQuery, getCurrentUser} from "@/services/api";
import {User} from "@/models/models.js";

export default {
  async mounted() {
    this.user = await getCurrentUser();
  },
  data() {
    return {
      documentId: null,
      question: "",
      user: User,
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async submitForm() {
      const organizationId = parseInt(this.$route.params.organizationId);

      try {
        if(this.question === "") {
          return alert("Вопрос не должен быть пустым!");
        }
        await addQuery({
          user_id: this.user.id,
          organization_id: organizationId,
          document_id: this.documentId,
          question: this.question
        });
        alert("Запрос отправлен!");
        this.$router.push({ name: 'MyQueries' });
      } catch (error) {
        console.error("Ошибка при отправке запроса:", error);
        alert("Не удалось отправить запрос. Попробуйте позже.");
      }
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
/* Стили */
.add-query-container {
  padding: 20px;
  background-color: #f4f4f4;
  min-height: 100vh;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input, textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  margin-top: 10px;
  background-color: #007bff;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 10px; /* Add some spacing */
}
</style>