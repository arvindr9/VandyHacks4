const express = require('express');

const app = express();
const server = require('http').Server(app);

// serves all static files in /public
app.use(express.static(`${__dirname}/public`));

const port = process.env.PORT || 8000;

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


const spawn = require('child_process').spawn;

// POST /api/users gets JSON bodies
app.post('/', jsonParser, (req, res) => {
  if (!req.body) return res.sendStatus(400);
  const longitude = req.longVal;
  const latitude = req.latVal;
  const radius = req.distanceVal;
  const query = req.

  let executeAPIScript = () => {
    // python stuff here
    py  = spawn('python', ['./api_caller.py']);
   data = [query]
   // data = [latitude, longitude, radius, category]
   // dataString = '';
    //run script
   /* py.stdout.on('data', function(data){
      dataString += data.toString();
    });
    py.stdout.on('end', function(){
      console.log('result:',dataString);
    });
    py.stdin.write(JSON.stringify(data));
    py.stdin.end();*/
  }
  let executeMLScript = () => {
    // python stuff here
    py  = spawn('python', ['./MachineLearning.py']);
    /*data = []
    dataString = '';
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
  executeAPIScript();
  console.log("ML start");
  executeMLScript();

  
  console.log(req.body);
  // create user in req.body
});