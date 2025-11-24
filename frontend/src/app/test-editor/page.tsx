"use client";

import dynamic from "next/dynamic";

const FabricEditor = dynamic(() => import("@/components/editor/FabricEditor"), {
    ssr: false,
    loading: () => <div className="h-screen w-screen flex items-center justify-center">Loading Editor...</div>,
});

export default function TestEditorPage() {
    return <FabricEditor />;
}

