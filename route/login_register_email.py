from .tool.func import *

def login_register_email_2(conn):
    curs = conn.cursor()
    
    if not 'reg_id' in flask.session:
        return redirect('/register')
    
    if flask.request.method == 'POST':
        flask.session['reg_key'] = load_random_key(6)

        user_email = flask.request.form.get('email', '')
        email_data = re.search(r'@([^@]+)$', user_email)
        if email_data:
            email_data = email_data.group(1)
            
            curs.execute(db_change(
                "select html from html_filter where html = ? and kind = 'email'"
            ), [email_data])
            if not curs.fetchall():                
                return redirect('/email_filter')

        curs.execute(db_change('select data from other where name = "email_title"'))
        sql_d = curs.fetchall()
        if sql_d and sql_d[0][0] != '':
            t_text = html.escape(sql_d[0][0])
        else:
            t_text = wiki_set()[0] + ' 인증코드'
        i_text = '[ 한마위 ]\n한마위에 가입해주셔서 감사해요.\n인증코드는 ' + str(flask.session.get('reg_key')+' 에요.\n만약 가입하지않았다면 잘못온걸수도있으니 무시해주세요!')
    

        curs.execute(db_change('select id from user_set where name = "email" and data = ?'), [user_email])
        if curs.fetchall():
            return re_error('/error/35')

        if send_email(user_email, t_text, i_text) == 0:
            return re_error('/error/18')

        flask.session['reg_email'] = user_email

        return redirect('/register/email/check')
    else:
        curs.execute(db_change('select data from other where name = "email_insert_text"'))
        sql_d = curs.fetchall()
        b_text = (sql_d[0][0] + '<hr class="main_hr">') if sql_d and sql_d[0][0] != '' else ''

        return easy_minify(flask.render_template(skin_check(),
            imp = [load_lang('email'), wiki_set(), wiki_custom(), wiki_css([0, 0])],
            data = '''
                <a href="/email_filter">(''' + load_lang('email_filter_list') + ''')</a>
                <hr class="main_hr">
                ''' + b_text + '''
                <form method="post">
                    <input placeholder="''' + load_lang('email') + '''" name="email" type="text">
                    <hr class="main_hr">
                    <button type="submit">''' + load_lang('save') + '''</button>
                </form>
            ''',
            menu = [['user', load_lang('return')]]
        ))
