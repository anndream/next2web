nxt.Document = Class.$extend({
	__init__: function( docname ){
		if (!docname) throw('nxt.Document requires an docname')
		this.docname
	},
	start_tags: function(){},
	start_comments: function(){}
})
