from typing import Dict, Any, List
from app.models.schemas import (
    VerificationResponse, AtomicClaim, ClaimReviewEvidence,
    ManipulationSignals, ShareableDebunkCard, PipelineStep
)

SEED_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "unesco-anthem": {
        "id": "unesco-anthem",
        "title": "UNESCO Best National Anthem Award",
        "sample_input": "Great news for every proud Indian! 🇮🇳 UNESCO has just officially announced that 'Jana Gana Mana' has been declared the BEST NATIONAL ANTHEM in the world! No other country's anthem got this honour. Please forward this message to at least 10 people and all your groups right now to show your patriotism! Jai Hind! Vande Mataram!",
        "type": "text",
        "category": "False Award / National Pride Bait",
        "response": VerificationResponse(
            status="success",
            overall_verdict="FALSE",
            credibility_score=8,
            risk_level="HIGH_VIRAL_DECEPTION",
            extracted_text="UNESCO has officially announced that 'Jana Gana Mana' has been declared the BEST NATIONAL ANTHEM in the world! Forward to 10 people right now...",
            atomic_claims=[
                AtomicClaim(
                    id=1,
                    text="UNESCO officially declared India's national anthem as the best in the world",
                    normalized_query="UNESCO declared Jana Gana Mana best national anthem award",
                    target_entity="UNESCO",
                    verdict="FALSE"
                ),
                AtomicClaim(
                    id=2,
                    text="UNESCO conducts competitions or awards for national anthems",
                    normalized_query="UNESCO national anthem competition rankings",
                    target_entity="UNESCO",
                    verdict="FALSE"
                )
            ],
            certified_evidence=[
                ClaimReviewEvidence(
                    claim_text="UNESCO declared Jana Gana Mana as the best national anthem in the world",
                    claimant="Viral WhatsApp Message",
                    fact_checker="AltNews",
                    rating="Pants on Fire / False",
                    review_date="2021-08-14",
                    review_url="https://www.altnews.in/unesco-declared-jana-gana-mana-best-national-anthem-no-viral-hoax-lives-on/",
                    is_ifcn_certified=True
                ),
                ClaimReviewEvidence(
                    claim_text="UNESCO ranks national anthems and awarded 1st prize to India",
                    claimant="Social Media Users",
                    fact_checker="BOOM Live",
                    rating="False",
                    review_date="2022-01-26",
                    review_url="https://www.boomlive.in/fake-news/unesco-best-national-anthem-india-viral-message-fact-check",
                    is_ifcn_certified=True
                ),
                ClaimReviewEvidence(
                    claim_text="United Nations official declaration on Indian anthem",
                    claimant="Forwarded WhatsApp Chain",
                    fact_checker="PIB Fact Check",
                    rating="Fake News",
                    review_date="2020-08-15",
                    review_url="https://factcheck.pib.gov.in",
                    is_ifcn_certified=True
                )
            ],
            web_grounding_citations=[
                {
                    "title": "UNESCO Official Clarification: No such award exists",
                    "publisher": "The Hindu (thehindu.com)",
                    "authority_badge": "Accredited National Newspaper",
                    "url": "https://www.thehindu.com/news/national/unesco-denies-ranking-national-anthems/article2470123.ece",
                    "pub_date": "National Investigative Reporting",
                    "snippet": "UNESCO had officially stated that it does not evaluate, rank, or award 'Best National Anthem' titles to any country."
                },
                {
                    "title": "Fact Check: Evolution of India's Longest Running Internet Hoax",
                    "publisher": "India Today (indiatoday.in)",
                    "authority_badge": "Certified IFCN Fact-Checking Desk",
                    "url": "https://www.indiatoday.in/fact-check",
                    "pub_date": "Fact-Check Investigation",
                    "snippet": "Analysis tracing the false viral anthem claim and confirming official UNESCO disclaimers."
                }
            ],
            manipulation_breakdown=ManipulationSignals(
                urgency_score=85,
                emotional_intensity=90,
                sensationalism_score=95,
                credibility_index=8,
                detected_tactics=[
                    "Patriotism / Identity Exploitation",
                    "Manufactured Viral Chain ('Forward to at least 10 people')",
                    "Institutional Name-Dropping (UNESCO)",
                    "Emotional Outrage / Guilt Induction if not shared"
                ],
                linguistic_markers=[
                    "Multiple exclamation marks (5x)",
                    "ALL CAPS emphasis ('BEST NATIONAL ANTHEM')",
                    "Flag emojis and moral obligation rhetoric"
                ],
                missing_elements=[
                    "Zero official UNESCO press links",
                    "No resolution number or official citation",
                    "No verifiable date of announcement"
                ]
            ),
            debunk_summary_en="This is a classic, recurring internet hoax that has circulated since 2006. UNESCO does not rank, judge, or bestow 'Best National Anthem' awards upon any nation. Both UNESCO spokespersons and official fact-checkers (AltNews, BOOM, PIB) have repeatedly debunked this claim.",
            debunk_summary_hi="यह 2006 से चल रहा एक पुराना फर्जी संदेश (इंटरनेट होक्स) है। यूनेस्को (UNESCO) किसी भी देश के राष्ट्रगान को 'सर्वश्रेष्ठ' घोषित करने जैसी कोई प्रतियोगिता या पुरस्कार आयोजित नहीं करता है। पीआईबी (PIB) और अंतरराष्ट्रीय फैक्ट-चेकर्स ने इसकी पुष्टि की है कि यह दावा पूरी तरह झूठा है।",
            verification_checklist=[
                "Check UNESCO official website (unesco.org) for any announcement before believing award claims.",
                "Notice emotional coercion ('Forward to 10 people if you are proud Indian'). Legitimate news never asks for chain forwards.",
                "Look for press release IDs or news coverage in reputable national newspapers."
            ],
            shareable_card=ShareableDebunkCard(
                headline_en="❌ FAKE ALERT: UNESCO Did NOT Declare India's Anthem 'The Best'",
                headline_hi="❌ फर्जी संदेश: यूनेस्को ने राष्ट्रगान को 'सर्वश्रेष्ठ' घोषित नहीं किया है",
                verdict="FALSE / FABRICATED",
                bullet_points_en=[
                    "UNESCO has officially confirmed it NEVER conducts national anthem contests or awards.",
                    "This viral forward is a 18-year-old internet hoax recycled every year.",
                    "Do NOT forward this chain message. Break the chain of false information."
                ],
                bullet_points_hi=[
                    "यूनेस्को ने स्पष्ट किया है कि वह राष्ट्रगान की कोई रैंकिंग या पुरस्कार नहीं देता।",
                    "यह 18 साल पुराना झूठा संदेश है जिसे बार-बार फॉरवर्ड किया जाता है।",
                    "इस संदेश को आगे फॉरवर्ड न करें। सच फैलाएं, अफवाह नहीं।"
                ],
                whatsapp_format_text_en="🚨 *SATYA SETU FACT CHECK: FAKE CLAIM* 🚨\n\n❌ *Claim:* UNESCO declared India's National Anthem as the best in the world.\n\n✅ *Fact:* 100% FALSE. UNESCO does not give any such awards or rankings. Certified false by AltNews, BOOM, and PIB.\n\n🔗 *Verify Source:* pib.gov.in / altnews.in\n\n🛡️ *Verified with SatyaSetu AI*",
                whatsapp_format_text_hi="🚨 *सत्यसेतु फैक्ट-चेक: फर्जी दावा* 🚨\n\n❌ *दावा:* यूनेस्को ने 'जन गण मन' को दुनिया का सर्वश्रेष्ठ राष्ट्रगान घोषित किया।\n\n✅ *सच्चाई:* बिल्कुल झूठा। यूनेस्को ऐसा कोई पुरस्कार या रैंकिंग नहीं देता। PIB और फैक्ट-चेकर्स द्वारा सत्यापित।\n\n🛡️ *सत्यसेतु (SatyaSetu) द्वारा सत्यापित - कृपया अफवाह न फैलाएं*",
                verification_source_tag="Certified by PIB Fact Check & AltNews"
            ),
            pipeline_steps=[
                PipelineStep(name="Input Sanitization & OCR", status="done", detail="Processed 312 characters of viral text", elapsed_ms=45),
                PipelineStep(name="Atomic Claim Deconstruction", status="done", detail="Extracted 2 atomic claims with normalized entities", elapsed_ms=120),
                PipelineStep(name="Google Fact Check Tools API", status="done", detail="Matched 3 certified ClaimReview schemas (AltNews, BOOM)", elapsed_ms=180),
                PipelineStep(name="Manipulation & Urgency Analysis", status="done", detail="Calculated 85% urgency score and moral coercion markers", elapsed_ms=30),
                PipelineStep(name="Bilingual Counter-Debunk Synthesis", status="done", detail="Generated dual-language WhatsApp cards and checklist", elapsed_ms=95)
            ],
            total_latency_ms=470,
            data_source_mode="Certified Fact-Check Archive (Tier 1 Direct Match)"
        )
    },
    "rbi-500-note": {
        "id": "rbi-500-note",
        "title": "Fake RBI ₹500 Currency Green Strip Notice",
        "sample_input": "URGENT WARNING FROM RBI! 🚨 Do not accept ₹500 currency notes where the green security thread is closer to Mahatma Gandhi's portrait instead of the Governor's signature. Such notes are completely FAKE and banks are confiscating them without refund! Check your wallet and forward to all friends and family right now!",
        "type": "text",
        "category": "Financial Panic / Banking Misinformation",
        "response": VerificationResponse(
            status="success",
            overall_verdict="FALSE",
            credibility_score=12,
            risk_level="HIGH_FINANCIAL_PANIC",
            extracted_text="URGENT WARNING FROM RBI! Do not accept ₹500 currency notes where the green security thread is closer to Mahatma Gandhi's portrait...",
            atomic_claims=[
                AtomicClaim(
                    id=1,
                    text="RBI issued a warning stating ₹500 notes with green strip near Gandhi's portrait are counterfeit",
                    normalized_query="RBI 500 note green strip near Gandhi portrait fake warning",
                    target_entity="Reserve Bank of India (RBI)",
                    verdict="FALSE"
                ),
                AtomicClaim(
                    id=2,
                    text="Both variations of ₹500 notes are not legally valid currency",
                    normalized_query="RBI validity 500 rupee note security thread placement",
                    target_entity="Reserve Bank of India",
                    verdict="FALSE"
                )
            ],
            certified_evidence=[
                ClaimReviewEvidence(
                    claim_text="RBI circular declares ₹500 notes with green thread near Gandhi picture as fake",
                    claimant="Viral Social Media Posts",
                    fact_checker="PIB Fact Check",
                    rating="Fake / Fabricated",
                    review_date="2023-09-18",
                    review_url="https://twitter.com/PIBFactCheck/status/1703649195932598380",
                    is_ifcn_certified=True
                ),
                ClaimReviewEvidence(
                    claim_text="500 rupee notes with green security strip close to Governor signature vs Gandhi are counterfeit",
                    claimant="WhatsApp Forward",
                    fact_checker="Factly",
                    rating="False",
                    review_date="2023-01-10",
                    review_url="https://factly.in/rbi-500-rupee-note-security-strip-fact-check",
                    is_ifcn_certified=True
                )
            ],
            web_grounding_citations=[
                {
                    "title": "RBI Official Paisa Bolta Hai Portal: ₹500 Security Features Clarification",
                    "publisher": "Reserve Bank of India (rbi.org.in)",
                    "authority_badge": "Central Bank Statutory Gazette",
                    "url": "https://paisaboltahai.rbi.org.in",
                    "pub_date": "Statutory Financial Gazette",
                    "snippet": "RBI clarified that both types of ₹500 currency notes with minor printing placement shifts of the security thread are 100% genuine and legal tender."
                },
                {
                    "title": "Fact Check: Viral message claiming ₹500 note with security thread near Gandhi is fake is bogus",
                    "publisher": "The Economic Times (economictimes.indiatimes.com)",
                    "authority_badge": "Accredited Financial Daily",
                    "url": "https://economictimes.indiatimes.com/wealth/personal-finance-news",
                    "pub_date": "Financial Daily Reporting",
                    "snippet": "The Economic Times confirms RBI clarification: Notes with either placement of security thread are completely valid legal tender."
                }
            ],
            manipulation_breakdown=ManipulationSignals(
                urgency_score=92,
                emotional_intensity=88,
                sensationalism_score=90,
                credibility_index=12,
                detected_tactics=[
                    "Financial Fear Exploitation (Loss of money)",
                    "Fabricated Institutional Directive (RBI)",
                    "Manufactured Urgent Forward Mandate ('Check your wallet immediately')"
                ],
                linguistic_markers=[
                    "Urgency words: 'URGENT WARNING', 'confiscating without refund'",
                    "Sensational punctuation '!'",
                    "Alarmist siren emoji"
                ],
                missing_elements=[
                    "No RBI Circular Number (e.g., RBI/2023-24/...)",
                    "No hyperlink to rbi.org.in or official press release"
                ]
            ),
            debunk_summary_en="The Reserve Bank of India has issued no such warning. Both variations of the ₹500 note—where the green security thread is slightly shifted—are completely genuine legal tender according to the RBI's official currency portal.",
            debunk_summary_hi="आरबीआई (RBI) ने ऐसी कोई चेतावनी जारी नहीं की है। ₹500 के दोनों तरह के नोट (चाहे हरी पट्टी गांधी जी की तस्वीर के पास हो या गवर्नर के हस्ताक्षर के पास) पूरी तरह से असली और वैध हैं। यह दावा सरासर फर्जी है।",
            verification_checklist=[
                "Check the official RBI currency verification portal: paisaboltahai.rbi.org.in",
                "Verify if the viral message mentions a specific RBI Circular Number. Genuine notices always have one.",
                "Never share financial advisories without verifying on official bank or RBI portals."
            ],
            shareable_card=ShareableDebunkCard(
                headline_en="❌ FAKE: Both Types of ₹500 Currency Notes Are 100% Genuine",
                headline_hi="❌ फर्जी खबर: ₹500 के दोनों तरह के नोट पूरी तरह असली और वैध हैं",
                verdict="FALSE / HOAX",
                bullet_points_en=[
                    "PIB Fact Check confirmed RBI released no such circular.",
                    "Both placements of the green security strip on ₹500 notes are authentic legal tender.",
                    "Do not refuse or circulate panic about ₹500 currency notes."
                ],
                bullet_points_hi=[
                    "PIB फैक्ट-चेक ने पुष्टि की है कि RBI ने ऐसा कोई नियम नहीं बनाया।",
                    "हरी पट्टी की मामूली स्थिति में बदलाव छपाई के कारण है, दोनों नोट असली हैं।",
                    "दुकानदारों या आम जनता में भ्रम न फैलाएं।"
                ],
                whatsapp_format_text_en="🚨 *SATYA SETU FACT CHECK: ₹500 NOTE RUMOR IS FAKE* 🚨\n\n❌ *Rumor:* ₹500 notes with green strip near Gandhi's picture are fake and banned by RBI.\n\n✅ *Truth:* 100% FALSE. RBI & PIB Fact Check have clarified that both variations are completely GENUINE legal tender.\n\n🔗 *Official Link:* paisaboltahai.rbi.org.in\n\n🛡️ *Verified with SatyaSetu AI*",
                whatsapp_format_text_hi="🚨 *सत्यसेतु फैक्ट-चेक: ₹500 नोट की अफवाह झूठी है* 🚨\n\n❌ *अफवाह:* गांधीजी के पास हरी पट्टी वाला ₹500 का नोट नकली है।\n\n✅ *सच्चाई:* 100% झूठ। RBI और PIB ने स्पष्ट किया है कि दोनों नोट पूरी तरह असली और मान्य हैं।\n\n🛡️ *सत्यसेतु (SatyaSetu) - अफवाहों से बचें, सच जानें*",
                verification_source_tag="Certified by RBI & PIB Fact Check"
            ),
            pipeline_steps=[
                PipelineStep(name="Input Sanitization & OCR", status="done", detail="Processed financial alert text", elapsed_ms=40),
                PipelineStep(name="Atomic Claim Deconstruction", status="done", detail="Identified RBI currency authenticity claim", elapsed_ms=110),
                PipelineStep(name="Google Fact Check Tools API", status="done", detail="Retrieved PIB Fact Check debunk from official schema", elapsed_ms=190),
                PipelineStep(name="Manipulation & Urgency Analysis", status="done", detail="Detected financial panic triggers and missing circular numbers", elapsed_ms=25),
                PipelineStep(name="Bilingual Counter-Debunk Synthesis", status="done", detail="Compiled RBI advisory card and WhatsApp debunk", elapsed_ms=85)
            ],
            total_latency_ms=450,
            data_source_mode="Certified Fact-Check Archive (Tier 1 Direct Match)"
        )
    },
    "salt-shortage": {
        "id": "salt-shortage",
        "title": "Countrywide Salt Shortage & Price Hike Panic",
        "sample_input": "EMERGENCY ALERT: Huge shortage of salt across India from tonight! Salt packets are already selling for ₹300 to ₹400 in Delhi, UP, and Bihar. Trucks have been stopped at borders due to new transport tax. Go to your local kirana store immediately and buy at least 5kg salt before stocks run out tonight! Forward to all your contacts immediately!",
        "type": "text",
        "category": "Supply Chain Panic / Artificial Scarcity",
        "response": VerificationResponse(
            status="success",
            overall_verdict="FALSE",
            credibility_score=5,
            risk_level="CRITICAL_CIVIC_PANIC",
            extracted_text="EMERGENCY ALERT: Huge shortage of salt across India from tonight! Salt packets are already selling for ₹300 to ₹400...",
            atomic_claims=[
                AtomicClaim(
                    id=1,
                    text="There is a nationwide shortage of edible salt in India",
                    normalized_query="salt shortage panic in India price hike rumor",
                    target_entity="Ministry of Consumer Affairs",
                    verdict="FALSE"
                ),
                AtomicClaim(
                    id=2,
                    text="Salt prices surged to ₹400 due to transport border taxes",
                    normalized_query="salt price 400 rupee per kg rumor border tax",
                    target_entity="Department of Food and Public Distribution",
                    verdict="FALSE"
                )
            ],
            certified_evidence=[
                ClaimReviewEvidence(
                    claim_text="Severe shortage of salt in India causing prices to soar to ₹400/kg",
                    claimant="Viral Audio & Text Messages",
                    fact_checker="India Today Fact Check",
                    rating="False / Pure Hoax",
                    review_date="2022-11-12",
                    review_url="https://www.indiatoday.in/fact-check",
                    is_ifcn_certified=True
                ),
                ClaimReviewEvidence(
                    claim_text="Salt supply disrupted across states causing panic buying",
                    claimant="Social Media Posts",
                    fact_checker="The Quint WebQoof",
                    rating="Misleading Rumor",
                    review_date="2022-11-14",
                    review_url="https://www.thequint.com/news/webqoof",
                    is_ifcn_certified=True
                )
            ],
            web_grounding_citations=[
                {
                    "title": "Ministry of Consumer Affairs: Sufficient Salt Reserves Available in India",
                    "publisher": "Press Information Bureau (pib.gov.in)",
                    "authority_badge": "Official Government Gazette",
                    "url": "https://pib.gov.in",
                    "pub_date": "Official Gazette Bulletin",
                    "snippet": "Government of India assured citizens that India produces over 300 lakh tonnes of salt annually, far exceeding domestic consumption of ~65 lakh tonnes."
                },
                {
                    "title": "No shortage of salt, do not believe in rumours: Government clarifies amidst viral panic",
                    "publisher": "The Indian Express (indianexpress.com)",
                    "authority_badge": "Accredited National Newspaper",
                    "url": "https://indianexpress.com/article/india/india-news-india/no-shortage-of-salt-dont-believe-in-rumours-up-government-clarifies/",
                    "pub_date": "National Daily Reporting",
                    "snippet": "National investigative report confirming ample salt supplies across wholesale markets and refuting viral hoard-buying rumors."
                }
            ],
            manipulation_breakdown=ManipulationSignals(
                urgency_score=98,
                emotional_intensity=95,
                sensationalism_score=96,
                credibility_index=5,
                detected_tactics=[
                    "Artificial Scarcity Induction (Panic Buying Trigger)",
                    "Extreme Price Exaggeration (₹400/kg)",
                    "Immediate Action Pressure ('Go to store before tonight')",
                    "Herd Mentality Exploitation"
                ],
                linguistic_markers=[
                    "Urgency words: 'EMERGENCY ALERT', 'tonight', 'immediately'",
                    "Sensational numbers and price inflation claims",
                    "Aggressive forward demands"
                ],
                missing_elements=[
                    "No confirmation from local market associations or administration",
                    "No government supply bulletin cited"
                ]
            ),
            debunk_summary_en="This is an artificial panic-buying rumor engineered to cause chaos and black marketing. India produces vast surplus salt every year. The Ministry of Consumer Affairs has clarified that there is no shortage or transport disruption whatsoever.",
            debunk_summary_hi="यह जमाखोरी और कालाबाजारी को बढ़ावा देने के लिए फैलाई गई सोची-समझी अफवाह है। भारत में नमक का भारी अधिशेष (सरप्लस) उत्पादन होता है। उपभोक्ता मामलों के मंत्रालय ने स्पष्ट किया है कि देश में नमक की कोई कमी नहीं है।",
            verification_checklist=[
                "Recognize artificial scarcity language: rumors always urge you to 'run to the market before tonight'.",
                "Check official government commodity statements or local police warnings against rumors.",
                "Do not engage in panic buying, as it artificially triggers actual shop-level shortages."
            ],
            shareable_card=ShareableDebunkCard(
                headline_en="❌ DANGEROUS RUMOR: No Salt Shortage in India",
                headline_hi="❌ खतरनाक अफवाह: देश में नमक की कोई कमी नहीं है",
                verdict="FALSE / HOAX",
                bullet_points_en=[
                    "India produces over 300 lakh tonnes of salt annually, 5x the national requirement.",
                    "Government has warned that hoarders and rumor mongers will face criminal prosecution.",
                    "Report anyone selling salt above printed MRP to local authorities."
                ],
                bullet_points_hi=[
                    "भारत अपनी जरूरत से 5 गुना अधिक नमक का उत्पादन करता है।",
                    "अफवाह फैलाने वालों और अधिक कीमत वसूलने वालों पर सख्त कानूनी कार्रवाई होगी।",
                    "दुकानदारों को MRP से ज्यादा पैसे न दें और अफवाहें न फैलाएं।"
                ],
                whatsapp_format_text_en="🚨 *ALERT: SALT SHORTAGE RUMOR IS BOGUS* 🚨\n\n❌ *Rumor:* Severe shortage of salt in India, prices jumping to ₹400/kg.\n\n✅ *Fact:* 100% FALSE RUMOR. India has abundant salt stocks. Ministry of Consumer Affairs confirmed normal supplies.\n\n⚠️ *Do NOT panic-buy or forward fake messages.*\n\n🛡️ *Verified via SatyaSetu AI*",
                whatsapp_format_text_hi="🚨 *सावधान: नमक की कमी की खबर कोरी अफवाह है* 🚨\n\n❌ *अफवाह:* देश में नमक खत्म हो रहा है और ₹400 में बिक रहा है।\n\n✅ *सच्चाई:* बिल्कुल झूठ। सरकार ने पुष्टि की है कि नमक का पर्याप्त भंडार मौजूद है।\n\n🛡️ *सत्यसेतु (SatyaSetu) - अफवाहों को रोकें, शांति बनाए रखें*",
                verification_source_tag="Certified by Ministry of Consumer Affairs & PIB"
            ),
            pipeline_steps=[
                PipelineStep(name="Input Sanitization & OCR", status="done", detail="Scanned panic broadcast text", elapsed_ms=35),
                PipelineStep(name="Atomic Claim Deconstruction", status="done", detail="Isolated supply shortage and price hike claims", elapsed_ms=105),
                PipelineStep(name="Google Fact Check Tools API", status="done", detail="Retrieved recurring commodity panic records", elapsed_ms=175),
                PipelineStep(name="Manipulation & Urgency Analysis", status="done", detail="Computed critical 98% urgency score (Panic-Buying Index)", elapsed_ms=30),
                PipelineStep(name="Bilingual Counter-Debunk Synthesis", status="done", detail="Constructed civic calm alert and legal caution notes", elapsed_ms=80)
            ],
            total_latency_ms=425,
            data_source_mode="Certified Fact-Check Archive (Tier 1 Direct Match)"
        )
    },
    "cbse-exam-circular": {
        "id": "cbse-exam-circular",
        "title": "Official CBSE Board Exam Date Sheet Announcement",
        "sample_input": "Central Board of Secondary Education (CBSE) has officially released the date sheet for Class 10 and 12 Board Examinations 2026. Students and parents can download the authenticated PDF timetable directly from the official portal cbse.gov.in. Principals are instructed to distribute admit cards as per circular no. CBSE/COORD/2026.",
        "type": "text",
        "category": "Official Government Notification (Control / True)",
        "response": VerificationResponse(
            status="success",
            overall_verdict="TRUE",
            credibility_score=94,
            risk_level="LOW_AUTHENTIC",
            extracted_text="Central Board of Secondary Education (CBSE) has officially released the date sheet for Class 10 and 12 Board Examinations...",
            atomic_claims=[
                AtomicClaim(
                    id=1,
                    text="CBSE released the official date sheet on cbse.gov.in",
                    normalized_query="CBSE official date sheet class 10 12 cbse.gov.in circular",
                    target_entity="Central Board of Secondary Education",
                    verdict="TRUE"
                )
            ],
            certified_evidence=[],
            web_grounding_citations=[
                {
                    "title": "CBSE Official Notification Portal: Class 10 & 12 Examination Schedule",
                    "publisher": "Central Board of Secondary Education (cbse.gov.in)",
                    "authority_badge": "Statutory Education Authority",
                    "url": "https://www.cbse.gov.in",
                    "pub_date": "Official Statutory Circular",
                    "snippet": "Official circular and authenticated timetable published by the Controller of Examinations, CBSE Head Office."
                },
                {
                    "title": "CBSE Date Sheet Announcement & Timetable Release",
                    "publisher": "The Indian Express / PTI (indianexpress.com)",
                    "authority_badge": "Accredited National Newspaper & Wire Service",
                    "url": "https://indianexpress.com/article/education/cbse-datesheet-class-10-12-board-exam-schedule-download-pdf/",
                    "pub_date": "National Newspaper Coverage",
                    "snippet": "National education reporting confirming release of authenticated PDF timetable on official CBSE portal."
                }
            ],
            manipulation_breakdown=ManipulationSignals(
                urgency_score=15,
                emotional_intensity=12,
                sensationalism_score=10,
                credibility_index=94,
                detected_tactics=["Institutional administrative communication"],
                linguistic_markers=["Formal objective language", "Specific circular reference number", "Official domain link (.gov.in)"],
                missing_elements=["No manipulative pressure detected"]
            ),
            debunk_summary_en="This announcement is authentic. The message points to the official government domain (cbse.gov.in), includes valid administrative circular references, and contains no alarmist rhetoric or coercive sharing demands.",
            debunk_summary_hi="यह सूचना पूरी तरह प्रामाणिक और आधिकारिक है। संदेश में आधिकारिक सरकारी डोमेन (cbse.gov.in) का संदर्भ और औपचारिक प्रशासनिक भाषा का उपयोग किया गया है। इसमें किसी भी तरह की सनसनी या फर्जीवाड़ा नहीं है।",
            verification_checklist=[
                "Confirm that links point strictly to official .gov.in or .nic.in domains.",
                "Note the presence of administrative circular identifiers.",
                "Observe the calm, informative tone devoid of 'URGENT FORWARD' demands."
            ],
            shareable_card=ShareableDebunkCard(
                headline_en="✅ VERIFIED AUTHENTIC: Official CBSE Notification",
                headline_hi="✅ सत्यापित प्रामाणिक: सीबीएसई (CBSE) की आधिकारिक सूचना",
                verdict="AUTHENTIC / TRUE",
                bullet_points_en=[
                    "Information verified directly against official cbse.gov.in records.",
                    "Always download examination datesheets directly from cbse.gov.in."
                ],
                bullet_points_hi=[
                    "यह सूचना सीबीएसई की आधिकारिक वेबसाइट cbse.gov.in से सत्यापित है।",
                    "छात्र केवल आधिकारिक वेबसाइट से ही टाइमटेबल डाउनलोड करें।"
                ],
                whatsapp_format_text_en="✅ *SATYA SETU VERIFICATION: OFFICIAL NOTIFICATION* ✅\n\n📌 *Subject:* CBSE Board Examination Date Sheet\n\n🔗 *Status:* AUTHENTIC & VERIFIED. Official circular available on cbse.gov.in.\n\n🛡️ *Verified via SatyaSetu AI*",
                whatsapp_format_text_hi="✅ *सत्यसेतु सत्यापन: आधिकारिक सूचना* ✅\n\n📌 *विषय:* सीबीएसई बोर्ड परीक्षा टाइमटेबल\n\n🔗 *स्थिति:* सत्यापित एवं प्रामाणिक। आधिकारिक सर्कुलर cbse.gov.in पर उपलब्ध।\n\n🛡️ *सत्यसेतु (SatyaSetu)*",
                verification_source_tag="Verified via Official Government Portal (cbse.gov.in)"
            ),
            pipeline_steps=[
                PipelineStep(name="Input Sanitization & OCR", status="done", detail="Processed official circular statement", elapsed_ms=30),
                PipelineStep(name="Atomic Claim Deconstruction", status="done", detail="Extracted institution and circular reference", elapsed_ms=80),
                PipelineStep(name="Official Domain Authentication", status="done", detail="Domain cbse.gov.in verified as authentic NIC domain", elapsed_ms=120),
                PipelineStep(name="Manipulation & Urgency Analysis", status="done", detail="Determined formal neutral tone with zero emotional coercion", elapsed_ms=25),
                PipelineStep(name="Bilingual Counter-Debunk Synthesis", status="done", detail="Generated green verification badge and student guidance card", elapsed_ms=75)
            ],
            total_latency_ms=330,
            data_source_mode="Official Government Domain Cross-Reference"
        )
    }
}
