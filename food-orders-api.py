import flask
from flask import render_template
import json
import pymongo

# client = pymongo.MongoClient(
#    "mongodb+srv://ryanhaber:ryanhaber@localhost:27017/test?retryWrites=true&w=majority")
# db = client.test

app = flask.Flask(__name__)
app.config["DEBUG"] = True


class ordersList:
	allOrders = {}
	lastIdNumber = 0;

	def createOrderId(self):
		self.lastIdNumber = self.lastIdNumber + 1;
		return( self.lastIdNumber )
	
	def createOrder(self, foodItem):
		if foodItem == "":
			return("no order")
		else:
			orderId = self.createOrderId()
			theOrder = {'orderId': str(orderId), 'food': foodItem}
			self.allOrders[str(orderId)] = theOrder
		return(self.allOrders[str(orderId)])


	def getOrderById(self, reqOrderId):
		itemId = str(reqOrderId)
		if self.allOrders[itemId] == None:
			return("no order with that number")
		return(self.allOrders[itemId])


	def getAllOrders(self):
		return(json.dumps(self.allOrders))




#----------------------------


myOrderList = ordersList()


#----------------------------


@app.route('/', methods=['GET'])
def home():
	apidocs = {
	'POST': {'/orders/<string:foodname>': 'creates an order of foodname, returns created resource'},
	'GET': [{'/orders/': 'returns the list of food orders'},
			{'/orders/<int:ordernumber>': 'returns the order resource specified by ordernumber'}]
	}
	return apidocs

@app.route('/orders/', methods=['GET'])
def get_all_orders():
	return(myOrderList.getAllOrders())


@app.route('/orders/<int:ordernumber>', methods=['GET'])
def get_order(ordernumber=None):
	if not ordernumber:
		return "list of orders"
	else:
		return myOrderList.getOrderById(ordernumber)
		# jinja2 !!!
		#return render_template('orderdetailspage.html', order=ordernum)


@app.route('/orders/<string:food>', methods=['POST'])
def post_orders(food = ''):
	return( myOrderList.createOrder(food) )

	
app.run()