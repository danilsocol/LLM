<template>
  <div class="organization-users">
    <h1>Пользователи организации</h1>
    <button @click="addUser" class="add-user-btn">Добавить пользователя</button>
    <table>
      <thead>
      <tr>
        <th>Id</th>
        <th>Email</th>
        <th>Роль</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="user in users" :key="user.id">
        <td>{{ user.id }}</td>
        <td>{{ user.email }}</td>
        <td>{{ user.role }}</td>
      </tr>
      </tbody>
    </table>
    <button @click="goBack">Назад</button>
  </div>
</template>

<script>
import {getUsersByOrganization, addUserToOrganization, getCurrentUser} from "@/services/api.js";
import { UserRole } from "@/models/models.js";

export default {
  data() {
    return {
      users: [],
      UserRole: UserRole,
      newUserEmail: ''
    };
  },
  async mounted() {
    if (this.$route.params.organizationId) {
      try {
        this.users = await getUsersByOrganization(this.$route.params.organizationId);
      } catch (error) {
        console.error("Ошибка при получении пользователей:", error);
        alert("Не удалось загрузить список пользователей.");
      }
    }
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    async addUser() {
      const userId = prompt("Введите id пользователя для добавления:");
      if (parseInt(userId)) {
        try {
          const admin = await getCurrentUser()
          await addUserToOrganization(this.$route.params.organizationId, admin.id, parseInt(userId));
          alert("Пользователь добавлен успешно!");
          this.users = await getUsersByOrganization(this.$route.params.organizationId);
        } catch (error) {
          console.error("Ошибка при добавлении пользователя:", error);
          alert("Не удалось добавить пользователя. Проверьте id или попробуйте позже.");
        }
      }
    }
  }
};
</script>
<style scoped>
.organization-users {
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

button {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.add-user-btn {
  position: absolute;
  top: 20px;
  right: 20px;
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.add-user-btn:hover {
  background-color: #218838;
}
</style>