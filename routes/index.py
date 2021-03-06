from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)
from werkzeug.utils import secure_filename
from models.user import User
from config import user_file_dir
import os

from utils import log

main = Blueprint('index', __name__)


def current_user():
    # 从 session 中找到 user_id 字段, 找不到就 -1
    # 然后 User.find_by 来用 id 找用户
    # 找不到就返回 None
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
def index():
    u = current_user()
    return render_template("index.html", user=u)


@main.route("/login_err")
def login_err():
    return render_template("login_err.html")


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('.login_err'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile/<username>')
def profile(username):
    u = User.find_by(username = username)
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    # file 是一个上传的文件对象
    file = request.files['file']
    if allow_file(file.filename):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        filename = secure_filename(file.filename)
        # 2017/6/14/19/56/yiasduifhy289389f.png
        file.save(os.path.join(user_file_dir, filename))
        # u.add_avatar(filename)
        u.user_image = '/uploads/' + filename
        u.save()

    return redirect(url_for(".profile",username = u.username))


# send_from_directory
# nginx 静态文件
@main.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(user_file_dir, filename)
