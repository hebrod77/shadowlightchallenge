from sqlalchemy_serializer import SerializerMixin
from app_config import db

class ViewAdsSpend(db.Model, SerializerMixin):
    __tablename__ = 'v_ads_spend'
    date = db.Column(db.Date, primary_key=True)
    platform = db.Column(db.String(100), primary_key=True)
    account = db.Column(db.String(100), primary_key=True)
    campaign = db.Column(db.String(100), primary_key=True)
    country = db.Column(db.String(100), primary_key=True)
    device = db.Column(db.String(100), primary_key=True)
    spend = db.Column(db.Numeric(10, 2))
    clicks = db.Column(db.Numeric(10))
    impressions = db.Column(db.Numeric(10))
    conversions = db.Column(db.Numeric(10))
    cac = db.Column(db.Numeric(10, 2))
    roas = db.Column(db.Numeric(10, 2))