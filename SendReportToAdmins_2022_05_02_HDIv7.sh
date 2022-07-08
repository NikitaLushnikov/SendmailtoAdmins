#!/bin/bash
# 2022.05.05
# sending report logs to admins #2
# 12 12 * * * sh /home/oracle/scripts/python/SendReportToAdmins_2022_05_02_HDIv7.sh >> /home/oracle/scripts/python/SendReportToAdmins.log 2>&1
year=`date +%Y`
month=`date +%m`
day=`date +%d`
hh=`date +%H`
mm=`date +%M`
ss=`date +%S`
date=$(date)
ia=$(whoami)
THIS_DIR=$(pwd)
prefixe=$year$month$day$hh$mm$ss

export NLS_LANG=AMERICAN_AMERICA.CL8MSWIN1251
export ORACLE_SID=OL11DIAP
export ORACLE_BASE=/home/oracle/app/oracle
export ORACLE_HOME=$ORACLE_BASE/product/11.2.0.4

SQL_LOG=$THIS_DIR/sql.log
alertlog=/home/oracle/app/oracle/diag/rdbms/ol11diap/OL11DIAP/trace/alert_OL11DIAP.log
alertlogcut=/home/oracle/scripts/python/alert_OL11DIAP_cut.log

backuplog=/home/oracle/dump/OL11DIAPBCKUP.log
backuplogcut=/home/oracle/scripts/python/OL11DIAPBCKUP_cut.log

free_space=/home/oracle/scripts/python/free_space_cut.log

echo ================================START BY $ia AT $date=============================
echo start tail
tail -n 700 $alertlog > $alertlogcut  2>&1
tail -n 6000 $backuplog > $backuplogcut  2>&1
echo end tail
echo start df -h
echo $date >> $free_space 2>&1
df -h >> $free_space 2>&1
echo end df
echo ===============================START SQL  AT $date=============================
#pochemyto vse ravno pishet v koren!!! /home/oracle/ kogda CRONTAB
#pochemyto pishet v diru kogda v ruchnyuy!!! /home/oracle/scripts/python/
$ORACLE_HOME/bin/sqlplus /nolog <<EOF >>$SQL_LOG  2>&1
 connect / as sysdba
 DEFINE THIS_DIR = $THIS_DIR
 set echo off
 set termout off
 set linesize 60
 set pagesize 20
 set markup html on spool on entmap off
 spool &THIS_DIR/tablespace.html
 select systimestamp from dual;
 select a.TABLESPACE_NAME tablespace_name, b.BYTES/1024/1024 total_MB, a.BYTES/1024/1024 free_MB,round(a.BYTES*100/b.BYTES,2) percent_free,round((b.BYTES-a.BYTES)*100/b.BYTES,2) percent_used
 from  (select TABLESPACE_NAME, sum(BYTES) BYTES from dba_free_space group by TABLESPACE_NAME) a,
       (select TABLESPACE_NAME, sum(BYTES) BYTES from dba_data_files group by TABLESPACE_NAME) b
 where a.TABLESPACE_NAME=b.TABLESPACE_NAME
 order by a.TABLESPACE_NAME;
 SPOOL OFF
exit
EOF
echo ===============================END SQL AT $date================================
echo ===============================START python  AT $date=============================
/usr/bin/python /home/oracle/scripts/python/SendReportToAdmins_2022_05_02_HDIv7.py
echo ===============================remove cutlogs from server======================
rm $alertlogcut
rm $backuplogcut
rm $SQL_LOG
rm $THIS_DIR/tablespace.html
rm /home/oracle/sql.log
rm /home/oracle/tablespace.html
echo ================================END   sh     AT $date==========================