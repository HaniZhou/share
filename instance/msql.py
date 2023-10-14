import pymysql as pysql
import hashlib
import os


class MSQl():

    def __init__(self):
        self.DB = pysql.connect(host="zhouhuanownspwadmin.cgze866ixmjn.rds.cn-north-1.amazonaws.com.cn", port=3306,
                                user="admin",
                                db="usermanage", password="zhouhuan")
        self.cursor = self.DB.cursor()

    def insertUser(self, username, password):
        """创建用户"""
        try:
            pw = hashlib.scrypt(password.encode(), salt=b'xxxx', n=2 ** 14, r=8, p=1, dklen=64)
            self.cursor.execute("""
            INSERT INTO usermanage.users (username,password_hash)values (%s,%s)
            """, (username, pw))
            self.DB.commit()
            print("create successful1")
        except Exception as e:
            print("this:", e)
            return False
        else:
            print("create successful2")
            return True

    def checkLogin(self, username, password):
        """检查用户"""
        try:
            pw = hashlib.scrypt(password.encode(), salt=b'xxxx', n=2 ** 14, r=8, p=1, dklen=64)
            result = self.cursor.execute("""
            SELECT password_hash FROM usermanage.users WHERE username=%s
            """, (username))
            pwReal = self.cursor.fetchone()[0]
            print("pwReal", pwReal, "\n", pw)
            if pw == pwReal:
                print("create successful")
                return True
            else:
                return False

        except Exception as e:
            print(e)

    def showUserInfo(self):
        """返回所以用户名称 > shape(n,1)"""
        self.cursor.execute("""
                    SELECT username FROM usermanage.users;
                    """)
        result=self.cursor.fetchall()
        return result

    def changeUserInfo(self, username=str(), password=str()):
        pw = hashlib.scrypt(password.encode(), salt=b'xxxx', n=2 ** 14, r=8, p=1, dklen=64)
        self.cursor.execute("""
                    UPDATE usermanage.users SET password_hash=%s
                    WHERE username=%s
        """, (pw, username))
        return True


if __name__ == "__main__":
    stance = MSQl()
    info=stance.showUserInfo()
    print(info)
