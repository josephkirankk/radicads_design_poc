-- Radic Initial Database Schema
-- Version: 1.0.0
-- Date: 2025-11-24

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- BRANDS TABLE
-- ============================================================================
CREATE TABLE brands (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    colors JSONB NOT NULL DEFAULT '{}',
    fonts JSONB NOT NULL DEFAULT '{}',
    logo_image_id UUID,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- DESIGNS TABLE
-- ============================================================================
CREATE TABLE designs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    brand_id UUID REFERENCES brands(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    format TEXT NOT NULL DEFAULT 'instagram_post',
    design_json JSONB NOT NULL,
    thumbnail_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- ASSETS TABLE
-- ============================================================================
CREATE TABLE assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('image', 'logo', 'generated')),
    url TEXT NOT NULL,
    filename TEXT,
    size_bytes INTEGER,
    mime_type TEXT,
    width INTEGER,
    height INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- SMART IMAGE RECIPES TABLE
-- ============================================================================
CREATE TABLE smart_image_recipes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    type TEXT NOT NULL CHECK (type IN ('product_ugc', 'infographic', 'smart_edit')),
    prompt TEXT NOT NULL,
    reference_asset_ids UUID[],
    model TEXT NOT NULL DEFAULT 'nano_banana_pro',
    options JSONB DEFAULT '{}',
    last_generated_asset_id UUID REFERENCES assets(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- CAMPAIGNS TABLE
-- ============================================================================
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    brand_id UUID REFERENCES brands(id) ON DELETE SET NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- CAMPAIGN DESIGNS (Many-to-Many relationship)
-- ============================================================================
CREATE TABLE campaign_designs (
    campaign_id UUID NOT NULL REFERENCES campaigns(id) ON DELETE CASCADE,
    design_id UUID NOT NULL REFERENCES designs(id) ON DELETE CASCADE,
    position INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (campaign_id, design_id)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Brands indexes
CREATE INDEX idx_brands_owner_id ON brands(owner_id);
CREATE INDEX idx_brands_created_at ON brands(created_at DESC);

-- Designs indexes
CREATE INDEX idx_designs_owner_id ON designs(owner_id);
CREATE INDEX idx_designs_brand_id ON designs(brand_id);
CREATE INDEX idx_designs_created_at ON designs(created_at DESC);
CREATE INDEX idx_designs_format ON designs(format);

-- Assets indexes
CREATE INDEX idx_assets_owner_id ON assets(owner_id);
CREATE INDEX idx_assets_type ON assets(type);
CREATE INDEX idx_assets_created_at ON assets(created_at DESC);

-- Smart Image Recipes indexes
CREATE INDEX idx_smart_image_recipes_owner_id ON smart_image_recipes(owner_id);
CREATE INDEX idx_smart_image_recipes_type ON smart_image_recipes(type);

-- Campaigns indexes
CREATE INDEX idx_campaigns_owner_id ON campaigns(owner_id);
CREATE INDEX idx_campaigns_brand_id ON campaigns(brand_id);
CREATE INDEX idx_campaigns_created_at ON campaigns(created_at DESC);

-- Campaign Designs indexes
CREATE INDEX idx_campaign_designs_campaign_id ON campaign_designs(campaign_id);
CREATE INDEX idx_campaign_designs_design_id ON campaign_designs(design_id);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE brands ENABLE ROW LEVEL SECURITY;
ALTER TABLE designs ENABLE ROW LEVEL SECURITY;
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE smart_image_recipes ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaign_designs ENABLE ROW LEVEL SECURITY;

-- Brands policies
CREATE POLICY "Users can view their own brands" ON brands
    FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can create their own brands" ON brands
    FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update their own brands" ON brands
    FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete their own brands" ON brands
    FOR DELETE USING (auth.uid() = owner_id);



-- Designs policies
CREATE POLICY "Users can view their own designs" ON designs
    FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can create their own designs" ON designs
    FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update their own designs" ON designs
    FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete their own designs" ON designs
    FOR DELETE USING (auth.uid() = owner_id);

-- Assets policies
CREATE POLICY "Users can view their own assets" ON assets
    FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can create their own assets" ON assets
    FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can delete their own assets" ON assets
    FOR DELETE USING (auth.uid() = owner_id);

-- Smart Image Recipes policies
CREATE POLICY "Users can view their own recipes" ON smart_image_recipes
    FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can create their own recipes" ON smart_image_recipes
    FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update their own recipes" ON smart_image_recipes
    FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete their own recipes" ON smart_image_recipes
    FOR DELETE USING (auth.uid() = owner_id);

-- Campaigns policies
CREATE POLICY "Users can view their own campaigns" ON campaigns
    FOR SELECT USING (auth.uid() = owner_id);
CREATE POLICY "Users can create their own campaigns" ON campaigns
    FOR INSERT WITH CHECK (auth.uid() = owner_id);
CREATE POLICY "Users can update their own campaigns" ON campaigns
    FOR UPDATE USING (auth.uid() = owner_id);
CREATE POLICY "Users can delete their own campaigns" ON campaigns
    FOR DELETE USING (auth.uid() = owner_id);

-- Campaign Designs policies (access through campaign ownership)
CREATE POLICY "Users can view campaign designs for their campaigns" ON campaign_designs
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM campaigns
            WHERE campaigns.id = campaign_designs.campaign_id
            AND campaigns.owner_id = auth.uid()
        )
    );
CREATE POLICY "Users can add designs to their campaigns" ON campaign_designs
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM campaigns
            WHERE campaigns.id = campaign_designs.campaign_id
            AND campaigns.owner_id = auth.uid()
        )
    );
CREATE POLICY "Users can remove designs from their campaigns" ON campaign_designs
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM campaigns
            WHERE campaigns.id = campaign_designs.campaign_id
            AND campaigns.owner_id = auth.uid()
        )
    );

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply triggers to tables with updated_at
CREATE TRIGGER update_brands_updated_at
    BEFORE UPDATE ON brands
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_designs_updated_at
    BEFORE UPDATE ON designs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_smart_image_recipes_updated_at
    BEFORE UPDATE ON smart_image_recipes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_campaigns_updated_at
    BEFORE UPDATE ON campaigns
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE brands IS 'Brand kits with colors, fonts, and logos';
COMMENT ON TABLE designs IS 'User-created designs with Design JSON v1.1 schema';
COMMENT ON TABLE assets IS 'Uploaded and generated images/assets';
COMMENT ON TABLE smart_image_recipes IS 'AI image generation recipes for regeneration';
COMMENT ON TABLE campaigns IS 'Collections of designs for marketing campaigns';
COMMENT ON TABLE campaign_designs IS 'Many-to-many relationship between campaigns and designs';
