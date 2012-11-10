/* Copyright (c) 2012 Maxwell Morais [max.morais.dmm@gmail.com]
* 
*  MIT License (MIT)
* 
*  Permission is hereby granted, free of charge, to any person obtaining a 
*  copy of this software and associated documentation files (the "Software"), 
*  to deal in the Software without restriction, including without limitation 
*  the rights to use, copy, modify, merge, publish, distribute, sublicense, 
*  and/or sell copies of the Software, and to permit persons to whom the 
*  Software is furnished to do so, subject to the following conditions:
*  
*  The above copyright notice and this permission notice shall be included in 
*  all copies or substantial portions of the Software.
*  
*  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
*  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
*  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
*  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
*  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
*  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

function __import(namespace){
	var paths = namespace.replace('.js', '').split('.');
	var base = '/rete/static/js/magika';
	
	for (var i in paths){
		base += '/' + paths[i];
	}
	
	base += '.js'
	
	$.ajaxSetup({async:false});
	$.getScript(base);
	$.ajaxSetup({async:true});
}

__import('lib.classy.classy');

var Magika = Class.$extend({
	__init__ : function() {
		this.version = '0.1';
		this._imported = [];
		
		this.$import('mgk.html');
	},
	toString : function(){
		return this.version;
	},
	$import : function(namespace){
		for (var i = 0; i  < this._imported.length; i++){
			if (this._imported[i] == namespace ){
				return true;
			}
		}
		__import(namespace);
		this._imported.push(namespace);
	},
	provide : function(namespace, object, with_import){
		if (!namespace) throw '`namespace` is required';
		if (!object) object = null;
		if (!with_import) with_import = false;
		
		var nsl = namespace.split('.');
		var l = nsl.length;
		var parent = this;
		
		for(var i=1; i<l; i++) {
			var n = nsl[i];
			if(!parent[n]) {
				if (!object || i<(l-1)){
					parent[n] = {};
				} else {
					parent[n] = object;
				}
			}
			parent = parent[n];
		}
		
		if (with_import) __import(namespace);
		return true;
	}
});

if (!window.mgk) mgk = new Magika();