(function(){
function Tree (args) {
	if (args==null) args = {};
	args["tag"] = "tree";
    this.Listable(args);
    this._type      = Phylo.Util.CONSTANT._TREE_;
    this._container = Phylo.Util.CONSTANT._FOREST_;
    return this;
}
Phylo.Forest.Tree = Tree;
copyPrototype(Phylo.Forest.Tree,Phylo.Listable);

Phylo.Forest.Tree.prototype._type = function() {
    return this._type;
};

Phylo.Forest.Tree.prototype._container = function() {
    return this._container;
};

Phylo.Forest.Tree.prototype.get_terminals = function () {
    var terminals = new Array();
    var allnodes = this.get_entities();
    for ( var i = 0; i < allnodes.length; i++ ) {
        if ( allnodes[i].is_terminal() ) {
            terminals.push(allnodes[i]);
        }
    }
    return terminals;
};

Phylo.Forest.Tree.prototype.get_internals = function () {
    var internals = new Array();
    var allnodes = this.get_entities();
    for ( var i = 0; i < allnodes.length; i++ ) {
        if ( allnodes[i].is_internals() ) {
            internals.push(allnodes[i]);
        }
    }
    return internals;
};

Phylo.Forest.Tree.prototype.get_root = function () {
    var nodes = this.get_entities();
    for ( var i = 0; i < nodes.length; i++ ) {
        if ( nodes[i].get_parent() == null ) {
            return nodes[i];
        }
    }
    return null;
};

Phylo.Forest.Tree.prototype.calc_number_of_terminals = function () {
	return this.get_terminals().length;
};

Phylo.Forest.Tree.prototype.visit_depth_first = function(args) {
	return this.get_root().visit_depth_first(args);
};

Phylo.Forest.Tree.prototype.to_newick = function () {
    return this.get_root().to_newick();
};

Phylo.Forest.Tree.prototype.to_xml = function () {
	var xsi_type = 'nex:IntTree';
	var nodes = this.get_entities();
	for ( var i = 0; i < nodes.length; i++ ) {
		var bl = nodes[i].get_branch_length();
		if ( bl != null && parseInt(bl) != bl ) {
			xsi_type = 'nex:FloatTree';
			break;
		}
	}
	this.set_attributes( { 'xsi:type' : xsi_type } );
	var xml = this.get_xml_tag();
	var root = this.get_root();
	if ( root != null ) {
		xml += root.to_xml();
	}
	xml += '</' + this.get_tag() + '>'; 
	return xml;		
};
})()