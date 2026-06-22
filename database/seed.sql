--
-- PostgreSQL database dump
--

\restrict nXc02wO0D184NVxNpxnDuPhprqBLhZgILzSBCkNYhkYv7VI62jGntEiGAm8uXGw

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: app_user; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.app_user (id, username, password_hash, full_name, is_active, created_at, role, phone_number, location, email, updated_at) VALUES (1, 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'System Admin', true, '2026-06-08 09:38:54.61058', 'ADMIN', NULL, NULL, NULL, '2026-06-22 12:21:31.842336');
INSERT INTO public.app_user (id, username, password_hash, full_name, is_active, created_at, role, phone_number, location, email, updated_at) VALUES (3, 'expert', '34a6c1a9600377c8dc05ea00380f406fb52e8104e921dc6bd5869bfdf1516164', 'Crop Expert', true, '2026-06-08 11:29:25.002776', 'EXPERT', NULL, NULL, NULL, '2026-06-22 12:21:31.842336');
INSERT INTO public.app_user (id, username, password_hash, full_name, is_active, created_at, role, phone_number, location, email, updated_at) VALUES (4, 'jim', 'b148f9352a4521ff41accc5ff7d81f765523967e6e3db875183dce3041085184', 'Takem Jim', true, '2026-06-09 13:12:18.078544', 'FARMER', '', 'bafanghihei', '', '2026-06-09 13:12:17.961759');
INSERT INTO public.app_user (id, username, password_hash, full_name, is_active, created_at, role, phone_number, location, email, updated_at) VALUES (2, 'farmer1', '26c07fc7be1668f8ea7e3801d4ffdbf33de487a593a69028936ec49f2c89f6ab', 'Demo Farmer', true, '2026-06-08 09:38:54.613659', 'FARMER', '670000000', 'Buea', 'farmer@demo.local', '2026-06-08 09:38:54.606799');


--
-- Data for Name: crop; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.crop (id, name, description) VALUES (1, 'Tomato', 'Solanum lycopersicum — primary crop for this expert system demo.');


