/**
 * CURVE AGENCY — INTERACTIVE ENGINE
 * Features:
 * - Full Arabic / English bilingual switching with dynamic RTL support
 * - IntersectionObserver scroll reveal animations
 * - Animated stats counters
 * - Portfolio filter system
 * - Mobile navigation drawer
 * - Interactive inquiry form validation & feedback
 */

document.addEventListener('DOMContentLoaded', () => {

  /* ==========================================================================
     1. BILINGUAL DICTIONARY & LOCALIZATION ENGINE
     ========================================================================== */
  const translations = {
    en: {
      nav_location: "EST. JEDDAH",
      nav_about: "PROFILE",
      nav_services: "SERVICES",
      nav_process: "PROCESS",
      nav_why: "WHY CURVE",
      nav_stats: "IMPACT",
      nav_work: "WORK",
      nav_partners: "CLIENTS",
      nav_contact: "CONTACT",
      nav_cta: "LET'S TALK",

      hero_badge: "FULL-SERVICE AGENCY",
      hero_title_1: "IGNITE",
      hero_title_2: "THE MOTION.",
      hero_lead: "Curve is a full-service creative agency dedicated to delivering innovative, motion-driven solutions. We specialize in brand identity, digital design, content creation, and media production — helping businesses move forward with clarity, momentum, and impact.",
      hero_btn_work: "EXPLORE WORK",
      hero_btn_contact: "START A PROJECT",
      hero_scroll: "SCROLL",

      about_idx_label: "ABOUT CURVE",
      about_headline: "WE SHAPE BRANDS THAT REFUSE TO STAND STILL.",
      about_who_label: "WHO WE ARE",
      about_who_text: "Curve is a modern creative agency built for momentum. We operate at the intersection of cultural insight, world-class aesthetics, and digital craft. From Riyadh to Jeddah and beyond, we partner with forward-looking brands, cultural institutions, and ambitious founders to transform strategic vision into palpable cultural reality.",
      about_vision_title: "OUR VISION",
      about_vision_text: "To become the leading creative agency for brands that refuse to stand still.",
      about_vision_caption: "Pioneering motion-led experiences that captivate Saudi audiences and set regional benchmarks.",
      about_mission_title: "OUR MISSION",
      about_mission_text: "To deliver identity, design, and content solutions that move brands forward with clarity and impact.",
      about_mission_caption: "Eliminating ambiguity with razor-sharp strategy, compelling motion, and flawless visual execution.",

      services_idx_label: "CAPABILITIES",
      services_headline: "A FULL SPECTRUM OF CREATIVE DISCIPLINES.",
      services_desc: "Six comprehensive pillars engineered to cover the complete lifecycle of brand growth, media engagement, and cultural resonance.",
      
      s1_tag: "CORE",
      s1_title: "BRANDING",
      s1_sub: "Identity, Logos & Guidelines",
      s1_desc: "From strategic brand architecture and bespoke typography to comprehensive design systems that build immediate distinction and enduring cultural authority.",
      s1_li1: "Visual Identity Systems",
      s1_li2: "Custom Typography & Logos",
      s1_li3: "Brand Books & Style Guidelines",
      s1_li4: "Packaging & Physical Touchpoints",

      s2_tag: "GROWTH",
      s2_title: "DIGITAL MARKETING",
      s2_sub: "SEO & Paid Ads",
      s2_desc: "Data-backed performance funnels, algorithmic search optimization, and precision ad targeting engineered to drive scalable user acquisition and verified ROI.",
      s2_li1: "Technical & Organic SEO",
      s2_li2: "Paid Search & Social Campaigns",
      s2_li3: "Conversion Rate Optimization",
      s2_li4: "Attribution & Analytics Dashboards",

      s3_tag: "CINEMATIC",
      s3_title: "MEDIA PRODUCTION",
      s3_sub: "Commercials, Photo & Video",
      s3_desc: "Full-scale cinematic production bringing high-end camera rigs, studio lighting, authentic Saudi heritage aesthetics, and meticulous post-production to life.",
      s3_li1: "High-End TV Commercials",
      s3_li2: "Commercial & Product Photography",
      s3_li3: "On-Location Festival Coverage",
      s3_li4: "Color Grading & Sound Design",

      s4_tag: "NARRATIVE",
      s4_title: "CONTENT CREATION",
      s4_sub: "Visuals, Videos & Copy",
      s4_desc: "Bespoke visual content and compelling Arabic & English copywriting tailored to capture viewer attention in high-velocity social environments.",
      s4_li1: "High-Impact Social Reels",
      s4_li2: "Creative Motion Graphics",
      s4_li3: "Bilingual Copywriting & Scripts",
      s4_li4: "Editorial Storytelling",

      s5_tag: "COMMUNITY",
      s5_title: "SOCIAL MEDIA",
      s5_sub: "Strategy & Management",
      s5_desc: "Always-on strategy, community curation, calendar deployment, and trend agility that elevate followers into passionate brand advocates.",
      s5_li1: "Omnichannel Social Strategy",
      s5_li2: "Daily Publishing & Community Care",
      s5_li3: "Real-Time Trend Hijacking",
      s5_li4: "Monthly Growth Audits",

      s6_tag: "SCALE",
      s6_title: "TALENT MANAGEMENT",
      s6_sub: "Casting & Creator Campaigns",
      s6_desc: "Direct access to a vetted network of 10,000+ creators and influencers across Saudi Arabia and the GCC for authentic UGC and high-converting reach.",
      s6_li1: "Actor & Model Casting",
      s6_li2: "10,000+ Regional Creator Network",
      s6_li3: "Authentic UGC Production",
      s6_li4: "End-to-End Campaign Briefing",

      process_idx_label: "METHODOLOGY",
      process_headline: "PRECISION EXECUTION IN FOUR STAGES.",
      process_desc: "A battle-tested workflow designed to eliminate friction, sharpen narrative focus, and turn concepts into market-defining momentum.",
      
      p1_title: "DISCOVER",
      p1_sub: "Deep Dive Into Your Brand",
      p1_desc: "We immerse ourselves in your brand DNA, market dynamics, competitive landscape, audience psychology, and cultural cues to pinpoint the core differentiator.",

      p2_title: "STRATEGIZE",
      p2_sub: "Build A Clear Creative Plan",
      p2_desc: "We construct a definitive strategic roadmap, aligning narrative tone, aesthetic moodboards, channel priorities, and production milestones for maximum clarity.",

      p3_title: "CREATE",
      p3_sub: "Bring The Design To Life",
      p3_desc: "From typography grids and commercial video shoots to social reels and packaging, our multidisciplinary team crafts every element with uncompromising detail.",

      p4_title: "LAUNCH",
      p4_sub: "Deliver And Follow Through",
      p4_desc: "We orchestrate flawless public rollouts, live campaign monitoring, audience response tracking, and continuous optimization to protect your brand momentum.",

      why_idx_label: "THE CURVE ADVANTAGE",
      why_headline: "WHY LEADING BRANDS CHOOSE CURVE.",
      why_lead: "In a marketplace cluttered with rigid templates and generic creative, we bring custom craftsmanship, agile collaboration, and measurable momentum.",
      
      w1_title: "CURVED SOLUTIONS",
      w1_sub: "Bent to fit every brand",
      w1_desc: "No cookie-cutter templates. We adapt our thinking, systems, and execution models around your brand's unique challenges and scale.",

      w2_title: "ONE TEAM",
      w2_sub: "Everything, Handled Together",
      w2_desc: "Strategists, directors, designers, and media buyers sitting at the same table. Zero agency silos, zero miscommunication.",

      w3_title: "WE GROW WITH YOU",
      w3_sub: "Built To Last And Expand",
      w3_desc: "We don't build disposable creative. We architect visual systems, content engines, and campaigns designed to expand across years.",

      w4_title: "PROVEN MOMENTUM",
      w4_sub: "Results you can see",
      w4_desc: "Tangible performance metrics, award-caliber aesthetics, national media buzz, and commercial growth that prove the value of your investment.",

      stats_idx_label: "MARKET MOMENTUM",
      stats_headline: "POISED AT THE EPICENTER OF SAUDI ARABIA’S DIGITAL SURGE.",
      stats_desc: "Operating in one of the most dynamic, connected, and forward-looking digital economies on Earth.",
      stat1_label: "Internet Penetration In Saudi Arabia",
      stat1_sub: "Universal Connectivity Across The Kingdom",
      stat2_label: "Social Media Users In Saudi Arabia",
      stat2_sub: "Hyper-Active Mobile & Video Consumption",
      stat3_label: "Regional Creator & Influencer Network",
      stat3_sub: "Vetted Creators Across TikTok, IG & Snapchat",
      stat4_label: "Peak Viral Reach Per Reel Format",
      stat4_sub: "Organic Cultural Resonance & High Engagement",
      stats_verified: "VERIFIED DATA",
      stats_source: "Source: DataReportal, Digital 2026 — Saudi Arabia Digital Overview",

      work_idx_label: "PORTFOLIO",
      work_headline: "SELECTED PRODUCTIONS & CASE STUDIES.",
      filter_all: "ALL",
      filter_prod: "PRODUCTION",
      filter_brand: "BRANDING",
      filter_camp: "CAMPAIGNS",
      filter_photo: "PHOTOGRAPHY",

      cat_campaign: "CAMPAIGN",
      cat_cinematic: "CINEMATIC",
      cat_coverage: "EVENT COVERAGE",
      cat_photo: "PHOTOGRAPHY",
      cat_fashion: "FASHION",
      cat_brand: "BRANDING",
      cat_lifestyle: "LIFESTYLE",
      cat_commercial: "COMMERCIAL",

      w_netflix_client: "NETFLIX",
      w_netflix_title: "SQUID GAME SEASON 2 — JEDDAH LAUNCH",
      w_netflix_desc: "Produced the Key Visual campaign for Netflix's Squid Game Season 2 launch in Jeddah, recreating the iconic characters on location to capture public attention and drive organic hype.",

      w_lomar_client: "LOMAR",
      w_lomar_title: "BRIDGING TRADITIONAL ELEGANCE & CONTEMPORARY LIFESTYLE",
      w_lomar_desc: "Crafted a high-impact creative concept capturing authentic moments of modern Saudi identity through striking, cinematic visual storytelling.",

      w_mcd_client: "MCDONALD'S",
      w_mcd_title: "MCCRISPY — JEDDAH RIVALRY CONCEPT",
      w_mcd_desc: "Created a buzz-driven concept featuring supporters of the two biggest rival football clubs in Jeddah who never agree on anything — until McCrispy.",

      w_sport_client: "MINISTRY OF SPORT",
      w_sport_title: "BRIDGE LEAGUE DEBUT — SOCIAL COVERAGE",
      w_sport_desc: "Delivered end-to-end digital and social media coverage for the debut of the Bridge League in Jeddah, turning on-ground sports energy into a nationwide digital narrative.",

      w_auto_client: "COMMERCIAL AUTOMOTIVE",
      w_auto_title: "OFF-ROAD DESERT THRILL AT GOLDEN HOUR",
      w_auto_desc: "Captured dynamic high-speed action shots across sand dunes, blending adrenaline, desert power, and cinematic light choreography.",

      w_fashion_client: "CONCEPTUAL EDITORIAL",
      w_fashion_title: "CRIMSON MYSTERY & MOVEMENT",
      w_fashion_desc: "A bold fashion series combining dramatic studio chiaroscuro lighting, flowing red fabrics, and striking silhouette studies.",

      w_dar_client: "DAR AL JOOD",
      w_dar_title: "AL-ULA NABATAEAN LUXURY IDENTITY",
      w_dar_desc: "Translating the verticality and architectural precision of Al-Ula ancient stone monuments into a contemporary Arabic typeface and earthy minimalist brand system.",

      w_badre_client: "BADRE",
      w_badre_title: "FUEL FOR EARLY RISERS — BRUNCH DESTINATION",
      w_badre_desc: "Crafted the complete visual language for Badre, celebrating morning rituals, artisanal specialty coffee, and local culinary craftsmanship.",

      w_onn_client: "ONN DRIVE-THRU COFFEE",
      w_onn_title: "URBAN STREET-STYLE & DAILY RETENTION",
      w_onn_desc: "Captured authentic outdoor street moments, skateboarding energy, and loyalty campaign storytelling for an energetic Saudi coffee culture.",

      w_perfume_client: "PREMIUM FRAGRANCE",
      w_perfume_title: "ATMOSPHERIC SCENT PORTRAITURE",
      w_perfume_desc: "Combining warm atmospheric lighting with organic rock and stone textures to elevate bespoke bottles into visual works of art.",

      w_food_client: "CULINARY ARTS",
      w_food_title: "PRECISION & TEXTURE IN EVERY PLATING",
      w_food_desc: "Showcasing culinary compositions through natural light, rich contrast, and appetizing macro detail that reflects gourmet craftsmanship.",

      w_elba_client: "ELBA ITALY",
      w_elba_title: "METALLIC CRAFT & KITCHEN LIVING",
      w_elba_desc: "High-end studio photography capturing stainless steel reflections and lifestyle kitchen scenes that communicate European prestige.",

      partners_idx_label: "TRUSTED BY LEADERS",
      partners_headline: "BRANDS WE HAVE ACCELERATED.",
      partners_desc: "We partner with national ministries, global enterprises, and pioneering regional creators to shape what's next.",
      banner_eyebrow: "CREATOR ECOSYSTEM",
      banner_title: "ANY INFLUENCER. ANYWHERE. UNLIMITED ACCESS.",
      banner_desc: "From micro-niche experts to global icons, our talent bureau handles end-to-end selection, contract compliance, content briefing, and ROI measurement across 10,000+ creators.",
      banner_btn: "REQUEST TALENT ROSTER",

      contact_idx_label: "INITIATE DIALOGUE",
      contact_title_1: "LET'S",
      contact_title_2: "GRAB COFFEE.",
      contact_lead: "Have a bold vision, a brand that needs repositioning, or a media production requiring cinematic caliber? We're ready to bend reality in your favor.",
      contact_call_label: "CALL DIRECT",
      contact_email_label: "INQUIRIES & BRIEFS",
      contact_hq_label: "HEADQUARTERS",
      contact_hq_val: "Al Rawdah District, Jeddah, Kingdom of Saudi Arabia",
      contact_address_val: "Al Rawdah District, Jeddah, KSA",
      contact_web_label: "DIGITAL DOMAIN",
      contact_social_label: "FOLLOW THE MOTION",

      form_title: "TELL US ABOUT YOUR VISION",
      form_desc: "Fill out the parameters below and our senior leadership team will respond within 24 hours.",
      form_label_name: "YOUR NAME *",
      form_label_email: "EMAIL ADDRESS *",
      form_label_company: "ORGANIZATION / BRAND",
      form_label_service: "DISCIPLINE NEEDED",
      form_label_msg: "PROJECT BRIEF & TIMELINE *",
      form_btn: "TRANSMIT INQUIRY",
      form_err_name: "Please provide your name",
      form_err_email: "Please provide a valid email",
      form_err_msg: "Please share a brief note about your project",
      form_success_msg: "Thank you. Your inquiry has been received. Our team will connect with you promptly.",

      opt_branding: "Branding & Visual Identity",
      opt_production: "Commercial Media Production",
      opt_social: "Social Media & Community",
      opt_marketing: "Digital Marketing & Paid Ads",
      opt_talent: "Talent & Influencer Management",
      opt_360: "Full-Service 360 Campaign",

      footer_motto: "Full-Service Creative Agency — Motion-Driven Solutions.",
      footer_copy: "© 2026 CURVE Agency. All rights reserved.",
      footer_location: "Jeddah, Kingdom of Saudi Arabia",
      footer_top: "BACK TO TOP",

      form_ph_name: "Fahad Al-Harbi",
      form_ph_email: "fahad@company.com",
      form_ph_company: "Acme Holdings",
      form_ph_msg: "Outline your objectives, current challenges, and intended launch window..."
    },

    ar: {
      nav_location: "تأسست في جدة",
      nav_about: "من نحن",
      nav_services: "خدماتنا",
      nav_process: "المنهجية",
      nav_why: "لماذا كيرف",
      nav_stats: "الأرقام",
      nav_work: "أعمالنا",
      nav_partners: "العملاء",
      nav_contact: "تواصل معنا",
      nav_cta: "تحدث معنا",

      hero_badge: "وكالة متكاملة",
      hero_title_1: "نُطلق",
      hero_title_2: "أثر الحركة.",
      hero_lead: "كيرف هي وكالة إبداعية متكاملة متخصصة في تقديم حلول مبتكرة مدفوعة بالحركة. نبتكر الهويات البصرية، والتصميم الرقمي، وصناعة المحتوى، والإنتاج الإعلامي — لنقود العلامات التجارية نحو الأمام بوضوح، وزخم، وأثر استثنائي.",
      hero_btn_work: "استكشف أعمالنا",
      hero_btn_contact: "ابدأ مشروعك",
      hero_scroll: "مرّر للأسفل",

      about_idx_label: "عن كيرف",
      about_headline: "نبني علامات تأبى الوقوف في مكانها.",
      about_who_label: "من نحن",
      about_who_text: "كيرف وكالة إبداعية حديثة صُممت لصناعة الزخم والريادة. نعمل عند نقطة التقاء الفهم الثقافي العميق، والجماليات العالمية، والبراعة الرقمية. من الرياض إلى جدة وما بعدها، نتشارك مع العلامات الطموحة والمؤسسات الوطنية لتحويل الرؤى الاستراتيجية إلى واقع ثقافي ملموس ومؤثر.",
      about_vision_title: "رؤيتنا",
      about_vision_text: "أن نكون الوكالة الإبداعية الرائدة للعلامات التجارية التي تأبى الركود وتسعى لريادة المستقبل.",
      about_vision_caption: "ابتكار تجارب ديناميكية تخاطب الوجدان السعودي وتضع معايير جديدة على مستوى المنطقة.",
      about_mission_title: "رسالتنا",
      about_mission_text: "تقديم حلول الهوية والتصميم والمحتوى التي تدفع العلامات نحو الأمام بوضوح وزخم وتأثير راسخ.",
      about_mission_caption: "إزالة الغموض عبر استراتيجيات حادة، وحركة بصرية جذابة، وتنفيذ فني لا يقبل المساومة.",

      services_idx_label: "قدراتنا",
      services_headline: "منظومة إبداعية شاملة ومتكاملة.",
      services_desc: "ست ركائز استراتيجية مصممة لتغطية دورة نمو العلامة بالكامل وصناعة الحضور والأثر الثقافي الممتد.",
      
      s1_tag: "الأساس",
      s1_title: "بناء الهوية",
      s1_sub: "الهوية، الشعارات ودليل العلامة",
      s1_desc: "من بناء المعمارية الاستراتيجية للعلامة وتصميم التايبوغرافي الخاص إلى أنظمة التصميم الشاملة التي تصنع تميزاً فورياً وحضوراً راسخاً.",
      s1_li1: "أنظمة الهوية البصرية المتكاملة",
      s1_li2: "الشعارات والخطوط المخصصة",
      s1_li3: "أدلة الاستخدام وهوية البراند",
      s1_li4: "تصميم التغليف والمنتجات",

      s2_tag: "النمو",
      s2_title: "التسويق الرقمي",
      s2_sub: "تحسين محركات البحث والإعلانات الممولة",
      s2_desc: "مسارات أداء قائمة على البيانات، وتحسين محركات البحث بالخوارزميات الذكية، واستهداف إعلاني دقيق لتحقيق نمو مستدام وعائد استثماري موثوق.",
      s2_li1: "تحسين محركات البحث العضوي والتقني",
      s2_li2: "إعلانات البحث وشبكات التواصل",
      s2_li3: "تحسين معدل التحويل (CRO)",
      s2_li4: "لوحات تحليل الأداء وتتبع النتائج",

      s3_tag: "سينمائي",
      s3_title: "الإنتاج الإعلامي",
      s3_sub: "الإعلانات التجارية، الفيديو والتصوير",
      s3_desc: "إنتاج سينمائي متكامل بأحدث معدات التصوير العالمية، والإضاءة الاستوديو الاحترافية، مع توظيف أصيل للثقافة السعودية وما بعد الإنتاج المتقن.",
      s3_li1: "إعلانات تلفزيونية سينمائية",
      s3_li2: "التصوير التجاري والمنتجات",
      s3_li3: "تغطية المهرجانات والفعاليات الكبرى",
      s3_li4: "تلوين سينمائي وتصميم صوتي متقدم",

      s4_tag: "سردي",
      s4_title: "صناعة المحتوى",
      s4_sub: "المحتوى المرئي، الفيديو والنصوص",
      s4_desc: "محتوى بصري متفرد وصياغة نصوص إبداعية بالعربية والإنجليزية مهيأة لجذب الانتباه في بيئات التواصل سريعة الإيقاع.",
      s4_li1: "مقاطع ريلز وفيديوهات قصيرة مؤثرة",
      s4_li2: "موشن جرافيكس ورسوم متحركة",
      s4_li3: "كتابة سيناريوهات ونصوص إعلانية",
      s4_li4: "رواية القصص التحريرية والتسويقية",

      s5_tag: "مجتمعي",
      s5_title: "إدارة السوشال ميديا",
      s5_sub: "الاستراتيجية وإدارة المجتمعات",
      s5_desc: "استراتيجيات تفاعل دائمة، وتخطيط للمحتوى الدوري، ومواكبة ذكية للترندات اليومية لتحويل المتابعين إلى مجتمع وفي للعلامة.",
      s5_li1: "استراتيجية شاملة متعددة المنصات",
      s5_li2: "نشر يومي وإدارة تفاعل الجمهور",
      s5_li3: "تفاعل آني مع الترندات والمناسبات",
      s5_li4: "تقارير تدقيق وتحليل نمو شهرية",

      s6_tag: "انتشار",
      s6_title: "إدارة المواهب",
      s6_sub: "الكاستينغ وحملات صناع المحتوى",
      s6_desc: "وصول مباشر لشبكة تضم أكثر من ١٠,٠٠٠ مبدع وصانع محتوى في السعودية والخليج لإنتاج محتوى UGC حقيقي وتحقيق وصول واسع.",
      s6_li1: "اختيار الممثلين والمودلز (Casting)",
      s6_li2: "شبكة تضم +١٠,٠٠٠ صانع محتوى",
      s6_li3: "إنتاج محتوى حقيقي وتجارب واقعية (UGC)",
      s6_li4: "إدارة الحملات من الفكرة إلى القياس",

      process_idx_label: "منهجية العمل",
      process_headline: "تنفيذ فائق الدقة في أربع مراحل.",
      process_desc: "مسار عمل مُجرّب صُمم لإزالة العوائق، وشحذ الرسالة الإبداعية، وتحويل الأفكار إلى زخم يفرض حضوره في السوق.",
      
      p1_title: "الاستكشاف",
      p1_sub: "غوص عميق في جوهر علامتك",
      p1_desc: "نتعمق في هوية علامتك التجارية، وتحليل السوق، ودراسة المنافسين، وسيكولوجية الجمهور لتحديد نقطة التمايز الفريدة بدقة.",

      p2_title: "بناء الاستراتيجية",
      p2_sub: "صياغة خطة إبداعية محكمة",
      p2_desc: "نبني خارطة طريق واضحة، محددين نبرة الخطاب، ولوحات الإلهام البصرية، وأولويات المنصات وجدول الإنتاج للوصول إلى أعلى درجات الوضوح.",

      p3_title: "الابتكار والتنفيذ",
      p3_sub: "تحويل التصميم إلى واقع نابض",
      p3_desc: "من شبكات الخطوط وتصوير الإعلانات إلى مقاطع الريلز وتصميم التغليف، يعتني فريقنا المتكامل بكل تفصيلة بدقة متناهية وحس جمالي رفيع.",

      p4_title: "الإطلاق والمتابعة",
      p4_sub: "تسليم استثنائي وزخم مستمر",
      p4_desc: "ندير عمليات الإطلاق الإعلامي باحترافية، مع رصد مباشر لتفاعل الجمهور وتحسين مستمر للحفاظ على قوة دفع علامتك التجارية.",

      why_idx_label: "ميزة كيرف",
      why_headline: "لماذا تختار كبرى العلامات كيرف؟",
      why_lead: "في سوق مليء بالقوالب الجاهزة والأفكار المكررة، نقدم حرفية مخصصة، وشراكة مرنة، وزخماً حقيقياً يمكن قياسه بالأرقام.",
      
      w1_title: "حلول مرنة ومصممة",
      w1_sub: "تتشكّل لتناسب كل علامة بدقة",
      w1_desc: "لا نؤمن بالقوالب المسبقة. نُطوّع تفكيرنا، وأنظمتنا، ونماذج تنفيذنا لتلائم تحديات علامتك وطموحاتها الفريدة.",

      w2_title: "فريق موحد",
      w2_sub: "كل التخصصات تعمل معاً",
      w2_desc: "المخططون الاستراتيجيون، والمخرجون، والمصممون، وخبراء الأداء يجلسون على نفس الطاولة بلا فجوات أو تشتت.",

      w3_title: "نكبر معك",
      w3_sub: "بناء يدوم ويتوسع للمستقبل",
      w3_desc: "لا نصنع أفكاراً عابرة. نبني أنظمة بصرية ومحركات محتوى قابلة للتوسع ومصممة لخدمة نموك لسنوات طويلة.",

      w4_title: "زخم ونتائج ملموسة",
      w4_sub: "أثر حقيقي يمكنك رؤيته وقياسه",
      w4_desc: "مؤشرات أداء رقمية ملموسة، وأعمال بمستوى عالمي، وتفاعل جماهيري واسع يترجم استثمارك إلى عائد تجاري حقيقي.",

      stats_idx_label: "زخم السوق",
      stats_headline: "في قلب القفزة الرقمية المتسارعة للمملكة.",
      stats_desc: "نعمل في واحدة من أكثر البيئات الرقمية ديناميكية وترابطاً وطموحاً على مستوى العالم.",
      stat1_label: "نسبة انتشار الإنترنت في السعودية",
      stat1_sub: "اتصال شامل وتغطية رقمية فائقة في أنحاء المملكة",
      stat2_label: "مستخدم نشط على وسائل التواصل",
      stat2_sub: "استهلاك قياسي لمحتوى الفيديو والمنصات الذكية",
      stat3_label: "شبكة صناع المحتوى والمؤثرين الإقليمية",
      stat3_sub: "مبدعون معتمدون عبر تيك توك وإنستغرام وسناب شات",
      stat4_label: "أعلى وصول للمقطع الإبداعي الواحد",
      stat4_sub: "تفاعل عضوي وأثر ثقافي واسع الانتشار",
      stats_verified: "بيانات معتمدة",
      stats_source: "المصدر: داتا ريبورتال، ديجيتال ٢٠٢٦ — التقرير الرقمي الشامل للمملكة العربية السعودية",

      work_idx_label: "أعمال مختارة",
      work_headline: "أحدث الإنتاجات والحملات الإبداعية.",
      filter_all: "الكل",
      filter_prod: "الإنتاج",
      filter_brand: "الهوية",
      filter_camp: "الحملات",
      filter_photo: "التصوير",

      cat_campaign: "حملة إعلانية",
      cat_cinematic: "سينمائي",
      cat_coverage: "تغطية فعاليات",
      cat_photo: "تصوير احترافي",
      cat_fashion: "أزياء",
      cat_brand: "هوية بصرية",
      cat_lifestyle: "أسلوب حياة",
      cat_commercial: "تجاري",

      w_netflix_client: "نتفليكس",
      w_netflix_title: "لعبة الحبار الموسم الثاني — إطلاق جدة",
      w_netflix_desc: "إنتاج الحملة البصرية الرئيسية (Key Visual) لإطلاق الموسم الثاني من مسلسل لعبة الحبار في جدة، وتجسيد الشخصيات على أرض الواقع لجذب انتباه الجمهور وصناعة تفاعل واسع.",

      w_lomar_client: "لومار",
      w_lomar_title: "الجمع بين الأناقة التراثية وأسلوب الحياة المعاصر",
      w_lomar_desc: "ابتكار مفهوم إبداعي عالي التأثير يجسد الهوية السعودية المعاصرة عبر سرد بصري سينمائي أخّاذ يعكس الأصالة والفخامة.",

      w_mcd_client: "ماكدونالدز",
      w_mcd_title: "ماك كريسبي — فكرة التنافس الكروي في جدة",
      w_mcd_desc: "صياغة فكرة حملة تفاعلية تجسد التنافس الأكبر بين مشجعي قطبي جدة الذين لا يتفقون على أي شيء — حتى ماك كريسبي.",

      w_sport_client: "وزارة الرياضة",
      w_sport_title: "تدشين دوري البريدج — تغطية رقمية وميدانية",
      w_sport_desc: "تغطية شاملة وإدارة محتوى لتدشين دوري البريدج في جدة لأول مرة، وتحويل أجواء الحدث الرياضي إلى حوار تفاعلي على مستوى الوطن.",

      w_auto_client: "تصوير السيارات التجاري",
      w_auto_title: "إثارة القيادة في الكثبان الصحراوية وقت الغروب",
      w_auto_desc: "لقطات حركة ديناميكية عالية السرعة لمركبات الدفع الرباعي فوق الكثبان الذهبية، تدمج روح المغامرة مع إضاءة سينمائية ساحرة.",

      w_fashion_client: "جلسة أزياء مفاهيمية",
      w_fashion_title: "غموض القماش القرمزي وحركة الظلال",
      w_fashion_desc: "سلسلة أزياء جريئة تدمج الإضاءة الدرامية المركزة والأقمشة الحمراء الانسيابية مع دراسات الظل والحركة الراقية.",

      w_dar_client: "دار الجود",
      w_dar_title: "هوية فاخرة مستوحاة من حضارة العلا النبطية",
      w_dar_desc: "ترجمة الهندسة المعمارية الصخرية الشامخة في العلا إلى خط عربي معاصر ونظام هوية بصرية يتميز بالبساطة الأرضية الراقية.",

      w_badre_client: "بدري برانش",
      w_badre_title: "وقود الصباح — وجهة البرانش والقهوة المختصة",
      w_badre_desc: "تطوير الهوية الكاملة لمطعم بدري، للاحتفاء بطقوس الصباح، وجودة القهوة الحرفية والمخبوزات الطازجة بلمسة عصرية مبتكرة.",

      w_onn_client: "أون كافيه درايف ثرو",
      w_onn_title: "حيوية الشارع وأسلوب الحياة اليومي",
      w_onn_desc: "توثيق لحظات الحياة الحضرية في شوارع جدة، وطاقة التزلج والشباب لبناء برامج ولاء واستهداف يومي لعلامة القهوة المتنقلة.",

      w_perfume_client: "عطور فاخرة",
      w_perfume_title: "بورتريه بصري لأفخر روائح العطور",
      w_perfume_desc: "دمج الإضاءة الدافئة المحيطية مع العناصر الطبيعية والصخور لإبراز تفاصيل الزجاجات وتحويلها إلى لوحات فنية جذابة.",

      w_food_client: "فنون الطهي",
      w_food_title: "الدقة وإبراز التفاصيل في كل طبق",
      w_food_desc: "إبراز المكونات الطازجة والألوان بتصوير ماكرو يعتمد على الضوء الطبيعي لإثارة الحواس وعكس البراعة في إعداد الأطباق.",

      w_elba_client: "إلبا الإيطالية",
      w_elba_title: "حرفية المعادن وأناقة المطابخ العصرية",
      w_elba_desc: "تصوير إعلاني عالي الجودة يبرز انعكاسات أسطح الستانلس ستيل ودمج المنتجات في بيئة مطبخ أنيقة تعكس فخامة الصناعة الإيطالية.",

      partners_idx_label: "شركاء النجاح",
      partners_headline: "علامات تجارية ومؤسسات وضعنا لها الزخم.",
      partners_desc: "نتشرف بشراكتنا مع الوزارات الحكومية، والشركات العالمية، والمشاريع السعودية الرائدة لصناعة المستقبل.",
      banner_eyebrow: "منظومة المبدعين",
      banner_title: "أي صانع محتوى. في أي مكان. بلا حدود.",
      banner_desc: "من المتخصصين في المجالات الدقيقة إلى مشاهير المنصات، يدير مكتبنا المتخصص اختيار المواهب، وصياغة العقود، وإعداد مسودات المحتوى وقياس العائد مع أكثر من ١٠,٠٠٠ مبدع.",
      banner_btn: "اطلب قائمة المواهب",

      contact_idx_label: "ابدأ الحوار",
      contact_title_1: "حيّاك",
      contact_title_2: "على فنجان قهوة.",
      contact_lead: "هل لديك رؤية طموحة، أو علامة تجارية ترغب في إعادة تموضعها، أو إنتاج إعلامي يتطلب لمسة سينمائية عالمية؟ نحن مستعدون لصناعة الفارق معك.",
      contact_call_label: "اتصل بنا مباشرة",
      contact_email_label: "المشاريع والاستفسارات",
      contact_hq_label: "المقر الرئيسي",
      contact_hq_val: "حي الروضة، جدة، المملكة العربية السعودية",
      contact_address_val: "حي الروضة، جدة، المملكة",
      contact_web_label: "الموقع الرقمي",
      contact_social_label: "تابع أثر حركتنا",

      form_title: "حدّثنا عن مشروعك وطموحاتك",
      form_desc: "املأ الحقول أدناه وسيتواصل معك أحد أعضاء القيادة الإبداعية خلال ٢٤ ساعة عمل.",
      form_label_name: "الاسم الكريم *",
      form_label_email: "البريد الإلكتروني *",
      form_label_company: "اسم الشركة / العلامة",
      form_label_service: "الخدمة المطلوبة",
      form_label_msg: "نبذة عن المشروع والجدول الزمني *",
      form_btn: "إرسال طلب المشروع",
      form_err_name: "يرجى كتابة الاسم الكريم",
      form_err_email: "يرجى كتابة بريد إلكتروني صحيح",
      form_err_msg: "يرجى مشاركة نبذة مختصرة عن المشروع",
      form_success_msg: "شكراً لتواصلك. تم استلام طلبك بنجاح وسيتواصل معك فريقنا في أقرب وقت.",

      opt_branding: "بناء الهوية وتصميم العلامة",
      opt_production: "الإنتاج الإعلامي والإعلانات",
      opt_social: "إدارة حسابات التواصل والمجتمعات",
      opt_marketing: "التسويق الرقمي والإعلانات الممولة",
      opt_talent: "إدارة المواهب وصناع المحتوى",
      opt_360: "حملة تسويقية وإبداعية متكاملة ٣٦٠°",

      footer_motto: "وكالة إبداعية متكاملة — حلول مدفوعة بالحركة.",
      footer_copy: "© ٢٠٢٦ وكالة كيرف (CURVE). جميع الحقوق محفوظة.",
      footer_location: "جدة، المملكة العربية السعودية",
      footer_top: "العودة للأعلى",

      form_ph_name: "فهد الحربي",
      form_ph_email: "fahad@company.sa",
      form_ph_company: "مجموعة أعمال القمة",
      form_ph_msg: "شاركنا أهداف المشروع، التحديات الحالية، والوقت المتوقع للإطلاق..."
    }
  };

  // ── إظهار / إخفاء اللغة العربية ──────────────────────────────────────────
  // ARABIC_ENABLED = false  →  يُخفى زر اللغة (EN/عربي) ويُثبَّت الموقع على الإنجليزية
  // ARABIC_ENABLED = true   →  يرجع الزر والعربي فوراً بالضغط عليه
  // ملاحظة: كل الترجمات العربية موجودة كما هي في translations.ar — ما انحذف شي.
  const ARABIC_ENABLED = false;

  let currentLang = localStorage.getItem('curve_lang') || 'en';

  if (!ARABIC_ENABLED) {
    currentLang = 'en';
    const _hideLangToggle = () => {
      const _btn = document.getElementById('lang-toggle');
      if (_btn) _btn.style.display = 'none';
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', _hideLangToggle);
    } else {
      _hideLangToggle();
    }
  }

  function applyLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('curve_lang', lang);

    const isRtl = lang === 'ar';
    document.documentElement.setAttribute('lang', lang);
    document.documentElement.setAttribute('dir', isRtl ? 'rtl' : 'ltr');

    // Update toggle buttons active class
    const langBtn = document.getElementById('lang-toggle');
    if (langBtn) {
      const enSpan = langBtn.querySelector('.lang-en');
      const arSpan = langBtn.querySelector('.lang-ar');
      if (enSpan && arSpan) {
        enSpan.classList.toggle('active', lang === 'en');
        arSpan.classList.toggle('active', lang === 'ar');
      }
    }

    // Apply translations to all data-i18n elements
    const i18nElements = document.querySelectorAll('[data-i18n]');
    i18nElements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (translations[lang] && translations[lang][key]) {
        el.textContent = translations[lang][key];
      }
    });

    // Apply placeholders
    const placeholderElements = document.querySelectorAll('[data-i18n-ph]');
    placeholderElements.forEach(el => {
      const key = el.getAttribute('data-i18n-ph');
      if (translations[lang] && translations[lang][key]) {
        el.setAttribute('placeholder', translations[lang][key]);
      }
    });

    // Refresh active filter text if needed
    updateStatNumerals(lang);
  }

  // Update stat numerals formatting for Arabic if desired
  function updateStatNumerals(lang) {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
      const numSpan = card.querySelector('.stat-num');
      const symSpan = card.querySelector('.stat-symbol');
      if (!numSpan || !symSpan) return;
      
      const target = numSpan.getAttribute('data-target');
      if (lang === 'ar') {
        if (target === '99') {
          numSpan.textContent = '٩٩';
          symSpan.textContent = '٪';
        } else if (target === '38.6') {
          numSpan.textContent = '٣٨.٦';
          symSpan.textContent = 'م+';
        } else if (target === '10000') {
          numSpan.textContent = '١٠,٠٠٠';
          symSpan.textContent = '+';
        } else if (target === '42000') {
          numSpan.textContent = '٤٢,٠٠٠';
          symSpan.textContent = '+';
        }
      } else {
        if (target === '99') {
          numSpan.textContent = '99';
          symSpan.textContent = '%';
        } else if (target === '38.6') {
          numSpan.textContent = '38.6';
          symSpan.textContent = 'M+';
        } else if (target === '10000') {
          numSpan.textContent = '10,000';
          symSpan.textContent = '+';
        } else if (target === '42000') {
          numSpan.textContent = '42,000';
          symSpan.textContent = '+';
        }
      }
    });
  }

  // Language toggle click listener
  const langToggleBtn = document.getElementById('lang-toggle');
  if (langToggleBtn) {
    langToggleBtn.addEventListener('click', () => {
      if (!ARABIC_ENABLED) return;   // hard guard — Arabic stays parked, even if the button is forced visible
      const nextLang = currentLang === 'en' ? 'ar' : 'en';
      applyLanguage(nextLang);
    });
  }

  // Initialize language (forced to English whenever Arabic is parked)
  applyLanguage(ARABIC_ENABLED ? currentLang : 'en');

  /* ==========================================================================
     2. STICKY HEADER & SCROLL BEHAVIOR
     ========================================================================== */
  const header = document.getElementById('header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }, { passive: true });

  /* ==========================================================================
     3. MOBILE NAVIGATION DRAWER
     ========================================================================== */
  const mobileToggle = document.getElementById('mobile-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link');

  if (mobileToggle && mobileMenu) {
    mobileToggle.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.contains('open');
      mobileMenu.classList.toggle('open');
      mobileToggle.classList.toggle('active');
      mobileToggle.setAttribute('aria-expanded', !isOpen);
      mobileMenu.setAttribute('aria-hidden', isOpen);
      document.body.style.overflow = isOpen ? '' : 'hidden';
    });

    mobileNavLinks.forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        mobileToggle.classList.remove('active');
        mobileToggle.setAttribute('aria-expanded', 'false');
        mobileMenu.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
      });
    });
  }

  /* ==========================================================================
     4. INTERSECTION OBSERVER FOR SCROLL REVEALS
     ========================================================================== */
  const revealElements = document.querySelectorAll('.reveal');
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const delay = entry.target.getAttribute('data-delay') || 0;
        setTimeout(() => {
          entry.target.classList.add('active');
        }, parseInt(delay, 10));
        observer.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: '0px 0px -40px 0px',
    threshold: 0.12
  });

  revealElements.forEach(el => revealObserver.observe(el));

  /* ==========================================================================
     5. PORTFOLIO FILTER SYSTEM
     ========================================================================== */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const workCards = document.querySelectorAll('.work-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filter = btn.getAttribute('data-filter');

      workCards.forEach(card => {
        const categories = card.getAttribute('data-category') || '';
        if (filter === 'all' || categories.includes(filter)) {
          card.classList.remove('hidden');
          // Add entrance animation
          card.style.opacity = '0';
          card.style.transform = 'translateY(16px)';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 50);
        } else {
          card.classList.add('hidden');
        }
      });
    });
  });

  /* ==========================================================================
     6. INTERACTIVE INQUIRY FORM (Validation & Feedback)
     ========================================================================== */
  const inquiryForm = document.getElementById('inquiry-form');
  const formStatus = document.getElementById('form-status');
  const submitBtn = document.getElementById('form-submit-btn');

  if (inquiryForm) {
    inquiryForm.addEventListener('submit', (e) => {
      e.preventDefault();

      let hasError = false;

      // Inputs to validate
      const nameInput = document.getElementById('form-name');
      const emailInput = document.getElementById('form-email');
      const msgInput = document.getElementById('form-message');

      // Clear previous error states
      [nameInput, emailInput, msgInput].forEach(inp => {
        inp.closest('.form-group').classList.remove('has-error');
      });

      // Name validation
      if (!nameInput.value.trim()) {
        nameInput.closest('.form-group').classList.add('has-error');
        hasError = true;
      }

      // Email validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailInput.value.trim() || !emailRegex.test(emailInput.value.trim())) {
        emailInput.closest('.form-group').classList.add('has-error');
        hasError = true;
      }

      // Message validation
      if (!msgInput.value.trim()) {
        msgInput.closest('.form-group').classList.add('has-error');
        hasError = true;
      }

      if (hasError) return;

      // Simulated sending state
      submitBtn.disabled = true;
      const originalText = submitBtn.querySelector('.btn-text').textContent;
      submitBtn.querySelector('.btn-text').textContent = currentLang === 'ar' ? 'جارٍ الإرسال...' : 'TRANSMITTING...';

      setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.querySelector('.btn-text').textContent = originalText;

        // Show success alert
        if (formStatus) {
          formStatus.className = 'form-status-box success';
          formStatus.textContent = translations[currentLang].form_success_msg;
        }

        // Reset form
        inquiryForm.reset();

        // Fade out message after 6 seconds
        setTimeout(() => {
          if (formStatus) formStatus.style.display = 'none';
        }, 6000);
      }, 900);
    });
  }

});
