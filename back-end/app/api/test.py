from flask import jsonify
from . import bp
from ...utils import mail
from flask import current_app


@bp.route('/test1', methods=['GET'])
def test1():
    return jsonify('It\'s a test message!')


@bp.route('/test2/<email>', methods=['GET'])
def test2(email):
    text_body = '''
                欢迎注册中国电信中山分公司人员招聘系统！
                点击链接完成账户激活：{}
                注意: 不要回复该邮件。
                '''.format('123')

    html_body = '''
                <p>欢迎注册<b>中国电信中山分公司人员招聘系统</b>！</p>
                <p>请点击该链接完成账户验证 <a href="{0}">点击这里</a>。</p>
                <p>如果打不开可以复制链接到浏览器窗口打开。</p>
                <p><b>{0}</b></p>
                <p><small>注意: 不要回复该邮件。</small></p>
                '''.format('123')

    mail.send_email('[中国电信中山分公司] 邮箱验证',
                    sender=current_app.config['MAIL_SENDER'],
                    recipients=[email],
                    text_body=text_body,
                    html_body=html_body)

    return jsonify({'message': 'good!'})