--
-- Data for Name: disease; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (1, 1, 'Early Blight', 'Fungal disease caused by Alternaria solani affecting leaves and fruit.', 'Early Blight is likely because brown leaf spots, yellowing, and warm humid conditions match known Alternaria patterns.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (2, 1, 'Late Blight', 'Destructive oomycete disease (Phytophthora infestans) spreading rapidly in cool wet weather.', 'Late Blight is likely because water-soaked lesions and high rainfall with cool temperatures favor Phytophthora infestans.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (3, 1, 'Septoria Leaf Spot', 'Fungal leaf spot disease with small circular lesions and dark borders.', 'Septoria Leaf Spot is likely because brown spots with yellowing on lower leaves appear under moderate humidity.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (4, 1, 'Powdery Mildew', 'Fungal disease producing white powdery patches on leaves.', 'Powdery Mildew is likely because white powdery coating on leaves occurs in warm dry conditions with dense planting.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (5, 1, 'Bacterial Spot', 'Bacterial disease causing dark lesions on leaves and fruit.', 'Bacterial Spot is likely because dark greasy lesions spread during warm wet periods with overhead watering.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (6, 1, 'Tomato Mosaic Virus', 'Viral disease causing mosaic patterns and stunted growth.', 'Tomato Mosaic Virus is likely because mosaic discoloration and stunting indicate viral infection.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (7, 1, 'Fusarium Wilt', 'Soil-borne fungal wilt affecting vascular tissue.', 'Fusarium Wilt is likely because wilting with yellowing progresses despite adequate moisture in warm soil.');
INSERT INTO public.disease (id, crop_id, name, description, explanation_template) VALUES (8, 1, 'Blossom End Rot', 'Physiological disorder linked to calcium transport and uneven watering.', 'Blossom End Rot is likely because fruit bottom rot appears with fluctuating soil moisture and calcium stress.');


--
-- Data for Name: rule; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (1, 1, 'EB-Rule-02: Brown spots + warm temperature', 75, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (2, 1, 'EB-Rule-01: Brown spots + yellowing + high humidity', 85, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (3, 2, 'LB-Rule-02: Wilting + cool temperature + high humidity', 88, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (4, 2, 'LB-Rule-01: Water-soaked lesions + high rainfall', 90, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (5, 3, 'SLS-Rule-01: Brown spots + yellowing + moderate humidity', 80, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (6, 4, 'PM-Rule-02: White coating + warm temperature', 78, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (7, 4, 'PM-Rule-01: White coating + dense spacing', 82, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (8, 5, 'BS-Rule-01: Dark lesions + warm + high rainfall', 83, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (9, 6, 'TMV-Rule-01: Mosaic pattern + stunted growth', 86, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (10, 7, 'FW-Rule-01: Wilting + yellowing + warm soil', 84, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (11, 8, 'BER-Rule-02: Fruit rot + waterlogged soil', 76, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (12, 8, 'BER-Rule-01: Fruit rot + dry soil moisture', 80, true);
INSERT INTO public.rule (id, disease_id, rule_name, confidence_score, is_active) VALUES (13, 5, 'XEF', 75, true);


--
-- Data for Name: consultation; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.consultation (id, farmer_id, crop_id, final_disease_id, final_confidence, consultation_date, performed_by_user_id, consultation_type, source, gemini_raw_extraction, match_tier, matched_rule_id, explanation) VALUES (1, NULL, 1, 6, 86, '2026-06-08 09:49:27.528312', 1, 'ADMIN_GENERAL', 'SYMPTOMS', NULL, 'HIGH', 9, 'Tomato Mosaic Virus is likely because mosaic discoloration and stunting indicate viral infection.');
INSERT INTO public.consultation (id, farmer_id, crop_id, final_disease_id, final_confidence, consultation_date, performed_by_user_id, consultation_type, source, gemini_raw_extraction, match_tier, matched_rule_id, explanation) VALUES (3, NULL, 1, 6, 86, '2026-06-08 12:16:10.781062', 3, 'ADMIN_GENERAL', 'SYMPTOMS', NULL, 'HIGH', 9, 'Tomato Mosaic Virus is likely because mosaic discoloration and stunting indicate viral infection.');
INSERT INTO public.consultation (id, farmer_id, crop_id, final_disease_id, final_confidence, consultation_date, performed_by_user_id, consultation_type, source, gemini_raw_extraction, match_tier, matched_rule_id, explanation) VALUES (2, 2, 1, 6, 86, '2026-06-08 11:53:12.809803', 2, 'FARMER_SELF', 'SYMPTOMS', NULL, 'HIGH', 9, 'Tomato Mosaic Virus is likely because mosaic discoloration and stunting indicate viral infection.');
INSERT INTO public.consultation (id, farmer_id, crop_id, final_disease_id, final_confidence, consultation_date, performed_by_user_id, consultation_type, source, gemini_raw_extraction, match_tier, matched_rule_id, explanation) VALUES (4, 4, 1, 6, 86, '2026-06-09 13:13:20.754621', 4, 'FARMER_SELF', 'SYMPTOMS', NULL, 'HIGH', 9, 'Tomato Mosaic Virus is likely because mosaic discoloration and stunting indicate viral infection.');


--
-- Data for Name: environmental_factor; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (1, 'Humidity', 'High', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (2, 'Humidity', 'Moderate', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (3, 'Humidity', 'Low', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (4, 'Temperature', 'Hot', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (5, 'Temperature', 'Warm', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (6, 'Temperature', 'Cool', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (7, 'Rainfall', 'High', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (8, 'Rainfall', 'Moderate', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (9, 'Rainfall', 'Low', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (10, 'Soil moisture', 'Waterlogged', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (11, 'Soil moisture', 'Adequate', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (12, 'Soil moisture', 'Dry', 'level');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (13, 'Plant spacing', 'Wide', 'density');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (14, 'Plant spacing', 'Normal', 'density');
INSERT INTO public.environmental_factor (id, category, value_name, unit) VALUES (15, 'Plant spacing', 'Dense', 'density');


--
-- Data for Name: consultation_environment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.consultation_environment (id, consultation_id, environmental_factor_id, matched) VALUES (1, 1, 3, false);
INSERT INTO public.consultation_environment (id, consultation_id, environmental_factor_id, matched) VALUES (2, 1, 15, false);
INSERT INTO public.consultation_environment (id, consultation_id, environmental_factor_id, matched) VALUES (3, 1, 8, false);
INSERT INTO public.consultation_environment (id, consultation_id, environmental_factor_id, matched) VALUES (4, 1, 12, false);
INSERT INTO public.consultation_environment (id, consultation_id, environmental_factor_id, matched) VALUES (5, 1, 6, false);


--
-- Data for Name: symptom; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.symptom (id, name, description) VALUES (1, 'Brown spots on leaves', 'Circular to irregular brown lesions on foliage');
INSERT INTO public.symptom (id, name, description) VALUES (2, 'Yellowing leaves', 'Chlorosis starting from lower or older leaves');
INSERT INTO public.symptom (id, name, description) VALUES (3, 'Wilting leaves', 'Leaves droop despite adequate soil moisture');
INSERT INTO public.symptom (id, name, description) VALUES (4, 'White powdery coating', 'Powdery white fungal growth on leaf surfaces');
INSERT INTO public.symptom (id, name, description) VALUES (5, 'Dark water-soaked lesions', 'Dark, greasy-looking spots that spread rapidly');
INSERT INTO public.symptom (id, name, description) VALUES (6, 'Leaf curling', 'Upward or downward curling of leaf margins');
INSERT INTO public.symptom (id, name, description) VALUES (7, 'Stunted growth', 'Reduced plant height and fruit development');
INSERT INTO public.symptom (id, name, description) VALUES (8, 'Fruit rot at blossom end', 'Dark sunken area at the bottom of fruit');
INSERT INTO public.symptom (id, name, description) VALUES (9, 'Mosaic leaf pattern', 'Mottled light and dark green leaf discoloration');
INSERT INTO public.symptom (id, name, description) VALUES (10, 'Stem cankers', 'Sunken lesions on stems and petioles');
INSERT INTO public.symptom (id, name, description) VALUES (11, 'Leaf drop', 'Premature shedding of lower leaves');
INSERT INTO public.symptom (id, name, description) VALUES (12, 'Purple leaf veins', 'Purplish discoloration along leaf veins');


--
-- Data for Name: consultation_symptom; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (1, 1, 8, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (2, 1, 5, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (7, 3, 1, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (8, 3, 5, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (9, 3, 8, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (10, 3, 6, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (11, 3, 11, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (13, 3, 12, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (14, 3, 10, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (16, 3, 4, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (17, 3, 3, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (18, 3, 2, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (19, 4, 1, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (20, 4, 5, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (21, 4, 8, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (22, 4, 6, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (23, 4, 11, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (25, 4, 12, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (26, 4, 10, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (28, 4, 4, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (29, 4, 3, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (30, 4, 2, false);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (3, 1, 9, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (4, 1, 7, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (5, 2, 7, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (6, 2, 9, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (12, 3, 9, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (15, 3, 7, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (24, 4, 9, true);
INSERT INTO public.consultation_symptom (id, consultation_id, symptom_id, matched) VALUES (27, 4, 7, true);


--
-- Data for Name: treatment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.treatment (id, name, description) VALUES (1, 'Remove infected leaves', 'Prune and destroy affected foliage to reduce pathogen spread');
INSERT INTO public.treatment (id, name, description) VALUES (2, 'Apply copper-based fungicide', 'Spray approved copper fungicide per label instructions');
INSERT INTO public.treatment (id, name, description) VALUES (3, 'Apply chlorothalonil fungicide', 'Broad-spectrum fungicide for fungal leaf diseases');
INSERT INTO public.treatment (id, name, description) VALUES (4, 'Improve plant spacing', 'Increase airflow by thinning or wider row spacing');
INSERT INTO public.treatment (id, name, description) VALUES (5, 'Reduce overhead irrigation', 'Water at soil level to keep foliage dry');
INSERT INTO public.treatment (id, name, description) VALUES (6, 'Apply calcium foliar spray', 'Supplement calcium to reduce blossom end rot risk');
INSERT INTO public.treatment (id, name, description) VALUES (7, 'Soil drench with approved fungicide', 'Target root-zone pathogens with labeled product');
INSERT INTO public.treatment (id, name, description) VALUES (8, 'Use disease-resistant varieties', 'Plant cultivars with known resistance genes');
INSERT INTO public.treatment (id, name, description) VALUES (9, 'Sanitize tools and stakes', 'Disinfect equipment between plants');
INSERT INTO public.treatment (id, name, description) VALUES (10, 'Isolate infected plants', 'Separate symptomatic plants to limit spread');


--
-- Data for Name: consultation_treatment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (1, 1, 1);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (2, 1, 10);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (3, 2, 1);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (4, 2, 10);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (5, 3, 1);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (6, 3, 10);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (7, 4, 1);
INSERT INTO public.consultation_treatment (id, consultation_id, treatment_id) VALUES (8, 4, 10);


--
-- Data for Name: disease_symptom; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (1, 3, 1, 3);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (2, 1, 1, 3);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (3, 7, 2, 3);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (4, 5, 2, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (5, 3, 2, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (6, 1, 2, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (7, 7, 3, 4);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (8, 2, 3, 3);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (9, 4, 4, 4);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (10, 5, 5, 3);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (11, 2, 5, 4);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (12, 6, 6, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (13, 4, 6, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (14, 8, 7, 1);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (15, 6, 7, 3);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (16, 4, 7, 1);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (17, 8, 8, 4);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (18, 6, 9, 4);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (19, 2, 10, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (20, 5, 11, 1);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (21, 3, 11, 1);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (22, 1, 11, 2);
INSERT INTO public.disease_symptom (id, disease_id, symptom_id, weight) VALUES (23, 7, 12, 2);


--
-- Data for Name: rule_environment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (1, 5, 2, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (2, 3, 1, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (3, 2, 1, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (4, 10, 5, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (5, 8, 5, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (6, 6, 5, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (7, 3, 6, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (8, 1, 5, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (9, 8, 7, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (10, 4, 7, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (11, 11, 10, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (12, 12, 12, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (13, 7, 15, true);
INSERT INTO public.rule_environment (id, rule_id, environmental_factor_id, is_required) VALUES (14, 13, 2, true);


--
-- Data for Name: rule_symptom; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (1, 1, 1, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (2, 2, 2, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (3, 2, 1, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (4, 3, 5, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (5, 3, 3, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (6, 4, 5, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (7, 5, 2, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (8, 5, 1, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (9, 6, 4, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (10, 7, 4, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (11, 8, 5, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (12, 9, 9, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (13, 9, 7, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (14, 10, 3, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (15, 10, 2, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (16, 11, 8, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (17, 12, 8, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (18, 13, 2, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (19, 13, 3, true);
INSERT INTO public.rule_symptom (id, rule_id, symptom_id, is_required) VALUES (20, 13, 4, true);


--
-- Data for Name: rule_treatment; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (1, 2, 4, 3);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (2, 2, 3, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (3, 2, 1, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (4, 4, 10, 3);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (5, 4, 2, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (6, 4, 1, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (7, 5, 3, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (8, 5, 1, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (9, 7, 4, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (10, 7, 3, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (11, 8, 5, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (12, 8, 2, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (13, 9, 10, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (14, 9, 1, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (15, 10, 8, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (16, 10, 7, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (17, 12, 6, 1);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (18, 12, 5, 2);
INSERT INTO public.rule_treatment (id, rule_id, treatment_id, priority_level) VALUES (19, 13, 8, 1);


--
-- Name: app_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.app_user_id_seq', 5, true);


--
-- Name: consultation_environment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consultation_environment_id_seq', 5, true);


--
-- Name: consultation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consultation_id_seq', 4, true);


--
-- Name: consultation_symptom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consultation_symptom_id_seq', 30, true);


--
-- Name: consultation_treatment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.consultation_treatment_id_seq', 8, true);


--
-- Name: crop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.crop_id_seq', 1, true);


--
-- Name: disease_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.disease_id_seq', 8, true);


--
-- Name: disease_symptom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.disease_symptom_id_seq', 23, true);


--
-- Name: environmental_factor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.environmental_factor_id_seq', 15, true);


--
-- Name: rule_environment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rule_environment_id_seq', 14, true);


--
-- Name: rule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rule_id_seq', 13, true);


--
-- Name: rule_symptom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rule_symptom_id_seq', 20, true);


--
-- Name: rule_treatment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.rule_treatment_id_seq', 19, true);


--
-- Name: symptom_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.symptom_id_seq', 12, true);


--
-- Name: treatment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.treatment_id_seq', 10, true);


--
-- PostgreSQL database dump complete
--

\unrestrict nXc02wO0D184NVxNpxnDuPhprqBLhZgILzSBCkNYhkYv7VI62jGntEiGAm8uXGw

