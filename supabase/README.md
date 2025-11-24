# Radic Database Migrations

This directory contains Supabase database migrations for the Radic application.

## Applying Migrations

### Option 1: Using Supabase Dashboard (Easiest)

1. Go to https://app.supabase.com
2. Select your project
3. Navigate to **SQL Editor**
4. Copy the contents of `migrations/001_initial_schema.sql`
5. Paste into the SQL editor
6. Click **Run** to execute the migration

### Option 2: Using Supabase CLI

```bash
# Install Supabase CLI (if not already installed)
npm install -g supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref your-project-ref

# Apply migrations
supabase db push
```

## Migration Files

### 001_initial_schema.sql

Creates the initial database schema including:

**Tables:**
- `brands` - Brand kits with colors, fonts, and logos
- `designs` - User-created designs with Design JSON v1.1 schema
- `assets` - Uploaded and AI-generated images
- `smart_image_recipes` - AI image generation recipes for regeneration
- `campaigns` - Collections of designs for marketing campaigns
- `campaign_designs` - Many-to-many relationship between campaigns and designs

**Features:**
- Row Level Security (RLS) policies for data isolation
- Indexes for query performance
- Automatic `updated_at` timestamp triggers
- Foreign key constraints for data integrity
- Check constraints for data validation

## Verifying Migration

After applying the migration, verify it worked:

```sql
-- Check that all tables exist
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;

-- Check RLS is enabled
SELECT tablename, rowsecurity 
FROM pg_tables 
WHERE schemaname = 'public';

-- Check policies exist
SELECT tablename, policyname 
FROM pg_policies 
WHERE schemaname = 'public';
```

You should see:
- 6 tables (brands, designs, assets, smart_image_recipes, campaigns, campaign_designs)
- RLS enabled on all tables
- Multiple policies per table

## Troubleshooting

**Error: "relation already exists"**
- The migration has already been applied
- Drop the tables and re-run, or create a new migration

**Error: "permission denied"**
- Make sure you're using the service role key or have admin access
- Check your Supabase project permissions

**RLS blocking queries:**
- Make sure you're authenticated when making queries
- Check that the `auth.uid()` function returns the correct user ID
- Verify policies are correctly defined

## Next Steps

After applying the migration:

1. Test authentication by creating a user
2. Test RLS by trying to access data from different users
3. Verify indexes are being used with `EXPLAIN ANALYZE`
4. Monitor query performance in Supabase dashboard

