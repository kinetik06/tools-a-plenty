#!/usr/bin/python
from flask import Flask, render_template, request, redirect, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

@app.route('/')
@app.route('/tools')
def showHomePage():
    return render_template('tools-catalog-home.html')

@app.route('/tools/<int:')


if __name__ == '__main__':
    app.secret_key = 'marcus'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
