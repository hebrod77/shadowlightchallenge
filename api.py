from flask import request
from app_config import app
from logic.base import *

@app.route('/api/v1/ads/metrics', methods=['GET'])
def get_ads_metrics():
    start = request.args.get('start')
    end = request.args.get('end')
    return logic_get_ads_metrics(start, end)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=9090)