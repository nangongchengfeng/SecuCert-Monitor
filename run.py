# -*- coding: utf-8 -*-
# @Time    : 2024-04-15 15:58
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : run.py
# @Software: PyCharm
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, threaded=True, host='0.0.0.0', port=5000)