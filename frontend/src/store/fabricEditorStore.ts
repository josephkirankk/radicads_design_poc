import { create } from "zustand";
import { Canvas, FabricObject } from "fabric";

export type Tool =
  | "select"
  | "text"
  | "rectangle"
  | "circle"
  | "line"
  | "draw"
  | "image";

export interface CanvasState {
  json: string;
  timestamp: number;
}

export interface EditorStore {
  // Canvas instance
  canvas: Canvas | null;
  setCanvas: (canvas: Canvas | null) => void;

  // Selection state
  selectedObjects: FabricObject[];
  setSelectedObjects: (objects: FabricObject[]) => void;

  // History state
  history: CanvasState[];
  historyIndex: number;
  canUndo: boolean;
  canRedo: boolean;
  undo: () => void;
  redo: () => void;
  addToHistory: () => void;
  clearHistory: () => void;

  // Tool state
  activeTool: Tool;
  setActiveTool: (tool: Tool) => void;

  // Drawing state
  isDrawingMode: boolean;
  setDrawingMode: (enabled: boolean) => void;
  brushColor: string;
  setBrushColor: (color: string) => void;
  brushWidth: number;
  setBrushWidth: (width: number) => void;

  // Canvas properties
  zoom: number;
  setZoom: (zoom: number) => void;
  backgroundColor: string;
  setBackgroundColor: (color: string) => void;

  // UI state
  showGrid: boolean;
  setShowGrid: (show: boolean) => void;
  showRulers: boolean;
  setShowRulers: (show: boolean) => void;
}

const MAX_HISTORY = 50;

export const useFabricEditorStore = create<EditorStore>((set, get) => ({
  // Canvas instance
  canvas: null,
  setCanvas: (canvas) => set({ canvas }),

  // Selection state
  selectedObjects: [],
  setSelectedObjects: (objects) => set({ selectedObjects: objects }),

  // History state
  history: [],
  historyIndex: -1,
  canUndo: false,
  canRedo: false,

  addToHistory: () => {
    const { canvas, history, historyIndex } = get();
    if (!canvas) return;

    const json = JSON.stringify(canvas.toJSON());
    const newState: CanvasState = {
      json,
      timestamp: Date.now(),
    };

    // Remove any states after current index (when undoing then making new changes)
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(newState);

    // Limit history size
    if (newHistory.length > MAX_HISTORY) {
      newHistory.shift();
    }

    set({
      history: newHistory,
      historyIndex: newHistory.length - 1,
      canUndo: true,
      canRedo: false,
    });
  },

  undo: () => {
    const { canvas, history, historyIndex } = get();
    if (!canvas || historyIndex <= 0) return;

    const newIndex = historyIndex - 1;
    const state = history[newIndex];

    canvas.loadFromJSON(state.json, () => {
      canvas.renderAll();
      set({
        historyIndex: newIndex,
        canUndo: newIndex > 0,
        canRedo: true,
      });
    });
  },

  redo: () => {
    const { canvas, history, historyIndex } = get();
    if (!canvas || historyIndex >= history.length - 1) return;

    const newIndex = historyIndex + 1;
    const state = history[newIndex];

    canvas.loadFromJSON(state.json, () => {
      canvas.renderAll();
      set({
        historyIndex: newIndex,
        canUndo: true,
        canRedo: newIndex < history.length - 1,
      });
    });
  },

  clearHistory: () =>
    set({
      history: [],
      historyIndex: -1,
      canUndo: false,
      canRedo: false,
    }),

  // Tool state
  activeTool: "select",
  setActiveTool: (tool) => set({ activeTool: tool }),

  // Drawing state
  isDrawingMode: false,
  setDrawingMode: (enabled) => {
    const { canvas } = get();
    if (canvas) {
      canvas.isDrawingMode = enabled;
    }
    set({ isDrawingMode: enabled });
  },
  brushColor: "#000000",
  setBrushColor: (color) => set({ brushColor: color }),
  brushWidth: 5,
  setBrushWidth: (width) => set({ brushWidth: width }),

  // Canvas properties
  zoom: 1,
  setZoom: (zoom) => set({ zoom }),
  backgroundColor: "#ffffff",
  setBackgroundColor: (color) => set({ backgroundColor: color }),

  // UI state
  showGrid: false,
  setShowGrid: (show) => set({ showGrid: show }),
  showRulers: false,
  setShowRulers: (show) => set({ showRulers: show }),
}));

