# Debugging Canvas Issue

## Current Status
The Fabric.js editor has been implemented but the canvas appears blank in the browser.

## What We've Done

### 1. Implementation Complete
- ✅ Created all editor components (FabricCanvas, Toolbar, PropertiesPanel, LayersPanel, FabricEditor)
- ✅ Set up Zustand state management
- ✅ Installed Fabric.js v6.9.0
- ✅ Build successful with no TypeScript errors
- ✅ Servers running (frontend on port 3000, backend on port 8000)

### 2. Test Page Created
- Created `/test-editor` route to test editor without needing a design ID
- Added test red rectangle to verify canvas rendering
- Added console logging to track canvas initialization

### 3. Layout Fixes Applied
- Changed canvas container from `overflow-hidden` to `overflow-auto`
- Added explicit `h-full` and `w-full` classes
- Added `bg-white` to canvas wrapper for visibility

## What to Check in Browser

### Open: http://localhost:3000/test-editor

### Expected to See:
1. **Header**: "Radic Editor" text at the top
2. **Toolbar**: Row of buttons (Add Text, Add Rectangle, Add Circle, etc.)
3. **Canvas Area**: Gray background with white canvas containing a red rectangle (100x100px at position 100,100)
4. **Right Sidebar**: Tabs for "Properties" and "Layers"

### Browser Console (F12)
Look for these console.log messages:
- "FabricCanvas: Initializing canvas with dimensions: 1080 1080"
- "FabricCanvas: Canvas created: [Canvas object]"
- "FabricCanvas: Canvas element: [HTMLCanvasElement]"
- "FabricCanvas: Initialization complete"
- "Canvas ready: [Canvas object]"

### Possible Issues

#### Issue 1: Canvas Not Rendering
**Symptoms**: Blank gray area where canvas should be
**Possible Causes**:
- Canvas element not being created
- Fabric.js not initializing properly
- CSS hiding the canvas

**Check**:
- Open browser DevTools (F12)
- Go to Elements tab
- Look for `<canvas id="fabric-canvas">`
- Check if it has width/height attributes
- Check computed styles

#### Issue 2: Canvas Too Small
**Symptoms**: Canvas exists but is tiny or not visible
**Possible Causes**:
- Canvas dimensions not being set
- Parent container has no height

**Check**:
- In Elements tab, find the canvas element
- Check its computed width and height
- Should be 1080x1080

#### Issue 3: Z-Index or Overflow Issue
**Symptoms**: Canvas exists but is behind other elements or clipped
**Possible Causes**:
- CSS z-index issues
- Overflow hidden on parent

**Check**:
- In Elements tab, check parent divs
- Look for `overflow: hidden` or negative z-index

#### Issue 4: Fabric.js Import Error
**Symptoms**: Console errors about Fabric.js
**Possible Causes**:
- Import statement incorrect
- Package not installed properly

**Check**:
- Console tab for errors
- Network tab for failed module loads

## Quick Fixes to Try

### Fix 1: Force Canvas Visibility
Add inline styles to canvas:
```tsx
<canvas 
  ref={canvasRef} 
  id="fabric-canvas"
  style={{ border: "2px solid red", display: "block" }}
/>
```

### Fix 2: Check Canvas Initialization
Add more logging:
```tsx
console.log("Canvas ref:", canvasRef.current);
console.log("Canvas width:", fabricCanvas.width);
console.log("Canvas height:", fabricCanvas.height);
console.log("Canvas element:", fabricCanvas.getElement());
```

### Fix 3: Verify Fabric.js is Loaded
In browser console, type:
```javascript
window.fabric
```
Should return undefined (Fabric v6 doesn't use global)

Try:
```javascript
document.querySelector('#fabric-canvas')
```
Should return the canvas element

### Fix 4: Check if Canvas Has Content
In browser console:
```javascript
const canvas = document.querySelector('#fabric-canvas');
const ctx = canvas.getContext('2d');
console.log('Canvas context:', ctx);
```

## Files to Review

1. `frontend/src/components/editor/FabricCanvas.tsx` - Canvas initialization
2. `frontend/src/components/editor/FabricEditor.tsx` - Layout structure
3. `frontend/src/store/fabricEditorStore.ts` - State management
4. `frontend/src/app/test-editor/page.tsx` - Test page

## Next Steps

1. **User checks browser** - Report what you see
2. **Check console logs** - Any errors or messages?
3. **Inspect element** - Does canvas element exist?
4. **Try clicking toolbar buttons** - Do they work?
5. **Check network tab** - Is Fabric.js loading?

## Contact Points

If canvas is visible but blank:
- Check if test rectangle was added
- Try clicking "Add Text" or "Add Rectangle" buttons
- Check if objects appear in Layers panel

If canvas is not visible at all:
- Check browser console for errors
- Inspect element to see if canvas exists
- Check if parent containers have height

If toolbar/panels not visible:
- Check if components are rendering
- Look for React errors in console
- Check if Tailwind CSS is loading

