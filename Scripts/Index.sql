-- Table: public.index

-- DROP TABLE IF EXISTS public.index;

CREATE TABLE IF NOT EXISTS public.index
(
    doc_number integer NOT NULL,
    term text COLLATE pg_catalog."default" NOT NULL,
    count integer NOT NULL,
    CONSTRAINT index_pkey PRIMARY KEY (doc_number, term),
    CONSTRAINT index_doc_number_fkey FOREIGN KEY (doc_number)
        REFERENCES public.documents (doc_number) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT index_term_fkey FOREIGN KEY (term)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.index
    OWNER to postgres;