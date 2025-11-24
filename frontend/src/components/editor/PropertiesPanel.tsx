"use client";

import React, { useState, useEffect } from "react";
import { useFabricEditorStore } from "@/store/fabricEditorStore";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import {
  AlignLeft,
  AlignCenter,
  AlignRight,
  AlignJustify,
  Bold,
  Italic,
  Underline,
} from "lucide-react";

// Helper function to convert color to hex format
const toHexColor = (color: any): string => {
  if (!color) return "#000000";
  if (typeof color === "string") {
    // If already hex, return as is
    if (color.startsWith("#")) return color;
    // Convert named colors to hex
    if (color === "red") return "#ff0000";
    if (color === "blue") return "#0000ff";
    if (color === "green") return "#00ff00";
    if (color === "white") return "#ffffff";
    if (color === "black") return "#000000";
    // For other formats, return black as fallback
    return "#000000";
  }
  return "#000000";
};

export const PropertiesPanel: React.FC = () => {
  const { canvas, selectedObjects } = useFabricEditorStore();
  const [properties, setProperties] = useState<any>({
    fill: "#000000",
    stroke: "#000000",
    strokeWidth: 0,
    opacity: 1,
    angle: 0,
    fontSize: 16,
    fontFamily: "Arial",
    fontWeight: "normal",
    fontStyle: "normal",
    textAlign: "left",
    underline: false,
  });

  useEffect(() => {
    if (selectedObjects.length === 1) {
      const obj = selectedObjects[0];
      setProperties({
        fill: toHexColor(obj.fill),
        stroke: toHexColor(obj.stroke),
        strokeWidth: obj.strokeWidth || 0,
        opacity: obj.opacity !== undefined ? obj.opacity : 1,
        angle: obj.angle || 0,
        // Text properties
        fontSize: (obj as any).fontSize || 16,
        fontFamily: (obj as any).fontFamily || "Arial",
        fontWeight: (obj as any).fontWeight || "normal",
        fontStyle: (obj as any).fontStyle || "normal",
        textAlign: (obj as any).textAlign || "left",
        underline: (obj as any).underline || false,
      });
    } else {
      // Reset to defaults when no object is selected
      setProperties({
        fill: "#000000",
        stroke: "#000000",
        strokeWidth: 0,
        opacity: 1,
        angle: 0,
        fontSize: 16,
        fontFamily: "Arial",
        fontWeight: "normal",
        fontStyle: "normal",
        textAlign: "left",
        underline: false,
      });
    }
  }, [selectedObjects]);

  if (selectedObjects.length === 0) {
    return (
      <div className="w-64 border-l bg-background p-4">
        <p className="text-sm text-muted-foreground">
          Select an object to edit its properties
        </p>
      </div>
    );
  }

  if (selectedObjects.length > 1) {
    return (
      <div className="w-64 border-l bg-background p-4">
        <p className="text-sm text-muted-foreground">
          {selectedObjects.length} objects selected
        </p>
      </div>
    );
  }

  const obj = selectedObjects[0];
  const isText = obj.type === "i-text" || obj.type === "text";

  const updateProperty = (key: string, value: any) => {
    if (!canvas) return;
    obj.set(key as any, value);
    canvas.renderAll();
    setProperties({ ...properties, [key]: value });
  };

  const handleColorChange = (key: string, value: string) => {
    updateProperty(key, value);
  };

  const handleTextAlign = (align: string) => {
    updateProperty("textAlign", align);
  };

  const toggleBold = () => {
    const newWeight = properties.fontWeight === "bold" ? "normal" : "bold";
    updateProperty("fontWeight", newWeight);
  };

  const toggleItalic = () => {
    const newStyle = properties.fontStyle === "italic" ? "normal" : "italic";
    updateProperty("fontStyle", newStyle);
  };

  const toggleUnderline = () => {
    updateProperty("underline", !properties.underline);
  };

  return (
    <div className="w-64 border-l bg-background p-4 overflow-y-auto">
      <h3 className="font-semibold mb-4">Properties</h3>

      <div className="space-y-4">
        {/* Fill Color */}
        <div>
          <Label htmlFor="fill">Fill Color</Label>
          <div className="flex gap-2 mt-1">
            <input
              id="fill"
              type="color"
              value={properties.fill}
              onChange={(e) => handleColorChange("fill", e.target.value)}
              className="w-12 h-8 rounded cursor-pointer"
            />
            <input
              type="text"
              value={properties.fill}
              onChange={(e) => handleColorChange("fill", e.target.value)}
              className="flex-1 px-2 py-1 text-sm border rounded"
            />
          </div>
        </div>

        {/* Stroke Color */}
        <div>
          <Label htmlFor="stroke">Stroke Color</Label>
          <div className="flex gap-2 mt-1">
            <input
              id="stroke"
              type="color"
              value={properties.stroke}
              onChange={(e) => handleColorChange("stroke", e.target.value)}
              className="w-12 h-8 rounded cursor-pointer"
            />
            <input
              type="text"
              value={properties.stroke}
              onChange={(e) => handleColorChange("stroke", e.target.value)}
              className="flex-1 px-2 py-1 text-sm border rounded"
            />
          </div>
        </div>

        {/* Stroke Width */}
        <div>
          <Label htmlFor="strokeWidth">Stroke Width</Label>
          <input
            id="strokeWidth"
            type="range"
            min="0"
            max="20"
            value={properties.strokeWidth}
            onChange={(e) =>
              updateProperty("strokeWidth", parseInt(e.target.value))
            }
            className="w-full mt-1"
          />
          <span className="text-sm text-muted-foreground">
            {properties.strokeWidth}px
          </span>
        </div>

        {/* Opacity */}
        <div>
          <Label htmlFor="opacity">Opacity</Label>
          <input
            id="opacity"
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={properties.opacity}
            onChange={(e) =>
              updateProperty("opacity", parseFloat(e.target.value))
            }
            className="w-full mt-1"
          />
          <span className="text-sm text-muted-foreground">
            {Math.round(properties.opacity * 100)}%
          </span>
        </div>

        {/* Text Properties */}
        {isText && (
          <>
            <div>
              <Label htmlFor="fontSize">Font Size</Label>
              <input
                id="fontSize"
                type="number"
                min="8"
                max="200"
                value={properties.fontSize}
                onChange={(e) =>
                  updateProperty("fontSize", parseInt(e.target.value))
                }
                className="w-full px-2 py-1 text-sm border rounded mt-1"
              />
            </div>

            <div>
              <Label>Text Style</Label>
              <div className="flex gap-1 mt-1">
                <Button
                  variant={
                    properties.fontWeight === "bold" ? "default" : "outline"
                  }
                  size="icon"
                  onClick={toggleBold}
                >
                  <Bold className="h-4 w-4" />
                </Button>
                <Button
                  variant={
                    properties.fontStyle === "italic" ? "default" : "outline"
                  }
                  size="icon"
                  onClick={toggleItalic}
                >
                  <Italic className="h-4 w-4" />
                </Button>
                <Button
                  variant={properties.underline ? "default" : "outline"}
                  size="icon"
                  onClick={toggleUnderline}
                >
                  <Underline className="h-4 w-4" />
                </Button>
              </div>
            </div>

            <div>
              <Label>Text Align</Label>
              <div className="flex gap-1 mt-1">
                <Button
                  variant={
                    properties.textAlign === "left" ? "default" : "outline"
                  }
                  size="icon"
                  onClick={() => handleTextAlign("left")}
                >
                  <AlignLeft className="h-4 w-4" />
                </Button>
                <Button
                  variant={
                    properties.textAlign === "center" ? "default" : "outline"
                  }
                  size="icon"
                  onClick={() => handleTextAlign("center")}
                >
                  <AlignCenter className="h-4 w-4" />
                </Button>
                <Button
                  variant={
                    properties.textAlign === "right" ? "default" : "outline"
                  }
                  size="icon"
                  onClick={() => handleTextAlign("right")}
                >
                  <AlignRight className="h-4 w-4" />
                </Button>
                <Button
                  variant={
                    properties.textAlign === "justify" ? "default" : "outline"
                  }
                  size="icon"
                  onClick={() => handleTextAlign("justify")}
                >
                  <AlignJustify className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

