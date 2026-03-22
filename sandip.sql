-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 22, 2026 at 09:02 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sandip`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `sno` int(50) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `ph_no` varchar(50) NOT NULL,
  `date` datetime DEFAULT current_timestamp(),
  `msg` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`sno`, `name`, `email`, `ph_no`, `date`, `msg`) VALUES
(1, 'sandip', 'sandip@gmail.com', '123456789', '2026-02-22 13:09:01', 'hello'),
(2, 's', 'ss@gmail.com', '12', '2026-02-22 22:12:10', 'ok'),
(3, 's', 'cs2366.diatm@gmail.com', '12', '2026-02-28 20:35:00', 'o'),
(4, 's', 'cs2366.diatm@gmail.com', '12', '2026-02-28 20:43:46', 'o'),
(5, 's', 'cs2366.diatm@gmail.com', '12', '2026-03-16 11:09:51', 'okk'),
(6, 's', 'cs2366.diatm@gmail.com', '12', '2026-03-16 11:17:31', 'okkkk');

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `sno` int(50) NOT NULL,
  `title` text NOT NULL,
  `tags` text NOT NULL,
  `slug` varchar(25) NOT NULL,
  `content` text NOT NULL,
  `img_file` varchar(255) DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`sno`, `title`, `tags`, `slug`, `content`, `img_file`, `date`) VALUES
(1, 'its ok', 'first also', 'good', 'wowzz', 'post-sample-image.jpg', '2026-03-21 12:07:11'),
(2, 'this is second', 'second yaar', 'post.slug', 'orem ipsum dolor sit amet consectetur adipisicing elit. Voluptas, voluptate. Voluptas, voluptate. Voluptas, voluptate. ', 'post-sample-image.jpg', '2026-03-16 11:08:27'),
(6, 'euwjhifrfew', 'redr', 'rdcrfce', 'recasfr', 'Screenshot_2024-05-11_165123.png', '2026-03-21 23:19:52'),
(10, 'srthgh', 'hrhtrfr', 'rhh', 'rhfv', 'Screenshot_2024-09-14_155915.png', '2026-03-21 23:19:16'),
(11, 'a', 'aefc', 'earrrsqqq', 'ewdcwfwlkm', 'Screenshot_2025-07-08_120106.png', '2026-03-21 23:26:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
