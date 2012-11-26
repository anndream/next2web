// Copyright (c) 2012 Maxwell Morais [max.morais.dmm@gmail.com]
// 
// MIT License (MIT)
// 
// Permission is hereby granted, free of charge, to any person obtaining a 
// copy of this software and associated documentation files (the "Software"), 
// to deal in the Software without restriction, including without limitation 
// the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the 
// Software is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in 
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
// PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
// CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
// OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//

var Exception = Class.$extend({
	type: 'Exception',
	__init__: function(message){
		this.message = message || 'Exception';
	},
	toString: function(){
		return '<'+this.type+'(`'+this.message+'`)>'
	}
});

var ValueError = Exception.$extend({type:'ValueError'});
var KeyError = Exception.$extend({type:'KeyError'});
var TypeError = Exception.$extend({type: 'TypeError'});
var NotImplementedError = Exception.$extend({type: 'NotImplementedError'});

mgk.provide('mgk.exceptions.Exception', Exception);
mgk.provide('mgk.exceptions.ValueError', ValueError);
mgk.provide('mgk.exceptions.KeyError', KeyError);
mgk.provide('mgk.exceptions.TypeError', TypeError);
mgk.provide('mgk.exceptions.NotImplementedError', NotImplementedError);
