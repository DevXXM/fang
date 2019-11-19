/*
SQLyog Community v12.09 (64 bit)
MySQL - 5.7.24 : Database - spider
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`spider` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;

USE `spider`;

/*Table structure for table `l_xiaoqu` */

DROP TABLE IF EXISTS `l_xiaoqu`;

CREATE TABLE `l_xiaoqu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `area` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '区名',
  `city` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '城市',
  `name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '小区名',
  `huxing` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '户型',
  `price` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '均价',
  `cover` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '封面',
  `years` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '建筑年代',
  `deal` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '成交量',
  `lease` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '出租数量',
  `house_id` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '小区ID',
  `url` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '外链',
  `property_costs` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '物业费',
  `arch_type` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '建筑类型',
  `property_company` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '物业公司',
  `developer` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '开发商',
  `build_num` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '栋数',
  `house_num` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '户数',
  `street` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '街道',
  `price_num` decimal(10,2) DEFAULT '0.00' COMMENT '数字价格',
  `price_desc` varchar(64) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '价格详情',
  `tag` varchar(512) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '标签，比如近地铁站',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=53168 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
