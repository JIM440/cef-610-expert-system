--
-- PostgreSQL database dump
--

\restrict xXcy2UM1NYE3XdELzUaeb7N1fdznHwk9zHRq7D48NhLoYcc5IgLGZeSwfB3CDel

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: app_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.app_user (
    id integer NOT NULL,
    username character varying(80),
    password_hash character varying(256),
    full_name character varying(150),
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    role character varying(10) DEFAULT 'FARMER'::character varying NOT NULL,
    phone_number character varying(20),
    location character varying(100),
    email character varying(100),
    updated_at timestamp without time zone,
    CONSTRAINT app_user_role_check CHECK (((role)::text = ANY ((ARRAY['ADMIN'::character varying, 'EXPERT'::character varying, 'FARMER'::character varying])::text[]))),
    CONSTRAINT chk_admin_has_login CHECK ((((role)::text <> 'ADMIN'::text) OR ((username IS NOT NULL) AND (password_hash IS NOT NULL))))
);


--
-- Name: app_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.app_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: app_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.app_user_id_seq OWNED BY public.app_user.id;


--
-- Name: consultation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultation (
    id integer NOT NULL,
    farmer_id integer,
    crop_id integer NOT NULL,
    final_disease_id integer,
    final_confidence integer,
    consultation_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    performed_by_user_id integer NOT NULL,
    consultation_type character varying(50) NOT NULL,
    source character varying(20) DEFAULT 'SYMPTOMS'::character varying NOT NULL,
    gemini_raw_extraction text,
    match_tier character varying(20) DEFAULT 'HIGH'::character varying NOT NULL,
    matched_rule_id integer,
    explanation text,
    CONSTRAINT consultation_confidence_score_check CHECK (((final_confidence >= 0) AND (final_confidence <= 100))),
    CONSTRAINT consultation_match_tier_check CHECK (((match_tier)::text = ANY ((ARRAY['HIGH'::character varying, 'LOW'::character varying, 'NONE'::character varying])::text[]))),
    CONSTRAINT consultation_source_check CHECK (((source)::text = ANY ((ARRAY['SYMPTOMS'::character varying, 'IMAGE'::character varying])::text[]))),
    CONSTRAINT consultation_type_check CHECK (((consultation_type)::text = ANY ((ARRAY['FARMER_SELF'::character varying, 'ADMIN_FOR_FARMER'::character varying, 'ADMIN_GENERAL'::character varying, 'IMAGE_FARMER_SELF'::character varying, 'IMAGE_ADMIN_FOR_FARMER'::character varying, 'IMAGE_ADMIN_GENERAL'::character varying])::text[])))
);


--
-- Name: consultation_environment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultation_environment (
    id integer NOT NULL,
    consultation_id integer NOT NULL,
    environmental_factor_id integer CONSTRAINT consultation_environment_condition_value_id_not_null NOT NULL,
    matched boolean DEFAULT false NOT NULL
);


--
-- Name: consultation_environment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultation_environment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consultation_environment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultation_environment_id_seq OWNED BY public.consultation_environment.id;


--
-- Name: consultation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consultation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultation_id_seq OWNED BY public.consultation.id;


--
-- Name: consultation_symptom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultation_symptom (
    id integer NOT NULL,
    consultation_id integer NOT NULL,
    symptom_id integer NOT NULL,
    matched boolean DEFAULT false NOT NULL
);


--
-- Name: consultation_symptom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultation_symptom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consultation_symptom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultation_symptom_id_seq OWNED BY public.consultation_symptom.id;


--
-- Name: consultation_treatment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.consultation_treatment (
    id integer NOT NULL,
    consultation_id integer NOT NULL,
    treatment_id integer NOT NULL
);


--
-- Name: consultation_treatment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.consultation_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: consultation_treatment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.consultation_treatment_id_seq OWNED BY public.consultation_treatment.id;


--
-- Name: crop; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.crop (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text
);


--
-- Name: crop_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.crop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: crop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.crop_id_seq OWNED BY public.crop.id;


--
-- Name: disease; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.disease (
    id integer NOT NULL,
    crop_id integer NOT NULL,
    name character varying(150) NOT NULL,
    description text,
    explanation_template text
);


--
-- Name: disease_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.disease_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: disease_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.disease_id_seq OWNED BY public.disease.id;


--
-- Name: disease_symptom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.disease_symptom (
    id integer NOT NULL,
    disease_id integer NOT NULL,
    symptom_id integer NOT NULL,
    weight integer DEFAULT 1 NOT NULL,
    CONSTRAINT disease_symptom_weight_check CHECK (((weight >= 1) AND (weight <= 10)))
);


