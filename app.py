from flask import Flask, render_template , request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "database.db"