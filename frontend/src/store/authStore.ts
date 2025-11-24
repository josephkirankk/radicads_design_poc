import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: string;
  email: string;
  created_at?: string;
}

interface Session {
  access_token: string;
  refresh_token?: string;
  expires_at?: number;
  user: User;
}

interface AuthState {
  session: Session | null;
  user: User | null;
  isAuthenticated: boolean;
  setSession: (session: Session | null) => void;
  clearSession: () => void;
  getAccessToken: () => string | null;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      session: null,
      user: null,
      isAuthenticated: false,

      setSession: (session: Session | null) => {
        set({
          session,
          user: session?.user || null,
          isAuthenticated: !!session,
        });
      },

      clearSession: () => {
        set({
          session: null,
          user: null,
          isAuthenticated: false,
        });
      },

      getAccessToken: () => {
        const { session } = get();
        return session?.access_token || null;
      },
    }),
    {
      name: "radic-auth-storage",
    }
  )
);

