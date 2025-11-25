# SAMPLE INPUTS WITH REFERENCE IMAGES - REALISTIC TEST CASES

## Test Case 1: E-commerce Product Launch (Instagram) - WITH PRODUCT REFERENCE

```
Create an Instagram post for our new sustainable water bottle launch. 
We're targeting eco-conscious millennials (28-38 years old) who care about both style and the environment.

Key messages:
- Made from 100% recycled ocean plastic
- Keeps drinks cold for 24 hours
- Limited edition forest green color
- Launch price: $34.99 (normally $49.99)

The bottle has a sleek, modern design with a bamboo cap. We want to emphasize both the eco-friendly aspect and the premium quality. The vibe should be fresh, natural, but also sophisticated - not too "crunchy granola".

Reference Images:
1. [image_ref_001] - "Minimalist product photography on neutral background with soft natural lighting and subtle shadows"
2. [image_ref_002] - "Our actual product - HydraFlow water bottle in forest green with bamboo cap, side angle view"
3. [image_ref_003] - "Clean typography layout with generous whitespace and earth tone color palette"

Brand Kit:
- Brand Name: HydraFlow
- Colors: Primary #2D5F3F (forest green), Secondary #F4E8D8 (warm cream), Accent #E8973F (terracotta)
- Fonts: Primary "Outfit", Secondary "Inter"
- Logo: Available (asset_logo_hydraflow)

Style preferences:
- Clean and modern
- Natural aesthetics without being overly earthy
- Professional product photography feel
- Avoid cluttered layouts

Please make it pop in the Instagram feed!
```

**Expected AI Behavior:**
- image_ref_001: Style inspiration (lighting, composition) → NO reference_image_id in prompts
- image_ref_002: Actual product → INCLUDE reference_image_id in product layer generation prompt
- image_ref_003: Layout inspiration → NO reference_image_id in prompts

---

## Test Case 2: SaaS Product Feature (LinkedIn) - STYLE REFERENCES ONLY

```
Create a LinkedIn post announcing our new AI-powered analytics dashboard feature.
Target audience: B2B decision makers, CTOs, product managers at mid-size companies (100-500 employees).

Key points:
- Real-time data visualization
- 10x faster insights
- Free trial available for 14 days
- Integrates with existing tools

We want to communicate innovation and reliability. This should look professional and data-driven, but not boring. Think "trustworthy tech company" not "corporate snooze-fest".

Reference Images:
1. [image_ref_001] - "Modern tech interface with glowing blue elements and dark background, futuristic aesthetic"
2. [image_ref_002] - "Data dashboard mockup with clean graphs and charts, professional UI design"
3. [image_ref_003] - "Bold sans-serif typography on gradient background with geometric shapes"

Brand Kit:
- Brand Name: DataPulse
- Colors: Primary #0066FF (electric blue), Secondary #1A1D2E (dark navy), Accent #00D9FF (cyan)
- Fonts: Primary "Inter", Secondary "Space Grotesk"
- Logo: Available (asset_logo_datapulse)

Design preferences:
- Modern and sleek
- Data/tech aesthetic
- Professional but approachable
- Use data visualization elements if possible

This will be posted during work hours on a Tuesday, so it needs to stop the scroll!
```

**Expected AI Behavior:**
- All three references are style/mood inspiration → NO reference_image_id in any generation prompts
- Apply dark background aesthetic from ref_001
- Include dashboard/data elements inspired by ref_002
- Use bold typography approach from ref_003

---

## Test Case 3: Restaurant Promotion (Instagram Story) - WITH SCENE REFERENCE

```
Create an Instagram Story for our weekend brunch special.
We're a trendy downtown café targeting local foodies, young couples, and brunch enthusiasts (21-35 years old).

The special:
- "Bottomless Mimosa Brunch" 
- Every Saturday & Sunday, 10am-2pm
- $35 per person
- Includes gourmet brunch plate + unlimited mimosas
- Limited seating - reservation required

We want this to feel fun, Instagram-worthy, and create FOMO. The aesthetic should be bright, fresh, and appetizing. Think "brunch goals" vibes.

Reference Images:
1. [image_ref_001] - "Overhead flat lay of brunch spread with avocado toast, eggs benedict, colorful fruit, and mimosas on marble table with natural lighting"
2. [image_ref_002] - "Instagram Story template with playful hand-drawn elements and stickers"
3. [image_ref_003] - "Bright and airy café interior with plants and natural light streaming through windows"

Brand Kit:
- Brand Name: Bloom Café
- Colors: Primary #FF69B4 (hot pink), Secondary #FFD700 (golden yellow), Accent #FFFFFF (white)
- Fonts: Primary "Playfair Display", Secondary "Montserrat"
- Logo: Available (asset_logo_bloomcafe)

Style: 
- Fun and vibrant
- Food photography should look delicious and Instagram-ready
- Playful but still upscale
- Hand-drawn or illustrated elements welcome

We want people to immediately want to book a table!
```

