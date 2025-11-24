"use client";

import dynamic from "next/dynamic";
import { useGetDesign } from "@/hooks/useDesign";
import { use, useEffect, useState } from "react";
import { useAppStore } from "@/store/useStore";

const FabricEditor = dynamic(() => import("@/components/editor/FabricEditor"), {
    ssr: false,
    loading: () => <div className="h-screen w-screen flex items-center justify-center">Loading Editor...</div>,
});

export default function EditorPage({ params }: { params: Promise<{ id: string }> }) {
    const { id } = use(params);
    const { currentDesignData, currentDesignId } = useAppStore();
    const [design, setDesign] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(true);

    // Check if we have the design in the store (for anonymous users or just-generated designs)
    const shouldFetchFromAPI = !currentDesignData || currentDesignId !== id;

    const { data: fetchedDesign, isLoading: isFetching } = useGetDesign(id, {
        enabled: shouldFetchFromAPI,
    });

    useEffect(() => {
        console.log("[Editor] Debug info:", {
            currentDesignData,
            currentDesignId,
            id,
            fetchedDesign,
            isFetching,
            shouldFetchFromAPI
        });

        if (currentDesignData && currentDesignId === id) {
            // Use design from store (anonymous user or just generated)
            console.log("[Editor] Using design from store:", currentDesignData);
            console.log("[Editor] Design structure check:", {
                hasDesignJson: !!currentDesignData.design_json,
                designJsonType: typeof currentDesignData.design_json,
                designJsonKeys: currentDesignData.design_json ? Object.keys(currentDesignData.design_json) : null
            });
            setDesign(currentDesignData);
            setIsLoading(false);
        } else if (fetchedDesign) {
            // Use design fetched from API (authenticated user)
            console.log("[Editor] Using design from API:", fetchedDesign);
            setDesign(fetchedDesign);
            setIsLoading(false);
        } else if (!isFetching && shouldFetchFromAPI) {
            // Fetch completed but no design found
            setIsLoading(false);
        }
    }, [currentDesignData, currentDesignId, id, fetchedDesign, isFetching, shouldFetchFromAPI]);

    if (isLoading || (shouldFetchFromAPI && isFetching)) {
        return <div className="h-screen w-screen flex items-center justify-center">Loading Design...</div>;
    }

    if (!design) {
        return <div className="h-screen w-screen flex items-center justify-center">Design not found</div>;
    }

    return <FabricEditor design={design} />;
}
