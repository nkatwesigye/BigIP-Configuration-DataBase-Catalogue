## Creates a table with the respective columns that store the Big_IP VIP details 
## To be run at a MySQL terminal or using a remote schema update script 
CREATE TABLE `vip_status` (`F5_device_name` varchar(80) DEFAULT NULL,`vip_name` varchar(80) DEFAULT NULL,`vip_ipaddress` varchar(80) NOT NULL,`vip_partition` varchar(80) DEFAULT NULL PRIMARY KEY(vip_ipaddress))
