from flask import jsonify
from app_config import db
from models.base import *

def logic_get_ads_metrics(start, end):
    #result = jsonify(
    #    list(map(lambda view_ads_spend: view_ads_spend.to_dict(), 
    #    ViewAdsSpend.query.filter_by(ViewAdsSpend.date >= start, ViewAdsSpend.date <= end)))
    #)
    result = jsonify(
        list(map(lambda view_ads_spend: view_ads_spend.to_dict(), 
        db.session.query(ViewAdsSpend).filter(ViewAdsSpend.date.between(start,end))
        ))
    )
    db.session.close()
    return result