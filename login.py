import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from login_ui import Ui_Form
from datetime import datetime

import pymysql

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

login_ui = Ui_Form()

NAME = 'Mirae makers | Naver Cafe Post Macro'

TABLE = 'n_c_home_userinfo nchu'


class secondWindow(QDialog,QWidget):
    def __init__(self):
        super(secondWindow, self).__init__()
        login_ui.setupUi(self)     
        self.setWindowTitle(NAME)

        window_ico = resource_path('favicon.ico')
        self.setWindowIcon(QIcon(window_ico))
        
        self.show()

        self.p = 0
        self.user_id = None
        self.user_pwd = None
        
        login_ui.btn_startLogin.clicked.connect(self.btn_startLoginClicked)


    def btn_startLoginClicked(self):
        self.user_id = login_ui.start_id.text()
        self.user_pwd = login_ui.start_pwd.text()
        self.conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')

        if all([self.user_id, self.user_pwd]):
            try:
                curs = self.conn.cursor()
                sql = "SELECT id, user_id, user_pw, login_session, macro_program_num FROM n_c_home_userinfo nchu WHERE user_id = %s AND macro_program_num = 1"
                curs.execute(sql, self.user_id)
                result = curs.fetchall()
                self.conn.commit()
                print(result)
                print(self.user_id, self.user_pwd)

                try:
                    if self.user_pwd in result[0]:
                        print('비밀번호 일치')
                        if result[0][3]:
                            print('이미 로그인 됨')
                            QMessageBox.information(self,NAME,'이미 로그인된 아이디 입니다.')
                            return
                        print('로그인 성공')
                        self.p = 1
                        sql = "UPDATE n_c_home_userinfo nchu SET login_session = 1 WHERE user_id = %s"
                        curs.execute(sql, self.user_id)
                        self.conn.commit()
                        
                        date = datetime.now()
                        insert_query = """
                        INSERT INTO login_log (user_id, macro_program_num, login_date_log, login_status)
                        VALUES (%s, %s, %s, %s);
                        """
                        curs.execute(insert_query, (result[0][0], result[0][4], date, "login"))
                        self.conn.commit()
                        
                        self.close()
                        return
                except:
                    QMessageBox.information(self,NAME, '로그인 정보가 일치하지 않습니다.')
                    return

            # 오류가 발생해도 반드시 실행
            finally:
                self.conn.close()


            QMessageBox.information(self,NAME, '로그인 정보가 일치하지 않습니다.')
            return
        else:
            QMessageBox.information(self,NAME,'아이디와 비밀번호를 모두 입력해주세요.')
            return
        