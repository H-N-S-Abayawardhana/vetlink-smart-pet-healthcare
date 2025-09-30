import { NextAuthOptions } from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import pool from './db';
import bcrypt from 'bcryptjs';

export const authOptions: NextAuthOptions = {
  providers: [
    CredentialsProvider({
      name: 'credentials',
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' }
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) {
          return null;
        }

        try {
          const result = await pool.query(
            'SELECT * FROM users WHERE email = $1 AND is_active = true',
            [credentials.email]
          );

          if (result.rows.length === 0) {
            return null;
          }

          const user = result.rows[0];
          const isPasswordValid = await bcrypt.compare(credentials.password, user.password_hash);

          if (!isPasswordValid) {
            return null;
          }

          // Update last login
          await pool.query(
            'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = $1',
            [user.id]
          );

          return {
            id: user.id.toString(),
            email: user.email,
            name: user.username,
            username: user.username,
            contactNumber: user.contact_number,
            createdAt: user.created_at,
            lastLogin: user.last_login
          };
        } catch (error) {
          console.error('Auth error:', error);
          return null;
        }
      }
    })
  ],
  session: {
    strategy: 'jwt',
    maxAge: 24 * 60 * 60, // 24 hours
  },
  jwt: {
    maxAge: 24 * 60 * 60, // 24 hours
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.username = (user as any).username;
        token.contactNumber = (user as any).contactNumber;
        token.createdAt = (user as any).createdAt;
        token.lastLogin = (user as any).lastLogin;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        session.user.id = token.id as string;
        (session.user as any).username = token.username;
        (session.user as any).contactNumber = token.contactNumber;
        (session.user as any).createdAt = token.createdAt;
        (session.user as any).lastLogin = token.lastLogin;
      }
      return session;
    }
  },
  pages: {
    signIn: '/signin',
  },
  secret: process.env.NEXTAUTH_SECRET,
};
