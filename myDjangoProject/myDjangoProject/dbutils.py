#coding:utf-8 
import sqlite3
import os

#数据库文件绝句路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

#表名称
TABLE_NAME = 'app_name_test'
#是否打印sql
SHOW_SQL = True

def get_conn(path):
  '''获取到数据库的连接对象，参数为数据库文件的绝对路径
     如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
     路径下的数据库文件的连接对象；否则，返回内存中的数据接
     连接对象'''
  conn = sqlite3.connect(path)
  if os.path.exists(path) and os.path.isfile(path):
    print('local:[{}]'.format(path))
    return conn
  else:
    conn = None
    print('memory:[:memory:]')
    return sqlite3.connect(':memory:')

def get_cursor(conn):
  '''该方法是获取数据库的游标对象，参数为数据库的连接对象
  如果数据库的连接对象不为None，则返回数据库连接对象所创
  建的游标对象；否则返回一个游标对象，该对象是内存中数据
  库连接对象所创建的游标对象'''
  if conn is not None:
    return conn.cursor()
  else:
    return get_conn('').cursor()

def close_all(conn, cu):
  '''关闭数据库游标对象和数据库连接对象'''
  try:
    if cu is not None:
      cu.close()
  finally:
    if cu is not None:
      cu.close()

def save(conn, sql, data):
  '''插入数据'''
  if sql is not None and sql != '':
    if data is not None:
      cu = get_cursor(conn)
      for d in data:
        if SHOW_SQL:
          print('execute sql:[{}],paramers:[{}]'.format(sql, d))
        cu.execute(sql, d)
        conn.commit()
      close_all(conn, cu)
  else:
    print('the [{}] is empty or equal None!'.format(sql))

def fetchone(conn, sql, data):
  '''查询一条数据'''
  if sql is not None and sql != '':
    if data is not None:
      #Do this instead
      d = (data,) 
      cu = get_cursor(conn)
      if SHOW_SQL:
        print('execute sql:[{}],paramers:[{}]'.format(sql, data))
      cu.execute(sql, d)
      r = cu.fetchall()
      if len(r) > 0:
        for e in range(len(r)):
        	return r[e]
      else:
        print('the [{}] equal None!'.format(data))
  else:
    print('the [{}] is empty or equal None!'.format(sql))
 
def update(conn, sql, data):
  '''更新数据'''
  if sql is not None and sql != '':
    if data is not None:
      cu = get_cursor(conn)
      for d in data:
        if SHOW_SQL:
          print('execute sql:[{}],paramers:[{}]'.format(sql, d))
        cu.execute(sql, d)
        conn.commit()
      close_all(conn, cu)
  else:
    print('the [{}] is empty or equal None!'.format(sql))

#####################################################################################
## Test
#####################################################################################
def fetchone_test():
    '''查询一条数据...'''
    print('query one row...')
    fetchone_sql = 'SELECT * FROM app_name_test limit 0,?'
    data = 1
    conn = get_conn(DB_FILE_PATH)
    return fetchone(conn, fetchone_sql, data)

def init():
    '''初始化方法'''
    #数据库文件绝句路径
    global DB_FILE_PATH
    DB_FILE_PATH = 'C:\\A-LICHUNHUI\\14_python\\myDjangoProject\\db.sqlite3'
    #数据库表名称
    global TABLE_NAME
    TABLE_NAME = 'app_name_test'
    #是否打印sql
    global SHOW_SQL
    SHOW_SQL = True
    print('show_sql : {}'.format(SHOW_SQL))

    

def main():
    init()
    r = fetchone_test()
    print r


if __name__ == '__main__':
    main()