--
-- Name: disease_symptom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.disease_symptom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: disease_symptom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.disease_symptom_id_seq OWNED BY public.disease_symptom.id;


--
-- Name: environmental_factor; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.environmental_factor (
    id integer NOT NULL,
    category character varying(30) NOT NULL,
    value_name character varying(100) NOT NULL,
    unit character varying(20)
);


--
-- Name: environmental_factor_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.environmental_factor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: environmental_factor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.environmental_factor_id_seq OWNED BY public.environmental_factor.id;


--
-- Name: rule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rule (
    id integer NOT NULL,
    disease_id integer NOT NULL,
    rule_name character varying(150) NOT NULL,
    confidence_score integer DEFAULT 70 NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    CONSTRAINT rule_confidence_score_check CHECK (((confidence_score >= 0) AND (confidence_score <= 100)))
);


--
-- Name: rule_environment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rule_environment (
    id integer NOT NULL,
    rule_id integer NOT NULL,
    environmental_factor_id integer CONSTRAINT rule_environment_condition_value_id_not_null NOT NULL,
    is_required boolean DEFAULT true NOT NULL
);


--
-- Name: rule_environment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rule_environment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rule_environment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rule_environment_id_seq OWNED BY public.rule_environment.id;


--
-- Name: rule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rule_id_seq OWNED BY public.rule.id;


--
-- Name: rule_symptom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rule_symptom (
    id integer NOT NULL,
    rule_id integer NOT NULL,
    symptom_id integer NOT NULL,
    is_required boolean DEFAULT true NOT NULL
);


--
-- Name: rule_symptom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rule_symptom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rule_symptom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rule_symptom_id_seq OWNED BY public.rule_symptom.id;


--
-- Name: rule_treatment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rule_treatment (
    id integer NOT NULL,
    rule_id integer NOT NULL,
    treatment_id integer NOT NULL,
    priority_level integer DEFAULT 1 NOT NULL,
    CONSTRAINT rule_treatment_priority_level_check CHECK (((priority_level >= 1) AND (priority_level <= 5)))
);


--
-- Name: rule_treatment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rule_treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rule_treatment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rule_treatment_id_seq OWNED BY public.rule_treatment.id;


--
-- Name: symptom; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.symptom (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    description text
);


--
-- Name: symptom_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.symptom_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: symptom_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.symptom_id_seq OWNED BY public.symptom.id;


--
-- Name: treatment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.treatment (
    id integer NOT NULL,
    name character varying(150) NOT NULL,
    description text
);


--
-- Name: treatment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.treatment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: treatment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.treatment_id_seq OWNED BY public.treatment.id;


--
-- Name: app_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.app_user ALTER COLUMN id SET DEFAULT nextval('public.app_user_id_seq'::regclass);


--
-- Name: consultation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation ALTER COLUMN id SET DEFAULT nextval('public.consultation_id_seq'::regclass);


--
-- Name: consultation_environment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_environment ALTER COLUMN id SET DEFAULT nextval('public.consultation_environment_id_seq'::regclass);


--
-- Name: consultation_symptom id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_symptom ALTER COLUMN id SET DEFAULT nextval('public.consultation_symptom_id_seq'::regclass);


--
-- Name: consultation_treatment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_treatment ALTER COLUMN id SET DEFAULT nextval('public.consultation_treatment_id_seq'::regclass);


--
-- Name: crop id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crop ALTER COLUMN id SET DEFAULT nextval('public.crop_id_seq'::regclass);


--
-- Name: disease id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease ALTER COLUMN id SET DEFAULT nextval('public.disease_id_seq'::regclass);


--
-- Name: disease_symptom id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease_symptom ALTER COLUMN id SET DEFAULT nextval('public.disease_symptom_id_seq'::regclass);


--
-- Name: environmental_factor id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environmental_factor ALTER COLUMN id SET DEFAULT nextval('public.environmental_factor_id_seq'::regclass);


--
-- Name: rule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule ALTER COLUMN id SET DEFAULT nextval('public.rule_id_seq'::regclass);


--
-- Name: rule_environment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_environment ALTER COLUMN id SET DEFAULT nextval('public.rule_environment_id_seq'::regclass);


--
-- Name: rule_symptom id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_symptom ALTER COLUMN id SET DEFAULT nextval('public.rule_symptom_id_seq'::regclass);


--
-- Name: rule_treatment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_treatment ALTER COLUMN id SET DEFAULT nextval('public.rule_treatment_id_seq'::regclass);


--
-- Name: symptom id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.symptom ALTER COLUMN id SET DEFAULT nextval('public.symptom_id_seq'::regclass);


--
-- Name: treatment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.treatment ALTER COLUMN id SET DEFAULT nextval('public.treatment_id_seq'::regclass);


