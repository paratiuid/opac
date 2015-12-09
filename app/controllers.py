# coding: utf-8

import datetime
from opac_schema.v1.models import Journal, Issue, Article, ArticleHTML
from flask import current_app
from app import dbsql
from . import models as sql_models


def get_journals_alpha():
    COLLECTION = current_app.config.get('OPAC_COLLECTION')
    return Journal.objects(collections__acronym=COLLECTION).order_by('title')


def get_journal_by_jid(jid):
    return Journal.objects(jid=jid).first()


def get_journals_by_jid(jids):
    return Journal.objects.in_bulk(jids)


def set_journal_is_public_bulk(jids, is_public=True):
    """
    """
    for journal in get_journals_by_jid(jids).values():
        journal.is_public = is_public
        journal.save()


def get_issues_by_jid(jid, sort=None):
    if not sort:
        sort = ["-year", "-volume", "-number"]
    return Issue.objects(journal_jid=jid).order_by(*sort)


def get_issue_by_iid(iid):
    return Issue.objects(iid=iid).first()


def get_issues_by_iid(iids):
    return Issue.objects.in_bulk(iids)


def set_issue_is_public_bulk(iids, is_public=True):
    """
    """
    for issue in get_issues_by_iid(iids).values():
        issue.is_public = is_public
        issue.save()


def get_article_by_aid(aid):
    return Article.objects(aid=aid).first()


def get_articles_by_aid(aids):
    return Article.objects.in_bulk(aids)


def set_article_is_public_bulk(aids, is_public=True):
    """
    """

    for article in get_articles_by_aid(aids).values():
        article.is_public = is_public
        article.save()


def get_articles_by_iid(iid):
    return Article.objects(issue_iid=iid)


# -------- SLQALCHEMY --------
def get_user_by_email(email):
    return dbsql.session.query(sql_models.User).filter_by(email=email).first()


def get_user_by_id(id):
    return dbsql.session.query(sql_models.User).get(id)


def set_user_email_confirmed(user):
    user.email_confirmed = True
    dbsql.session.add(user)
    dbsql.session.commit()


def set_user_password(user, password):
    user.password = password
    dbsql.session.add(user)
    dbsql.session.commit()


def filter_articles_by_ids(ids):
    return Article.objects(_id__in=ids)


def new_article_html_doc(language, source):
    return ArticleHTML(language=language, source=source)