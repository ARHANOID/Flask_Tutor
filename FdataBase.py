import sqlite3, time, math, re
from flask import url_for




class FdataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def close_db(self):
        self.__db.close()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        menu = []
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                # print("return res", res)
                for i in range(len(res)):
                    submenu = {}
                    submenu['id'] = res[i][0]
                    submenu['name'] = res[i][1]
                    submenu['url'] = res[i][2]
                    menu.append(submenu)

                # print(menu)
                return menu
            else:
                print("error")
        except:
            print("error FdataBase.getMenu")

        return []

    def addPost(self, title, text):
        print("addPost")
        try:
            print("addPost try")
            tm = math.floor(time.time())
            inst = "INSERT INTO posts VALUES(NULL, ?, ?, ?)"
            self.__cur.execute(inst, (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("error FdataBase.addPost  " + str(e))
            return False
        return True

    # def replaser(self, text):
    #     print("replaser")
    #     inter = 0
    #     look_for = "src=/static/images_html/./"
    #     change_for = "src=./static/images_html/"
    #     # while text.find(look_for) != -1:
    #     #     inter+=1
    #     #     print(inter)
    #     text = text.replace(look_for, change_for)
    #     print(text)
    #     # text.find()
    #     return text
    def replaser(self, text):
        print("replaser")
        inter = 0
        # look_for = "src=/static/images_html/./tv_ARHANOID - Overview - DOTABUFF - Dota 2 Stats_files/"
        # change_for = "src=/static/images_html2/tvARX/"
        look_for = "src=/static/images_html/./The Path of Exile Wiki_files/"
        change_for = "src=./static/images_html2/POE/"
        # while text.find(look_for) != -1:
        #     inter+=1
        #     print(inter)
        text = text.replace(look_for, change_for)
        print(text)
        # text.find()
        return text

    def addHTML(self, title, text, url):
        print("addHTML")
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM posts_html WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()

            if res['count'] > 0:
                print("url already exist in posts_html")
                return False
            base = url_for('static', filename='images_html')

            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>",
                          text)
            text = self.replaser(text)

            print("addPost try")
            tm = math.floor(time.time())
            inst = "INSERT INTO posts_html VALUES(NULL, ?, ?, ?, ?)"
            self.__cur.execute(inst, (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("error FdataBase.addHTML  " + str(e))
            return False
        return True

    def addUser(self, name, email, hpsw):
        print("addUser")
        try:
            self.__cur.execute("SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()

            if res['count'] > 0:
                print("email already exist in users")
                return False
            self.__cur.execute("SELECT COUNT() as 'count' FROM users WHERE name LIKE '{name}'")
            res = self.__cur.fetchone()

            if res['count'] > 0:
                print("name already exist in users")
                return False

            tm = math.floor(time.time())
            inst = "INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)"
            self.__cur.execute(inst, (name, email, hpsw, tm))
            self.__db.commit()
            print("addUser is done", name, email, hpsw)
        except sqlite3.Error as e:
            print("error FdataBase.addHTML  " + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            print("getUser", user_id)
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()

            if not res:
                print("There is no such USER in db")
                return False

            print("user_id : ", user_id)
            return res
        except sqlite3.Error as e:
            print("error getUser  " + str(e))
        return False

    def getUserByEmail(self, email):
        print("getUserByEmail", email)
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()

            if not res:
                print("There is no such USER in db")
                return False

            print("email : ", email)
            return res
        except sqlite3.Error as e:
            print("error getUserByEmail  " + str(e))
        return False

    def getPost(self, post_id):
        try:
            print("post_id", post_id)
            self.__cur.execute(f"SELECT title, text FROM posts WHERE id = {post_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                print(res)

                return (res[0], res[1])
            else:
                print("if res is False")
        except sqlite3.Error as e:
            print("error getPost  " + str(e))
        return (False, False)

    def getHtml(self, alias):
        try:
            print("post_id", alias)
            self.__cur.execute(f"SELECT title, text FROM posts_html WHERE url LIKE '{alias}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                print((res[0], res[1]))

                return (res[0], res[1])
            else:
                print("if res is False")
        except sqlite3.Error as e:
            print("error getHtml  " + str(e))
        return (False, False)

    def getPostsAnonce(self):
        content = []
        try:
            # self.__cur.execute(f"SELECT id, title, text, url FROM posts_html ORDER BY time DESC")
            self.__cur.execute("SELECT id FROM posts_html ORDER BY id")
            ids = self.__cur.fetchall()
            if not ids:
                return (False, False)
            ids_arrey = []
            for elem in ids:
                ids_arrey.append(elem[0])

            self.__cur.execute("SELECT title FROM posts_html ORDER BY id")
            title = self.__cur.fetchall()
            title_arrey = []
            for elem in title:
                title_arrey.append(elem[0])

            self.__cur.execute("SELECT text FROM posts_html ORDER BY id")
            text = self.__cur.fetchall()
            text_arrey = []
            for elem in text:
                text_arrey.append(elem[0])

            self.__cur.execute("SELECT url FROM posts_html ORDER BY id")
            url = self.__cur.fetchall()
            url_arrey = []
            for elem in url:
                url_arrey.append(elem[0])

            for i in range(len(ids_arrey)):
                content.append((ids_arrey[i], title_arrey[i], text_arrey[i], url_arrey[i]))
            # print(content)
            return content
        except sqlite3.Error as e:
            print("error getPostsAnonce.addPost  " + str(e))
        return (False, False)

    def getPostsAnince(self):
        print("getPostsAnince")
        content = []
        try:
            self.__cur.execute(f"SELECT id, title, text FROM posts ORDER BY time DESC")
            self.__cur.execute("SELECT id FROM posts ORDER BY id")
            ids = self.__cur.fetchall()
            if not ids:
                return (False, False)
            ids_arrey = []
            for elem in ids:
                ids_arrey.append(elem[0])

            self.__cur.execute("SELECT title FROM posts ORDER BY id")
            title = self.__cur.fetchall()
            title_arrey = []
            for elem in title:
                title_arrey.append(elem[0])

            self.__cur.execute("SELECT text FROM posts ORDER BY id")
            text = self.__cur.fetchall()
            text_arrey = []
            for elem in text:
                text_arrey.append(elem[0])

            for i in range(len(ids_arrey)):
                content.append((ids_arrey[i], title_arrey[i], text_arrey[i]))
            # print(content)
            return content
        except sqlite3.Error as e:
            print("error getPostsAnince.addPost  " + str(e))
        return (False, False)

    def updateUserAvatar(self, avatar, user_id):
        print("updateUserAvatar")
        if not avatar:
            print(" if not avatar  return False")
            return False

        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("error updateUserAvatar  " + str(e))
            return False
        return True

