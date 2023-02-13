from datetime import datetime
from sqlalchemy import desc
from flask import render_template, request, flash, redirect, url_for, abort
from flask.helpers import make_response
from flask_login import current_user
from flask_login.utils import login_required
from web.models import Pastebin
from web.pastebin import bp
from web import db
from web.pastebin.forms import CreatePastebinForm, PrivatePastebin

#-----STARTING METRICS-----
from prometheus_client import (Counter,)

#Home counter
HOME_REQUESTS = Counter('home_requests_total', 'Total number of requests to home endpoint')

#-----FINISHED METRICS-----


@bp.route("/", methods=["GET", "POST"])
def home():

   # Increment counter used for register the total number of calls in the home endpoint
   HOME_REQUESTS.inc()

   form = CreatePastebinForm()

   if request.method == "POST" and form.validate_on_submit():
      new_pastebin = Pastebin(title=form.title.data, content=form.content.data, syntax=form.syntax.data.lower(), user_id=current_user.get_id(), expire_date=form.expire.data.lower(), password=form.password.data)
      response = make_response(redirect(url_for("pastebins.pastebin", link=new_pastebin.link)))
      if form.private.data and form.password.data :
         response.set_cookie(new_pastebin.link, new_pastebin.password)
      db.session.add(new_pastebin)
      db.session.commit()

      flash("Pastebin added!", category="success")
      return response
         
   return render_template("home.html", user=current_user, form=form, public_pastebins=get_public_pastebins())

@bp.route("/<link>", methods=["GET", "POST"])
def pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()
   password_cookie = request.cookies.get(link)
   form = PrivatePastebin()

   #If pastebin expire_date is past current date delete it from db and return 404 error
   if pastebin.is_expired():
      abort(404)

   if request.method == "POST" and form.validate_on_submit():
      if pastebin.check_password(form.password.data):
         response = make_response(render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0), form=form))
         response.set_cookie(link, pastebin.password)
         return response
      else:
         flash("Wrong password.", category="error")

   #If password in cookie is equal to pastebin's password, return render without password attribute else render with password
   if password_cookie == pastebin.password:
      response = make_response(render_template("pastebin.html", user=current_user, pastebin=pastebin, time=datetime.utcnow().replace(microsecond=0), form=form))
   else:
      response = make_response(render_template("pastebin.html", user=current_user, pastebin=pastebin, password=pastebin.password, time=datetime.utcnow().replace(microsecond=0), form=form))
   
   return response

#View raw pastebin
@bp.route("/raw/<link>")
def raw_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()
   password_cookie = request.cookies.get(link)

   if not pastebin.is_expired():   
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            abort(403)
   else:
      abort(404)

#Download pastebin
@bp.route("/download/<link>")
def download_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()
   password_cookie = request.cookies.get(link)

   if not pastebin.is_expired():
      response = make_response(pastebin.content)
      response.headers.add("Content-Type", "text/plain")
      response.headers.add("Content-Disposition", "attachment", filename=link+".txt")

      if not pastebin.password or password_cookie == pastebin.password:
         return response
      else:
         if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
            return response
         else:
            abort(403)
   else:
      abort(404)

#Delete pastebin (Only user can remove his own pastebin)
@login_required
@bp.route("/delete/<link>")
def delete_pastebin(link: str):
   pastebin = Pastebin.query.filter_by(link=link).first_or_404()

   if not pastebin.is_expired():
      if pastebin.user_id and str(pastebin.user_id) == current_user.get_id():
         db.session.delete(pastebin)
         db.session.commit()
         flash("Sucessfully removed pastebin.", category="success")
         return redirect(url_for("users.user"))
      else:
         abort(403)
   else:
      abort(404)

def get_public_pastebins():
   """
   Get last 10 pastebins that are not private
   """
   pastebins = Pastebin.query.order_by(desc(Pastebin.date)).filter_by(password=None).limit(10).from_self()
   for pastebin in pastebins:
      pastebin.is_expired()
   return pastebins
