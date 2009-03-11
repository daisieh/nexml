package org.nexml.model;

import org.junit.Assert;
import org.junit.Test;

public class TestTreeBlock {
	@Test
	public void makeIntNetwork() {
		Document doc = DocumentFactory.createDocument();
		TreeBlock treeBlock = doc.createTreeBlock();
		Network<IntEdge> network = treeBlock.createIntNetwork();
		Node node1 = network.createNode();
		Node node2 = network.createNode();
		IntEdge edge = network.createEdge();
		edge.setSource(node1);
		edge.setTarget(node2);
		Assert.assertEquals("node1 == getSource is what we want", node1, edge
				.getSource());
		Assert.assertEquals("node2 == getTarget is what we want", node2, edge
				.getTarget());

		edge.setLength(34);
		Assert.assertEquals("edge.setLength should be 34", 34, edge.getLength()
				.intValue());

		OTUs mammals = doc.createOTUs();

		OTU chimp = mammals.createOTU();
		chimp.setLabel("chimp");
		node2.setOTU(chimp);
		Assert.assertEquals("node2.getOTU should be chimp", chimp, node2
				.getOTU());


	}
	
	@Test
	public void makeFloatNetwork() {
		Document doc = DocumentFactory.createDocument();
		TreeBlock treeBlock = doc.createTreeBlock();

		Network<FloatEdge> floatNetwork = treeBlock.createFloatNetwork();
		Node floatNode1 = floatNetwork.createNode();
		Node floatNode2 = floatNetwork.createNode();
		FloatEdge floatEdge = floatNetwork.createEdge();
		floatEdge.setSource(floatNode1);
		floatEdge.setTarget(floatNode2);
		Assert.assertEquals(
				"floatNode1 == floatEdge.getSource is what we want",
				floatNode1, floatEdge.getSource());
		Assert.assertEquals(
				"floatNode2 == floatEdge.getTarget is what we want",
				floatNode2, floatEdge.getTarget());		
	}
}