import { create } from "zustand";

interface AppState {
    currentDesignId: string | null;
    setCurrentDesignId: (id: string | null) => void;
    currentDesignData: any | null;
    setCurrentDesignData: (data: any | null) => void;
    isGenerating: boolean;
    setIsGenerating: (isGenerating: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
    currentDesignId: null,
    setCurrentDesignId: (id) => set({ currentDesignId: id }),
    currentDesignData: null,
    setCurrentDesignData: (data) => set({ currentDesignData: data }),
    isGenerating: false,
    setIsGenerating: (isGenerating) => set({ isGenerating }),
}));