--
-- Name: app_user app_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.app_user
    ADD CONSTRAINT app_user_pkey PRIMARY KEY (id);


--
-- Name: app_user app_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.app_user
    ADD CONSTRAINT app_user_username_key UNIQUE (username);


--
-- Name: consultation_environment consultation_environment_consultation_factor_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_environment
    ADD CONSTRAINT consultation_environment_consultation_factor_key UNIQUE (consultation_id, environmental_factor_id);


--
-- Name: consultation_environment consultation_environment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_environment
    ADD CONSTRAINT consultation_environment_pkey PRIMARY KEY (id);


--
-- Name: consultation consultation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation
    ADD CONSTRAINT consultation_pkey PRIMARY KEY (id);


--
-- Name: consultation_symptom consultation_symptom_consultation_id_symptom_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_symptom
    ADD CONSTRAINT consultation_symptom_consultation_id_symptom_id_key UNIQUE (consultation_id, symptom_id);


--
-- Name: consultation_symptom consultation_symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_symptom
    ADD CONSTRAINT consultation_symptom_pkey PRIMARY KEY (id);


--
-- Name: consultation_treatment consultation_treatment_consultation_id_treatment_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_treatment
    ADD CONSTRAINT consultation_treatment_consultation_id_treatment_id_key UNIQUE (consultation_id, treatment_id);


--
-- Name: consultation_treatment consultation_treatment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_treatment
    ADD CONSTRAINT consultation_treatment_pkey PRIMARY KEY (id);


--
-- Name: crop crop_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crop
    ADD CONSTRAINT crop_name_key UNIQUE (name);


--
-- Name: crop crop_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.crop
    ADD CONSTRAINT crop_pkey PRIMARY KEY (id);


--
-- Name: disease disease_crop_id_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_crop_id_name_key UNIQUE (crop_id, name);


--
-- Name: disease disease_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_pkey PRIMARY KEY (id);


--
-- Name: disease_symptom disease_symptom_disease_id_symptom_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease_symptom
    ADD CONSTRAINT disease_symptom_disease_id_symptom_id_key UNIQUE (disease_id, symptom_id);


--
-- Name: disease_symptom disease_symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease_symptom
    ADD CONSTRAINT disease_symptom_pkey PRIMARY KEY (id);


--
-- Name: environmental_factor environmental_factor_category_value_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environmental_factor
    ADD CONSTRAINT environmental_factor_category_value_name_key UNIQUE (category, value_name);


--
-- Name: environmental_factor environmental_factor_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.environmental_factor
    ADD CONSTRAINT environmental_factor_pkey PRIMARY KEY (id);


--
-- Name: rule rule_disease_id_rule_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule
    ADD CONSTRAINT rule_disease_id_rule_name_key UNIQUE (disease_id, rule_name);


--
-- Name: rule_environment rule_environment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_environment
    ADD CONSTRAINT rule_environment_pkey PRIMARY KEY (id);


--
-- Name: rule_environment rule_environment_rule_factor_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_environment
    ADD CONSTRAINT rule_environment_rule_factor_key UNIQUE (rule_id, environmental_factor_id);


--
-- Name: rule rule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule
    ADD CONSTRAINT rule_pkey PRIMARY KEY (id);


--
-- Name: rule_symptom rule_symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_symptom
    ADD CONSTRAINT rule_symptom_pkey PRIMARY KEY (id);


--
-- Name: rule_symptom rule_symptom_rule_id_symptom_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_symptom
    ADD CONSTRAINT rule_symptom_rule_id_symptom_id_key UNIQUE (rule_id, symptom_id);


--
-- Name: rule_treatment rule_treatment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_treatment
    ADD CONSTRAINT rule_treatment_pkey PRIMARY KEY (id);


--
-- Name: rule_treatment rule_treatment_rule_id_treatment_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_treatment
    ADD CONSTRAINT rule_treatment_rule_id_treatment_id_key UNIQUE (rule_id, treatment_id);


--
-- Name: symptom symptom_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.symptom
    ADD CONSTRAINT symptom_name_key UNIQUE (name);


--
-- Name: symptom symptom_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.symptom
    ADD CONSTRAINT symptom_pkey PRIMARY KEY (id);


--
-- Name: treatment treatment_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.treatment
    ADD CONSTRAINT treatment_name_key UNIQUE (name);


--
-- Name: treatment treatment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.treatment
    ADD CONSTRAINT treatment_pkey PRIMARY KEY (id);


--
-- Name: consultation consultation_crop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation
    ADD CONSTRAINT consultation_crop_id_fkey FOREIGN KEY (crop_id) REFERENCES public.crop(id);


