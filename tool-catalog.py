#!/usr/bin/python
from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Tool, Brand, User

app = Flask(__name__)

engine = create_engine('sqlite:///toolcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/brands')
def showHomePage():
    brands = session.query(Brand).all()
    print('these are the brands: ')
    print (brands)
    return render_template('tools-catalog-home.html', brands=brands)

@app.route('/brands/<int:brand_id>')
def showBrandPage(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tools = session.query(Tool).filter_by(brand_id=brand_id).all()
    print ('Brand: ')
    print (brand.id)
    print ('these are the tools')
    print (tools)
    return render_template('brand-public-page.html', brand=brand, tools=tools)

@app.route('/brands/create-brand', methods=['GET', 'POST'])
def newBrand():
    if request.method == 'POST':
        newBrand = Brand(name = request.form['name'], description = request.form['description'])
        session.add(newBrand)
        session.commit()
        return redirect(url_for('showHomePage'))
    else:
        return render_template('newbrand.html')

@app.route('/brands/<int:brand_id>/newtool', methods=['GET', 'POST'])
def newTool(brand_id):
    if request.method == 'POST':
        newTool = Tool(name = request.form['name'], description = request.form['description'], price = request.form['price'],
            type = request.form['type'], brand_id = brand_id)
        session.add(newTool)
        session.commit()
        return redirect(url_for('showBrandPage', brand_id = brand_id))
    else:
        return render_template('newtool.html', brand_id = brand_id)

@app.route('/brands/<int:brand_id>/tools/<int:tool_id>/delete', methods=['GET', 'POST'])
def deleteTool(brand_id, tool_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tool = session.query(Tool).filter_by(id=tool_id).one()
    if request.method == 'POST':
        session.delete(tool)
        session.commit()
        return redirect(url_for('showBrandPage', brand_id=brand_id))
    else:
        return render_template('deletetool.html', brand = brand,  tool = tool)

@app.route('/brands/<int:brand_id>/tools/<int:tool_id>')
def viewTool(brand_id, tool_id):
    brand = session.query(Brand).filter_by(id=brand_id).one()
    tool = session.query(Tool).filter_by(id = tool_id).one()
    return render_template('tooldetails.html', brand = brand, tool = tool)

@app.route('/brands/<int:brand_id>/tools/<int:tool_id>/edit', methods = ['GET', 'POST'])
def editTool(brand_id, tool_id):
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
        return redirect(url_for('viewTool', brand_id = brand_id, tool_id = tool_id))
    else:
        return render_template('edittool.html', brand = brand, tool = tool)



if __name__ == '__main__':
    app.secret_key = 'marcus'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
