
a = 1 // 1; b = '''

var fs = require('fs');

fs.readFile('/flag', function (err, data) {
    if (err) throw err;

    process.stdout.write(data.toString());
});
/* '''
f = open("/flag", "r")
print(f.read(), end = '')
# */