**Expected AI Behavior:**
- image_ref_001: Scene reference for background or food elements → INCLUDE reference_image_id if generating brunch scene background
- image_ref_002: Style inspiration for layout elements → NO reference_image_id
- image_ref_003: Mood reference for overall aesthetic → NO reference_image_id

---

## Test Case 4: Fitness App (Facebook) - WITH PERSON REFERENCE

```
Create a Facebook ad for our new fitness app launch.
Target: Busy professionals (30-45) who want to work out at home but struggle with motivation.

Key selling points:
- 15-minute workouts that fit any schedule
- Personalized AI trainer
- No equipment needed
- First month free, then $9.99/month
- 50,000+ users already transformed their fitness

The tone should be motivating but realistic - we're not selling false promises. Show that fitness can be accessible and achievable. Appeal to people who are intimidated by traditional gyms.

Reference Images:
1. [image_ref_001] - "Woman in athletic wear doing yoga in modern living room, natural lighting, relatable home environment"
2. [image_ref_002] - "Smartphone mockup showing fitness app interface with workout timer and exercise demonstrations"
3. [image_ref_003] - "Energetic color palette with gradients - red to orange - dynamic and motivating"

Brand Kit:
- Brand Name: FitQuick
- Colors: Primary #FF4655 (energetic red), Secondary #2B2D42 (charcoal), Accent #8ECAE6 (sky blue)
- Fonts: Primary "Poppins", Secondary "Inter"
- Logo: Available (asset_logo_fitquick)

Preferences:
- Energetic but not overwhelming
- Relatable (not fitness models, regular people)
- Modern and app-focused
- Clear call-to-action
- Mobile-first design thinking

Show the app interface if possible and make the CTA really clear!
```

**Expected AI Behavior:**
- image_ref_001: Person and scene reference → INCLUDE reference_image_id for person doing workout
- image_ref_002: App interface reference → INCLUDE reference_image_id if generating app mockup
- image_ref_003: Color inspiration → NO reference_image_id (just inform gradient/color choices)

---

## Test Case 5: Real Estate (Instagram) - WITH PROPERTY REFERENCE

```
Create an Instagram post for a luxury condo listing.
Target: High-income professionals and investors (35-55) looking for premium downtown living.

Property highlights:
- 2 bed, 2 bath penthouse
- Floor-to-ceiling windows with city skyline views
- Modern smart home features
- Rooftop pool and gym access
- $1.2M - Open house this Saturday 2-4pm

The aesthetic should scream luxury and aspiration. This is a premium property and the design should reflect that. Think architectural photography, clean lines, sophisticated.

Reference Images:
1. [image_ref_001] - "Actual property photo - luxury condo living room with floor-to-ceiling windows, city skyline view at sunset, modern furniture"
2. [image_ref_002] - "Minimalist luxury real estate ad with black and gold color scheme"
3. [image_ref_003] - "Elegant serif typography with thin lines and generous letter spacing"

Brand Kit:
- Brand Name: Skyline Realty
- Colors: Primary #1A1A1A (black), Secondary #D4AF37 (gold), Accent #FFFFFF (white)
- Fonts: Primary "Cormorant Garamond", Secondary "Lato"
- Logo: Available (asset_logo_skylinerealty)

Style requirements:
- Luxurious and elegant
- Minimalist high-end aesthetic
- Architectural focus
- Sophisticated color palette
- Clean, uncluttered design

This needs to attract serious buyers who appreciate quality and design!
```

**Expected AI Behavior:**
- image_ref_001: Actual property photo → INCLUDE reference_image_id for property image layer
- image_ref_002: Style inspiration (color scheme, minimalism) → NO reference_image_id
- image_ref_003: Typography inspiration → NO reference_image_id

---

## Test Case 6: Black Friday Sale (Twitter/X) - STYLE REFERENCES WITH COMPOSITION

```
Create a Twitter post for our Black Friday sale.
We sell premium wireless earbuds and we're running our biggest sale of the year.

The deal:
- 60% OFF all products
- Today only (Black Friday)
- Free shipping
- Limited stock - selling out fast

Target: Tech enthusiasts, music lovers, anyone looking for Black Friday deals (18-45).

This needs to create URGENCY. People are scrolling through dozens of Black Friday deals - ours needs to stand out and make them click NOW.

Reference Images:
1. [image_ref_001] - "High-contrast Black Friday sale graphic with diagonal split composition, black and neon colors"
2. [image_ref_002] - "Bold percentage discount shown in huge typography with dynamic angle"
3. [image_ref_003] - "Tech product floating on dark background with colorful RGB lighting effects"

Brand Kit:
- Brand Name: SonicWave
- Colors: Primary #8B00FF (electric purple), Secondary #000000 (black), Accent #00FF88 (neon green)
- Fonts: Primary "Space Grotesk", Secondary "Inter"
- Logo: Available (asset_logo_sonicwave)

Must-haves:
- Bold and attention-grabbing
- Clear discount percentage
- Urgency indicators
- Tech/modern aesthetic
- High energy design

Make it IMPOSSIBLE to scroll past!
```

