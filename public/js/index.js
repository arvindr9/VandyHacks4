const spawn = require('child_process').spawn,

const express = require('express');

const app = express();

// serves all static files in /public
app.use(express.static(`${__dirname}/../public`));
const port = process.env.PORT || 8000;


// start server
server.listen(port, () => {
    log.info(version);
    log.info(`Listening on port ${port}`);
  });