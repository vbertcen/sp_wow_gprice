#日均价（分平台）
select date_format(rec_time,'%Y%m%d') as 时间,platform 平台,avg(unit_price) 日均价 from gprice_list t group by date_format(rec_time,'%Y%m%d'),platform;

#日均价
select date_format(rec_time,'%Y%m%d') as 时间,avg(unit_price) 日均价 from gprice_list t group by date_format(rec_time,'%Y%m%d');

#时点均价（分平台）
select date_format(rec_time,'%Y%m%d-%H') as 时间,platform 平台,avg(unit_price) 时点均价 from gprice_list t group by date_format(rec_time,'%Y-%m-%d %H点'),platform;

#时点均价
select date_format(rec_time,'%Y%m%d-%H') as 时间,avg(unit_price) 时点均价 from gprice_list t group by date_format(rec_time,'%Y-%m-%d %H点');

