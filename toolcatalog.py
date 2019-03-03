#!/usr/bin/python
from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   jsonify,
                   url_for,
                   make_response)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Tool, Brand, User
import httplib2
import json
from flask import session as login_session
import random
import string
import urllib

app = Flask(__name__)
app.secret_key = 'marcus'
app.debug = True
engine = create_engine('sqlite:///toolcatalogwithusers.db'
                       '?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = 'amzn1.application-oa2-client.85ec9be03eac431ca601ede5c2fcbd4b'
CLIENT_SECRET = ('6121ea4c40ab6811219ae26e75c647'
                 'facb57bc30ba1257bb14db47209778551e')


@app.route('/brands/JSON')
def brandsJSON():
    brands = session.query(Brand).all()
    return jsonify(Brands=[brand.serialize for brand in brands])


@app.route('/brands/<int:brand_id>/tools/JSON')
def brandToolsJSON(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tools = session.query(Tool).filter_by(brand_id=brand.id).all()
    return jsonify(Tools=[tool.serialize for tool in tools])


@app.route('/brands/<int:brand_id>/tools/<int:tool_id>/JSON')
def toolJSON(brand_id, tool_id):
    tool = session.query(Tool).filter_by(id=tool_id).one()
    return jsonify(Tool=tool.serialize)


@app.route('/')
@app.route('/brands')
def showHomePage():
    brands = session.query(Brand).all()
    if 'username' not in login_session:
        return render_template('tools-catalog-public.html', brands=brands)
    else:
        return render_template('tools-catalog-home.html', brands=brands,
                               user=login_session['username'])


@app.route('/brands/<int:brand_id>')
def showBrandPage(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tools = session.query(Tool).filter_by(brand_id=brand_id).all()
    creator = getUserInfo(brand.user_id)
    if ('username' not in login_session
            or creator.id != login_session['user_id']):
        # User not authenticated -- display public page
        return render_template('brand-public-page.html',
                               brand=brand, tools=tools)
    else:
        return render_template('brand-private-page.html',
                               brand=brand, tools=tools,
                               user=login_session['username'])


@app.route('/brands/create-brand', methods=['GET', 'POST'])
def newBrand():
    if 'username' not in login_session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        newBrand = Brand(name=request.form['name'],
                         description=request.form['description'],
                         user_id=login_session['user_id'])
        session.add(newBrand)
        session.commit()
        return redirect(url_for('showHomePage'))
    else:
        return render_template('newbrand.html', user=login_session['username'])


@app.route('/brands/<int:brand_id>/newtool', methods=['GET', 'POST'])
def newTool(brand_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        newTool = Tool(name=request.form['name'],
                       description=request.form['description'],
                       price=request.form['price'],
                       type=request.form['type'],
                       brand_id=brand_id,
                       user_id=login_session['user_id'])
        session.add(newTool)
        session.commit()
        return redirect(url_for('showBrandPage', brand_id=brand_id))
    else:
        return render_template('newtool.html',
                               brand_id=brand_id,
                               user=login_session['username'])


@app.route('/brands/<int:brand_id>/tools/<int:tool_id>/delete',
           methods=['GET', 'POST'])
def deleteTool(brand_id, tool_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tool = session.query(Tool).filter_by(id=tool_id).one()
    if request.method == 'POST':
        session.delete(tool)
        session.commit()
        return redirect(url_for('showBrandPage', brand_id=brand_id))
    else:
        return render_template('deletetool.html',
                               brand=brand,
                               tool=tool,
                               user=login_session['username'])


@app.route('/brands/<int:brand_id>/tools/<int:tool_id>')
def viewTool(brand_id, tool_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tool = session.query(Tool).filter_by(id=tool_id).one()
    creator = getUserInfo(brand.user_id)
    if ('username' not in login_session
            or creator.id != login_session['user_id']):
        return render_template('tooldetailspublic.html',
                               brand=brand,
                               tool=tool)
    else:
        return render_template('tooldetails.html',
                               brand=brand,
                               tool=tool,
                               user=login_session['username'])


@app.route('/brands/<int:brand_id>/tools/<int:tool_id>/edit',
           methods=['GET', 'POST'])
def editTool(brand_id, tool_id):
    if 'username' not in login_session:
        return redirect(url_for('login'))
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tool = session.query(Tool).filter_by(id=tool_id).one()
    if request.method == 'POST':
        if request.form['name']:
            tool.name = request.form['name']
        if request.form['description']:
            tool.description = request.form['description']
        if request.form['type']:
            tool.type = request.form['type']
        if request.form['price']:
            tool.price = request.form['price']
        session.add(tool)
        session.commit()
        return redirect(url_for('viewTool', brand_id=brand_id, tool_id=tool_id,
                                user=login_session['username']))
    else:
        return render_template('edittool.html', brand=brand, tool=tool,
                               user=login_session['username'])


@app.route('/privacy-policy')
def privacy():
    return render_template('privacypolicy.html')

# emma's page


@app.route('/supersecretpage')
def emma():
    return render_template('emma.html')


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase
                                  + string.digits)for x in xrange(32))
    login_session['state'] = state
    url = ('https://www.amazon.com/ap/oa?client_id=%s&scope=profile'
           '&response_type=code&state=%s'
           '&redirect_uri=https://www.zombietechinc.com'
           '/toolsaplenty/amazonlogin') % (CLIENT_ID, state)

    return render_template('login2.html', STATE=state, url=url)


@app.route('/amazonlogin', methods=['GET', 'POST'])
def amazonlogin():
    code = request.args.get('code', '')
    confirm_state = request.args.get('state', '')
    print code
    print confirm_state
    url = 'https://api.amazon.com/auth/o2/token'
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    body = ('grant_type=authorization_code&code=%s'
            '&redirect_uri=https://www.zombietechinc.com/'
            'toolsaplenty/amazonlogin'
            '&client_id=%s'
            '&client_secret=%s') % (code, CLIENT_ID, CLIENT_SECRET)
    h = httplib2.Http()
    result = h.request(url, 'POST', headers=headers, body=body)[1]
    print 'this is the result'
    print result
    data = json.loads(result)
    access_token = data['access_token']
    print access_token
    profile_url = 'https://api.amazon.com/user/profile'
    profile_request = h.request(profile_url,
                                'GET', headers={"Authorization": "Bearer "
                                                + access_token})[1]
    print 'this is the request'
    print profile_request
    profile_data = json.loads(profile_request)
    print profile_data
    name = profile_data["name"]
    email = profile_data["email"]
    print email
    login_session['username'] = profile_data['name']
    login_session['email'] = profile_data['email']
    login_session['provider'] = 'amazon'

    # check database for user. If the user does not exist, create a new one
    user_id = getUserID(email)
    if not user_id:
        print 'No user found, creating new one'
        print login_session['username']
        print login_session['email']
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    print user_id
    print name
    print email
    return redirect(url_for('showHomePage'))


@app.route('/disconnect')
def disconnect():
    del login_session['username']
    del login_session['email']
    del login_session['provider']
    return redirect(url_for('showHomePage'))

# implement user creation and user lookup


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    user = session.query(User).filter_by(email=email).one_or_none()
    return user.id


if __name__ == '__main__':
    app.run()
