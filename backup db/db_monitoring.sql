-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 21, 2022 at 11:07 AM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 7.4.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_monitoring`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('3a2ebf54d526');

-- --------------------------------------------------------

--
-- Table structure for table `auth_token_block`
--

CREATE TABLE `auth_token_block` (
  `id` int(11) NOT NULL,
  `jti` varchar(36) NOT NULL,
  `created_at` datetime NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `username` varchar(128) NOT NULL,
  `password` varchar(256) NOT NULL,
  `group` varchar(128) NOT NULL,
  `join_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `is_active` varchar(2) NOT NULL,
  `user_last_login` datetime DEFAULT NULL,
  `user_logout` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `username`, `password`, `group`, `join_date`, `update_date`, `is_active`, `user_last_login`, `user_logout`) VALUES
(5, 'admin', 'pbkdf2:sha256:260000$ppQCAb9XeA0ySjUp$ec7695e8ca5c83fdf7a3a7198862af70c31cadce3a3b96287fd65e2555bc9826', 'admin', '2022-11-21 08:59:26', NULL, '1', '2022-12-21 10:29:55', NULL),
(6, '196606271996022001', 'pbkdf2:sha256:260000$NS1yfMhyPjaf792v$19ecfb1c7a645732ee6c0767128b282763629ecf4b8a03f770dcca2d3cee5d95', 'guru', '2022-11-23 10:45:46', '2022-12-17 21:58:41', '1', '2022-12-17 21:58:57', NULL),
(7, '196204141987032019', 'pbkdf2:sha256:260000$MMeaDwSNRQ3ARN4U$e44985c1d72630be619674e95c137060cb16ae3d1d3c43f3dcdea8f0b8957cbd', 'guru', '2022-11-23 11:08:44', NULL, '1', '2022-12-18 13:06:59', NULL),
(8, '196910171992032008', 'pbkdf2:sha256:260000$6ZY9butqm04lQJBT$007ff3307c52fa684482fb24d4d9a9866e19530e1207f895a15ef6058d038b68', 'guru', '2022-11-23 11:08:44', NULL, '1', '2022-12-13 11:50:07', NULL),
(9, '196501021987032021', 'pbkdf2:sha256:260000$ciDiGmznZ6r9LyqS$57b7487d7f19b9b918c94358c91de9afac0cef2c907af4da0752dd48b6072245', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(10, '196905041998022004', 'pbkdf2:sha256:260000$5CCTPpKEwU4uxlek$1e036fd3e8a23aba35d8057445c3a41a77e91098cc264c5d446182943c8bf79b', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(11, '198512072011011008', 'pbkdf2:sha256:260000$7x53OC52o0UTJopc$eeda5256c88e04eaf2ed9eeb0babb6937007a3583a6af81c7d32d31a45d7db49', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(12, '197209152000032003', 'pbkdf2:sha256:260000$ARFmTsYoMDqWj6ad$0c06f0c7fc0652906caaf0c6d21d22d4c03b46c39d9dac30622c406f6c851b3e', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(13, '197008182006042000', 'pbkdf2:sha256:260000$5iJn2hLZzxofDs27$abf40d5b69774e87cb2ca22b685280269695e39cfec43895403647b5e40d8666', 'guru', '2022-11-23 11:08:44', NULL, '1', NULL, NULL),
(14, '197008182006042008', 'pbkdf2:sha256:260000$yV565KKXayH4cvjP$de6cb43b94ad125f04be9667652e43109db405600d205c6b6c0128f2a1340d85', 'guru', '2022-11-23 11:08:44', NULL, '1', '2022-12-08 16:27:36', NULL),
(15, '196701221995122001', 'pbkdf2:sha256:260000$TRNddbol1pvrXoFk$914ff1b2d7fa445ef6aef3df9a887aefb3c234599418acd1d3965ed68f8f230b', 'guru', '2022-11-23 11:08:44', '2022-11-23 11:47:21', '1', '2022-12-13 11:50:36', NULL),
(16, '0094755743', 'pbkdf2:sha256:260000$ML9TPvjwvoRkXRlc$2ac7283adc7e2b23210aa4cc815891f760cd7288c45fb92ca7f2f087b75b003c', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(17, '0099789908', 'pbkdf2:sha256:260000$IxrgSpm1OdaIRHiw$07b40cf46bd1bccc9e5fb37f05f2de2fcfc0b5e23902181a3ac7bafac38c4045', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(18, '0094125167', 'pbkdf2:sha256:260000$XiEMZ3lc84rxmSNg$5547334703162b6d5de070e528bda10cefb54c1d89065ade98e80810e5622db2', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(19, '0095787926', 'pbkdf2:sha256:260000$JTRY49t1Ldzu55kr$d6460b91f9e943fece13de1e894c6544a6a642b142b192edc670477e9fc0a5d3', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(20, '0085321166', 'pbkdf2:sha256:260000$72p1lOU3A4KG9Uc2$72a55d99071debe3833a857d3a8c1be9ead96587b74adbee12c497dd871abe55', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(21, '0096991422', 'pbkdf2:sha256:260000$h3fqF2lWUhcL6Cf4$4c2f1714a947969eea806afc551de8a2ee41a51b3269c172144901e3a87ae66e', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(22, '0082803614', 'pbkdf2:sha256:260000$QJHf5FUGh55IGbB0$42718f61c621dc341516ba04fc3f455d789064eaeff17f06556314d1aec24dd4', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(23, '0081227491', 'pbkdf2:sha256:260000$rdn8mzlaaRTY4NOP$043dc8641b48ad01d4fe0865bb1d63c77eaa2e475e1c56f242010bd85b15f97f', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(24, '0084835186', 'pbkdf2:sha256:260000$52kFS3XISmvOzgAr$aad75485875917b109c501b76eb69f95696003dbe21db4c7f3ae102d63f24ce0', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(25, '0095267997', 'pbkdf2:sha256:260000$gZodkTyvH5gnho4h$2c5eb6a9be688d53af8efae986493a1b86cf1f62e4f87710b49484bc958fefa0', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(26, '0086737425', 'pbkdf2:sha256:260000$V0rgIzgrlMVjonrc$83d96778abe92ae8b56e8abe80c220f81c9febf9713cb2fc6a7a725388d415b0', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(27, '0088283893', 'pbkdf2:sha256:260000$ziJz2NHvmkU50TvG$1480e329fe8b85f4bf2956f47ff411cfb5aa06d90c38efed65c34a86eb595f96', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(28, '0098182346', 'pbkdf2:sha256:260000$5JCO14IKtRK1ko1v$1beabc030166114030395b3f8d012f8f0f5792dbcd668cff5d496e6298d63c27', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(29, '0096041815', 'pbkdf2:sha256:260000$AnEY9J7FmVPzcWll$ac102a317ea0684961ed1e0bbac15dc3567b493af21e45ef437303cd8ef3c11e', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(30, '0097282248', 'pbkdf2:sha256:260000$rJHbrYsXaPv7S3L8$4dc317566a9ae65963763e3259f8299516ed42e9abf912d1b3078895357f7284', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(31, '0099049864', 'pbkdf2:sha256:260000$ooA2Wg5ZfbPKG5OS$08e060ae798530c488a6838dde29d3b6ea2349a13bc21d744f87ff6f35ea141a', 'siswa', '2022-11-23 11:31:51', NULL, '1', NULL, NULL),
(32, '0071412829', 'pbkdf2:sha256:260000$rZ9HEEPohgO8fC9j$4a07f87a2126af570d1f2e98874bfb2a6bee43570dc61f85a715c8b193ef2406', 'siswa', '2022-11-23 11:31:51', NULL, '1', '2022-11-23 12:06:34', NULL),
(33, '0083083027', 'pbkdf2:sha256:260000$obSCRkge0aCgToLi$68d66ec4019e5b5591bfaa21cba5370a2009b878b0c50817df3cdcb07d6833fc', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(34, '0099631922', 'pbkdf2:sha256:260000$up3QPN9hgOSj6Z67$c53daca0c82c704c8d5295b4765bfa22bfba667f12b42689001f6cf8f48a5f83', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(35, '0095459342', 'pbkdf2:sha256:260000$gYDnabg5ky8XHn8v$554f6856c28572550019c64f00789bc75a03221f52cef31ec4822a525dad6d26', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL),
(36, '0091604225', 'pbkdf2:sha256:260000$rBBOl2DoD7PBpocT$47985d62393ffd6671d37785ad18469624d9e3f53994cca81269315022bd4dfa', 'siswa', '2022-12-01 00:18:15', NULL, '1', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `data_absensi`
--

CREATE TABLE `data_absensi` (
  `id` int(11) NOT NULL,
  `mengajar_id` int(11) DEFAULT NULL,
  `siswa_id` int(11) DEFAULT NULL,
  `tgl_absen` date DEFAULT NULL,
  `ket` varchar(16) NOT NULL,
  `pertemuan_ke` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `detail_admin`
--

CREATE TABLE `detail_admin` (
  `id` int(11) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) DEFAULT NULL,
  `alamat` varchar(128) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `detail_admin`
--

INSERT INTO `detail_admin` (`id`, `first_name`, `last_name`, `gender`, `alamat`, `user_id`) VALUES
(1, 'Ari', 'Sajalah', 'laki-laki', 'Makassar', 5);

-- --------------------------------------------------------

--
-- Table structure for table `detail_guru`
--

CREATE TABLE `detail_guru` (
  `id` int(11) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) NOT NULL,
  `agama` varchar(32) DEFAULT NULL,
  `alamat` varchar(256) DEFAULT NULL,
  `telp` varchar(16) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `detail_guru`
--

INSERT INTO `detail_guru` (`id`, `first_name`, `last_name`, `gender`, `agama`, `alamat`, `telp`, `user_id`) VALUES
(1, 'Dra.', 'Rosmawati', 'perempuan', 'islam', '', '', 6),
(2, 'Dra.', 'Haslinda', 'perempuan', 'islam', '', '', 7),
(3, 'Harnidah,', 'S.Pd.', 'perempuan', 'islam', '', '', 8),
(4, 'Hj.', 'St. Nurbaya, S.Pd.,M.Pd.', 'perempuan', 'islam', '', '', 9),
(5, 'Hj.', 'Suriani, S.Ag.', 'perempuan', 'islam', '', '', 10),
(6, 'Ruslan', 'Talebe, S.Pd.', 'laki-laki', 'islam', '', '', 11),
(7, 'Rahmini,', 'S.Pd.,M.Mpd.', 'perempuan', 'islam', '', '', 12),
(8, 'Mariyani', 'Mannya, S.Pd.', 'perempuan', 'islam', '', '', 13),
(9, 'Hj.', 'Sahiah, S.Pd', 'perempuan', 'islam', '', '', 14),
(10, 'Sahabuddin,', 'S.Pd.', 'laki-laki', 'islam', 'Makassar', '', 15);

-- --------------------------------------------------------

--
-- Table structure for table `detail_siswa`
--

CREATE TABLE `detail_siswa` (
  `id` int(11) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `gender` varchar(32) NOT NULL,
  `tempat_lahir` varchar(128) DEFAULT NULL,
  `tgl_lahir` date DEFAULT NULL,
  `agama` varchar(128) NOT NULL,
  `nama_ortu_or_wali` varchar(128) DEFAULT NULL,
  `no_telp` varchar(16) DEFAULT NULL,
  `alamat` varchar(250) DEFAULT NULL,
  `qr_code` text DEFAULT NULL,
  `pic` text DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `detail_siswa`
--

INSERT INTO `detail_siswa` (`id`, `first_name`, `last_name`, `gender`, `tempat_lahir`, `tgl_lahir`, `agama`, `nama_ortu_or_wali`, `no_telp`, `alamat`, `qr_code`, `pic`, `user_id`, `kelas_id`) VALUES
(5, 'Ar', 'Rijal Dhaffa Nugraha', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 16, 9),
(6, 'ALISYAH', 'PUTRI RAMADHANI', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 17, 9),
(7, 'ANANDA', 'PUTRI AURELIA AKBAR', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_ananda_48ddf3afe6e410cbeca3ad26d07d393a.png', NULL, 18, 9),
(8, 'RHIFQI', 'ASHRAF SHANDY', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 19, 9),
(9, 'Salsabila', 'Azisah Az Zahra', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, 'VIII-1_salsabila_1fc49a06f936cdc6ee3b10f1ccead8a3.png', NULL, 20, 9),
(10, 'A.', 'ZHIL ZHILLAH ANUGRAH TANDIARI', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 21, 10),
(11, 'ADZKIYAH', 'ADELIAH', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 22, 10),
(12, 'M.', 'Dede Irza Saputra', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 23, 10),
(13, 'Lingga', 'Gwen Safitri', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 24, 10),
(14, 'RAFA', 'PUTRA RAMADHAN. A', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 25, 10),
(15, 'Ahmad', 'Fachri Al Farabi', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 26, 11),
(16, 'ALIKA', 'ZAYRAH DWI SEPTIA K', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 27, 11),
(17, 'Aqyla', 'Utami Putri Patriot', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 28, 11),
(18, 'BIMA', 'SASTRANEGARA ARY PUTRA', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 29, 11),
(19, 'Sitti', 'Adelia Mukarramah Munafr', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 30, 11),
(20, 'A.', 'AYU APRILIA', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 31, 12),
(21, 'Andi', 'Irgi', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 32, 13),
(22, 'AHMAD', 'AL FAHREZI', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 33, 12),
(23, 'Andi', 'Wafiqah Raidah Khamilah', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 34, 12),
(24, 'Muh.', 'Rifqy Athaillah Hamran', 'laki-laki', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 35, 12),
(25, 'SARIFA', 'ALIFIYAH ISWANDI', 'perempuan', NULL, NULL, 'islam', NULL, '', NULL, NULL, NULL, 36, 12);

-- --------------------------------------------------------

--
-- Table structure for table `master_guru_bk`
--

CREATE TABLE `master_guru_bk` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `master_hari`
--

CREATE TABLE `master_hari` (
  `id` int(11) NOT NULL,
  `hari` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_hari`
--

INSERT INTO `master_hari` (`id`, `hari`) VALUES
(1, 'senin'),
(2, 'selasa'),
(3, 'rabu'),
(4, 'kamis'),
(5, 'jumat'),
(7, 'sabtu');

-- --------------------------------------------------------

--
-- Table structure for table `master_jadwal_mengajar`
--

CREATE TABLE `master_jadwal_mengajar` (
  `id` int(11) NOT NULL,
  `kode_mengajar` varchar(32) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `mapel_id` int(11) DEFAULT NULL,
  `jam_ke` varchar(6) DEFAULT NULL,
  `hari_id` int(11) DEFAULT NULL,
  `jam_mulai` varchar(12) DEFAULT NULL,
  `jam_selesai` varchar(12) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL,
  `semester_id` int(11) DEFAULT NULL,
  `tahun_ajaran_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_jadwal_mengajar`
--

INSERT INTO `master_jadwal_mengajar` (`id`, `kode_mengajar`, `guru_id`, `mapel_id`, `jam_ke`, `hari_id`, `jam_mulai`, `jam_selesai`, `kelas_id`, `semester_id`, `tahun_ajaran_id`) VALUES
(33, 'MPL-955566', 9, 2, '1', 1, '07:30', '09:30', 9, 1, 2),
(34, 'MPL-642394', 14, 3, '2', 1, '09:30', '11:00', 9, 1, 2),
(35, 'MPL-2049658', 8, 6, '3', 1, '11:00', '12:55', 9, 1, 2),
(36, 'MPL-649138', 8, 6, '1', 1, '07:30', '09:30', 10, 1, 2),
(37, 'MPL-8917823', 15, 5, '2', 1, '09:30', '11:00', 10, 1, 2),
(38, 'MPL-2699945', 12, 1, '3', 1, '11:00', '12:55', 10, 1, 2),
(39, 'MPL-9091926', 12, 1, '1', 1, '07:30', '08:50', 11, 1, 2),
(40, 'MPL-0855632', 15, 5, '2', 1, '08:50', '09:30', 11, 1, 2),
(41, 'MPL-496497', 10, 8, '3', 1, '09:30', '11:40', 11, 1, 2),
(42, 'MPL-1266716', 14, 3, '4', 1, '11:40', '12:55', 11, 1, 2),
(43, 'MPL-4209483', 13, 4, '1', 1, '07:30', '09:30', 12, 1, 2),
(44, 'MPL-7297764', 9, 2, '2', 1, '09:30', '11:00', 12, 1, 2),
(45, 'MPL-2787924', 12, 1, '3', 1, '11:00', '12:55', 12, 1, 2),
(46, 'MPL-964149', 14, 3, '1', 1, '07:30', '08:50', 13, 1, 2),
(47, 'MPL-935434', 12, 1, '2', 1, '08:50', '11:00', 13, 1, 2),
(48, 'MPL-7705064', 13, 4, '3', 1, '11:00', '12:55', 13, 1, 2),
(49, 'MPL-769659', 13, 4, '1', 2, '07:15', '09:15', 9, 1, 2),
(50, 'MPL-4828076', 6, 7, '2', 2, '09:15', '10:45', 9, 1, 2),
(51, 'MPL-971107', 10, 8, '3', 2, '10:45', '12:40', 9, 1, 2),
(52, 'MPL-624748', 8, 6, '1', 2, '07:15', '08:35', 10, 1, 2),
(53, 'MPL-9747136', 10, 8, '2', 2, '08:35', '10:45', 10, 1, 2),
(54, 'MPL-5785005', 12, 1, '3', 2, '10:45', '12:40', 10, 1, 2),
(55, 'MPL-3774605', 9, 2, '1', 2, '07:15', '09:15', 11, 1, 2),
(56, 'MPL-4230661', 13, 4, '2', 2, '09:15', '11:25', 11, 1, 2),
(57, 'MPL-2690954', 6, 7, '3', 2, '11:25', '12:40', 11, 1, 2),
(58, 'MPL-3618176', 6, 7, '1', 2, '07:15', '08:35', 12, 1, 2),
(59, 'MPL-6286607', 8, 6, '2', 2, '08:35', '10:45', 12, 1, 2),
(60, 'MPL-2728553', 9, 2, '3', 2, '10:45', '12:40', 12, 1, 2),
(61, 'MPL-2372444', 11, 10, '1', 2, '07:15', '09:15', 13, 1, 2),
(62, 'MPL-4727843', 6, 7, '2', 2, '09:15', '10:45', 13, 1, 2),
(63, 'MPL-145499', 8, 6, '3', 2, '10:45', '12:40', 13, 1, 2),
(64, 'MPL-0572498', 12, 1, '1', 3, '07:15', '09:15', 9, 1, 2),
(65, 'MPL-9665446', 8, 6, '2', 3, '09:15', '10:45', 9, 1, 2),
(66, 'MPL-1854267', 7, 9, '3', 3, '10:45', '12:40', 9, 1, 2),
(67, 'MPL-3523862', 13, 4, '1', 3, '07:15', '09:15', 10, 1, 2),
(68, 'MPL-7090046', 11, 10, '2', 3, '09:15', '11:25', 10, 1, 2),
(69, 'MPL-553489', 14, 3, '3', 3, '11:25', '12:40', 10, 1, 2),
(70, 'MPL-9910965', 8, 6, '1', 3, '07:15', '09:15', 11, 1, 2),
(71, 'MPL-7209883', 12, 1, '2', 3, '09:15', '10:45', 11, 1, 2),
(72, 'MPL-8258874', 15, 5, '3', 3, '10:45', '11:25', 11, 1, 2),
(73, 'MPL-030209', 9, 2, '4', 3, '11:25', '12:40', 11, 1, 2),
(74, 'MPL-8716755', 7, 9, '1', 3, '07:15', '09:15', 12, 1, 2),
(75, 'MPL-3001113', 14, 3, '2', 3, '09:15', '10:45', 12, 1, 2),
(76, 'MPL-9592643', 10, 8, '3', 3, '10:45', '12:40', 12, 1, 2),
(77, 'MPL-8577526', 9, 2, '1', 3, '07:15', '08:35', 13, 1, 2),
(78, 'MPL-6703382', 15, 5, '2', 3, '08:35', '09:50', 13, 1, 2),
(79, 'MPL-10255', 6, 7, '3', 3, '10:05', '11:25', 13, 1, 2),
(80, 'MPL-079401', 8, 6, '4', 3, '11:25', '12:40', 13, 1, 2),
(81, 'MPL-5040846', 6, 7, '1', 4, '07:15', '08:35', 9, 1, 2),
(82, 'MPL-2512572', 9, 2, '2', 4, '08:35', '09:50', 9, 1, 2),
(83, 'MPL-33468', 15, 5, '3', 4, '10:05', '11:25', 9, 1, 2),
(84, 'MPL-6281545', 14, 3, '4', 4, '11:25', '12:40', 9, 1, 2),
(85, 'MPL-069096', 7, 9, '1', 4, '07:15', '09:15', 10, 1, 2),
(86, 'MPL-3795192', 6, 7, '2', 4, '09:15', '10:45', 10, 1, 2),
(87, 'MPL-9334261', 9, 2, '3', 4, '10:45', '12:40', 10, 1, 2),
(88, 'MPL-7867444', 11, 10, '1', 4, '07:15', '09:15', 11, 1, 2),
(89, 'MPL-363804', 12, 1, '2', 4, '09:15', '10:45', 11, 1, 2),
(90, 'MPL-9890945', 7, 9, '3', 4, '10:45', '12:40', 11, 1, 2),
(91, 'MPL-2045546', 12, 1, '1', 4, '07:15', '09:15', 12, 1, 2),
(92, 'MPL-832374', 11, 10, '2', 4, '09:15', '11:25', 12, 1, 2),
(93, 'MPL-9587512', 6, 7, '3', 4, '11:25', '12:40', 12, 1, 2),
(94, 'MPL-9440625', 10, 8, '1', 4, '07:15', '09:15', 13, 1, 2),
(95, 'MPL-2316525', 14, 3, '2', 4, '09:15', '10:45', 13, 1, 2),
(96, 'MPL-889407', 9, 2, '3', 4, '10:45', '12:40', 13, 1, 2),
(97, 'MPL-5329022', 12, 1, '1', 5, '07:15', '09:15', 9, 1, 2),
(98, 'MPL-6249998', 11, 10, '2', 5, '09:15', '11:30', 9, 1, 2),
(99, 'MPL-364484', 9, 2, '1', 5, '07:15', '08:35', 10, 1, 2),
(100, 'MPL-4111667', 6, 7, '2', 5, '08:35', '10:10', 10, 1, 2),
(101, 'MPL-7619693', 14, 3, '3', 5, '10:10', '11:30', 10, 1, 2),
(102, 'MPL-1705787', 14, 3, '1', 5, '07:15', '08:35', 11, 1, 2),
(103, 'MPL-1095114', 8, 6, '2', 5, '08:35', '10:10', 11, 1, 2),
(104, 'MPL-8916461', 6, 7, '3', 5, '10:10', '11:30', 11, 1, 2),
(105, 'MPL-8990536', 8, 6, '1', 5, '07:15', '08:35', 12, 1, 2),
(106, 'MPL-9599771', 14, 3, '2', 5, '08:35', '10:10', 12, 1, 2),
(107, 'MPL-1323905', 15, 5, '3', 5, '10:10', '11:30', 12, 1, 2),
(108, 'MPL-668466', 12, 1, '1', 5, '07:15', '09:15', 13, 1, 2),
(109, 'MPL-028389', 7, 9, '2', 5, '09:15', '11:30', 13, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `master_jam_mengajar`
--

CREATE TABLE `master_jam_mengajar` (
  `id` int(11) NOT NULL,
  `jam` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_jam_mengajar`
--

INSERT INTO `master_jam_mengajar` (`id`, `jam`) VALUES
(1, '07:00'),
(2, '07:15'),
(3, '07:30'),
(4, '07:45'),
(5, '08:00'),
(6, '08:30'),
(7, '09:00'),
(8, '09:30'),
(9, '10:00'),
(10, '10:30'),
(11, '11:00'),
(12, '11:30'),
(13, '12:00');

-- --------------------------------------------------------

--
-- Table structure for table `master_kelas`
--

CREATE TABLE `master_kelas` (
  `id` int(11) NOT NULL,
  `kelas` varchar(16) NOT NULL,
  `jml_laki` int(11) DEFAULT NULL,
  `jml_perempuan` int(11) DEFAULT NULL,
  `jml_seluruh` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_kelas`
--

INSERT INTO `master_kelas` (`id`, `kelas`, `jml_laki`, `jml_perempuan`, `jml_seluruh`) VALUES
(9, 'VIII-1', 2, 3, 5),
(10, 'VIII-2', 2, 3, 5),
(11, 'VIII-3', 2, 3, 5),
(12, 'VIII-4', 2, 3, 5),
(13, 'VIII-5', 1, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `master_kepsek`
--

CREATE TABLE `master_kepsek` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `status` varchar(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `master_mapel`
--

CREATE TABLE `master_mapel` (
  `id` int(11) NOT NULL,
  `mapel` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_mapel`
--

INSERT INTO `master_mapel` (`id`, `mapel`) VALUES
(1, 'Bahasa Indonesia '),
(2, 'Matematika'),
(3, 'Bahasa Inggris'),
(4, 'Seni Budaya'),
(5, 'Prakarya'),
(6, 'Ilmu Pengetahuan Alam'),
(7, 'Ilmu Pengetahuan Sosial'),
(8, 'Pendidikan Agama Islam'),
(9, 'Pendidikan Kewarganegaraan'),
(10, 'Pendidikan Jasmani, Olahraga, dan Kesehatan');

-- --------------------------------------------------------

--
-- Table structure for table `master_nama_bulan`
--

CREATE TABLE `master_nama_bulan` (
  `id` int(11) NOT NULL,
  `nama_bulan` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_nama_bulan`
--

INSERT INTO `master_nama_bulan` (`id`, `nama_bulan`) VALUES
(1, 'januari'),
(2, 'februari'),
(3, 'maret'),
(4, 'april'),
(5, 'mei'),
(6, 'juni'),
(7, 'juli'),
(8, 'agustus'),
(9, 'september'),
(10, 'oktober'),
(11, 'november'),
(12, 'desember');

-- --------------------------------------------------------

--
-- Table structure for table `master_semester`
--

CREATE TABLE `master_semester` (
  `id` int(11) NOT NULL,
  `semester` varchar(32) NOT NULL,
  `is_active` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_semester`
--

INSERT INTO `master_semester` (`id`, `semester`, `is_active`) VALUES
(1, 'ganjil', '1'),
(2, 'genap', '0');

-- --------------------------------------------------------

--
-- Table structure for table `master_tahun`
--

CREATE TABLE `master_tahun` (
  `id` int(11) NOT NULL,
  `tahun` varchar(4) NOT NULL,
  `status` varchar(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_tahun`
--

INSERT INTO `master_tahun` (`id`, `tahun`, `status`) VALUES
(4, '2021', '0'),
(7, '2022', '1'),
(8, '2023', '1');

-- --------------------------------------------------------

--
-- Table structure for table `master_tahun_ajaran`
--

CREATE TABLE `master_tahun_ajaran` (
  `id` int(11) NOT NULL,
  `th_ajaran` varchar(32) NOT NULL,
  `is_active` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_tahun_ajaran`
--

INSERT INTO `master_tahun_ajaran` (`id`, `th_ajaran`, `is_active`) VALUES
(1, '2021-2022', '0'),
(2, '2022-2023', '1'),
(3, '2023-2024', '0');

-- --------------------------------------------------------

--
-- Table structure for table `master_wali_kelas`
--

CREATE TABLE `master_wali_kelas` (
  `id` int(11) NOT NULL,
  `guru_id` int(11) DEFAULT NULL,
  `kelas_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `master_wali_kelas`
--

INSERT INTO `master_wali_kelas` (`id`, `guru_id`, `kelas_id`) VALUES
(1, 7, 9),
(2, 8, 11),
(3, 10, 13),
(4, 12, 10),
(5, 13, 12);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `auth_token_block`
--
ALTER TABLE `auth_token_block`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `ix_auth_token_block_jti` (`jti`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_absensi`
--
ALTER TABLE `data_absensi`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mengajar_id` (`mengajar_id`),
  ADD KEY `siswa_id` (`siswa_id`);

--
-- Indexes for table `detail_admin`
--
ALTER TABLE `detail_admin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `detail_guru`
--
ALTER TABLE `detail_guru`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `detail_siswa`
--
ALTER TABLE `detail_siswa`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kelas_id` (`kelas_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `master_guru_bk`
--
ALTER TABLE `master_guru_bk`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indexes for table `master_hari`
--
ALTER TABLE `master_hari`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_jadwal_mengajar`
--
ALTER TABLE `master_jadwal_mengajar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`),
  ADD KEY `hari_id` (`hari_id`),
  ADD KEY `kelas_id` (`kelas_id`),
  ADD KEY `mapel_id` (`mapel_id`),
  ADD KEY `semester_id` (`semester_id`),
  ADD KEY `tahun_ajaran_id` (`tahun_ajaran_id`);

--
-- Indexes for table `master_jam_mengajar`
--
ALTER TABLE `master_jam_mengajar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_kelas`
--
ALTER TABLE `master_kelas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_kepsek`
--
ALTER TABLE `master_kepsek`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`);

--
-- Indexes for table `master_mapel`
--
ALTER TABLE `master_mapel`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_nama_bulan`
--
ALTER TABLE `master_nama_bulan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_semester`
--
ALTER TABLE `master_semester`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_tahun`
--
ALTER TABLE `master_tahun`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tahun` (`tahun`);

--
-- Indexes for table `master_tahun_ajaran`
--
ALTER TABLE `master_tahun_ajaran`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `master_wali_kelas`
--
ALTER TABLE `master_wali_kelas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `guru_id` (`guru_id`),
  ADD KEY `kelas_id` (`kelas_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auth_token_block`
--
ALTER TABLE `auth_token_block`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `data_absensi`
--
ALTER TABLE `data_absensi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=108;

--
-- AUTO_INCREMENT for table `detail_admin`
--
ALTER TABLE `detail_admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `detail_guru`
--
ALTER TABLE `detail_guru`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `detail_siswa`
--
ALTER TABLE `detail_siswa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `master_guru_bk`
--
ALTER TABLE `master_guru_bk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_hari`
--
ALTER TABLE `master_hari`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `master_jadwal_mengajar`
--
ALTER TABLE `master_jadwal_mengajar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=110;

--
-- AUTO_INCREMENT for table `master_jam_mengajar`
--
ALTER TABLE `master_jam_mengajar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `master_kelas`
--
ALTER TABLE `master_kelas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `master_kepsek`
--
ALTER TABLE `master_kepsek`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `master_mapel`
--
ALTER TABLE `master_mapel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `master_nama_bulan`
--
ALTER TABLE `master_nama_bulan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `master_semester`
--
ALTER TABLE `master_semester`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `master_tahun`
--
ALTER TABLE `master_tahun`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `master_tahun_ajaran`
--
ALTER TABLE `master_tahun_ajaran`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `master_wali_kelas`
--
ALTER TABLE `master_wali_kelas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_token_block`
--
ALTER TABLE `auth_token_block`
  ADD CONSTRAINT `auth_token_block_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `data_absensi`
--
ALTER TABLE `data_absensi`
  ADD CONSTRAINT `data_absensi_ibfk_1` FOREIGN KEY (`mengajar_id`) REFERENCES `master_jadwal_mengajar` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `data_absensi_ibfk_2` FOREIGN KEY (`siswa_id`) REFERENCES `detail_siswa` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `detail_admin`
--
ALTER TABLE `detail_admin`
  ADD CONSTRAINT `detail_admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `detail_guru`
--
ALTER TABLE `detail_guru`
  ADD CONSTRAINT `detail_guru_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `detail_siswa`
--
ALTER TABLE `detail_siswa`
  ADD CONSTRAINT `detail_siswa_ibfk_1` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`),
  ADD CONSTRAINT `detail_siswa_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_guru_bk`
--
ALTER TABLE `master_guru_bk`
  ADD CONSTRAINT `master_guru_bk_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `master_jadwal_mengajar`
--
ALTER TABLE `master_jadwal_mengajar`
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_2` FOREIGN KEY (`hari_id`) REFERENCES `master_hari` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_3` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_4` FOREIGN KEY (`mapel_id`) REFERENCES `master_mapel` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_5` FOREIGN KEY (`semester_id`) REFERENCES `master_semester` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `master_jadwal_mengajar_ibfk_6` FOREIGN KEY (`tahun_ajaran_id`) REFERENCES `master_tahun_ajaran` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `master_kepsek`
--
ALTER TABLE `master_kepsek`
  ADD CONSTRAINT `master_kepsek_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`) ON UPDATE CASCADE;

--
-- Constraints for table `master_wali_kelas`
--
ALTER TABLE `master_wali_kelas`
  ADD CONSTRAINT `master_wali_kelas_ibfk_1` FOREIGN KEY (`guru_id`) REFERENCES `detail_guru` (`user_id`),
  ADD CONSTRAINT `master_wali_kelas_ibfk_2` FOREIGN KEY (`kelas_id`) REFERENCES `master_kelas` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