**Expected AI Behavior:**
- image_ref_001: Composition inspiration (diagonal split) → NO reference_image_id, but apply composition pattern
- image_ref_002: Typography approach → NO reference_image_id, but apply bold percentage treatment
- image_ref_003: Product styling reference → Could INCLUDE reference_image_id if generating product image with similar lighting

---

## Test Case 7: Non-Profit (Facebook) - WITH SUBJECT REFERENCE

```
Create a Facebook post for our annual giving campaign.
We're a wildlife conservation non-profit focused on protecting endangered sea turtles.

Campaign message:
- "Adopt a Sea Turtle" program
- $50 adoption includes certificate, photo, and updates
- 100% of proceeds go to conservation efforts
- Every adoption helps protect nesting sites and rescue injured turtles
- Year-end giving campaign

Target: Animal lovers, environmentally conscious individuals, donors (25-65).

The tone should be heartfelt and inspiring without being manipulative. Show the impact of their donation. Make people feel good about contributing.

Reference Images:
1. [image_ref_001] - "Beautiful sea turtle swimming in clear blue ocean water, underwater photography, natural habitat"
2. [image_ref_002] - "Warm and inviting donation campaign layout with soft colors and heart icons"
3. [image_ref_003] - "Conservation workers releasing baby sea turtles on beach at sunset, emotional documentary style"

Brand Kit:
- Brand Name: Ocean Guardians
- Colors: Primary #006994 (ocean blue), Secondary #F4A261 (sand orange), Accent #2A9D8F (teal)
- Fonts: Primary "Merriweather", Secondary "Open Sans"
- Logo: Available (asset_logo_oceanguardians)

Design approach:
- Warm and inviting
- Nature-focused
- Emotionally compelling but not guilt-tripping
- Show the sea turtles (cute but realistic)
- Clear donation ask

People should feel inspired to help after seeing this!
```

**Expected AI Behavior:**
- image_ref_001: Subject reference for sea turtle → INCLUDE reference_image_id if using as main hero image
- image_ref_002: Layout/style inspiration → NO reference_image_id
- image_ref_003: Scene/emotion reference → INCLUDE reference_image_id if generating background scene with volunteers

---

## Test Case 8: Fashion Brand (Instagram) - MIXED REFERENCES

```
Create an Instagram post for our summer collection launch.
We're a sustainable fashion brand targeting environmentally conscious Gen Z and young millennials (18-30).

Collection highlights:
- 100% organic cotton and recycled materials
- Limited edition tropical print collection
- Bold colors: coral, turquoise, sunshine yellow
- Pre-order now, ships June 1st
- 20% off for early birds (code: SUMMER20)

We want this to feel fresh, youthful, and vibrant while still communicating our sustainability values. The design should be eye-catching and make people want to shop immediately.

Reference Images:
1. [image_ref_001] - "Our model wearing the coral tropical print dress from the collection, outdoor natural setting"
2. [image_ref_002] - "Vibrant tropical leaves pattern - monstera and palm leaves in bold colors"
3. [image_ref_003] - "Modern fashion ad layout with text overlay on lifestyle photography, magazine editorial style"
4. [image_ref_004] - "Playful handwritten typography mixed with clean sans-serif fonts"

Brand Kit:
- Brand Name: EcoThreads
- Colors: Primary #FF6B6B (coral), Secondary #4ECDC4 (turquoise), Accent #FFE66D (sunshine yellow)
- Fonts: Primary "Montserrat", Secondary "Quicksand"
- Logo: Available (asset_logo_ecothreads)

Style requirements:
- Vibrant and energetic
- Youthful and playful
- Sustainable fashion aesthetic (not fast fashion)
- Instagram-native design language
- Clear call-to-action with discount code

Make it irresistible to our target audience!
```

**Expected AI Behavior:**
- image_ref_001: Actual model photo → INCLUDE reference_image_id for model/product layer
- image_ref_002: Pattern/background reference → INCLUDE reference_image_id if generating tropical background
- image_ref_003: Layout inspiration → NO reference_image_id
- image_ref_004: Typography style → NO reference_image_id

---

## Test Case 9: Coffee Shop (Instagram Story) - NO REFERENCES

