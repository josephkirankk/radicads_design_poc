# Fabric.js Editor Testing Guide

## Overview
This guide provides a comprehensive testing checklist for the new Fabric.js editor implementation.

## Prerequisites
- Frontend dev server running on http://localhost:3001
- Backend server running on http://localhost:8000 (for save/load functionality)

## Testing Checklist

### 1. Canvas Initialization ✓
- [ ] Open http://localhost:3001/create
- [ ] Verify canvas loads without errors
- [ ] Check canvas size is 1080x1080
- [ ] Verify white background is displayed

### 2. Text Tools
- [ ] Click "Add Text" button
- [ ] Verify text appears on canvas with "Double click to edit"
- [ ] Double-click text to edit inline
- [ ] Type new text and verify it updates
- [ ] Select text and test properties panel:
  - [ ] Change font size (slider)
  - [ ] Toggle bold
  - [ ] Toggle italic
  - [ ] Toggle underline
  - [ ] Change text alignment (left, center, right, justify)
  - [ ] Change fill color
  - [ ] Change opacity

### 3. Shape Tools
#### Rectangle
- [ ] Click "Add Rectangle" button
- [ ] Verify rectangle appears on canvas
- [ ] Select rectangle and test:
  - [ ] Change fill color
  - [ ] Change stroke color
  - [ ] Change stroke width
  - [ ] Change opacity
  - [ ] Resize using corner handles
  - [ ] Rotate using rotation handle

#### Circle
- [ ] Click "Add Circle" button
- [ ] Verify circle appears on canvas
- [ ] Test same properties as rectangle

### 4. Image Tools
- [ ] Click "Add Image" button
- [ ] Select an image file from your computer
- [ ] Verify image loads on canvas
- [ ] Test image manipulation:
  - [ ] Move image
  - [ ] Resize image
  - [ ] Rotate image
  - [ ] Change opacity
  - [ ] Delete image

### 5. Drawing Tools
- [ ] Click "Draw" button to enable drawing mode
- [ ] Verify cursor changes
- [ ] Draw freehand on canvas
- [ ] Verify drawing appears as path object
- [ ] Click "Draw" again to disable drawing mode
- [ ] Select drawn path and test:
  - [ ] Change stroke color
  - [ ] Change stroke width
  - [ ] Delete path

### 6. Object Selection
#### Single Selection
- [ ] Click on any object
- [ ] Verify selection handles appear
- [ ] Verify properties panel updates

#### Multiple Selection
- [ ] Press Ctrl+A to select all objects
- [ ] Verify all objects are selected
- [ ] Verify properties panel shows "Multiple objects selected"
- [ ] Click canvas to deselect

### 7. Object Transformation
- [ ] Select any object
- [ ] Test move: Drag object to new position
- [ ] Test resize: Drag corner handles
- [ ] Test rotate: Drag rotation handle
- [ ] Verify transformations are smooth

### 8. Keyboard Shortcuts
- [ ] Select object and press Delete → Verify object is deleted
- [ ] Select object and press Ctrl+C → Copy
- [ ] Press Ctrl+V → Verify object is pasted
- [ ] Make a change and press Ctrl+Z → Verify undo works
- [ ] Press Ctrl+Y or Ctrl+Shift+Z → Verify redo works
- [ ] Press Ctrl+A → Verify all objects are selected

### 9. Layers Panel
- [ ] Open Layers tab in right sidebar
- [ ] Verify all objects are listed
- [ ] Test layer visibility:
  - [ ] Click eye icon to hide object
  - [ ] Click again to show object
- [ ] Test layer locking:
  - [ ] Click lock icon to lock object
  - [ ] Try to select locked object (should not be selectable)
  - [ ] Click lock icon again to unlock
- [ ] Test layer ordering:
  - [ ] Click up arrow to move object forward
  - [ ] Click down arrow to move object backward
  - [ ] Verify visual order changes on canvas
- [ ] Test layer selection:
  - [ ] Click layer name to select object
  - [ ] Verify object is selected on canvas
- [ ] Test layer deletion:
  - [ ] Click trash icon to delete object
  - [ ] Verify object is removed from canvas

### 10. Undo/Redo
- [ ] Add several objects to canvas
- [ ] Click Undo button multiple times
- [ ] Verify objects are removed in reverse order
- [ ] Click Redo button multiple times
- [ ] Verify objects are restored
- [ ] Test undo/redo with keyboard shortcuts (Ctrl+Z, Ctrl+Y)

### 11. Zoom Controls
- [ ] Click "Zoom In" button
- [ ] Verify canvas zooms in and percentage updates
- [ ] Click "Zoom Out" button
- [ ] Verify canvas zooms out and percentage updates
- [ ] Verify zoom percentage is displayed correctly

### 12. Clear Canvas
- [ ] Add multiple objects to canvas
- [ ] Click "Clear" button
- [ ] Verify all objects are removed
- [ ] Verify undo still works after clear

### 13. Export Functionality
- [ ] Add some objects to canvas
- [ ] Click "Export" button
- [ ] Test each export format:
  - [ ] PNG - Verify download starts
  - [ ] JPEG - Verify download starts
  - [ ] SVG - Verify download starts
  - [ ] JSON - Verify download starts
- [ ] Open downloaded files to verify they're correct

### 14. Save/Load (Requires Backend)
- [ ] Add objects to canvas
- [ ] Click "Save" button
- [ ] Verify design is saved (check console for success)
- [ ] Refresh page
- [ ] Verify design loads correctly
- [ ] Test with complex designs (multiple objects, different types)

### 15. Browser Compatibility
Test in multiple browsers:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if available)

### 16. Performance Testing
- [ ] Add 50+ objects to canvas
- [ ] Test selection performance
- [ ] Test transformation performance
- [ ] Test undo/redo with many objects
- [ ] Verify no lag or freezing

### 17. Error Handling
- [ ] Try to add image with invalid file type
- [ ] Try to load corrupted JSON
- [ ] Test with very large images
- [ ] Verify appropriate error messages

## Known Limitations
1. Backend integration for save/load needs to be updated to handle Fabric.js JSON format
2. Image filters not yet implemented
3. Object grouping not yet implemented
4. Advanced alignment tools not yet implemented

## Reporting Issues
If you find any issues during testing:
1. Note the exact steps to reproduce
2. Check browser console for errors
3. Take screenshots if applicable
4. Document expected vs actual behavior

## Next Steps After Testing
1. Fix any bugs found during testing
2. Implement remaining features (filters, grouping, etc.)
3. Optimize performance if needed
4. Update backend API for Fabric.js JSON format
5. Add comprehensive unit and integration tests

