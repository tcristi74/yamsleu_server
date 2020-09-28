CREATE TABLE public.plays
(
    game_id integer NOT NULL ,
	user_id integer NOT NULL ,
	current_position integer NOT NULL default 0,
	current_score integer NOT NULL default 0,
	play_table jsonb,
	comments character varying(250) COLLATE pg_catalog."default",
    modified_at timestamp(6) without time zone NOT NULL DEFAULT timezone('UTC'::text, clock_timestamp()),
    created_at timestamp without time zone NOT NULL DEFAULT timezone('UTC'::text, clock_timestamp()),
    CONSTRAINT plays_pkey PRIMARY KEY (game_id,user_id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

CREATE TRIGGER plays_table
    BEFORE UPDATE 
    ON public.plays
    FOR EACH ROW
    EXECUTE PROCEDURE public.modified_at_changes();


--CREATE INDEX splunk_ebs3_tags_idx1
--    ON public.splunk_ebs3 USING btree
--    ((tags ->> 'EBS_VERSION'::text) COLLATE pg_catalog."default", (tags ->> 'POD_TYPE'::text) COLLATE pg_catalog."default", (tags ->> 'POD'::text) COLLATE pg_catalog."default")
--    TABLESPACE pg_default;



ALTER TABLE public.plays
    OWNER to postgres;

GRANT ALL ON TABLE public.plays TO ctudosestroe;

GRANT ALL ON TABLE public.plays TO postgres;

alter table public.plays 
   add CONSTRAINT fk_user
      FOREIGN KEY(user_id) 
	  REFERENCES public.users(id);

alter table public.plays 
   add CONSTRAINT fk_game
      FOREIGN KEY(game_id) 
	  REFERENCES public.games(id);