"use client";

/**
 * Better Auth context provider.
 *
 * This replaces the custom AuthContext with Better Auth integration.
 * Provides authentication state and methods using Better Auth.
 */

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { authClient, useSession } from "@/lib/auth-client";
import { User } from "@/types/api";

interface BetterAuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const BetterAuthContext = createContext<BetterAuthContextType | undefined>(undefined);

export function BetterAuthProvider({ children }: { children: React.ReactNode }) {
  const { data: session, isPending } = useSession();
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();

  // Update user state when session changes
  useEffect(() => {
    if (session?.user) {
      setUser({
        id: parseInt(session.user.id) || 0,
        email: session.user.email || "",
        created_at: session.user.createdAt?.toISOString() || new Date().toISOString(),
      });
    } else {
      setUser(null);
    }
  }, [session]);

  const login = async (email: string, password: string) => {
    const result = await authClient.signIn.email({
      email,
      password,
    });

    if (result.error) {
      throw new Error(result.error.message || "Login failed");
    }

    router.push("/dashboard");
  };

  const register = async (email: string, password: string) => {
    const result = await authClient.signUp.email({
      email,
      password,
    });

    if (result.error) {
      throw new Error(result.error.message || "Registration failed");
    }

    // Auto-login after registration
    await login(email, password);
  };

  const logout = async () => {
    await authClient.signOut();
    setUser(null);
    router.push("/login");
  };

  return (
    <BetterAuthContext.Provider
      value={{
        user,
        isAuthenticated: !!session?.user,
        isLoading: isPending,
        login,
        register,
        logout,
      }}
    >
      {children}
    </BetterAuthContext.Provider>
  );
}

export function useBetterAuth() {
  const context = useContext(BetterAuthContext);
  if (context === undefined) {
    throw new Error("useBetterAuth must be used within BetterAuthProvider");
  }
  return context;
}
