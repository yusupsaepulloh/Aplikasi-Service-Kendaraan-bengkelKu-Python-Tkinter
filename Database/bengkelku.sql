-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 23 Jul 2025 pada 16.35
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bengkelku`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `akun_login`
--

CREATE TABLE `akun_login` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `role` enum('admin','petugas') DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `akun_login`
--

INSERT INTO `akun_login` (`id_user`, `username`, `password`, `role`) VALUES
(1, '1', '1', 'admin'),
(6, '2', '2', 'petugas'),
(4, 'admin', 'admin', 'admin'),
(5, 'petugas', 'petugas', 'petugas');

-- --------------------------------------------------------

--
-- Struktur dari tabel `mekanik`
--

CREATE TABLE `mekanik` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `mekanik`
--

INSERT INTO `mekanik` (`id`, `nama`) VALUES
(1, 'Rudi'),
(2, 'Budi'),
(3, 'Andi'),
(7, 'Yusup'),
(6, 'Amad'),
(9, 'Abdul');

-- --------------------------------------------------------

--
-- Struktur dari tabel `service`
--

CREATE TABLE `service` (
  `id` int(11) NOT NULL,
  `mekanik_id` int(11) DEFAULT NULL,
  `sparepart_id` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL,
  `harga_sparepart` int(11) DEFAULT NULL,
  `harga_jasa` int(11) DEFAULT NULL,
  `total` int(11) DEFAULT NULL,
  `tanggal` datetime DEFAULT NULL,
  `nama_pelanggan` varchar(100) DEFAULT NULL,
  `plat_kendaraan` varchar(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `service`
--

INSERT INTO `service` (`id`, `mekanik_id`, `sparepart_id`, `qty`, `harga_sparepart`, `harga_jasa`, `total`, `tanggal`, `nama_pelanggan`, `plat_kendaraan`) VALUES
(57, 7, 15, 1, 500000, 10000, 510000, '2025-07-03 17:41:56', 'Yusup', 'Z 400 S'),
(58, 3, 2, 1, 40000, 10000, 50000, '2025-07-03 17:43:36', 'Ahmed', 'T 5 U'),
(59, 6, 2, 1, 40000, 100000, 140000, '2025-07-03 17:44:19', 'Junan', 'Z 400 X'),
(60, 3, 11, 1, 25000, 10000, 35000, '2025-07-03 17:49:23', 'Rena', 'Z 700 U'),
(61, 7, 22, 5, 400000, 1, 2000001, '2025-07-07 18:41:27', 'y', 'Z'),
(62, 7, 9, 1, 80000, 50000, 130000, '2025-07-10 18:47:23', 'Andi Cobra', 'Z 4040 U'),
(63, 7, 11, 1, 25000, 200000, 225000, '2025-07-10 18:47:48', 'Andi Cobra', 'Z 4040 U');

-- --------------------------------------------------------

--
-- Struktur dari tabel `sparepart`
--

CREATE TABLE `sparepart` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `stok` int(11) DEFAULT NULL,
  `harga` int(11) DEFAULT NULL,
  `harga_jasa` int(100) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `sparepart`
--

INSERT INTO `sparepart` (`id`, `nama`, `stok`, `harga`, `harga_jasa`) VALUES
(8, 'Filter Oli', 100, 30000, 10000),
(2, 'Oli Mesin', 0, 40000, 10000),
(9, 'Filter Udara', 98, 80000, 10000),
(10, 'Filter AC', 100, 50000, 10000),
(11, 'Busi (Spark Plug)', 97, 25000, 10000),
(12, 'Kampas Rem', 100, 100000, 10000),
(13, 'Kampas Kopling', 100, 300000, 10000),
(14, 'Aki (Battery)', 100, 800000, 10000),
(15, 'Ban Luar', 99, 500000, 15000),
(16, 'Ban Dalam', 100, 200000, 10000),
(17, 'Lampu Depan', 100, 2100000, 30000),
(18, 'Lampu Belakang', 100, 150000, 20000),
(19, 'Shockbreaker', 100, 350000, 30000),
(20, 'V-Belt', 100, 100000, 15000),
(21, 'Radiator', 100, 700000, 30000),
(22, 'Power Window Regulator', 95, 400000, 50000),
(23, 'Brake Pad Sensor', 100, 250000, 15000);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `akun_login`
--
ALTER TABLE `akun_login`
  ADD PRIMARY KEY (`id_user`);

--
-- Indeks untuk tabel `mekanik`
--
ALTER TABLE `mekanik`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`id`),
  ADD KEY `mekanik_id` (`mekanik_id`),
  ADD KEY `sparepart_id` (`sparepart_id`);

--
-- Indeks untuk tabel `sparepart`
--
ALTER TABLE `sparepart`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `akun_login`
--
ALTER TABLE `akun_login`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `mekanik`
--
ALTER TABLE `mekanik`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT untuk tabel `service`
--
ALTER TABLE `service`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=64;

--
-- AUTO_INCREMENT untuk tabel `sparepart`
--
ALTER TABLE `sparepart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
