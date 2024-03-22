--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (`username` varchar(16) NOT NULL, `email` varchar(50) NOT NULL, `password` varchar(64) NOT NULL, `date_of_birth` date NOT NULL, `registered_at` date NOT NULL, `logged_at` date NOT NULL, `friends` text, PRIMARY KEY (`username`));

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `users` (`username`, `email`, `password`, `date_of_birth`, `registered_at`, `logged_at`, `friends`) VALUES ('tartur', 'tartur.dev@gmail.com', 'supermdp', '2006-06-26', '2023-10-06', '2023-10-06', NULL), ('ghosty', 'gae35.9234@skiff.com', 'TarturI<3U', '2007-01-19', '2023-10-06', '2023-10-06', NULL), ('Nicocoin_AHH', 'nicolas.bernier2508@gmail.com', 'nicolas.25', '2006-08-25', '2023-10-06', '2023-10-06', NULL);