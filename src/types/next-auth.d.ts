import NextAuth from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      email: string;
      name: string;
      username: string;
      contactNumber?: string;
      createdAt: string;
      lastLogin?: string;
    };
  }

  interface User {
    id: string;
    email: string;
    name: string;
    username: string;
    contactNumber?: string;
    createdAt: string;
    lastLogin?: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    id: string;
    username: string;
    contactNumber?: string;
    createdAt: string;
    lastLogin?: string;
  }
}
