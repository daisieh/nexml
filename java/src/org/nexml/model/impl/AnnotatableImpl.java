package org.nexml.model.impl;

import java.util.Set;

import org.nexml.model.Annotatable;
import org.nexml.model.Annotation;
import org.w3c.dom.Document;
import org.w3c.dom.Element;

abstract class AnnotatableImpl extends NexmlWritableImpl implements Annotatable {
    
    private Set<Annotation> mAnnotations;
    
    /**
     * Protected constructors are intended for recursive parsing, i.e.
     * starting from the root element (which maps onto DocumentImpl) we
     * traverse the element tree such that for every child element that maps
     * onto an Impl class the containing class calls that child's protected
     * constructor, passes in the element of the child. From there the 
     * child takes over, populates itself and calls the protected 
     * constructors of its children. These should probably be protected
     * because there is all sorts of opportunity for outsiders to call
     * these in the wrong context, passing in the wrong elements etc.
     * @param document the containing DOM document object. Every Impl 
     * class needs a reference to this so that it can create DOM element
     * objects
     * @param element the equivalent NeXML element (e.g. for OTUsImpl, it's
     * the <otus/> element)
     * @author rvosa
     */
    protected AnnotatableImpl(Document document, Element element) {
        super(document, element);
    }

    /**
     * Protected constructors that take a DOM document object but not
     * an element object are used for generating new element nodes in
     * a NeXML document. On calling such constructors, a new element
     * is created, which can be retrieved using getElement(). After this
     * step, the Impl class that called this constructor would still 
     * need to attach the element in the proper location (typically
     * as a child element of the class that called the constructor). 
     * @param document a DOM document object
     * @author rvosa
     */
    protected AnnotatableImpl(Document document) {
        super(document);
    }
    
    protected AnnotatableImpl() {}

    /*
     * (non-Javadoc)
     * @see org.nexml.model.Annotatable#getAnnotationValues(java.lang.String)
     */
    public Set<Object> getAnnotationValues(String property) {
        //TODO
           return null;
    }
    
    /*
     * (non-Javadoc)
     * @see org.nexml.model.Annotatable#addAnnotationValue(java.lang.String, java.lang.Object)
     */
    public void addAnnotationValue(String property, Object value) {
           AnnotationImpl annotation = new AnnotationImpl(property, value);
           mAnnotations.add(annotation);
           getElement().appendChild(annotation.getElement());
    }
       
}