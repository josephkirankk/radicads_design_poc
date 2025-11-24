"use client";

import React, { useEffect, useRef } from "react";
import { Canvas, PencilBrush } from "fabric";
import { useFabricEditorStore } from "@/store/fabricEditorStore";

interface FabricCanvasProps {
  width?: number;
  height?: number;
  onReady?: (canvas: Canvas) => void;
}

export const FabricCanvas: React.FC<FabricCanvasProps> = ({
  width = 1080,
  height = 1080,
  onReady,
}) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const {
    canvas,
    setCanvas,
    setSelectedObjects,
    brushColor,
    brushWidth,
    backgroundColor,
    addToHistory,
  } = useFabricEditorStore();

  // Initialize Fabric.js canvas
  useEffect(() => {
    if (!canvasRef.current) {
      return;
    }

    const fabricCanvas = new Canvas(canvasRef.current, {
      width,
      height,
      backgroundColor,
      selection: true,
      preserveObjectStacking: true,
    });

    // Set up default brush for drawing mode
    const brush = new PencilBrush(fabricCanvas);
    brush.color = brushColor;
    brush.width = brushWidth;
    fabricCanvas.freeDrawingBrush = brush;

    // Set canvas in store
    setCanvas(fabricCanvas);

    // Call onReady callback
    if (onReady) {
      onReady(fabricCanvas);
    }

    // Add initial state to history
    setTimeout(() => {
      addToHistory();
    }, 100);

    // Cleanup on unmount
    return () => {
      fabricCanvas.dispose();
      setCanvas(null);
    };
  }, []); // Only run once on mount

  // Update brush properties when they change
  useEffect(() => {
    if (!canvas || !canvas.freeDrawingBrush) return;
    canvas.freeDrawingBrush.color = brushColor;
    canvas.freeDrawingBrush.width = brushWidth;
  }, [canvas, brushColor, brushWidth]);

  // Update background color when it changes
  useEffect(() => {
    if (!canvas) return;
    canvas.backgroundColor = backgroundColor;
    canvas.renderAll();
  }, [canvas, backgroundColor]);

  // Handle selection events
  useEffect(() => {
    if (!canvas) return;

    const handleSelection = () => {
      const activeObjects = canvas.getActiveObjects();
      setSelectedObjects(activeObjects);
    };

    const handleObjectModified = () => {
      addToHistory();
    };

    const handleObjectAdded = () => {
      addToHistory();
    };

    const handleObjectRemoved = () => {
      addToHistory();
    };

    // Subscribe to events
    canvas.on("selection:created", handleSelection);
    canvas.on("selection:updated", handleSelection);
    canvas.on("selection:cleared", handleSelection);
    canvas.on("object:modified", handleObjectModified);
    canvas.on("object:added", handleObjectAdded);
    canvas.on("object:removed", handleObjectRemoved);

    // Cleanup
    return () => {
      canvas.off("selection:created", handleSelection);
      canvas.off("selection:updated", handleSelection);
      canvas.off("selection:cleared", handleSelection);
      canvas.off("object:modified", handleObjectModified);
      canvas.off("object:added", handleObjectAdded);
      canvas.off("object:removed", handleObjectRemoved);
    };
  }, [canvas, setSelectedObjects, addToHistory]);

  // Handle keyboard shortcuts
  useEffect(() => {
    if (!canvas) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      // Delete selected objects
      if (e.key === "Delete" || e.key === "Backspace") {
        const activeObjects = canvas.getActiveObjects();
        if (activeObjects.length > 0) {
          activeObjects.forEach((obj) => canvas.remove(obj));
          canvas.discardActiveObject();
          canvas.renderAll();
        }
      }

      // Select all
      if ((e.ctrlKey || e.metaKey) && e.key === "a") {
        e.preventDefault();
        const allObjects = canvas.getObjects();
        const selection = new (Canvas as any).ActiveSelection(allObjects, {
          canvas,
        });
        canvas.setActiveObject(selection);
        canvas.renderAll();
      }

      // Copy (Ctrl+C)
      if ((e.ctrlKey || e.metaKey) && e.key === "c") {
        const activeObject = canvas.getActiveObject();
        if (activeObject) {
          activeObject.clone().then((cloned: any) => {
            (window as any)._clipboard = cloned;
          });
        }
      }

      // Paste (Ctrl+V)
      if ((e.ctrlKey || e.metaKey) && e.key === "v") {
        const clipboard = (window as any)._clipboard;
        if (clipboard) {
          clipboard.clone().then((clonedObj: any) => {
            canvas.discardActiveObject();
            clonedObj.set({
              left: clonedObj.left + 10,
              top: clonedObj.top + 10,
              evented: true,
            });
            if (clonedObj.type === "activeSelection") {
              clonedObj.canvas = canvas;
              clonedObj.forEachObject((obj: any) => {
                canvas.add(obj);
              });
              clonedObj.setCoords();
            } else {
              canvas.add(clonedObj);
            }
            (window as any)._clipboard.top += 10;
            (window as any)._clipboard.left += 10;
            canvas.setActiveObject(clonedObj);
            canvas.requestRenderAll();
          });
        }
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [canvas]);

  return (
    <div
      ref={containerRef}
      className="flex items-center justify-center bg-gray-100 p-4 w-full h-full"
    >
      <div className="shadow-lg bg-white">
        <canvas ref={canvasRef} id="fabric-canvas" />
      </div>
    </div>
  );
};

