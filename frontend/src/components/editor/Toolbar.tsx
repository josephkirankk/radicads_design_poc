"use client";

import React, { useRef } from "react";
import {
  Type,
  Square,
  Circle,
  Image as ImageIcon,
  Pencil,
  Undo2,
  Redo2,
  Download,
  Trash2,
  ZoomIn,
  ZoomOut,
  Save,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { useFabricEditorStore } from "@/store/fabricEditorStore";
import { IText, Rect, Circle as FabricCircle, FabricImage } from "fabric";
import { useFabricDesign } from "@/hooks/useFabricDesign";

export const Toolbar: React.FC = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const {
    canvas,
    activeTool,
    setActiveTool,
    isDrawingMode,
    setDrawingMode,
    undo,
    redo,
    canUndo,
    canRedo,
    zoom,
    setZoom,
  } = useFabricEditorStore();
  const { saveDesignToJSON, downloadDesign } = useFabricDesign();

  const handleAddText = () => {
    if (!canvas) return;

    const text = new IText("Edit this text", {
      left: canvas.width! / 2 - 50,
      top: canvas.height! / 2 - 20,
      fontSize: 32,
      fill: "#000000",
      fontFamily: "Arial",
    });

    canvas.add(text);
    canvas.setActiveObject(text);
    canvas.renderAll();
    setActiveTool("text");
  };

  const handleAddRectangle = () => {
    if (!canvas) return;

    const rect = new Rect({
      left: canvas.width! / 2 - 50,
      top: canvas.height! / 2 - 50,
      width: 100,
      height: 100,
      fill: "#3b82f6",
      stroke: "#1e40af",
      strokeWidth: 2,
    });

    canvas.add(rect);
    canvas.setActiveObject(rect);
    canvas.renderAll();
    setActiveTool("rectangle");
  };

  const handleAddCircle = () => {
    if (!canvas) return;

    const circle = new FabricCircle({
      left: canvas.width! / 2 - 50,
      top: canvas.height! / 2 - 50,
      radius: 50,
      fill: "#10b981",
      stroke: "#059669",
      strokeWidth: 2,
    });

    canvas.add(circle);
    canvas.setActiveObject(circle);
    canvas.renderAll();
    setActiveTool("circle");
  };

  const handleAddImage = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !canvas) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const imgUrl = event.target?.result as string;
      FabricImage.fromURL(imgUrl).then((img) => {
        img.scaleToWidth(300);
        img.set({
          left: canvas.width! / 2 - (img.getScaledWidth() / 2),
          top: canvas.height! / 2 - (img.getScaledHeight() / 2),
        });
        canvas.add(img);
        canvas.setActiveObject(img);
        canvas.renderAll();
      });
    };
    reader.readAsDataURL(file);
    e.target.value = "";
  };

  const handleToggleDrawing = () => {
    setDrawingMode(!isDrawingMode);
    setActiveTool(isDrawingMode ? "select" : "draw");
  };

  const handleClearCanvas = () => {
    if (!canvas) return;
    if (window.confirm("Are you sure you want to clear the canvas?")) {
      canvas.clear();
      canvas.backgroundColor = "#ffffff";
      canvas.renderAll();
    }
  };

  const handleSave = () => {
    const json = saveDesignToJSON();
    if (json) {
      console.log("Design saved:", json);
      // TODO: Send to backend API to save
      alert("Design saved to console. Backend integration pending.");
    }
  };

  const handleExport = () => {
    downloadDesign("png");
  };

  const handleZoomIn = () => {
    if (!canvas) return;
    const newZoom = Math.min(zoom + 0.1, 3);
    canvas.setZoom(newZoom);
    setZoom(newZoom);
  };

  const handleZoomOut = () => {
    if (!canvas) return;
    const newZoom = Math.max(zoom - 0.1, 0.1);
    canvas.setZoom(newZoom);
    setZoom(newZoom);
  };

  return (
    <div className="flex items-center gap-2 p-4 border-b bg-background">
      <div className="flex items-center gap-1 border-r pr-2">
        <Button
          variant={activeTool === "text" ? "default" : "ghost"}
          size="icon"
          onClick={handleAddText}
          title="Add Text"
        >
          <Type className="h-4 w-4" />
        </Button>
        <Button
          variant={activeTool === "rectangle" ? "default" : "ghost"}
          size="icon"
          onClick={handleAddRectangle}
          title="Add Rectangle"
        >
          <Square className="h-4 w-4" />
        </Button>
        <Button
          variant={activeTool === "circle" ? "default" : "ghost"}
          size="icon"
          onClick={handleAddCircle}
          title="Add Circle"
        >
          <Circle className="h-4 w-4" />
        </Button>
        <Button
          variant={activeTool === "image" ? "default" : "ghost"}
          size="icon"
          onClick={handleAddImage}
          title="Add Image"
        >
          <ImageIcon className="h-4 w-4" />
        </Button>
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          className="hidden"
        />
        <Button
          variant={isDrawingMode ? "default" : "ghost"}
          size="icon"
          onClick={handleToggleDrawing}
          title="Drawing Mode"
        >
          <Pencil className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex items-center gap-1 border-r pr-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={undo}
          disabled={!canUndo}
          title="Undo"
        >
          <Undo2 className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          onClick={redo}
          disabled={!canRedo}
          title="Redo"
        >
          <Redo2 className="h-4 w-4" />
        </Button>
      </div>

      <div className="flex items-center gap-1 border-r pr-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={handleZoomIn}
          title="Zoom In"
        >
          <ZoomIn className="h-4 w-4" />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          onClick={handleZoomOut}
          title="Zoom Out"
        >
          <ZoomOut className="h-4 w-4" />
        </Button>
        <span className="text-sm text-muted-foreground px-2">
          {Math.round(zoom * 100)}%
        </span>
      </div>

      <div className="flex items-center gap-1 ml-auto">
        <Button
          variant="ghost"
          size="icon"
          onClick={handleClearCanvas}
          title="Clear Canvas"
        >
          <Trash2 className="h-4 w-4" />
        </Button>
        <Button variant="outline" size="sm" onClick={handleSave} title="Save">
          <Save className="h-4 w-4 mr-2" />
          Save
        </Button>
        <Button
          variant="default"
          size="sm"
          onClick={handleExport}
          title="Export as PNG"
        >
          <Download className="h-4 w-4 mr-2" />
          Export
        </Button>
      </div>
    </div>
  );
};