```
Create an Instagram Story for our new seasonal drink launch.
We're an artisan coffee shop targeting coffee enthusiasts and local professionals (22-40).

Product:
- "Lavender Honey Latte" - our new spring signature drink
- Made with locally sourced lavender and raw honey
- Available hot or iced
- $6.50
- Limited time - spring season only

The vibe should be cozy, artisanal, and Instagram-worthy. Think coffeehouse aesthetic meets modern design. We want people to come in and try it today.

Brand Kit:
- Brand Name: Ritual Coffee Co.
- Colors: Primary #6B4423 (coffee brown), Secondary #E8D5C4 (cream), Accent #9B7EBD (lavender)
- Fonts: Primary "Crimson Text", Secondary "Work Sans"
- Logo: Available (asset_logo_ritualcoffee)

Design preferences:
- Warm and inviting
- Artisanal coffee shop aesthetic
- Show the drink looking delicious
- Include price and "limited time" messaging
- Cozy, Instagram-friendly vibe

Make people crave this drink immediately!
```

**Expected AI Behavior:**
- No reference images provided
- AI designs based solely on brief, brand kit, and design principles
- Generate coffee drink image without reference guidance
- Apply appropriate coffeehouse aesthetic

---

## Test Case 10: Tech Hardware (LinkedIn) - TECHNICAL PRODUCT REFERENCE

```
Create a LinkedIn post for our new enterprise laptop line launch.
Target: IT managers, CTOs, and procurement officers at corporations (35-60 years old).

Product features:
- MobileBook Pro X1 - enterprise-grade laptop
- 14-hour battery life
- Military-grade durability (MIL-STD-810G certified)
- Advanced security features
- Starting at $1,299 with volume discounts available

The messaging needs to be professional, technical, and emphasize reliability and ROI. This is B2B corporate sales, so focus on business value, not consumer appeal.

Reference Images:
1. [image_ref_001] - "Our actual product - MobileBook Pro X1 laptop, space gray, open at 45-degree angle showing keyboard and screen, professional product photography"
2. [image_ref_002] - "Clean corporate tech ad layout with feature callouts and icons"
3. [image_ref_003] - "Business professional using laptop in modern office environment, natural lighting"

Brand Kit:
- Brand Name: TechCore Systems
- Colors: Primary #0052CC (corporate blue), Secondary #172B4D (navy), Accent #36B37E (success green)
- Fonts: Primary "IBM Plex Sans", Secondary "Inter"
- Logo: Available (asset_logo_techcoresystems)

Requirements:
- Professional and corporate
- Technical credibility
- B2B focused (not consumer-friendly)
- Show product clearly
- Feature highlights visible
- Trust and reliability emphasis

This needs to generate qualified leads from enterprise buyers!
```

**Expected AI Behavior:**
- image_ref_001: Actual product → INCLUDE reference_image_id for laptop product layer
- image_ref_002: Layout inspiration → NO reference_image_id, but apply feature callout approach
- image_ref_003: Scene reference → Could INCLUDE reference_image_id if generating background with professional

---

## Summary of Reference Usage Patterns

| Test Case | Reference Types | Expected reference_image_id Usage |
|-----------|----------------|-----------------------------------|
| 1. HydraFlow | Product photo, style, layout | ✅ Yes - for product (ref_002) |
| 2. DataPulse | All style/mood references | ❌ No - all are inspiration only |
| 3. Bloom Café | Scene, style, mood | ✅ Yes - for brunch scene (ref_001) |
| 4. FitQuick | Person scene, app UI, colors | ✅ Yes - for person (ref_001) and app (ref_002) |
| 5. Skyline Realty | Property photo, style, typography | ✅ Yes - for property (ref_001) |
| 6. SonicWave | Composition, typography, product styling | ⚠️ Maybe - for product if generating with RGB lighting |
| 7. Ocean Guardians | Turtle photo, layout, scene | ✅ Yes - for turtle (ref_001) or scene (ref_003) |
| 8. EcoThreads | Model photo, pattern, layout, typography | ✅ Yes - for model (ref_001) and pattern (ref_002) |
| 9. Ritual Coffee | None provided | ❌ N/A - no references |
| 10. TechCore | Product photo, layout, scene | ✅ Yes - for laptop (ref_001), maybe scene (ref_003) |

---

## How to Test

1. **Copy any test case** from above
2. **Paste into the prompt system** as user input
3. **Check the JSON output** for:
   - `reference_images` array properly populated
   - `reference_image_id` included ONLY when appropriate
   - `key_elements_extracted` showing what the AI learned from each reference
   - `design_rationale` explaining reference application
   - Generation prompts incorporate reference styling principles

4. **Validate reference logic:**
   - Product/person/scene photos → Should have reference_image_id
   - Style/mood/composition references → Should NOT have reference_image_id
   - Generated images should still specify "transparent background"