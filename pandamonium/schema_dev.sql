--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE users(uuid VARCHAR(36), username VARCHAR(50) NOT NULL, email VARCHAR(50), password VARCHAR(512), date_of_birth DATE, friends VARCHAR(3600), relations VARCHAR(3600), bamboos VARCHAR(3600), registration_date DATE, last_connection_date DATETIME, pronouns VARCHAR(50), public_display_name VARCHAR(50), public_bio VARCHAR(300), private_display_name VARCHAR(50), private_bio VARCHAR(300), PRIMARY KEY(uuid), UNIQUE(username), UNIQUE(email));

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `users` (`uuid`, `username`, `email`, `password`, `date_of_birth`, `registration_date`, `last_connection_date`, `friends`) VALUES ('e2008d2f-92f6-4e88-80dd-58f08f9581ed', 'tartur', 'tartur.dev@gmail.com', 'supermdp', '2006-06-26', '2023-10-06', '2023-10-06', NULL), ('cae10a02-8555-42ba-8ead-314879f725e3', 'ghosty', 'gae35.9234@skiff.com', 'TarturI<3U', '2007-01-19', '2023-10-06', '2023-10-06', NULL), ('39bfec44-5492-49b2-9063-fb69794a8d73', 'Nicocoin_AHH', 'nicolas.bernier2508@gmail.com', 'nicolas.25', '2006-08-25', '2023-10-06', '2023-10-06', NULL);