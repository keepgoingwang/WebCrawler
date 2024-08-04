import flask
import json

from flask import Flask, render_template, send_from_directory, jsonify
from data_exchange import tranform_data_to_json

'''
Flask 应用,开启后由浏览器访问 http://localhost:5000/
由python后端处理数据,并返回JSON数据,存储于data_tmp文件夹中
前端通过AJAX请求获取数据,进行渲染画面
'''

# 创建 Flask 应用实例
app = Flask(__name__)
template_folder = 'templates'
app.static_folder = 'data_tmp'

# 定义路由和视图函数，用于处理请求
@app.route('/')
def home():
    return render_template('board.html')


@app.route('/get-json/<filename>')
def get_json(filename):
    # 从静态文件夹中发送JSON文件,使得前端可以获取数据
    return send_from_directory(app.static_folder, filename)

# 检查是否是 main 模块，如果是，则运行 Flask 应用
if __name__ == '__main__':
    tranform_data_to_json() # 转换数据
    app.run(debug=True)  # 开启调试模式 debug=True