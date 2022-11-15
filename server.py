from flask import Flask
from flask import request, redirect

app = Flask(__name__)

nextId = 4
topics = [
    {'id': 1, 'title': 'html', 'body': 'html is ...'},
    {'id': 2, 'title': 'css', 'body': 'css is ...'},
    {'id': 3, 'title': 'javascript', 'body': 'javascript is ...'}
]
# 리스트와 딕셔너리 등의 메모리에 올라가는 데이터를 사용
# 쓰기 기능 구현 시, 애플리케이션 종료되면 원래 값으로 돌아감

def template(contents, content, id=None):
    contextUI = ''
    if id != None:      # id가 존재할 때 contextUI가 생성됨
        contextUI = f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
            {content}
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
    </html>
    '''

def getContents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

@app.route('/')
def index():
    return template(getContents(), '<h2>Welcome</h2>Hello, web')
# 브라우저 입장에서는 html을 작성하든, flask를 이용하여 작성하든 결과적으로 html만 해석함.
# html 코드 작성은 정적. flask는 동적 작성이 가능함.

@app.route('/create/', methods=['GET', 'POST'])
def create():
    # form 태그: 사용자가 입력한 정보를 서버로 전송하는 기능을 하는 태그
    if request.method == 'GET':
        content = '''
        <form action="/create/" method="POST">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit" value="create"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId                           # 전역변수 nextId를 수정하기 전에 함수에게 nextId가 전역변수임을 알림.
        title = request.form['title']
        body = request.form['body']
        newTopic = {'id': nextId, 'title': title, 'body': body}
        topics.append(newTopic)
        url = '/read/' + str(nextId) + '/'
        nextId = nextId + 1
        return redirect(url)
        # request.form 방식을 통해 POST한 title과 body를 가져올 수 있다. 

@app.route('/read/<int:id>/')   # 동적 변수 설정. id가 string이기 때문에, 이를 integer로 변경하여 넣음
def read(id):
    title = ''
    body = ''
    for topic in topics:
        if id == topic['id']:
            title = topic['title']
            body = topic['body']
            break
    return template(getContents(), f'<h2>{title}</h2>{body}', id)

@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        title = ''
        body = ''
        for topic in topics:
            if id == topic['id']:
                title = topic['title']
                body = topic['body']
                break
        content = f'''
        <form action="/update/{id}/" method="POST">
            <p><input type="text" name="title" placeholder="title" value="{title}"></p>
            <p><textarea name="body" placeholder="body">{body}</textarea></p>
            <p><input type="submit" value="update"></p>
        </form>
        '''
        return template(getContents(), content)
    elif request.method == 'POST':
        global nextId
        title = request.form['title']
        body = request.form['body']
        for topic in topics:
            if id == topic['id']:
                topic['title'] = title
                topic['body'] = body
                break
        url = '/read/' + str(id) + '/'
        return redirect(url)

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    return redirect('/')

app.run(port=5001)
# app.run(port=5001, debug=True)
# port=5001: flask 동작은 port 5001에서 동작함.
# debug=True: 디버깅 모드로 open. 내용 수정 시, 자동으로 flask off & on.
# 실제 서비스 시에는 디버깅 모드 꺼야 함.