--
-- Name: consultation consultation_diagnosis_disease_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation
    ADD CONSTRAINT consultation_diagnosis_disease_id_fkey FOREIGN KEY (final_disease_id) REFERENCES public.disease(id);


--
-- Name: consultation_environment consultation_environment_consultation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_environment
    ADD CONSTRAINT consultation_environment_consultation_id_fkey FOREIGN KEY (consultation_id) REFERENCES public.consultation(id) ON DELETE CASCADE;


--
-- Name: consultation_environment consultation_environment_environmental_factor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_environment
    ADD CONSTRAINT consultation_environment_environmental_factor_id_fkey FOREIGN KEY (environmental_factor_id) REFERENCES public.environmental_factor(id);


--
-- Name: consultation consultation_farmer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation
    ADD CONSTRAINT consultation_farmer_id_fkey FOREIGN KEY (farmer_id) REFERENCES public.app_user(id) ON DELETE SET NULL;


--
-- Name: consultation consultation_matched_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation
    ADD CONSTRAINT consultation_matched_rule_id_fkey FOREIGN KEY (matched_rule_id) REFERENCES public.rule(id) ON DELETE SET NULL;


--
-- Name: consultation consultation_performed_by_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation
    ADD CONSTRAINT consultation_performed_by_user_id_fkey FOREIGN KEY (performed_by_user_id) REFERENCES public.app_user(id);


--
-- Name: consultation_symptom consultation_symptom_consultation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_symptom
    ADD CONSTRAINT consultation_symptom_consultation_id_fkey FOREIGN KEY (consultation_id) REFERENCES public.consultation(id) ON DELETE CASCADE;


--
-- Name: consultation_symptom consultation_symptom_symptom_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_symptom
    ADD CONSTRAINT consultation_symptom_symptom_id_fkey FOREIGN KEY (symptom_id) REFERENCES public.symptom(id);


--
-- Name: consultation_treatment consultation_treatment_consultation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_treatment
    ADD CONSTRAINT consultation_treatment_consultation_id_fkey FOREIGN KEY (consultation_id) REFERENCES public.consultation(id) ON DELETE CASCADE;


--
-- Name: consultation_treatment consultation_treatment_treatment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.consultation_treatment
    ADD CONSTRAINT consultation_treatment_treatment_id_fkey FOREIGN KEY (treatment_id) REFERENCES public.treatment(id);


--
-- Name: disease disease_crop_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease
    ADD CONSTRAINT disease_crop_id_fkey FOREIGN KEY (crop_id) REFERENCES public.crop(id) ON DELETE CASCADE;


--
-- Name: disease_symptom disease_symptom_disease_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease_symptom
    ADD CONSTRAINT disease_symptom_disease_id_fkey FOREIGN KEY (disease_id) REFERENCES public.disease(id) ON DELETE CASCADE;


--
-- Name: disease_symptom disease_symptom_symptom_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disease_symptom
    ADD CONSTRAINT disease_symptom_symptom_id_fkey FOREIGN KEY (symptom_id) REFERENCES public.symptom(id) ON DELETE CASCADE;


--
-- Name: rule rule_disease_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule
    ADD CONSTRAINT rule_disease_id_fkey FOREIGN KEY (disease_id) REFERENCES public.disease(id) ON DELETE CASCADE;


--
-- Name: rule_environment rule_environment_environmental_factor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_environment
    ADD CONSTRAINT rule_environment_environmental_factor_id_fkey FOREIGN KEY (environmental_factor_id) REFERENCES public.environmental_factor(id) ON DELETE CASCADE;


--
-- Name: rule_environment rule_environment_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_environment
    ADD CONSTRAINT rule_environment_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.rule(id) ON DELETE CASCADE;


--
-- Name: rule_symptom rule_symptom_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_symptom
    ADD CONSTRAINT rule_symptom_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.rule(id) ON DELETE CASCADE;


--
-- Name: rule_symptom rule_symptom_symptom_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_symptom
    ADD CONSTRAINT rule_symptom_symptom_id_fkey FOREIGN KEY (symptom_id) REFERENCES public.symptom(id) ON DELETE CASCADE;


--
-- Name: rule_treatment rule_treatment_rule_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_treatment
    ADD CONSTRAINT rule_treatment_rule_id_fkey FOREIGN KEY (rule_id) REFERENCES public.rule(id) ON DELETE CASCADE;


--
-- Name: rule_treatment rule_treatment_treatment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rule_treatment
    ADD CONSTRAINT rule_treatment_treatment_id_fkey FOREIGN KEY (treatment_id) REFERENCES public.treatment(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict xXcy2UM1NYE3XdELzUaeb7N1fdznHwk9zHRq7D48NhLoYcc5IgLGZeSwfB3CDel
