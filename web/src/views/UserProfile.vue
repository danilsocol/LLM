<template>
  <div class="user-profile-container">
    <h1>Профиль пользователя</h1>
    <div class="user-info">
      <h2>Информация о пользователе</h2>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Роль:</strong> {{ user.role }}</p>
    </div>

    <div class="organization-info" v-if="organization">
      <h2>Информация об организации</h2>
      <p><strong>Название:</strong> {{ organization.name }}</p>
      <p><strong>Монеты:</strong> {{ organization.coins }}</p>

      <button v-if="user.role === UserRole.ORG_ADMIN" @click="addCoins">Пополнить койны</button>

      <button @click="viewUsers">Список пользователей</button>
      <button @click="viewDocumentation">Список документации</button>

      <button v-if="user.role === UserRole.ORG_ADMIN" @click="removeOrganization">
        Удалить организацию
      </button>
      <button v-else @click="leaveOrganization">
        Выйти из организации
      </button>

      <button @click="logout">Выйти из аккаунта</button>
    </div>

    <div class="no-organization" v-else>
      <h2>У вас нет организации</h2>
      <button @click="createOrganization">Создать организацию</button>
    </div>
  </div>
</template>

<script>
import { getUser , removeUser , setUser  } from '../services/auth';
import { Organization, User, UserRole } from "@/models/models.js";
import {
  addCoinsToOrganization,
  createOrganization, deleteOrganization,
  getDocumentationByOrganization,
  getOrganizationByOrgId,
  getUsersByOrganization, leaveOrganization
} from "@/services/api.js";

export default {
  computed: {
    UserRole() {
      return UserRole
    }
  },
  data() {
    return {
      user: User,
      organization: null,
    };
  },
  async mounted() {
    this.user = await getUser ();
    console.log(this.user);
    if (this.user.organization_id) {
      try {
        const response = await getOrganizationByOrgId(this.user.organization_id);
        this.organization = response;
      } catch (error) {
        console.error("Ошибка получения организации:", error);
      }
    }
  },
  methods: {
    async createOrganization() {
      const organizationName = prompt("Введите название вашей организации:");
      if (organizationName) {
        try {
          const org = await createOrganization({ name: organizationName, coins: 0 }, await getUser ().id);
          this.organization = org;
          this.user.role = UserRole.ORG_ADMIN;
          this.user.organization_id = org.id;
          setUser(this.user);
          alert("Организация успешно создана!");
        } catch (error) {
          console.error("Ошибка создания организации:", error);
          alert("Ошибка при создании организации. Попробуйте позже.");
        }
      }
    },
    async leaveOrganization() {
      try {
        await leaveOrganization(this.user.id, this.organization.id);
        alert("Вы вышли из организации.");
        this.user.organization_id = null;
        this.user.role = UserRole.NONE;
        setUser (this.user);
      } catch (error) {
        console.error("Ошибка при выходе из организации:", error);
        alert("Ошибка при выходе из организации. Попробуйте позже.");
      }
    },
    async removeOrganization() {
      if (confirm("Вы уверены, что хотите удалить организацию? Это действие необратимо.")) {
        try {
          await deleteOrganization(this.organization.id);
          alert("Организация успешно удалена.");
          this.organization = null; // Обнуляем организацию после удаления
          this.user.organization_id = null;
          this.user.role = UserRole.NONE;
          setUser (this.user);
        } catch (error) {
          console.error("Ошибка при удалении организации:", error);
          alert("Ошибка при удалении организации. Попробуйте позже.");
        }
      }
    },
    async addCoins() {
      const coins = prompt("Введите количество койнов для пополнения:");
      if (coins && !isNaN(coins)) {
        try {
          console.log(this.organization);
          console.log(coins);
          console.log(parseInt(coins));
          await addCoinsToOrganization(this.organization.id, parseInt(coins));
          this.organization.coins += parseInt(coins);
          alert(`Койны успешно пополнены на ${coins}.`);
        } catch (error) {
          console.error("Ошибка при пополнении койнов:", error);
          alert("Ошибка при пополнении койнов. Попробуйте позже.");
        }
      } else {
        alert("Пожалуйста, введите корректное количество койнов.");
      }
    },
    async viewUsers() {
      this.$router.push({
        name: 'OrganizationUsers',
        params: { organizationId: this.organization.id }
      });
    },
    async viewDocumentation() {
      try {
        const documentation = await getDocumentationByOrganization(this.organization.id);
        console.log(documentation);
        alert("Список документации: " + documentation.map(doc => doc.title).join(", "));
      } catch (error) {
        console.error("Ошибка получения списка документации:", error);
        alert("Ошибка при получении списка документации. Попробуйте позже.");
      }
    },
    async logout() {
      removeUser ();
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.user-profile-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f4f4;
  padding: 40px;
}

.user-info, .organization-info, .no-organization {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 300px;
  margin: 20px 0;
}

h1 {
  color: #333;
}

h2 {
  color: #333;
}

button {
  background-color: #007bff;
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-top: 10px;
}

button:hover {
  background-color: #0056b3;
}
</style>