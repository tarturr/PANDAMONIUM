--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateur` (`pseudo` varchar(16) NOT NULL, `email` varchar(50) NOT NULL, `mot_de_passe` varchar(64) NOT NULL, `date_naiss` date NOT NULL, `date_enregistre` date NOT NULL, `date_connecte` date NOT NULL, `liste_amis` text, PRIMARY KEY (`pseudo`));

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`pseudo`, `email`, `mot_de_passe`, `date_naiss`, `date_enregistre`, `date_connecte`, `liste_amis`) VALUES ('tartur', 'tartur.dev@gmail.com', 'supermdp', '2006-06-26', '2023-10-06', '2023-10-06', NULL), ('ghosty', 'gae35.9234@skiff.com', 'TarturI<3U', '2007-01-19', '2023-10-06', '2023-10-06', NULL), ('Nicocoin_AHH', 'nicolas.bernier2508@gmail.com', 'nicolas.25', '2006-08-25', '2023-10-06', '2023-10-06', NULL);