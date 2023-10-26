import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import mainCode as api
from ui import Ui_MainWindow
from datetime import datetime

import login
import pymysql
import traceback

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

main_ui = Ui_MainWindow()

NAME = 'Mirae makers | Naver Cafe Post Macro'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        main_ui.setupUi(self)     

        window_ico = resource_path('favicon.ico')
        self.setWindowIcon(QIcon(window_ico))

        self.timer = QTimer(self)

        # self.openLogin()     
        
        self.setWindowTitle("Cafe Macro")
        self.browser = None
        self.PATH_IMG1 = None
        self.PATH_IMG2 = None


        self.ids = []
        self.pwds = []
        self.contents = []

        self.selected_category_name = []
        self.selected_category_href = []


        # self.timer.timeout.connect(self.btn_logoutClicked)

        # main_ui.btn_logout.clicked.connect(self.btn_logoutClicked)
        main_ui.btn_get_login_info.clicked.connect(self.btn_get_login_infoClicked)
        main_ui.input_pwd.returnPressed.connect(self.addid)
        main_ui.btn_add_id.clicked.connect(self.btn_add_idClicked)
        main_ui.btn_del_id.clicked.connect(self.btn_del_idClicked)

        main_ui.btn_get_contents.clicked.connect(self.btn_get_contentsClicked)
        main_ui.btn_del_contents.clicked.connect(self.btn_del_contentsClicked)

        main_ui.btn_get_cafe.clicked.connect(self.btn_get_cafeClicked)
        main_ui.btn_getCate.clicked.connect(self.btn_getCateClicked)
        
        main_ui.btn_add.clicked.connect(self.btn_addClicked)
        main_ui.btn_del.clicked.connect(self.btn_delClicked)

        main_ui.btn_get_image_1.clicked.connect(self.btn_get_image_1Clicked)
        main_ui.btn_get_image_2.clicked.connect(self.btn_get_image_2Clicked)
        main_ui.btn_delete_image_1.clicked.connect(self.btn_delete_image_1Clicked)
        main_ui.btn_delete_image_2.clicked.connect(self.btn_delete_image_2Clicked)

        main_ui.btn_start.clicked.connect(self.btn_startClicked)


    # def closeEvent(self, event):
    #     conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
    #     curs = conn.cursor()
    #     sql = "UPDATE n_c_home_userinfo nchu SET login_session = 0 WHERE user_id = %s"
    #     curs.execute(sql, self.second.user_id)
    #     conn.commit()
        
    #     select_query = """
    #     SELECT id, login_session, macro_program_num
    #     FROM n_c_home_userinfo WHERE user_id = %s AND macro_program_num = 1
    #     """
    #     curs.execute(select_query, self.second.user_id)
    #     result = curs.fetchall()
    #     conn.commit()
        
    #     print(result)
    #     date = datetime.now()
        
    #     insert_query = """
    #     INSERT INTO login_log (user_id, macro_program_num, login_date_log, login_status)
    #     VALUES (%s, %s, %s, %s)
    #     """
    #     curs.execute(insert_query, (result[0][0], result[0][2], date, "logout"))
    #     conn.commit()
        
    #     conn.close()
        
    

    # def openLogin(self):
    #     self.hide()
    #     self.second = login.secondWindow()
    #     self.second.exec()
    #     print(self.second.p)
    #     if self.second.p:
    #         self.timer.start(172800000) #48시간
    #         self.show()
    #     else:
    #         sys.exit(0)

    # def btn_logoutClicked(self):
    #     conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
    #     curs = conn.cursor()
    #     sql = "UPDATE n_c_home_userinfo nchu SET login_session = 0 WHERE user_id = %s"
    #     curs.execute(sql, self.second.user_id)
    #     conn.commit()
        
    #     select_query = """
    #     SELECT id, login_session, macro_program_num
    #     FROM n_c_home_userinfo WHERE user_id = %s AND macro_program_num = 1
    #     """
    #     curs.execute(select_query, self.second.user_id)
    #     result = curs.fetchall()
    #     conn.commit()
        
    #     print(result)
    #     date = datetime.now()
        
    #     insert_query = """
    #     INSERT INTO login_log (user_id, macro_program_num, login_date_log, login_status)
    #     VALUES (%s, %s, %s, %s)
    #     """
    #     curs.execute(insert_query, (result[0][0], result[0][2], date, "logout"))
    #     conn.commit()

    #     self.openLogin()
    #     conn.close()
        

    def btn_get_login_infoClicked(self):
        path = QFileDialog.getOpenFileNames(self)    
        for i in path[0]:
            try:
                if i == '':
                    return 
                file = open(i, 'rt', encoding='UTF8')
                
                while True:
                    line = file.readline()
                    if not line:
                        break
                    elif line == '\n':
                        continue
                    line = line.strip().split(' ')
                    if line[0] in self.ids:
                        continue
                    self.ids.append(line[0])
                    self.pwds.append(line[1])
                    main_ui.login_info.addItem(line[0] + '\t' + line[1])
            except:
                j = i.split('/')[-1]
                QMessageBox.information(self,NAME,f'{j}파일 내용이 잘못되었습니다.')
                return 

    def addid(self):
        id = main_ui.input_id.text()
        pwd = main_ui.input_pwd.text()
        if all([id, pwd]):
            if id in self.ids:
                QMessageBox.information(self,NAME,'중복된 아이디 입니다.')
                return
            self.ids.append(id)
            self.pwds.append(pwd)
            main_ui.login_info.addItem(id + '\t' + pwd)
        else:
            return
        
    def btn_add_idClicked(self):
        self.addid()
        
    def btn_del_idClicked(self):
        if main_ui.login_info.currentItem():
            tmp = main_ui.login_info.currentRow()
            main_ui.login_info.takeItem(main_ui.login_info.currentRow())
            self.ids.remove(self.ids[tmp])
            self.pwds.remove(self.pwds[tmp])
        return
    

    def btn_get_contentsClicked(self):
        path = QFileDialog.getOpenFileNames(self)   
        for i in path[0]:
            try:
                if i == '':
                    return 
                file = open(i, 'rt', encoding='UTF8')

                contents = file.read()
                main_ui.content_list.addItem(contents.split(']')[0][1:])
                self.contents.append(contents)
            except:
                j = i.split('/')[-1]
                QMessageBox.information(self,NAME,f'{j} 파일을 읽어오는 도중에 오류가 발생하였습니다.\n파일을 다시 확인해주세요.')
                return 
        

    def btn_del_contentsClicked(self):
        if main_ui.content_list.currentItem():
            tmp = main_ui.content_list.currentRow()
            main_ui.content_list.takeItem(main_ui.content_list.currentRow())
            self.contents.remove(self.contents[tmp])
        return



    def btn_get_cafeClicked(self):
        if len(self.ids) == 0:
            QMessageBox.information(self, NAME, '등록된 로그인 정보가 없습니다.')
            return

        id = self.ids[0]
        pwd = self.pwds[0]

        self.browser = api.naverCafePostStart()
                
        main_ui.cafe_list.clear()
        main_ui.category_list.clear()
        main_ui.selected.clear()

        try:
            api.naverLogin(id, pwd, self.browser)
            
            if self.browser.current_url == 'https://nid.naver.com/nidlogin.login':
                self.browser.close()
                QMessageBox.information(self, NAME, f'{id} 아이디로 로그인에 실패하였습니다. 로그인 정보를 다시 확인해주세요.')
                self.browser = None
                return 
        except Exception as ex:
            QMessageBox.information(self, NAME, '에러가 발생하였습니다. \t\n다시 시도후 동일 증상 발생 시 \t\n관리자에게 문의 바랍니다.')
            
            # date = datetime.now()
            # err_msg = traceback.format_exc()
            
            # conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
            # curs = conn.cursor()
            # select_query = """
            # SELECT id, macro_program_num
            # FROM n_c_home_userinfo
            # WHERE user_id = %s;
            # """
            # curs.execute(select_query, self.second.user_id)
            # conn.commit()
            # e_result = curs.fetchone()
            # print(e_result[0])
            # print(e_result[1])
            
            # insert_query = """
            # INSERT INTO error_msg (user_id, error_message, macro_program_num, date_time)
            # VALUES (%s, %s, %s, %s);
            # """
            # curs.execute(insert_query, (e_result[0], err_msg, e_result[1], date))
            # conn.commit()
            # conn.close()
            
        
        try:
            self.cafe_hrefs, self.cafe_name = api.checkSubscriptionCafe(self.browser)
            main_ui.cafe_list.addItems(self.cafe_name)
        except Exception as ex:
            QMessageBox.information(self, NAME, '에러가 발생하였습니다. \t\n다시 시도후 동일 증상 발생 시 \t\n관리자에게 문의 바랍니다.')
            
            # date = datetime.now()
            # err_msg = traceback.format_exc()
            
            # conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
            # curs = conn.cursor()
            # select_query = """
            # SELECT id, macro_program_num
            # FROM n_c_home_userinfo
            # WHERE user_id = %s;
            # """
            # curs.execute(select_query, self.second.user_id)
            # conn.commit()
            # e_result = curs.fetchone()
            # print(e_result[0])
            # print(e_result[1])
            
            # insert_query = """
            # INSERT INTO error_msg (user_id, error_message, macro_program_num, date_time)
            # VALUES (%s, %s, %s, %s);
            # """
            # curs.execute(insert_query, (e_result[0], err_msg, e_result[1], date))
            # conn.commit()
            # conn.close()
            

    def btn_getCateClicked(self):
        if self.browser is None:
            QMessageBox.information(self, NAME,'카페 불러오기 버튼 먼저 눌러주세요.')
            return
        
        main_ui.category_list.clear()
        
        try:
            self.final_hrefs_true, self.category_name_true = api.CafeCategoryGet(self.browser, self.cafe_hrefs[main_ui.cafe_list.currentIndex().row()])
            self.current_cafe = self.cafe_name[main_ui.cafe_list.currentIndex().row()]
            main_ui.category_list.addItems(self.category_name_true)
        except Exception as ex:
            print("에러 발생!!_2", ex)



    def btn_addClicked(self):
        if main_ui.category_list.currentItem():
            main_ui.selected.addItem('['+ self.current_cafe + '] ' + main_ui.category_list.currentItem().text())
            self.selected_category_href.append(self.final_hrefs_true[self.category_name_true.index(main_ui.category_list.currentItem().text())])
            self.selected_category_name.append(main_ui.category_list.currentItem().text())

        return

    def btn_delClicked(self):
        if main_ui.selected.currentItem():
            tmp = main_ui.selected.currentRow()
            main_ui.selected.takeItem(main_ui.selected.currentRow())
            self.selected_category_href.remove(self.selected_category_href[tmp])
            self.selected_category_name.remove(self.selected_category_name[tmp])

            

    def btn_get_image_1Clicked(self):
        extension = ['png', 'jpg', 'jpeg', 'gif']
        image_path = QFileDialog.getOpenFileName(self)  
        if image_path[0] == '':
            return     
        if image_path[0].split('.')[-1] in extension:
            self.PATH_IMG1 = image_path[0]
            main_ui.image_1.setText(self.PATH_IMG1)
            self.PATH_IMG1 = self.PATH_IMG1.replace("/", "\\")
        else:
            QMessageBox.information(self,NAME,'확장자는 png, jpg, jpeg, gif만 사용 가능합니다.')
        
        return 
    
    def btn_get_image_2Clicked(self):
        extension = ['png', 'jpg', 'jpeg', 'gif']
        image_path = QFileDialog.getOpenFileName(self)  
        if image_path[0] == '':
            return     
        if image_path[0].split('.')[-1] in extension:
            self.PATH_IMG2 = image_path[0]
            main_ui.image_2.setText(self.PATH_IMG2)
            self.PATH_IMG2 = self.PATH_IMG2.replace("/", "\\")
        else:
            QMessageBox.information(self,NAME,'확장자는 png, jpg, jpeg, gif만 사용 가능합니다.')
        
        return 

    def btn_delete_image_1Clicked(self):
        if self.PATH_IMG1:
            self.PATH_IMG1 = None
            main_ui.image_1.setText("")
        else:
            return 
    
    def btn_delete_image_2Clicked(self):
        if self.PATH_IMG2:
            self.PATH_IMG2 = None
            main_ui.image_2.setText("")
        else:
            return 
        


    def btn_startClicked(self):
        date = datetime.now()
        
        if len(self.ids) == 0:
            QMessageBox.information(self, NAME, '등록된 로그인 정보가 없습니다.')
            return

        if self.selected_category_href:
            print("선택한 게시물은 총 ", len(self.selected_category_href), "개 입니다.")
            pass
        else:
            QMessageBox.information(self, NAME,'선택된 게시판이 없습니다!')
            return 
        
        if self.contents:
            pass
        else:
            QMessageBox.information(self, NAME, '작성할 원고를 넣어주세요.')
            return
        
        if main_ui.input_time.text():
            timesleep = main_ui.input_time.text()
        else:
            QMessageBox.information(self, NAME, '작성 딜레이를 넣어주세요.')
            return
        
        if self.browser:
            self.browser.close()
        
        self.browser = api.naverCafePostStart()

        if self.PATH_IMG2 and self.PATH_IMG1:
            PATH_IMG = [self.PATH_IMG1, self.PATH_IMG2]
        elif self.PATH_IMG1:
            PATH_IMG = [self.PATH_IMG1]
        elif self.PATH_IMG2:
            PATH_IMG = [self.PATH_IMG2]
        else:
            PATH_IMG = []

        if main_ui.tags.toPlainText():
            tag_list = main_ui.tags.toPlainText().replace(" ", "").split(',')
        else:
            tag_list = []

        if main_ui.links.toPlainText():
            self.url_list = main_ui.links.toPlainText().replace(" ", "").split("\n")
        else:
            self.url_list = []

        for i in self.contents:
            print(i)
        print('----------------------')
        for i in range(len(self.ids)):
            print(self.ids[i], self.pwds[i])
        print('----------------------')
        for i in self.selected_category_href:
            print(i)
        print('----------------------')

        try:
            rt, self.post_urls = api.start_post_write(self.browser, self.contents, [self.ids, self.pwds], self.selected_category_href, PATH_IMG, tag_list, self.url_list, int(timesleep))
            print("rt : ", rt)
            if rt:
                for i in self.post_urls:
                    main_ui.post_urls.append(i)
                
                # conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
                # curs = conn.cursor()
                # select_query = """
                # SELECT id
                # FROM n_c_home_userinfo
                # WHERE user_id = %s;
                # """
                # curs.execute(select_query, self.second.user_id)
                # result = curs.fetchone()
                # conn.commit()
                
                # insert_query = """
                # INSERT INTO naver_cafe_post (user_id, number_of_cafepost, write_number_of_cafepost ,date_time)
                # VALUES (%s, %s, %s);
                # """
                # curs.execute(insert_query, (result[0], int(len(self.selected_category_href)), int(len(self.post_urls)), date))
                # conn.commit()
                
                # conn.close()
                
                QMessageBox.information(self, NAME, '게시물 작성이 완료되었습니다.')
            else:
                QMessageBox.information(self, NAME, f'{self.post_urls} 아이디로 로그인에 실패하였습니다. 로그인 정보를 다시 확인해주세요.')
                
            
                
        except Exception:
            if rt == 2:
                print("1. 여기에 저장")
                # conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
                # curs = conn.cursor()
                # select_query = """
                # SELECT id, macro_program_num
                # FROM n_c_home_userinfo
                # WHERE user_id = %s;
                # """
                # curs.execute(select_query, self.second.user_id)
                # conn.commit()
                
                # e_result = curs.fetchone()
                # insert_query = """
                # INSERT INTO error_msg (user_id, error_message, macro_program_num, date_time)
                # VALUES (%s, %s, %s, %s);
                # """
                # curs.execute(insert_query, (e_result[0], self.post_urls, e_result[1], date))
                # conn.commit()
                # conn.close()
            else:
                print("2. 여기에 저장")
                # err_msg = traceback.format_exc()
                
                # conn = pymysql.connect(host='mmproject.cgezkk2syeki.ap-northeast-2.rds.amazonaws.com', user='miraemakers', password='445566mmK!', db='mmkdb', charset='utf8')
                # curs = conn.cursor()
                # select_query = """
                # SELECT id, macro_program_num
                # FROM n_c_home_userinfo
                # WHERE user_id = %s;
                # """
                # curs.execute(select_query, self.second.user_id)
                # conn.commit()
                
                # e_result = curs.fetchone()
                # insert_query = """
                # INSERT INTO error_msg (user_id, error_message, macro_program_num, date_time)
                # VALUES (%s, %s, %s, %s);
                # """
                # curs.execute(insert_query, (e_result[0], err_msg, e_result[1], date))
                # conn.commit()
                # conn.close()
            
            QMessageBox.information(self, NAME, '에러가 발생하였습니다. \t\n다시 시도후 동일 증상 발생 시 \t\n관리자에게 문의 바랍니다.')
            
        self.browser = None

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    # sys.exit(1)
        

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook
    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook

    sys.exit(app.exec_())
    
