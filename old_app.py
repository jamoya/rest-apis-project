from flask import Flask, request
app = Flask(__name__)
stores = [
    {
        'name': 'My Store',
        'items':[
            {"name":"CHAIR","price":15.99}
        ]
    }
]

@app.get('/store')     # http://127.0.0.1:5000
def get_stores():
    return {"stores": stores}

@app.post('/store')     # http://127.0.0.1:5000
def create_stores():
    request_data = request.get_json()
    new_store = {"name":request_data["name"],"items":[]}
    stores.append(new_store)
    #print("stores in app.post('/store')/n",stores)
    return new_store, 201

@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    #print("stores in app.post('/store/<string:name>/item')\n",stores)
    #print("request_data\n",request_data)
    for store in stores:
        #print('store=',store["name"],name)
        if store["name"] == name:
            new_item = {"name":request_data["name"],"price":request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message":"Mecachis, Store not found"}, 404

@app.get('/store/<string:name>')     # http://127.0.0.1:5000
def get_store(name):
    for store in stores:
        if store['name']== name:
            return store, 200
    return {"message":"Mecachis, Store not found"}, 404

@app.get('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store['items']}
    return {"message":"Mecachis, Store not found"}, 404
