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

var _tags = ["a", "abbr", "address", "area", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "br", "button", "canvas", "caption",
		        "cite", "code", "col", "colgroup", "command", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "embed", "fieldset",
		        "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "hgroup", "i", "iframe", "img", "input",
		        "ins", "keygen", "kdb", "label", "legend", "li", "link", "map", "mark", "menu", "meta", "meter", "nav", "noscript", "object", "ol",
		        "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select",
		        "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead",
		        "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr",

		        "html", "head", "body"];

var HTML = Class.$extend({
	__init__: function(){
		this.version = '0.1';
		this.templates = {};
		this.Node = Node;
		this.Template = Template;

        var parseArguments = function(args){
            var obj = {};

            for (var i = 0; i < args.length; i++){
                switch(typeof(args[i])){
                    case "string":{
                        if (!obj["text"]) {
                            obj["text"] = TextNode(args[i]);
                        } else {
                            if (!(obj["text"] instanceof Array)){
                                obj["text"]=[obj["text"], HTML.br(), TextNode(args[i])];
                            } else {
                                obj["text"].push(HTML.br());
                                obj["text"].push(TextNode(args[i]));
                            }
                        }
                        break;
                    }
                    case "object":{
                        if (args[i] instanceof Array){
                            if (!obj["list"]){
                                obj["list"] = args[i];
                            } else {
                                obj["list"].concat(args[i]);
                            }
                        } else {
                            if (!obj["dict"]) {
                                obj["dict"] = args[i];
                            } else {
                                for (var key in args[i]){
                                    obj["dict"][key] = args[key];
                                }
                            }
                        }
                        break;
                    }
                }
            }
            return obj;
        }

		var makeTagHelper = function(tag){
			return function(){
                parse = parseArguments(arguments);
               	if (!(typeof(children)=='undefined') && !(children instanceof Array)) children = [children];
				node = Node(tag);
                if (!(typeof(parse["text"]) == "undefined")){
                    if (parse["text"] instanceof Array){
                        for (var i=0; i < parse["text"].length; i++){
                            node.addChild(parse["text"][i]);
                        }
                    } else {
                        node.addChild(parse["text"]);
                    }
                }
				if (!(typeof(parse["dict"])=='undefined')){
					node.setAttributes(parse["dict"]);
				}
				if (parse["list"] instanceof Array){
					for (var i in parse["list"]){
						node.addChild(parse["list"][i]);
					}
				}
				return node;
			};
		};

		for (var i=0; i < _tags.length; i++){
			this[_tags[i]] = makeTagHelper(_tags[i]);
		}

	},
	register : function(name, template){
		this.templates[name] = template;
	},
	render : function(name, thisObj, data){
		var template = this.templates[name],
		    renderer = new Template(template);
		return renderer.render.apply(renderer, Array.prototype.slice.call(arguments, 1));
	},
})();

var Node = Class.$extend({
	__init__: function(tagName){
		this.tagName = tagName;
		this.attributes = {};
		this.children = [];
		this.notSelfClosingTags = ['textarea', 'script', 'em', 'strong', 'option', 'select'];

	},
	setAttributes: function(attrs){
		for (var key in attrs){
			var mappedKey = (key == 'cls') ? 'class': (key == 'data') ? 'data-options': key;
			this.attributes[mappedKey] = attrs[key];
		}
		return this;
	},
	addChild : function(childText){
		this.children.push(childText);
		return this;
	},
	render: function(lpad){
		lpad = lpad||0;
		var node      = [],
		    attrs     = [],
		    textnode  = (this instanceof TextNode),
		    multiline = this.multiLineTag();

		if (!textnode) node.push(this.getPadding(lpad));
		node.push('<'+this.tagName);
		for (var key in this.attributes){
			attrs.push(key+'="'+this.attributes[key]+'"');
		}
		attrs.sort();
		for (var i=0; i < attrs.length; i++){
			node.push(' '+attrs[i]);
		}
		if (this.isSelfClosing() && this.children.length==0){
			node.push('/>\n');
		} else {
			node.push('>');
			if (multiline) node.push('\n');
				this.renderChildren(node, this.children, lpad);
			if (multiline) node.push(this.getPadding(lpad));
				node.push('</', this.tagName, '>\n');
		}
		return node.join('');
	},
	renderChildren: function(node, children, lpad){
		var childLpad = lpad + 2;

	    for (var i=0; i < children.length; i++) {
	    	var child = children[i];
	    	if (child instanceof Array) {
	    		var nestedChildren = child;
	    		this.renderChildren(node, nestedChildren, lpad);
	    	} else {
	    		node.push(child.render(childLpad));
	    		//node.push(child);
	    	}
	    }
	},
	multiLineTag : function(){
		var childLength = this.children.length,
			multiLine = childLength > 0;
		if (childLength == 1 && this.children[0] instanceof TextNode) multiLine=false;
		return multiLine;
	},
	getPadding: function(amount){
		return new Array(amount+1).join(' ');
	},
	isSelfClosing: function(){
		for (var i = this.notSelfClosingTags.length - 1; i >= 0; i--){
			if (this.tagName.toUpperCase() === this.notSelfClosingTags[i].toUpperCase()) {
				return false;
			}
		}
		return true;
	}
});

