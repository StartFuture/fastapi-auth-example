CREATE TABLE public.users (
	id_user serial4 NOT NULL,
	username varchar(255) NOT NULL,
	email varchar(255) NOT NULL UNIQUE,
	password_user varchar(255) NOT NULL,
	CONSTRAINT users_pkey PRIMARY KEY (id_user)
);