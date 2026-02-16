/**
 * Better Auth server configuration.
 *
 * This file configures Better Auth for Next.js with email/password authentication.
 * Better Auth handles user registration, login, and session management.
 * 
 * Better Auth uses its own database for sessions, but we'll sync users with FastAPI backend.
 */

import { betterAuth } from "better-auth";

// Determine database provider from DATABASE_URL
const getDatabaseConfig = () => {
  const dbUrl = process.env.DATABASE_URL || "file:./auth.db";

  if (dbUrl.startsWith("postgresql://") || dbUrl.startsWith("postgres://")) {
    return {
      provider: "postgresql" as const,
      url: dbUrl,
    };
  } else {
    return {
      provider: "sqlite" as const,
      url: dbUrl,
    };
  }
};

export const auth = betterAuth({
  database: getDatabaseConfig(),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true in production
    minPasswordLength: 8,
  },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24, // 1 day
  },
  secret: process.env.BETTER_AUTH_SECRET || process.env.NEXTAUTH_SECRET || "your-secret-key-change-in-production",
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  basePath: "/api/auth",
  trustedOrigins: [
    process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  ],
});

// Export auth handler for API routes
export type Auth = typeof auth;
