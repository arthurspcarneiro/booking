from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm, TradeForm, LegForm
from .. import db
from ..models import Permission, Role, User, Post, Trade
from ..decorators import admin_required
import numexpr as ne
import numpy as np

@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                           pagination=pagination)
#straddle, strangle, trava, 
@main.route('/booking', methods=['GET', 'POST'])
@login_required
def booking_trade():
    print("again")
    form1 = TradeForm(prefix="form1")
    form2 = TradeForm(prefix="form2")
    form3 = TradeForm(prefix="form3")
    form4 = TradeForm(prefix="form4")
    form5 = TradeForm(prefix="form5")
    forms = [(1,form1),(2,form2),(3,form3),(4,form4),(5,form5)]
    #forms = [TradeForm() for x in range(legsForm.order.data)]
    #forms = [(1,form1),(2,form2)]
    if request.method == 'POST':
        print("here aaa")
        trades = []
        central = 0.
        graphic = False
        for form in forms:
            print(form[1].validate_on_submit())
            if form[1].validate_on_submit():
                trade = Trade(order = form[1].order.data,\
                    product = form[1].product.data,code = form[1].code.data,\
                    strategy = form[1].strategy.data,\
                    trade_date = form[1].trade_date.data,\
                    strike = form[1].strike.data,amount = form[1].amount.data,\
                    price = form[1].price.data,
                    trade_user = current_user._get_current_object() ) 
                trades.append(trade)
                central += float(trade.strike)
                graphic = True
        if graphic:
            central /= len(trades)
            s,payoff = trades[0].payoff(central)
            for trade in trades[1:]:
                s,payoff2 = trade.payoff(central)
                payoff += payoff2
            values =  np.column_stack((s,payoff))
            legend = 'Payoff'
            return render_template('booking.html', forms=forms, values=values,legend=legend)
 
        return render_template('booking.html', forms=forms)
        #return render_template('chart.html', values=values, legend=legend)


    if current_user.can(Permission.WRITE) and form1.validate_on_submit() and form2.validate_on_submit():
            trade = Trade(order = form1.order.data,\
                product = form1.product.data,code = form1.code.data,\
                    strategy = form1.strategy.data,\
                    trade_date = form1.trade_date.data,\
                    strike = form1.strike.data,amount = form1.amount.data,\
                    price = form1.price.data,
                    trade_user = current_user._get_current_object() ) 
            values = trade.payoff()
            db.session.add(trade)
            db.session.commit()
            trade = Trade(order = form2.order.data,\
                product = form2.product.data,code = form2.code.data,\
                    strategy = form2.strategy.data,\
                    trade_date = form2.trade_date.data,\
                    strike = form2.strike.data,amount = form2.amount.data,\
                    price = form2.price.data,
                    trade_user = current_user._get_current_object() ) 
            db.session.add(trade)
            db.session.commit()
            flash('The trade has been booked.')
            return redirect(url_for('.portfolio',username=current_user.username))
    return render_template('booking.html', forms=forms)


@main.route('/portfolio/<username>')
@login_required
def portfolio(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.trades.order_by(Trade.trade_date_ping.desc()).paginate(page, \
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],\
        error_out=False)
    trades = pagination.items
    print(pagination.items)
    print(len(pagination.items))
    return render_template('portfolio.html', user=user, trades=trades,\
                           pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    print(page)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],\
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMIN):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated.')
        return redirect(url_for('.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

@login_required
@main.route("/simple_chart/<int:id>", methods=['GET', 'POST'])
def basechart(id):
    trade = Trade.query.filter_by(id=id).first_or_404()
    values = np.column_stack(trade.payoff())
    legend = 'Payoff'
    return render_template('chart.html', values=values, legend=legend)