var TextNode = Class.$extend({
	__init__: function(text){
		this.text = text;
	},
	render: function(){
		return this.text;
	}
});

var Template = Class.$extend({
	__init__: function(template){
		this.template = template;
		this.nodes = [];

		var makeTagHelper = function(tagName){
			return function(attrs){
				var node = Node(tagName);
				var firstArgsIsAttributes = (typeof attrs == 'object')
				                            && !(attrs instanceof Node)
											&& !(attrs instanceof TextNode);
				if (fistArgIsAttributes) node.setAttributes(attrs);

				var startIndex = firstArgsIsAttributes ? 1 : 0;

				for (var i=startIndex; i < arguments.length; i++){
					var arg = arguments[i];
					if (typeof arg == 'string' || arg == 'undefined') arg = new TextNode(arg||'');
					if (arg instanceof Node || arg instanceof TextNode) arg.parent = node;
					node.addChild(arg);
				}
				this.nodes.push(node);
				return node;
			};
		};

		for (var i = 0, tag; tag=_tags[i]; i++){
			this[tag] = makeTagHelper(tag);
		}
	},
	render: function(thisObj, data){
		data = data || (thisObj = thisObj || {});
		if (data.construtor.toString().indexOf('Array') === -1){
			data = [data];
		}
		with(this){
			for (var i=0; i < data.length; i++){
				eval('('+this.template.toString()+').call(thisObj), data[i], i)');
			}
		}

		var roots = this.getRoots(), output = '';
		for (var i=0; i < roots.length; i++){
			output += roots[i].render();
		}

		return output;
	},
	getRoots : function(){
		var roots = [];
		for ( var i=0; i < this.nodes.length; i++ ){
			if (node.parent == undefined) roots.push(node);
		}
		return roots;
	},
	tags : _tags
});

//(function(){
//	var makeTagHelper = function(tagName){
//		return function(attrs){
//			var node = HTML.Node(tagName);
//			var firstArgsIsAttributes = (typeof attrs == 'object')
//			                            && !(attrs instanceof HTML.Node)
//										&& !(attrs instanceof HTML.TextNode);
//			if (fistArgIsAttributes) node.setAttributes(attrs);
//
//			var startIndex = firstArgsIsAttributes ? 1 : 0;
//
//			for (var i=startIndex; i < arguments.length; i++){
//				var arg = arguments[i];
//				if (typeof arg == 'string' || arg == 'undefined') arg = new HTML.TextNode(arg||'');
//				if (arg instanceof HTML.Node || arg instanceof HTML.TextNode) arg.parent = node;
//				node.addChild(arg);
//			}
//			this.nodes.push(node);
//			return node;
//		};
//	};
//
//	for (var i = 0, tag; tag=_tags[i]; i++){
//		HTML.Template.prototype[tag.toUpperCase()] = makeTagHelper(tag);
//	}
//})();

mgk.provide('mgk.html', HTML);