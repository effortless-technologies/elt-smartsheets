from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
import smartsheet, json
import requests


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/properties": {"origins": "*"}})

access_token = "8iorlqtxib1xix8xsrh4tnbwmq"

token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZG1pbiI6dHJ1ZSwiZ' \
        'XhwIjoxNTI2NDAyMjAzLCJmcmFuY2hpc2VfaWQiOjAsIm5hbWUiOiIiLCJyb2xlIj' \
        'oiIn0.aiMBSdrlpR_XdmJsiDcvAMd4isp5IVUhUgw_kHJVA0o'


@app.route('/sheets')
def sheets():

    resp = ss_client.Sheets.list_sheets()

    return resp.to_json()


@app.route('/properties', methods=['GET'])
@cross_origin('*')
def properties():
    
    sheet = ss_client.Sheets.get_sheet(2398906471475076)
    cols = sheet.columns.to_list()
    rows = sheet.rows.to_list()

    resp = dict()

    schema = list()
    for i, col in enumerate(cols):
        column = dict()
        column['title'] = col.title
        column['id'] = col.id
        schema.append(column)

    resp['schema'] = schema

    payload = dict()
    for i, row in enumerate(rows):
        item = dict()
        for j, cell in enumerate(row.cells):
            item[str(cell._column_id)] = cell._value
        payload[row.id] = item

    resp['payload'] = payload
    resp['count'] = len(payload)

    return json.dumps(resp)


@app.route('/port', methods=['GET'])
def port():

    column_id = request.args.get('column_id')
    property_param = request.args.get('property_param')

    sheet = ss_client.Sheets.get_sheet(2398906471475076)
    cols = sheet.columns.to_list()
    rows = sheet.rows.to_list()

    schema = list()
    for i, col in enumerate(cols):
        column = dict()
        column['title'] = col.title
        column['id'] = col.id
        schema.append(column)

    payload = dict()
    for i, row in enumerate(rows):
        item = dict()
        for j, cell in enumerate(row.cells):
            item[str(cell._column_id)] = cell._value
        payload[row.id] = item

    param_array = list()
    param_value = ""
    lodgix_id = -1
    for k, v in payload.items():
        for kk, vv in v.items():
            if kk == '5806974957840260':
                lodgix_id = vv
            if kk == column_id:
                param_value = vv
        param_dict = dict()
        param_dict['lodgix_id'] = lodgix_id
        param_dict['param_value'] = param_value
        param_array.append(param_dict)

    uri = 'http://104.197.53.226:7001/restricted/properties'

    resp = requests.get(
        url=uri,
        headers={'Authorization': token},
    )

    update_array = list()
    properties = json.loads(resp.content)
    print(properties)
    for i, p in enumerate(properties):
        for ii, pp in enumerate(param_array):
            if p['lodgix_id'] == pp['lodgix_id']:
                update = dict()
                update['param_name'] = property_param
                update['param_value'] = pp['param_value']
                update['property_id'] = p['id']
                update_array.append(update)

    responses = list()
    for i, ua in enumerate(update_array):
        if ua['param_name'] != None:
            data = {ua['param_name']: ua['param_value']}
            uri = 'http://104.197.53.226:7001/restricted/properties/' \
                  + ua['property_id']

            headers = {
                'Authorization': token,
                'content-type': 'application/json',
            }
            resp = requests.put(url=uri, headers=headers, json=data)
            payload = {
                'property_id': ua['property_id'],
                'status_code': resp.status_code,
                'param_changed': ua['param_name'],
                'new_param_value': ua['param_value'],
            }
            responses.append(payload)

    return json.dumps(responses)


@app.route('/columns')
def columns():

    sheet = ss_client.Sheets.get_sheet(2398906471475076)
    cols = sheet.columns.to_list()

    for i, col in enumerate(cols):
        print(col.title)

    return cols[0].to_json()


@app.route('/rows')
def rows():

    sheet = ss_client.Sheets.get_sheet(2398906471475076)
    rows = sheet.rows.to_list()
    print(type(rows))
    for i, row in enumerate(rows):
        print(row)

    return rows[0].to_json()


@app.route('/debug')
def debug():

    sheet = ss_client.Sheets.get_sheet(2398906471475076)
    cols = sheet.columns.to_list()

    payload = list()
    for i, col in enumerate(cols):
        column = dict()
        column['title'] = col.title
        column['id'] = col.id
        payload.append(column)

    return json.dumps(payload)


if __name__ == '__main__':

    ss_client = smartsheet.Smartsheet(access_token)
    ss_client.errors_as_exceptions(True)

    app.run(debug=True, host='0.0.0.0', threaded=True)
