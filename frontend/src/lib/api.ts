// ✅ CORRECT: Use Next.js API routes instead of direct backend calls
// This avoids CORS issues and follows Next.js best practices

import { useAuthStore } from "@/store/authStore";

// Helper function to get auth headers
const getAuthHeaders = (): HeadersInit => {
    const token = useAuthStore.getState().getAccessToken();
    const headers: HeadersInit = {
        "Content-Type": "application/json",
    };

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    return headers;
};

export const api = {
    generateDesign: async (prompt: string) => {
        // ✅ Call Next.js API route (same origin, no CORS issues)
        const url = '/api/ai/generate';
        console.log('[Client] Making request to Next.js API route:', url);
        console.log('[Client] Request body:', { prompt });

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: getAuthHeaders(),
                body: JSON.stringify({ prompt }),
            });

            console.log('[Client] Response status:', response.status);
            console.log('[Client] Response ok:', response.ok);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error('[Client] Error response:', errorData);
                throw new Error(errorData.error || "Failed to generate design");
            }

            const data = await response.json();
            console.log('[Client] Success response:', data);
            return data;
        } catch (error) {
            console.error('[Client] Fetch error:', error);
            throw error;
        }
    },

    getDesign: async (id: string) => {
        // ✅ Call Next.js API route (same origin, no CORS issues)
        const url = `/api/designs/${id}`;
        console.log('[Client] Fetching design from Next.js API route:', url);

        const headers = getAuthHeaders();
        const response = await fetch(url, { headers });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || "Failed to fetch design");
        }

        return response.json();
    },

    login: async (email: string, password: string) => {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Login failed');
        }

        return response.json();
    },

    signup: async (email: string, password: string) => {
        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.error || 'Signup failed');
        }

        return response.json();
    },
};
