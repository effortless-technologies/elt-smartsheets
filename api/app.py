from flask import Flask
import smartsheet, json


app = Flask(__name__)
access_token = "8iorlqtxib1xix8xsrh4tnbwmq"


@app.route('/sheets')
def sheets():

    resp = ss_client.Sheets.list_sheets()

    return resp.to_json()


@app.route('/properties')
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

    return json.dumps(resp)


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

    app.run(debug=True, host='0.0.0.0')
