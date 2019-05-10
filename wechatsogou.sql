CREATE DATABASE IF NOT EXISTS `wechatsogou`;
USE `wechatsogou`;

--
-- Table structure for table `add_mp_list`
--
DROP TABLE IF EXISTS `add_mp_list`;
CREATE TABLE `add_mp_list`
(
    `_id`  int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name` text COMMENT '要添加的公众号名称',
    PRIMARY KEY (`_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

--
-- Table structure for table `mp_info`
--
DROP TABLE IF EXISTS `mp_info`;
CREATE TABLE `mp_info`
(
    `_id`           int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name`          text COMMENT '公众号名称',
    `wx_hao`        text COMMENT '公众号微信号',
    `company`       text COMMENT '微信认证',
    `description`   text COMMENT '功能介绍',
    `logo_url`      text COMMENT 'logo地址',
    `qr_url`        text COMMENT '二维码地址',
    `create_time`   datetime COMMENT '创建时间',
    `update_time`   datetime COMMENT '更新时间',
    `recent_wz`     text COMMENT '最近文章标题',
    `recent_time`   datetime COMMENT '最近文章发布时间',
    `wz_url`        text COMMENT '文章列表地址',
    `last_qunfa_id` int(30) COMMENT '最后的群发ID',
    PRIMARY KEY (`_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

--
-- Table structure for table `wenzhang_info`
--
DROP TABLE IF EXISTS `wenzhang_info`;
CREATE TABLE `wenzhang_info`
(
    `_id`         int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `title`       text COMMENT '文章标题',
    `source_url`  text COMMENT '原文地址',
    `cover_url`   text COMMENT '封面图地址',
    `description` text COMMENT '文章摘要',
    `date_time`   datetime COMMENT '文章推送时间',
    `mp_id`       int(11) COMMENT '对应的公众号ID',
    `content_url` text COMMENT '文章临时地址',
    `author`      text COMMENT '作者',
    `qunfa_id`    int(30) COMMENT '群发消息ID',
    `msg_index`   int(2) COMMENT '一次群发中的图文顺序 1是头条',
    `content`     longtext COMMENT '文章正文',
    PRIMARY KEY (`_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
