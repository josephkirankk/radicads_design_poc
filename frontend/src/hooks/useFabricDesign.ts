import { useFabricEditorStore } from "@/store/fabricEditorStore";
import { useCallback } from "react";

export const useFabricDesign = () => {
  const { canvas } = useFabricEditorStore();

  const saveDesignToJSON = useCallback(() => {
    if (!canvas) {
      console.error("Canvas not initialized");
      return null;
    }

    try {
      const json = canvas.toJSON();
      return json;
    } catch (error) {
      console.error("Error saving design to JSON:", error);
      return null;
    }
  }, [canvas]);

  const loadDesignFromJSON = useCallback(
    (jsonData: any) => {
      if (!canvas) {
        console.error("Canvas not initialized");
        return false;
      }

      try {
        canvas.loadFromJSON(jsonData, () => {
          canvas.renderAll();
          console.log("Design loaded successfully");
        });
        return true;
      } catch (error) {
        console.error("Error loading design from JSON:", error);
        return false;
      }
    },
    [canvas]
  );

  const exportToPNG = useCallback(
    (options?: { quality?: number; multiplier?: number }) => {
      if (!canvas) {
        console.error("Canvas not initialized");
        return null;
      }

      try {
        const dataURL = canvas.toDataURL({
          format: "png",
          quality: options?.quality || 1,
          multiplier: options?.multiplier || 2,
        });
        return dataURL;
      } catch (error) {
        console.error("Error exporting to PNG:", error);
        return null;
      }
    },
    [canvas]
  );

  const exportToJPEG = useCallback(
    (options?: { quality?: number; multiplier?: number }) => {
      if (!canvas) {
        console.error("Canvas not initialized");
        return null;
      }

      try {
        const dataURL = canvas.toDataURL({
          format: "jpeg",
          quality: options?.quality || 0.9,
          multiplier: options?.multiplier || 2,
        });
        return dataURL;
      } catch (error) {
        console.error("Error exporting to JPEG:", error);
        return null;
      }
    },
    [canvas]
  );

  const exportToSVG = useCallback(() => {
    if (!canvas) {
      console.error("Canvas not initialized");
      return null;
    }

    try {
      const svg = canvas.toSVG();
      return svg;
    } catch (error) {
      console.error("Error exporting to SVG:", error);
      return null;
    }
  }, [canvas]);

  const clearCanvas = useCallback(() => {
    if (!canvas) {
      console.error("Canvas not initialized");
      return false;
    }

    try {
      canvas.clear();
      canvas.backgroundColor = "#ffffff";
      canvas.renderAll();
      return true;
    } catch (error) {
      console.error("Error clearing canvas:", error);
      return false;
    }
  }, [canvas]);

  const downloadDesign = useCallback(
    (format: "png" | "jpeg" | "svg" | "json" = "png", filename?: string) => {
      if (!canvas) {
        console.error("Canvas not initialized");
        return;
      }

      try {
        let dataURL: string;
        let extension: string;

        switch (format) {
          case "png":
            dataURL = exportToPNG() || "";
            extension = "png";
            break;
          case "jpeg":
            dataURL = exportToJPEG() || "";
            extension = "jpg";
            break;
          case "svg":
            const svg = exportToSVG() || "";
            dataURL = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(
              svg
            )}`;
            extension = "svg";
            break;
          case "json":
            const json = saveDesignToJSON();
            dataURL = `data:application/json;charset=utf-8,${encodeURIComponent(
              JSON.stringify(json, null, 2)
            )}`;
            extension = "json";
            break;
          default:
            console.error("Unsupported format:", format);
            return;
        }

        const link = document.createElement("a");
        link.download = filename || `design-${Date.now()}.${extension}`;
        link.href = dataURL;
        link.click();
      } catch (error) {
        console.error("Error downloading design:", error);
      }
    },
    [canvas, exportToPNG, exportToJPEG, exportToSVG, saveDesignToJSON]
  );

  return {
    saveDesignToJSON,
    loadDesignFromJSON,
    exportToPNG,
    exportToJPEG,
    exportToSVG,
    clearCanvas,
    downloadDesign,
  };
};

