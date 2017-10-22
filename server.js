const express = require('express');

const app = express();
const server = require('http').Server(app);

// serves all static files in /public
app.use(express.static(`${__dirname}/public`));

const port = process.env.PORT || 3000;

// start server
server.listen(port, () => {
  console.log(`Listening on port ${port}`);
});

// 'body-parser' middleware for POST
const bodyParser = require('body-parser');
// create application/json parser
const jsonParser = bodyParser.json();
// create application/x-www-form-urlencoded parser

const urlencodedParser = bodyParser.urlencoded({
  extended: false,
});

const { exec } = require('child_process');
const spawn = require('child_process').spawn;

// POST /api/users gets JSON bodies
app.post('/', jsonParser, (req, res) => {
  if (!req.body) return res.sendStatus(400);
  let longitude = req.longVal;
  let latitude = req.latVal;
  let radius = req.distanceVal;
  let query = req.queryVal;
  let cost = req.costVal;

  let executeAPIScript = () => {
    py  = spawn('python', ['./api_caller.py']);
  }
  let executeParam = () => {
    py  = spawn('python', ['./parameterer.py']);
  }
  let executeMLScript = () => {
    // python stuff here
    py  = spawn('python', ['./MachineLearning.py']);
    /*query = "apple"
    data = [query];
    dataString = '';
    //run script
    py.stdout.on('data', function(data){
      dataString += data.toString();
    });*/
    /*py.stdout.on('end', function(){
      console.log('done');
    });
    /*py.stdin.write(JSON.stringify(data));
    py.stdin.end();*/
} 
  let PredictScript = () => {
    py = spawn('python', ['./prediction.py']);
    //data = [longitude, latitude, radius, query, cost]
    /*dataString = '';
    //run script
    py.stdout.on('data', function(data){
      dataString += data.toString();
    });
    py.stdout.on('end', function(){
      console.log('result:',dataString);
    });
    py.stdin.write(JSON.stringify(data));
    py.stdin.end();*/
  }
  console.log("API start");
  /*executeAPIScript();
  executeParam();
  console.log("ML start");
  executeMLScript();*/
  executeAPIScript();
  executeParam();
  executeMLScript();
  PredictScript();

  
  console.log(req.body);
  // create user in req.body
});