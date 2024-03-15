-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : ven. 01 déc. 2023 à 08:45
-- Version du serveur :  5.7.31
-- Version de PHP : 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `belongs_to`
--

DROP TABLE IF EXISTS `belongs_to`;
CREATE TABLE IF NOT EXISTS `belongs_to` (
  `id_channel` int(11) NOT NULL,
  `id_category` int(11) NOT NULL,
  PRIMARY KEY (`id_channel`,`id_category`),
  KEY `id_category` (`id_category`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `category`
--

DROP TABLE IF EXISTS `category`;
CREATE TABLE IF NOT EXISTS `category` (
  `id_category` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id_category`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `channel`
--

DROP TABLE IF EXISTS `channel`;
CREATE TABLE IF NOT EXISTS `channel` (
  `id_channel` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id_channel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `contains`
--

DROP TABLE IF EXISTS `contains`;
CREATE TABLE IF NOT EXISTS `contains` (
  `id_server` int(11) NOT NULL,
  `id_role` int(11) NOT NULL,
  PRIMARY KEY (`id_server`,`id_role`),
  KEY `id_role` (`id_role`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `exists_in`
--

DROP TABLE IF EXISTS `exists_in`;
CREATE TABLE IF NOT EXISTS `exists_in` (
  `id_server` int(11) NOT NULL,
  `id_category` int(11) NOT NULL,
  PRIMARY KEY (`id_server`,`id_category`),
  KEY `id_category` (`id_category`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `got`
--

DROP TABLE IF EXISTS `got`;
CREATE TABLE IF NOT EXISTS `got` (
  `id_member` int(11) NOT NULL,
  `id_role` int(11) NOT NULL,
  PRIMARY KEY (`id_member`,`id_role`),
  KEY `id_role` (`id_role`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `is_in`
--

DROP TABLE IF EXISTS `is_in`;
CREATE TABLE IF NOT EXISTS `is_in` (
  `id_member` int(11) NOT NULL,
  `id_server` int(11) NOT NULL,
  PRIMARY KEY (`id_member`,`id_server`),
  KEY `id_server` (`id_server`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `member_channel_access`
--

DROP TABLE IF EXISTS `member_channel_access`;
CREATE TABLE IF NOT EXISTS `member_channel_access` (
  `id_member` int(11) NOT NULL,
  `id_channel` int(11) NOT NULL,
  `writing` tinyint(1) NOT NULL,
  `viewing` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_member`,`id_channel`),
  KEY `id_channel` (`id_channel`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `membre`
--

DROP TABLE IF EXISTS `membre`;
CREATE TABLE IF NOT EXISTS `membre` (
  `id_member` int(11) NOT NULL,
  `pseudo_server` varchar(50) DEFAULT NULL,
  `pseudo` varchar(50) NOT NULL,
  PRIMARY KEY (`id_member`),
  KEY `pseudo` (`pseudo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `message`
--

DROP TABLE IF EXISTS `message`;
CREATE TABLE IF NOT EXISTS `message` (
  `id_message` int(11) NOT NULL,
  `valeur` varchar(2000) NOT NULL,
  `envoi` datetime DEFAULT NULL,
  `modified` tinyint(1) NOT NULL,
  `id_message_1` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_message`),
  KEY `id_message_1` (`id_message_1`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE IF NOT EXISTS `role` (
  `id_role` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `color` char(6) DEFAULT NULL,
  `hierarchie` varchar(50) DEFAULT NULL,
  `admin` tinyint(1) NOT NULL,
  `perm_managing_channels` tinyint(1) NOT NULL,
  `perm_managing_roles` tinyint(1) NOT NULL,
  `perm_delete` tinyint(1) NOT NULL,
  `perm_ban` tinyint(1) NOT NULL,
  `perm_kick` tinyint(1) NOT NULL,
  `perm_mute` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_role`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `role_channel_access`
--

DROP TABLE IF EXISTS `role_channel_access`;
CREATE TABLE IF NOT EXISTS `role_channel_access` (
  `id_channel` int(11) NOT NULL,
  `id_role` int(11) NOT NULL,
  `writing` tinyint(1) NOT NULL,
  `viewing` tinyint(1) NOT NULL,
  PRIMARY KEY (`id_channel`,`id_role`),
  KEY `id_role` (`id_role`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `sent_by`
--

DROP TABLE IF EXISTS `sent_by`;
CREATE TABLE IF NOT EXISTS `sent_by` (
  `id_member` int(11) NOT NULL,
  `id_message` int(11) NOT NULL,
  PRIMARY KEY (`id_member`,`id_message`),
  KEY `id_message` (`id_message`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `sent_in`
--

DROP TABLE IF EXISTS `sent_in`;
CREATE TABLE IF NOT EXISTS `sent_in` (
  `id_channel` int(11) NOT NULL,
  `id_message` int(11) NOT NULL,
  PRIMARY KEY (`id_channel`,`id_message`),
  KEY `id_message` (`id_message`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `serveur`
--

DROP TABLE IF EXISTS `serveur`;
CREATE TABLE IF NOT EXISTS `serveur` (
  `id_server` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `creation_server` date DEFAULT NULL,
  PRIMARY KEY (`id_server`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateur` (
  `pseudo` varchar(16) NOT NULL,
  `email` varchar(50) NOT NULL,
  `mot_de_passe` varchar(64) NOT NULL,
  `date_naiss` date NOT NULL,
  `date_enregistre` date NOT NULL,
  `date_connecte` date NOT NULL,
  `liste_amis` text,
  PRIMARY KEY (`pseudo`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`pseudo`, `email`, `mot_de_passe`, `date_naiss`, `date_enregistre`, `date_connecte`, `liste_amis`) VALUES
('tartur', 'tartur.dev@gmail.com', 'supermdp', '2006-06-26', '2023-10-06', '2023-10-06', NULL),
('ghosty', 'gae35.9234@skiff.com', 'TarturI<3U', '2007-01-19', '2023-10-06', '2023-10-06', NULL),
('Nicocoin_AHH', 'nicolas.bernier2508@gmail.com', 'nicolas.25', '2006-08-25', '2023-10-06', '2023-10-06', NULL);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;