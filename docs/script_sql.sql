BEGIN;

-- Table utilisateurs
CREATE TABLE IF NOT EXISTS public.utilisateurs
(
    id serial PRIMARY KEY,
    nom character varying(100) NOT NULL,
    email character varying(150) NOT NULL UNIQUE
);

-- Table categories
CREATE TABLE IF NOT EXISTS public.categories
(
    id serial PRIMARY KEY,
    nom character varying(100) NOT NULL UNIQUE,
    description text
);

-- Table articles
CREATE TABLE IF NOT EXISTS public.articles
(
    id serial PRIMARY KEY,
    titre character varying(255) NOT NULL,
    contenu text,
    date_publication timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    categorie_id integer NOT NULL,
    auteur_id integer NOT NULL
);

-- Table commentaires
CREATE TABLE IF NOT EXISTS public.commentaires
(
    id serial PRIMARY KEY,
    contenu text NOT NULL,
    date_commentaire timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    article_id integer NOT NULL,
    auteur_id integer NOT NULL
);

-- Contraintes de clés étrangères

ALTER TABLE IF EXISTS public.articles
    ADD CONSTRAINT fk_articles_categories FOREIGN KEY (categorie_id)
    REFERENCES public.categories (id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT;

ALTER TABLE IF EXISTS public.articles
    ADD CONSTRAINT fk_articles_utilisateurs FOREIGN KEY (auteur_id)
    REFERENCES public.utilisateurs (id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT;

ALTER TABLE IF EXISTS public.commentaires
    ADD CONSTRAINT fk_commentaires_articles FOREIGN KEY (article_id)
    REFERENCES public.articles (id)
    ON UPDATE CASCADE
    ON DELETE CASCADE;

ALTER TABLE IF EXISTS public.commentaires
    ADD CONSTRAINT fk_commentaires_utilisateurs FOREIGN KEY (auteur_id)
    REFERENCES public.utilisateurs (id)
    ON UPDATE CASCADE
    ON DELETE RESTRICT;

COMMIT;
