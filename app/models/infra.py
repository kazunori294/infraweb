# -*- coding:utf-8 -*-

import app.models.db as db
import subprocess
import random

class Infra:

      def load(self):

        result = {}

        sql = "select * from host order by regdate DESC"
        db.con.execute(sql)
        result["hosts"] = db.con.fetchall()

        return result

 
      def edit(self,id):

        sql = "select * from host where id = %s"
        db.con.execute(sql,(id,))

        return db.con.fetchone()

      def createvm(self):
	
	source_str = 'abcdefghijklmnopqrstuvwxyz'
	vname = "".join([random.choice(source_str) for x in xrange(15)])
	subprocess.call(['sudo','/usr/bin/python', '/root/script/vmware/clonevm/clonevm.py' , '-s', '192.168.12.4', '-u', 'root', '-p', '51SdlQ#A', '-n', vname])


      def get_hostname(self,ipaddress):

        sql = "select * from host where ipaddress = %s"
        db.con.execute(sql,(ipaddress,))

        return db.con.fetchone()


      def reg_dns(self,id):
	
	sql = "select * from host where id = %s"
	db.con.execute(sql,(id,))
	host = db.con.fetchone()
	fqdn = host["hostname"].split('.', 1)
        hostn = fqdn[0]
	domain = fqdn[1]
        ip = host["ipaddress"]

	subprocess.call(['/usr/local/bin/cli53', 'rrcreate' , domain, hostn, 'A', ip, '--ttl', '3600'])

      def reg(self,host):
 
        sql = "select id from host where ipaddress = %s"
	db.con.execute(sql, (host["ipaddress"],))
	result = db.con.fetchone()

	if result:

                sql = "update host set"
                sql += " regdate=CURRENT_TIMESTAMP,"
                sql += " subnet= %s,"
                sql += " macaddress= %s,"
                sql += " os= %s,"
                sql += " kernel= %s,"
                sql += " uptime= %s,"
                sql += " cpufm= %s,"
                sql += " cpunum= %s,"
                sql += " mem= %s"
                sql += " where ipaddress = %s"
                db.con.execute(sql, (
                                    host["subnet"],
                                    host["macaddress"],
                                    host["os"],
                                    host["kernel"],
                                    host["uptime"],
                                    host["cpufm"],
                                    host["cpunum"],
                                    host["mem"],
				    host["ipaddress"],
                                    ))

	else:
        
		sql = "insert into host (hostname, ipaddress, regdate) values (%s, %s, CURRENT_TIMESTAMP)"
        	db.con.execute(sql, (
                	            host["hostname"],
                        	    host["ipaddress"],
                            	    ))
		
        db.dbhandle.commit()
        return


      def done(self,params):

	if params["del"]:
                sql = "delete from host where id = %s"
                db.con.execute(sql, (params["id"],))

	else:
		
                sql = "update host set "
                sql += " hostname=%s"
                sql += ",regdate=CURRENT_TIMESTAMP"
                sql += ",comment=%s"
                sql += " where id = %s"
                db.con.execute(sql, (
                                    params["hostname"],
                                    params["comment"],
                                    params["id"],
                                    ))
		
        db.dbhandle.commit()
        return
