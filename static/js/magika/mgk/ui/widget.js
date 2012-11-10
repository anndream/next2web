// Copyright (c) 2012 Maxwell Morais [max dot morais dot dmm at gmail dot com]
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

mgk.$import('mgk.exceptions');
mgk.$import('mgk.html');
mgk.$import('mgk.model');

pattern_widget_class = /^\w*/; 

var Widget = Class.$extend({
	_atributes: function(field, widget_atributes, options){
		if (!field) throw mgk.exceptions.ValueError('Widget.field is required!');
		if (!(field instanceof Field)) throw mgk.exceptions.TypeError('Widget.field requires a valid Field');
		
		attr = {
			id: field.$model.$name+"_"+field.name,
			cls : this.cls || field.type.match(pattern_widget_class)[0],
			name: field.name
		}
		for (var key in widget_atributes){
			attr[key] = widget_attributes[key];
		}
		for (var key in options){
			attr[key] = options[key];
		}
		return attr
	},
	widget: function(field, value, attributes){
		throw mgk.exceptions.NotImplementedError();
	},
	cls: 'generic-widget',
});

var StringWidget = Widget.$extend({
	cls: 'string',
	widget: function(field, value, attributes){
		dlft = {
			type: 'text',
			value : value || ''
		},
		attr = this._attributes(field, dflt, attributes)
		return HTML.input(attr);
	}
	
})();

var IntegerWidget = StringWidget.$extend({
	cls: 'integer'
})();

var DoubleWidget = StringWidget.$extend({
	cls: 'double'
})();


var DecimalWidget = StringWidget.$extend({
	cls: 'decimal'
})();

var TimeWidget = StringWidget.$extend({
	cls: 'time'
})();

var DateWidget = StringWidget.$extend({
	cls: 'date'
})();

var DatetimeWidget = StringWidget.$extend({
	cls: 'date'
})();

var TextWidget = StringWidget.$extend({
	cls: 'text',
	widget: function(cls, field, value, atributes){
		dflt = {value: value}
		attr = cls._atributes(field, dflt, atributes)
		return HTML.textarea(attr)
	}
})();