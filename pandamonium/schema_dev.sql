--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE users(uuid VARCHAR(36), username VARCHAR(50) NOT NULL, email VARCHAR(50), password VARCHAR(512), date_of_birth DATE, friends VARCHAR(3600), relations VARCHAR(3600), bamboos VARCHAR(3600), registration_date DATE, last_connection_date DATETIME, pronouns VARCHAR(50), public_display_name VARCHAR(50), public_bio VARCHAR(300), private_display_name VARCHAR(50), private_bio VARCHAR(300), PRIMARY KEY(uuid), UNIQUE(username), UNIQUE(email));
CREATE TABLE bamboos(uuid VARCHAR(36), name VARCHAR(50) NOT NULL, creation_date DATE, members TEXT, owner_uuid VARCHAR(36) NOT NULL, PRIMARY KEY(uuid), FOREIGN KEY(owner_uuid) REFERENCES users(uuid));
CREATE TABLE category(uuid VARCHAR(36), name VARCHAR(20), bamboo_uuid VARCHAR(36) NOT NULL, PRIMARY KEY(uuid), FOREIGN KEY(bamboo_uuid) REFERENCES bamboos(uuid));
CREATE TABLE branches(uuid VARCHAR(36), name VARCHAR(30) NOT NULL, category_uuid VARCHAR(36) NOT NULL, PRIMARY KEY(uuid), FOREIGN KEY(category_uuid) REFERENCES category(uuid));
CREATE TABLE messages(uuid VARCHAR(36), content VARCHAR(2000) NOT NULL, date_sent DATETIME, modified BOOLEAN NOT NULL, sender_uuid VARCHAR(36) NOT NULL, branch_uuid VARCHAR(36) NOT NULL, response_to_message_uuid VARCHAR(36), PRIMARY KEY(uuid), FOREIGN KEY(sender_uuid) REFERENCES users(uuid), FOREIGN KEY(branch_uuid) REFERENCES branches(uuid), FOREIGN KEY(response_to_message_uuid) REFERENCES messages(uuid));

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `users` (`uuid`, `username`, `email`, `password`, `date_of_birth`, `registration_date`, `last_connection_date`, `friends`) VALUES ('e2008d2f-92f6-4e88-80dd-58f08f9581ed', 'tartur', 'tartur.dev@gmail.com', 'supermdp', '2006-06-26', '2023-10-06', '2023-10-06', NULL), ('cae10a02-8555-42ba-8ead-314879f725e3', 'ghosty', 'gae35.9234@skiff.com', 'TarturI<3U', '2007-01-19', '2023-10-06', '2023-10-06', NULL), ('39bfec44-5492-49b2-9063-fb69794a8d73', 'Nicocoin_AHH', 'nicolas.bernier2508@gmail.com', 'nicolas.25', '2006-08-25', '2023-10-06', '2023-10-06', NULL);