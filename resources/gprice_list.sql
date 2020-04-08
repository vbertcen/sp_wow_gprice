CREATE TABLE `gprice_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(50) not null comment '平台名称',
  `unit_price` decimal(14,4) not null comment '单价',
  `sale_price` decimal(14,2) not NULL comment '售价',
  `rec_time` datetime NOT NULL comment '记录时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;