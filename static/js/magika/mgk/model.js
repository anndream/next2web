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

function UUID() {
   var chars = '0123456789abcdef'.split('');

   var uuid = [], rnd = Math.random, r;
   uuid[8] = uuid[13] = uuid[18] = uuid[23] = '-';
   uuid[14] = '4'; // version 4

   for (var i = 0; i < 36; i++)
   {
      if (!uuid[i])
      {
         r = 0 | rnd()*16;

         uuid[i] = chars[(i == 19) ? (r & 0x3) | 0x8 : r & 0xf];
      }
   }

   return uuid.join('');
}


var pattern = /^([a-zA-Z_]{1})([a-zA-Z0-9]{1})([a-zA-Z0-9_]*)$/;
var types = [
   'string',
   'integer',
   'double',
   'decimal',
   'date',
   'time',
   'datetime',
   'boolean'
];

var Meta = Class.$extend({
	__init__: function(){
		this.UUID = UUID();
	},
	setUUID: function(uuid){
		this.UUID = uuid;
	},
	getUUID: function(){
		if (!this.UUID) this.setUUID(UUID());
		return this.UUID;
	},
	toJSON: function(){
		var object = {};
		for (var attr in this){
			if ((attr.substring(0,2) == '__')||(attr == '$model')) continue;
			if (this[attr] instanceof Array){
				object[attr] = this.JSONFromArray(this[attr]);
			} else
			{			
				if (!(typeof(this[attr]) == 'function')||(this[attr] instanceof Meta)){
					object[attr] = this[attr].hasOwnProperty('toJSON')? this[attr].toJSON() : this[attr];
				}
			}
		}
		return {key: this.UUID, objects: object};
	},
	JSONFromArray : function(subSet){
		if (!subSet) throw '`subSet` is required';
		if (!(subSet instanceof Array)) throw 'It require an Array to `subSet`';
		if (subSet.length == 0) return subSet;
		
		var objects = [];
		
		for (var i=0; i < subSet.length; i++){
			if (subSet[i].hasOwnProperty('toJSON')){
				objects[objects.length] = subSet[i].toJSON();
			}
		}
		return objects;
	}
});

var Relation = Meta.$extend({
	lft_field: null,
	__init__: function(field){
		this.$super();
		
		if (!field) throw 'Relation.field is required';
		if (!(model instanceof Field)) throw 'Relation.field requires a valid field';
		
		this.rgt_field = field;
	},
	registerField: function(field){
		if (!field) throw 'Relation.field is required';
				
		if (!this.lft_field){
			this.lft_field = field;
		}
	},
	
});

var Field = Meta.$extend({
	$model: null,
	options: {
		required: false,
        deft: null,
	},
	__init__: function (name, type, options){
		this.$super();
		
		var contains = false;
		
		if (!name) throw 'Field.name is required';
		if (!name.match(pattern)) throw 'Field.name does not match a valid name';
		if (!type) throw 'Field.type is required';		
		for (var i = 0; i < types.length; i++){
			if (types[i] == type) contains = true;
		};
		if (!contains && !(type instanceof Relation)) throw 'Invalid type for Field.type';
		if (!options) options = {};
		
		this.name = name;
		this.type = type;
		
		for (var option in options){
			if (option in this.options) this.options[option] = options[option];
		}
		if (type instanceof relation) {
			for (var relation in options['relation']){
				this.type.registerField(this);
				this.type.push(relation);
			};
		};	
	},
	registerModel: function(model){
		this.$model = model;
	}
});

var Model = Meta.$extend({
	$relations : [],
	__init__: function(name, fields){
		this.$super();
		
		if (!name) throw 'Model.name is required';
		if (!name.match(pattern)) throw 'Model.name does not match a valid name';
		if (!fields|| !(fields.length >= 1)) throw 'Model.fields requires one or more fields';
		while (fields.length > 0){
			if (!(fields[fields.length-1] instanceof Field)) throw 'Model.fields contains a invalid field';
			this.addField(fields.pop(fields.length-1));
		}
		this.$name = name;
	},
	addField: function(field){
		if(!(field instanceof Field)) throw 'Model.addField requires a valid field';
		field.registerModel(this);
		if (field.type instanceof Relation){
			this.addRelation(field);
			field.type = 'relation '+this.$name;
		}
		this[field.name]=field;
	},
	removeField: function(fieldName){
		if(!(fieldName in this)) throw 'Model.removeField does not contains this field';
		delete this[fieldName];
	},
	addRelation: function(relation){
		if (!(relation instanceof Relation)) throw '`relation` requires a valid Relation';
		this.$relations.push(relation);
	},
	removeRelation: function(index){
		if (index <= this.$relations.length){
			delete this.$relations[index]
			return;
		}
		throw 'Cold not find an Relation on index';
	},
	toString: function(){
		return '<Model name="'+this.$name+'"/>';
	}
});

var Db = Meta$.extend({
	$options : {},
	__init__: function(url, options){
		this.$url = url;
		this.$storage = window.localStorage;
		this.$lastSync = null;
		this.$queue = [];
		if ( !typeof options === 'undefined' ) {
			for (var key in options){
				this.$options[key] = options[key];
			}
		};
	},
	getData: function(key){
		var strData = this.$storage.getItem(key);
		return JSON.parse(strData);
	},
	setData: function(key, data){
		var text = JSON.stringify(data);
		this.storage.setItem(key, text);
	},
	sync: function(key, data){
		if (!this.isOnline()) return false;
		
		this.$lastSync = this.getData('lastSync');
		
		if (!this.$lastSync){ 
			this.$lastSync = { when: new Date().strftime("'%Y-%m-%d'")  , isModified : false};
		}
		if (!this.$lastSync.isModified){
			while ( this.$queue.length > 0 ){
				this.$requestOptions = this.$queue.pop();
				$.ajax(this.$requestOptions.ajax);
				this.setData('queue', []);
				this.$lastSync['isModified'] = false;
			}
			this.setData('lastSync', this.$lastSync);
			
			$.ajax({
				type: 'POST',
				url: this.$url,
				dataType: 'json',
				data: {'lastSync': this.lastSync.syncDate},
				beforeSend: (!this.$options.beforeSync) ? function(){} : this.$options.beforeSync,
				error: (!this.$options.onError) ? function(){} : this.$options.onError,
				sucess: (!this.$options.onSucess) ? function(){} : this.$options.onSucess,
			});
		}
	},
	$send: function(){
	},
	$receive: function(){
	},
	isOnLine: function(){
		return navigator.isOnline;
	}
});

mgk.provide('mgk.model.types', types);
mgk.provide('mgk.model.Field', Field);
mgk.provide('mgk.model.Model', Model);
mgk.provide('mgk.model.Relation', Relation);