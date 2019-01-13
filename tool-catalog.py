#!/usr/bin/python
from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Tool, Brand, User

app = Flask(__name__)

engine = create_engine('sqlite:///toolcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/tools')
def showHomePage():
    brands = session.query(Brand).all()
    print('these are the brands: ')
    print (brands)
    return render_template('tools-catalog-home.html', brands=brands)

@app.route('/tools/<int:brand_id>')
def showBrandPage(brand_id):
    brand = session.query(Brand).filter_by(id=brand_id)
    tools = session.query(Tool).filter_by(brand_id=brand_id).all()
    print ('these are the tools')
    print (tools)
    return render_template('brand-public-page.html', brand=brand, tools=tools)


if __name__ == '__main__':
    app.secret_key = 'marcus'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
