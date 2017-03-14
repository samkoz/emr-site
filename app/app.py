from flask import Flask, render_template, redirect, url_for, request, flash
from .factory import create_app

app = create_app(__name__)
