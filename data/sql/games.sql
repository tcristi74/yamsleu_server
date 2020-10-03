CREATE SEQUENCE games_id_seq INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
GRANT ALL ON sequence public.games_id_seq TO ctudosestroe;


CREATE TABLE public.games
(
    id integer NOT NULL DEFAULT nextval('games_id_seq'::regclass) ,
    game_name character varying(50) COLLATE pg_catalog."default",
	started_at timestamp without time zone ,
	ended_at timestamp without time zone ,
	status character varying(20) COLLATE pg_catalog."default",
	game_comments character varying(250) COLLATE pg_catalog."default",
	winner_id integer,
	score integer,
    modified_at timestamp(6) without time zone NOT NULL DEFAULT timezone('UTC'::text, clock_timestamp()),
    created_at timestamp without time zone NOT NULL DEFAULT timezone('UTC'::text, clock_timestamp()),
    CONSTRAINT games_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.games
    OWNER to postgres;

GRANT ALL ON TABLE public.games TO ctudosestroe;

GRANT ALL ON TABLE public.games TO postgres;


CREATE TRIGGER games_table
    BEFORE UPDATE 
    ON public.games
    FOR EACH ROW
    EXECUTE PROCEDURE public.modified_at_changes();


alter table public.games
   add CONSTRAINT fk_winner
      FOREIGN KEY(winner_id) 
	  REFERENCES public.users(id);
