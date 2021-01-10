CREATE SCHEMA public AUTHORIZATION postgres;

COMMENT ON SCHEMA public IS 'standard public schema';

CREATE TABLE public.authors (
	id serial NOT NULL,
	"name" text NULL,
	book _text NULL,
	CONSTRAINT authors_pkey PRIMARY KEY (id)
);

CREATE TABLE public.books (
	isbn text NOT NULL,
	"name" text NULL,
	author text NULL,
	"year" int4 NULL,
	CONSTRAINT books_pkey PRIMARY KEY (isbn)
);

CREATE TABLE public.users (
	id serial NOT NULL,
	username text NOT NULL,
	"password" text NOT NULL,
	mail text NULL,
	"role" text NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id)
);