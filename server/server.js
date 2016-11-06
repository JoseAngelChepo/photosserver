var express = require('express');
var app = express();

app.use(express.static('public'));

app.listen(8090, function (err) {
	if (err) return console.log('Error'), process.exit(1);
	console.log('success');
})
