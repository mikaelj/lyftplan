'use strict';

// FROM: https://gist.github.com/antelle/7021916
//
// "{} {}".format("a", "b") => "a b"
// "{1} {0}".format("a", "b") => "b a"
// "{foo} {bar}".format({ foo: "a", bar: "b" }) => "a b"
String.prototype.format = function() {
    var args = arguments;
    var argNum = 0;
    return this.replace(/\{(\w*)\}/gi, function(match) {
        var curArgNum, prop = null;
        if (match == "{}") {
            curArgNum = argNum;
            argNum++;
        } else {
            curArgNum = match.substr(1, match.length - 2);
            var parsed = ~~curArgNum;
            if (parsed.toString() === curArgNum) {
                curArgNum = parsed;
            } else {
                prop = curArgNum;
                curArgNum = 0;
            }
        }
        var result = curArgNum >= args.length ? "" : prop ? args[curArgNum][prop] || "" : args[curArgNum];
        return result;
    });
};

Date.prototype.ymdString = function() {
    return "{}-{}-{}".format(this.getFullYear(), this.getMonth()+1, this.getDate())
}
