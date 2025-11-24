# Fabric.js v6 Migration Plan

## Executive Summary
This document outlines the comprehensive plan to replace Polotno UI with Fabric.js v6 in the Radic application. The migration will maintain all existing functionality while providing a more flexible, performant, and maintainable canvas editor solution.

## Current State Analysis

### Polotno Implementation
- **Location**: `frontend/src/components/editor/Editor.tsx`
- **Features Used**:
  - Canvas workspace with zoom controls
  - Side panel for tools
  - Toolbar with download functionality
  - Store-based state management (MobX State Tree)
  - JSON serialization (store.toJSON/loadJSON)
  - Page management

### Dependencies to Remove
- `polotno` (v2.32.4)
- `@blueprintjs/core`, `@blueprintjs/icons`, `@blueprintjs/select` (Polotno dependencies)
- `mobx`, `mobx-react-lite`, `mobx-state-tree` (if only used by Polotno)
- `konva` (will be replaced by Fabric.js's own canvas implementation)

## Target Architecture

### Technology Stack
- **Canvas Library**: Fabric.js v6.9.0 (latest stable)
- **State Management**: Zustand (already in use)
- **UI Components**: shadcn/ui (already in use)
- **Icons**: lucide-react (already in use)
- **TypeScript**: Full type safety with Fabric.js v6 native types

### Component Structure
```
frontend/src/components/editor/
├── FabricEditor.tsx          # Main editor component
├── FabricCanvas.tsx          # Canvas wrapper with Fabric.js initialization
├── Toolbar/
│   ├── Toolbar.tsx           # Main toolbar container
│   ├── ToolButton.tsx        # Reusable tool button
│   ├── TextTools.tsx         # Text formatting tools
│   ├── ShapeTools.tsx        # Shape creation tools
│   ├── ImageTools.tsx        # Image manipulation tools
│   └── ExportTools.tsx       # Export and download tools
├── SidePanel/
│   ├── SidePanel.tsx         # Side panel container
│   ├── LayersPanel.tsx       # Layers management
│   ├── PropertiesPanel.tsx   # Object properties editor
│   └── AssetsPanel.tsx       # Images and templates
├── Controls/
│   ├── ZoomControls.tsx      # Zoom in/out/fit
│   └── HistoryControls.tsx   # Undo/redo buttons
└── hooks/
    ├── useFabricCanvas.ts    # Canvas initialization and management
    ├── useCanvasHistory.ts   # Undo/redo functionality
    ├── useCanvasObjects.ts   # Object manipulation
    └── useCanvasExport.ts    # Export functionality
```

### State Management (Zustand)
```typescript
interface EditorStore {
  // Canvas state
  canvas: fabric.Canvas | null;
  setCanvas: (canvas: fabric.Canvas | null) => void;
  
  // Selection state
  selectedObjects: fabric.Object[];
  setSelectedObjects: (objects: fabric.Object[]) => void;
  
  // History state
  history: CanvasState[];
  historyIndex: number;
  undo: () => void;
  redo: () => void;
  addToHistory: (state: CanvasState) => void;
  
  // Tool state
  activeTool: Tool;
  setActiveTool: (tool: Tool) => void;
  
  // Drawing state
  isDrawingMode: boolean;
  setDrawingMode: (enabled: boolean) => void;
  brushColor: string;
  brushWidth: number;
  
  // Canvas properties
  zoom: number;
  setZoom: (zoom: number) => void;
  backgroundColor: string;
  setBackgroundColor: (color: string) => void;
}
```

## Implementation Phases

### Phase 1: Setup and Core Infrastructure (Tasks 1-5)
1. ✅ Research Fabric.js v6 documentation and best practices
2. Install Fabric.js and TypeScript types
3. Create base canvas component with React integration
4. Set up Zustand store for editor state
5. Implement canvas initialization and cleanup

### Phase 2: Basic Editing Features (Tasks 6-10)
6. Build toolbar component structure
7. Implement object selection and transformation
8. Add text creation and editing
9. Implement image import and basic manipulation
10. Add basic shapes (rectangle, circle, triangle, line)

### Phase 3: Advanced Features (Tasks 11-15)
11. Implement layers panel with drag-and-drop reordering
12. Add freehand drawing with brush customization
13. Implement image filters and effects
14. Add undo/redo with keyboard shortcuts (Ctrl+Z, Ctrl+Y)
15. Implement comprehensive keyboard shortcuts

### Phase 4: Data Management (Tasks 16-17)
16. Implement JSON serialization/deserialization
17. Add export to PNG, JPG, SVG formats
18. Update design API to work with Fabric.js JSON format

### Phase 5: Integration and Cleanup (Tasks 18-20)
19. Replace Polotno Editor component
20. Update all design-related hooks and API calls
21. Remove Polotno dependencies and clean up code

### Phase 6: Testing and Optimization (Tasks 21-23)
22. Comprehensive testing of all features
23. Performance optimization (object caching, rendering)
24. Documentation and code comments

## Key Features to Implement

### 1. Canvas Management
- Initialize Fabric.js canvas with proper dimensions (1080x1080 for Instagram)
- Responsive canvas sizing
- Zoom controls (fit, zoom in, zoom out, percentage)
- Pan/drag canvas
- Grid and guidelines (optional)

### 2. Object Manipulation
- Selection (single and multiple)
- Move, resize, rotate, skew
- Alignment tools (left, center, right, top, middle, bottom)
- Distribution tools
- Grouping/ungrouping
- Layer ordering (bring forward, send backward, bring to front, send to back)
- Lock/unlock objects
- Delete objects

### 3. Text Editing
- Add text (IText for editable, Text for static)
- Font family, size, weight, style
- Text color and background
- Text alignment (left, center, right, justify)
- Line height and letter spacing
- Text effects (shadow, stroke)

### 4. Image Handling
- Import images (drag-and-drop, file picker)
- Image filters (grayscale, sepia, brightness, contrast, saturation, blur, etc.)
- Image cropping
- Image replacement
- Opacity control

### 5. Shapes and Drawing
- Basic shapes (rectangle, circle, ellipse, triangle, polygon)
- Lines and arrows
- Freehand drawing (PencilBrush, CircleBrush, SprayBrush)
- Shape fill and stroke customization

### 6. History Management
- Undo/redo stack
- Keyboard shortcuts (Ctrl+Z, Ctrl+Shift+Z or Ctrl+Y)
- History limit (e.g., 50 states)

### 7. Export and Save
- Export to PNG (high quality)
- Export to JPG
- Export to SVG
- Save design as JSON
- Load design from JSON
- Auto-save to local storage

## Migration Strategy

### Backward Compatibility
- Convert existing Polotno JSON designs to Fabric.js format
- Provide migration utility for existing designs in database
- Maintain design_json structure in database

### Data Format Conversion
```typescript
// Polotno format (simplified)
{
  "pages": [{
    "children": [
      { "type": "text", "text": "Hello", "x": 100, "y": 100 }
    ]
  }]
}

// Fabric.js format
{
  "version": "6.0.0",
  "objects": [
    { "type": "i-text", "text": "Hello", "left": 100, "top": 100 }
  ]
}
```

## Best Practices

### Performance
1. Use object caching for complex objects
2. Disable rendering during batch operations
3. Use `canvas.requestRenderAll()` instead of `canvas.renderAll()`
4. Implement virtual scrolling for layers panel
5. Debounce history updates

### Code Quality
1. Full TypeScript coverage
2. Proper error handling
3. Comprehensive JSDoc comments
4. Unit tests for utilities
5. Integration tests for key workflows

### User Experience
1. Loading states for async operations
2. Keyboard shortcuts help panel
3. Tooltips for all tools
4. Responsive design
5. Accessibility (ARIA labels, keyboard navigation)

## Risk Mitigation

### Potential Issues
1. **Learning Curve**: Fabric.js API differs from Polotno
   - *Mitigation*: Comprehensive documentation and examples
   
2. **Feature Parity**: Ensuring all Polotno features are replicated
   - *Mitigation*: Feature checklist and thorough testing
   
3. **Performance**: Large canvases with many objects
   - *Mitigation*: Object caching, lazy loading, pagination
   
4. **Browser Compatibility**: Canvas API differences
   - *Mitigation*: Test on all major browsers, use polyfills if needed

## Success Criteria

1. ✅ All Polotno features replicated in Fabric.js
2. ✅ No regression in existing functionality
3. ✅ Performance equal to or better than Polotno
4. ✅ Full TypeScript type safety
5. ✅ Comprehensive test coverage
6. ✅ Documentation complete
7. ✅ Zero Polotno dependencies remaining

## Timeline Estimate

- **Phase 1**: 2-3 days
- **Phase 2**: 3-4 days
- **Phase 3**: 4-5 days
- **Phase 4**: 2-3 days
- **Phase 5**: 2-3 days
- **Phase 6**: 3-4 days

**Total**: 16-22 days (3-4 weeks)

## Next Steps

1. Review and approve this migration plan
2. Set up development branch for migration
3. Begin Phase 1 implementation
4. Regular progress reviews and adjustments

