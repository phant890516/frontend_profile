-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025 年 08 月 07 日 16:22
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */
--
-- 資料庫： `py23db`
--
CREATE DATABASE py23db;
USE py23db;
-- --------------------------------------------------------

--
-- 資料表結構 `lunch`
--

CREATE TABLE `lunch` (
  `scode` int(3) NOT NULL,
  `sname` varchar(50) NOT NULL,
  `price` int(11) NOT NULL,
  `detail` varchar(100) DEFAULT NULL,
  `filename` varchar(255) NOT NULL,
  PRIMARY KEY (`scode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `lunch`
--

INSERT INTO `lunch` (`scode`, `sname`, `price`, `detail`, `filename`) VALUES
(1, 'ルーナ', 10000, 'ルーナかわいい', '20250715221446_luna_cute.png'),
(2, '姫', 2000, '魅惑のルーナ', '20250715221541_luna_cuteeeee.png'),
(3, 'ルーナたん', 10000, 'ルーナ様だ！', '20250715221935_naaaaaaaa.png'),
(4, '超かわいい', 2000, 'お姫様', '20250715221646_luna_kawaii.png'),
(5, '姫森ルーナ', 600, 'ルーナなのら', '20250715221738_luna_princess.png'),
(10, 'んなたん', 10000, 'んなあああ', '20250715221806_lunananonanora.png'),
(12, 'sss', 10000, 'detail', '20250711103449_2024-06-24_020627.png'),
(13, 'んな姫', 10000, 'んな姫んなっしょい！', '20250715221842_the_cutest_luna.png'),
(14, 'ane', 1999, 'detail', '20250611145336_noa_reference_up02.png'),
(15, 'noa', 10000, 'んなあああ', '20250611145422_noa_reference_up.png'),
(1999, 'deiii1', 898989, '89898', '20250711102213_2024-06-24_020521.png'),
(2222, '222', 222, '222', '20250711104055_2024-06-24_020521.png'),
(77878, 'hiiiu', 87878, 'uiuiui', '20250611152248_noa_reference_up02.png'),
(166666, 'deiiiii', 2147483647, 'jijijiji', '20250611151434_noa_reference_up.png');

-- --------------------------------------------------------

--
-- 資料表結構 `user`
--

CREATE TABLE `user` (
  `userid` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `authority` int(1) NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `user`

INSERT INTO `user` (`userid`, `password`, `authority`) VALUES
('aa', 'aaa', 0),
('aaaaa', 'aaaaa', 1),
('anemoriluna', 'luknight', 0),
('himemori', 'luna', 1),
('JJJ', 'JJJ', 0),
('kawashima', '123', 0),
('linhungxiu', 'lunaluna', 0),
('nakao', '123', 0),
('nakao2', '123', 0),
('nakao3', '123', 1);

--
-- 已傾印資料表的索引

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
