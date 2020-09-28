-- Table: public.users

-- DROP TABLE public.users;
CREATE SEQUENCE users_id_seq INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
GRANT ALL ON sequence public.users_id_seq TO ctudosestroe;


CREATE TABLE public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass) ,
    email_address character varying(100) COLLATE pg_catalog."default",
    last_name character varying(50) COLLATE pg_catalog."default",
    first_name character varying(50) COLLATE pg_catalog."default",
    skill_level integer,
    modified_at timestamp(6) without time zone NOT NULL DEFAULT timezone('UTC'::text, clock_timestamp()),
    created_at timestamp without time zone NOT NULL DEFAULT timezone('UTC'::text, clock_timestamp()),
    CONSTRAINT users_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.users
    OWNER to postgres;

GRANT ALL ON TABLE public.users TO ctudosestroe;

GRANT ALL ON TABLE public.users TO postgres;

-- Index: users_lower_idx

-- DROP INDEX public.users_lower_idx;

CREATE UNIQUE INDEX users_lower_idx
    ON public.users USING btree
    (lower(email_address::text) COLLATE pg_catalog."default")
    TABLESPACE pg_default;

-- Trigger: users_table

-- DROP TRIGGER users_table ON public.users;
CREATE OR REPLACE FUNCTION modified_at_changes()
  RETURNS TRIGGER 
  LANGUAGE PLPGSQL  
  AS
$$
BEGIN
	IF NEW.MODIFIED_AT = OLD.MODIFIED_AT THEN
		--UPDATE GAMES
		--SET MODIFIED_AT =  now() at time zone 'utc'
		--where id = NEW.id;
		NEW.MODIFIED_AT := now() at time zone 'utc';
	END IF;
	return NEW;
END;
$$

-- this trigger might need to be changed as it writes data in local time, not UTC
CREATE TRIGGER users_table
    BEFORE UPDATE 
    ON public.users
    FOR EACH ROW
    EXECUTE PROCEDURE public.modified_at_changes();

alter table users
	add column is_deprecated BOOLEAN;
	
