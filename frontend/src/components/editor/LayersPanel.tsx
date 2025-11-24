"use client";

import React, { useState, useEffect } from "react";
import { useFabricEditorStore } from "@/store/fabricEditorStore";
import { Button } from "@/components/ui/button";
import {
  Eye,
  EyeOff,
  Lock,
  Unlock,
  Trash2,
  ChevronUp,
  ChevronDown,
} from "lucide-react";
import { FabricObject } from "fabric";

interface LayerItem {
  id: string;
  object: FabricObject;
  name: string;
  type: string;
  visible: boolean;
  locked: boolean;
}

export const LayersPanel: React.FC = () => {
  const { canvas, selectedObjects } = useFabricEditorStore();
  const [layers, setLayers] = useState<LayerItem[]>([]);

  useEffect(() => {
    if (!canvas) return;

    const updateLayers = () => {
      const objects = canvas.getObjects();
      const layerItems: LayerItem[] = objects.map((obj, index) => ({
        id: `layer-${index}`,
        object: obj,
        name: (obj as any).name || `${obj.type} ${index + 1}`,
        type: obj.type || "object",
        visible: obj.visible !== false,
        locked: obj.selectable === false,
      }));
      setLayers(layerItems.reverse()); // Reverse to show top layer first
    };

    updateLayers();

    canvas.on("object:added", updateLayers);
    canvas.on("object:removed", updateLayers);
    canvas.on("object:modified", updateLayers);

    return () => {
      canvas.off("object:added", updateLayers);
      canvas.off("object:removed", updateLayers);
      canvas.off("object:modified", updateLayers);
    };
  }, [canvas]);

  const handleSelectLayer = (layer: LayerItem) => {
    if (!canvas) return;
    canvas.setActiveObject(layer.object);
    canvas.renderAll();
  };

  const handleToggleVisibility = (layer: LayerItem, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!canvas) return;
    layer.object.visible = !layer.object.visible;
    canvas.renderAll();
    setLayers([...layers]);
  };

  const handleToggleLock = (layer: LayerItem, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!canvas) return;
    layer.object.selectable = !layer.object.selectable;
    layer.object.evented = !layer.object.evented;
    canvas.renderAll();
    setLayers([...layers]);
  };

  const handleDeleteLayer = (layer: LayerItem, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!canvas) return;
    canvas.remove(layer.object);
    canvas.renderAll();
  };

  const handleMoveUp = (layer: LayerItem, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!canvas) return;
    canvas.bringObjectForward(layer.object);
    canvas.renderAll();
  };

  const handleMoveDown = (layer: LayerItem, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!canvas) return;
    canvas.sendObjectBackwards(layer.object);
    canvas.renderAll();
  };

  const isSelected = (layer: LayerItem) => {
    return selectedObjects.some((obj) => obj === layer.object);
  };

  return (
    <div className="w-64 border-l bg-background p-4 overflow-y-auto">
      <h3 className="font-semibold mb-4">Layers</h3>

      {layers.length === 0 ? (
        <p className="text-sm text-muted-foreground">No layers yet</p>
      ) : (
        <div className="space-y-1">
          {layers.map((layer) => (
            <div
              key={layer.id}
              className={`flex items-center gap-2 p-2 rounded cursor-pointer hover:bg-accent ${
                isSelected(layer) ? "bg-accent" : ""
              }`}
              onClick={() => handleSelectLayer(layer)}
            >
              <div className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6"
                  onClick={(e) => handleToggleVisibility(layer, e)}
                >
                  {layer.visible ? (
                    <Eye className="h-3 w-3" />
                  ) : (
                    <EyeOff className="h-3 w-3" />
                  )}
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6"
                  onClick={(e) => handleToggleLock(layer, e)}
                >
                  {layer.locked ? (
                    <Lock className="h-3 w-3" />
                  ) : (
                    <Unlock className="h-3 w-3" />
                  )}
                </Button>
              </div>

              <div className="flex-1 min-w-0">
                <p className="text-sm truncate">{layer.name}</p>
                <p className="text-xs text-muted-foreground">{layer.type}</p>
              </div>

              <div className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6"
                  onClick={(e) => handleMoveUp(layer, e)}
                >
                  <ChevronUp className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6"
                  onClick={(e) => handleMoveDown(layer, e)}
                >
                  <ChevronDown className="h-3 w-3" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-6 w-6"
                  onClick={(e) => handleDeleteLayer(layer, e)}
                >
                  <Trash2 className="h-3 w-3" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

