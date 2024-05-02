/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `nsi_eleve1`
--

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE users(uuid VARCHAR(36), username VARCHAR(50) NOT NULL, email VARCHAR(50), password VARCHAR(50), date_of_birth DATE, friends VARCHAR(3600), relations VARCHAR(3600), registration_date DATE, last_connection_date DATETIME, pronouns VARCHAR(50), public_display_name VARCHAR(50), public_bio VARCHAR(300), private_display_name VARCHAR(50), private_bio VARCHAR(300), PRIMARY KEY(uuid), UNIQUE(username));

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;