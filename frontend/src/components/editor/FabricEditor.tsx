"use client";

import React, { useEffect, useState } from "react";
import { FabricCanvas } from "./FabricCanvas";
import { Toolbar } from "./Toolbar";
import { PropertiesPanel } from "./PropertiesPanel";
import { LayersPanel } from "./LayersPanel";
import { useFabricEditorStore } from "@/store/fabricEditorStore";
import { Canvas } from "fabric";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

interface FabricEditorProps {
  design?: any;
  width?: number;
  height?: number;
}

export const FabricEditor: React.FC<FabricEditorProps> = ({
  design,
  width = 1080,
  height = 1080,
}) => {
  const { canvas, undo, redo } = useFabricEditorStore();
  const [activeTab, setActiveTab] = useState("properties");

  // Load design data when provided
  useEffect(() => {
    if (!canvas || !design) {
      console.log("[FabricEditor] Canvas or design not ready:", { canvas: !!canvas, design: !!design });
      return;
    }

    console.log("[FabricEditor] Loading design data:", design);

    try {
      // Check if design has Fabric.js JSON format
      if (design.design_json && typeof design.design_json === "object") {
        console.log("[FabricEditor] Loading design_json (object):", design.design_json);

        // Load the JSON and ensure proper rendering
        canvas.loadFromJSON(design.design_json).then(() => {
          console.log("[FabricEditor] Design loaded, rendering canvas");

          // Set canvas dimensions if specified in the design
          if (design.design_json.width) {
            canvas.setWidth(design.design_json.width);
          }
          if (design.design_json.height) {
            canvas.setHeight(design.design_json.height);
          }

          // Set background if specified
          if (design.design_json.background) {
            canvas.backgroundColor = design.design_json.background;
          }

          // Force canvas to render
          canvas.requestRenderAll();

          // Additional render after a short delay to ensure everything is loaded
          setTimeout(() => {
            canvas.requestRenderAll();
            console.log("[FabricEditor] Design loaded successfully, objects:", canvas.getObjects().length);
          }, 100);
        }).catch((error) => {
          console.error("[FabricEditor] Error in loadFromJSON:", error);
        });
      } else if (design.design_json && typeof design.design_json === "string") {
        console.log("[FabricEditor] Loading design_json (string)");
        const jsonData = JSON.parse(design.design_json);

        canvas.loadFromJSON(jsonData).then(() => {
          console.log("[FabricEditor] Design loaded, rendering canvas");

          // Set canvas dimensions if specified in the design
          if (jsonData.width) {
            canvas.setWidth(jsonData.width);
          }
          if (jsonData.height) {
            canvas.setHeight(jsonData.height);
          }

          // Set background if specified
          if (jsonData.background) {
            canvas.backgroundColor = jsonData.background;
          }

          // Force canvas to render
          canvas.requestRenderAll();

          // Additional render after a short delay to ensure everything is loaded
          setTimeout(() => {
            canvas.requestRenderAll();
            console.log("[FabricEditor] Design loaded successfully, objects:", canvas.getObjects().length);
          }, 100);
        }).catch((error) => {
          console.error("[FabricEditor] Error in loadFromJSON:", error);
        });
      } else {
        console.log("[FabricEditor] No valid design data to load");
      }
    } catch (error) {
      console.error("[FabricEditor] Error loading design:", error);
    }
  }, [canvas, design]);

  // Handle keyboard shortcuts for undo/redo
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Undo: Ctrl+Z or Cmd+Z
      if ((e.ctrlKey || e.metaKey) && e.key === "z" && !e.shiftKey) {
        e.preventDefault();
        undo();
      }

      // Redo: Ctrl+Shift+Z or Cmd+Shift+Z or Ctrl+Y
      if (
        ((e.ctrlKey || e.metaKey) && e.key === "z" && e.shiftKey) ||
        ((e.ctrlKey || e.metaKey) && e.key === "y")
      ) {
        e.preventDefault();
        redo();
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [undo, redo]);

  const handleCanvasReady = (fabricCanvas: Canvas) => {
    console.log("Canvas ready:", fabricCanvas);
  };

  return (
    <div className="h-screen w-screen flex flex-col">
      <div className="h-12 border-b flex items-center px-4 justify-between bg-background">
        <div className="font-bold">Radic Editor</div>
      </div>
      <Toolbar />
      <div className="flex-1 flex overflow-hidden">
        <div className="flex-1 overflow-auto h-full">
          <FabricCanvas
            width={width}
            height={height}
            onReady={handleCanvasReady}
          />
        </div>
        <div className="w-64 border-l bg-background">
          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="w-full">
              <TabsTrigger value="properties" className="flex-1">
                Properties
              </TabsTrigger>
              <TabsTrigger value="layers" className="flex-1">
                Layers
              </TabsTrigger>
            </TabsList>
            <TabsContent value="properties" className="m-0">
              <PropertiesPanel />
            </TabsContent>
            <TabsContent value="layers" className="m-0">
              <LayersPanel />
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
};

export default FabricEditor;

