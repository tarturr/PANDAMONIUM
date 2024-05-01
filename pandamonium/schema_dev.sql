--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE users(uuid VARCHAR(36), username VARCHAR(50) NOT NULL, email VARCHAR(50), password VARCHAR(50), date_of_birth DATE, friends VARCHAR(3600), relations VARCHAR(3600), registration_date DATE, last_connection_date DATETIME, pronouns VARCHAR(50), pb_displayed_name VARCHAR(50), pb_bio VARCHAR(300), pv_displayed_name VARCHAR(50), pv_bio VARCHAR(300), PRIMARY KEY(uuid));

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `users` (`username`, `email`, `password`, `date_of_birth`, `registered_at`, `logged_at`, `friends`) VALUES ('tartur', 'tartur.dev@gmail.com', 'supermdp', '2006-06-26', '2023-10-06', '2023-10-06', NULL), ('ghosty', 'gae35.9234@skiff.com', 'TarturI<3U', '2007-01-19', '2023-10-06', '2023-10-06', NULL), ('Nicocoin_AHH', 'nicolas.bernier2508@gmail.com', 'nicolas.25', '2006-08-25', '2023-10-06', '2023-10-06', NULL);