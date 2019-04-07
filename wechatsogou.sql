CREATE DATABASE IF NOT EXISTS `wechatsogou`;
USE `wechatsogou`;
-- MySQL dump 10.13  Distrib 5.7.22, for Win64 (x86_64)
--
-- Host: localhost    Database: wechatsogou
-- ------------------------------------------------------
-- Server version	5.7.22-log

--
-- Table structure for table `add_mp_list`
--
DROP TABLE IF EXISTS `add_mp_list`;
CREATE TABLE `add_mp_list`
(
    `_id`    int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name`   varchar(50) DEFAULT '' COMMENT '要添加的公众号名称',
    `wx_hao` varchar(50) DEFAULT '' COMMENT '公众号的微信号',
    PRIMARY KEY (`_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

--
-- Table structure for table `mp_info`
--
DROP TABLE IF EXISTS `mp_info`;
CREATE TABLE `mp_info`
(
    `_id`            int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `name`           varchar(50)  DEFAULT '' COMMENT '公众号名称',
    `wx_hao`         varchar(20)  DEFAULT '' COMMENT '公众号的微信号',
    `company`        varchar(100) DEFAULT '' COMMENT '主体名称',
    `description`    varchar(200) DEFAULT '' COMMENT '功能简介',
    `logo_url`       varchar(200) DEFAULT '' COMMENT 'logo url',
    `qr_url`         varchar(200) DEFAULT '' COMMENT '二维码URL',
    `create_time`    datetime     DEFAULT NULL COMMENT '加入牛榜时间',
    `update_time`    datetime     DEFAULT NULL COMMENT '最后更新时间',
    `last_qunfa_id`  int(30)      DEFAULT '0' COMMENT '最后的群发ID',
    `last_qufa_time` datetime     DEFAULT NULL COMMENT '最后一次群发的时间',
    `wz_url`         varchar(300) DEFAULT '' COMMENT '最近文章URL',
    PRIMARY KEY (`_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

--
-- Table structure for table `wenzhang_info`
--
DROP TABLE IF EXISTS `wenzhang_info`;
CREATE TABLE `wenzhang_info`
(
    `_id`            int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
    `title`          text COMMENT '文章标题',
    `source_url`     text COMMENT '原文地址',
    `cover_url`      text COMMENT '封面图URL',
    `description`    text COMMENT '文章摘要',
    `date_time`      datetime    DEFAULT NULL COMMENT '文章推送时间',
    `mp_id`          int(11)     DEFAULT '0' COMMENT '对应的公众号ID',
    `content_url`    text COMMENT '文章临时地址',
    `author`         varchar(50) DEFAULT '' COMMENT '作者',
    `msg_index`      int(11)     DEFAULT '0' COMMENT '一次群发中的图文顺序 1是头条 ',
    `copyright_stat` int(1)      DEFAULT '0' COMMENT '11表示原创 其它表示非原创',
    `qunfa_id`       int(30)     DEFAULT '0' COMMENT '群发消息ID',
    `type`           int(11)     DEFAULT '0' COMMENT '消息类型',
    `content`        longtext COMMENT '文章正文',
    PRIMARY KEY (`_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
