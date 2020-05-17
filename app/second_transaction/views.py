from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from . import transaction
from .. import db
from ..decorators import permission_required
from ..models import Transaction, Permission


@transaction.route('/new_transaction', methods=['GET', 'POST'])
def new_transaction():
    if request.method == 'GET':
        return render_template('transaction/new_transaction.html')
    if request.method == 'POST':
        name = request.form["item_name"]
        describe = request.form["item_describe"]
        link = request.form["link"]
        mode = request.form["transaction_mode"]
        wechat = request.form["seller_WeChat"]
        if name == "" or describe == "" or link == "" or mode == "" or wechat == "":
            flash("Item information cannot be empty")
            return render_template('transaction/new_transaction.html')
        trans = Transaction(item_name=name,
                            item_describe=describe,
                            link=link,
                            transaction_mode=mode,
                            seller_WeChat=wechat,
                            seller_id=current_user.id,
                            seller=current_user
                            )
        db.session.add(trans)
        db.session.commit()
        flash('Your transaction request has been sent!')
        return redirect(url_for('.index'))


@transaction.route('/sold/<item_id>')
def sold_item(item_id):
    transactions = Transaction.query.filter_by(id=item_id).first()
    transactions.is_sold = True
    db.session.add(transactions)
    db.session.commit()
    return redirect(url_for('.user', username=current_user.username))


@transaction.route('/collect/<transaction_id>')
@permission_required(Permission.FOLLOW)
def collect(transaction_id):
    transactions = Transaction.query.filter_by(id=transaction_id).first()
    if transactions is None:
        flash('Invalid transaction.')
        return redirect(url_for('.index'))
    if current_user.is_collecting(transactions):
        flash('You are already collecting this post.')
        return redirect(url_for('.index', id=transaction_id))
    current_user.collect(transactions)
    transactions.collect(current_user)
    transactions.recent_activity = datetime.utcnow()
    db.session.commit()
    flash('You are now collecting this post')
    return redirect(url_for('.index', id=transaction_id))


@transaction.route('/not_collect/<transaction_id>')
@permission_required(Permission.FOLLOW)
def not_collect(transaction_id):
    transactions = Transaction.query.filter_by(id=transaction_id).first()
    if transactions is None:
        flash('Invalid transaction.')
        return redirect(url_for('.index'))
    if not current_user.is_collecting(transactions):
        flash('You are not collecting this post.')
        return redirect(url_for('.transaction', id=transaction_id))
    current_user.not_collect(transactions)
    transactions.not_collect(current_user)
    db.session.commit()
    flash('You are not collecting this post')
    return redirect(url_for('.index', id=transaction_id))
