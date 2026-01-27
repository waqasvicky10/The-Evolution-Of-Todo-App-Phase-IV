/**
 * Better Auth client for React components.
 *
 * This provides the Better Auth client instance for use in React components.
 * Use this client to access authentication methods and session state.
 */

import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  basePath: "/api/auth",
  fetchOptions: {
    credentials: "include", // Include cookies for session management
  },
});

// Export hooks for convenience
export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient;
