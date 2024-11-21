export class User {
    constructor(id , role, email, password, organization_id) {
        this.id = id;
        this.role = role;
        this.email = email;
        this.password = password;
        this.organization_id = organization_id;
    }
}

export class Organization {
    constructor(id, name, coins) {
        this.id = id;
        this.name = name;
        this.coins = coins;
    }
}

export class Document {
    constructor(id, title, content, organizationId, modifiedById) {
        this.id = id;
        this.title = title;
        this.content = content;
        this.organizationId = organizationId;
        this.modifiedById = modifiedById;
    }
}

export class Query {
    constructor(id, userId, organizationId, documentId, question, answer) {
        this.id = id;
        this.userId = userId;
        this.organizationId = organizationId;
        this.documentId = documentId;
        this.question = question;
        this.answer = answer;
    }
}

export const UserRole = {
    ADMIN: "admin",
    ORG_ADMIN: "org_admin",
    USER: "user",
    NONE: "none",
};