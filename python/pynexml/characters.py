#! /usr/bin/env python

############################################################################
##  characters.py
##
##  Part of the PyNexml phylogenetic data parsing library.
##  
##  Copyright 2007 Jeet Sukumaran and Mark T. Holder.
##
##  This program is free software; you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation; either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License along
##  with this program. If not, see <http://www.gnu.org/licenses/>.
##
############################################################################

"""
This module handles the core definitions of character data types, as well as 
specializations to handle nucleotide, etc. character types.
"""

#                [    [0],                // A
#                     [1],                // C
#                     [2],                // G
#                     [3],                // T
#                     [-1, 0, 1, 2, 3],   // ?
#                     [0, 1, 2, 3],       // N or X
#                     [0, 1],             // M
#                     [0, 2],             // R
#                     [0, 3],             // W
#                     [1, 2],             // S
#                     [1, 3],             // Y
#                     [2, 3],             // K
#                     [0, 1, 2],          // V
#                     [0, 1, 3],          // H
#                     [0, 2, 3],          // D
#                     [1, 2, 3],          // B
#                 ]        

from pynexml import base
from pynexml import taxa

class DiscreteStateAlphabetElement(base.IdTagged):
    """
    A character state definition, which can either be a fundamental state or
    a mapping to a set of other character states (for polymorphic or ambiguous
    characters).
    """
    
    # multistate enums
    SINGLE_STATE = 0
    AMBIGUOUS_STATE = 1
    POLYMORPHIC_STATE = 2
    
    def __init__(self, 
                 elem_id=None, 
                 label=None,
                 symbol=None, 
                 token=None, 
                 multistate=SINGLE_STATE, 
                 member_states=None):
        base.IdTagged.__init__(self, elem_id=elem_id, label=label)
        self.symbol = symbol
        self.token = token
        self.multistate = multistate
        self.member_states = member_states
        
    def __str__(self):
        return str(self.symbol)
        
    def __repr__(self):
        return str([self.elem_id, 
                    self.symbol, 
                    '[' + (', '.join(self._get_fundamental_symbols())) + ']'])
        
    def _get_fundamental_states(self):
        """
        Returns value of self in terms of a set of _get_fundamental states (i.e.,
        set of single states) that correspond to this state.
        """
        if self.member_states is None:
            return set([self])
        else:
            states = set()
            for state in self.member_states:
                states.update(state._get_fundamental_states())
            return states
            
    fundamental_states = property(_get_fundamental_states)          
                 
    def _get_fundamental_ids(self):
        """
        Returns set of id's of all _get_fundamental states to which this state maps.
        """
        return set([state.elem_id for state in self._get_fundamental_states()])
        
    fundamental_ids = property(_get_fundamental_ids)          
        
    def _get_fundamental_symbols(self):
        """
        Returns set of symbols of all _get_fundamental states to which this state maps.
        """
        return set([state.symbol for state in self._get_fundamental_states() if state.symbol]) 
        
    fundamental_symbols = property(_get_fundamental_symbols)
        
    def _get_fundamental_tokens(self):
        """
        Returns set of tokens of all _get_fundamental states to which this state maps.
        """
        return set([state.token for state in self._get_fundamental_states() if state.token])        
        
    fundamental_tokens = property(_get_fundamental_tokens)   
             
class DiscreteStateAlphabetSet(base.IdTagged, set):
    """
    A set of states available for a particular character type/format.
    """
    
    def __init__(self, elem_id=None, label=None):
        base.IdTagged.__init__(self, elem_id=elem_id, label=label)  
        set.__init__(self)
        
    def get_state(self, attr_name, value):
        """
        Returns state in self in which attr_name equals value.
        """
#         attr_name = None
#         value = None
#         if elem_id is not None:
#             attr_name = 'elem_id'
#             value = elem_id
#         elif symbol is not None:
#             attr_name = 'symbol'
#             value = symbol
#         elif token is not None:
#             attr_name = 'token'
#             value = token
#         else:
#             raise Exception("Must specify id, symbol or token")
        for state in self:
            if getattr(state, attr_name) == value:
                return state
        raise Exception("State with %s value of '%s' not defined" % (attr_name, str(value)))
    
    def get_states(self, elem_ids=None, symbols=None, tokens=None):
        """
        Returns list of states with ids/symbols/tokens equal to values
        given in a list of ids/symbols/tokens (exact matches, one-to-one
        correspondence between state and attribute value in list).
        """
        if elem_ids is not None:
            attr_name = 'elem_id'
            values = elem_ids
        elif symbols is not None:
            attr_name = 'symbol'
            values = symbols
        elif tokens is not None:
            attr_name = 'token'
            values = tokens
        else:
            raise Exception("Must specify ids, symbols or tokens")    
        states = []
        for value in values:
            states.append(self.get_state(attr_name=attr_name, value=value))
        return states
    
    def match_state(self, elem_ids=None, symbols=None, tokens=None):
        """
        Returns SINGLE state that has ids/symbols/tokens as member states.
        """
        if elem_ids is not None:
            attr_name = 'fundamental_ids'
            values = elem_ids
        elif symbols is not None:
            attr_name = 'fundamental_symbols'
            values = symbols
        elif tokens is not None:
            attr_name = 'fundamental_tokens'
            values = tokens
        else:
            raise Exception("Must specify ids, symbols or tokens")  
        if isinstance(values, list):
            values = set(values)
        elif isinstance(values, str):
            values = set([ch for ch in values])

        for state in self:
            if getattr(state, attr_name) == values:
                return state
        return None
           
class DnaStateAlphabetSet(DiscreteStateAlphabetSet):

    def __init__(self, elem_id=None, label=None):
        DiscreteStateAlphabetSet.__init__(self, elem_id=elem_id, label=label)
        self.append(DiscreteStateAlphabetElement(symbol="A"))
        self.append(DiscreteStateAlphabetElement(symbol="C"))     
        self.append(DiscreteStateAlphabetElement(symbol="G"))
        self.append(DiscreteStateAlphabetElement(symbol="T"))
        self.append(DiscreteStateAlphabetElement(symbol="-")) 
        self.append(DiscreteStateAlphabetElement(symbol="?",
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'C', 'G', 'T', '-'])))
        self.append(DiscreteStateAlphabetElement(symbol="N",
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'C', 'G', 'T'])))
        self.append(DiscreteStateAlphabetElement(symbol="M", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'C'])))                                            
        self.append(DiscreteStateAlphabetElement(symbol="R", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'G'])))
        self.append(DiscreteStateAlphabetElement(symbol="W",
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'T'])))
        self.append(DiscreteStateAlphabetElement(symbol="S", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['C', 'G'])))                                            
        self.append(DiscreteStateAlphabetElement(symbol="Y", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['C', 'T'])))   
        self.append(DiscreteStateAlphabetElement(symbol="K", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['G', 'T'])))                                            
        self.append(DiscreteStateAlphabetElement(symbol="V", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'C', 'G'])))
        self.append(DiscreteStateAlphabetElement(symbol="H",
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'C', 'T'])))
        self.append(DiscreteStateAlphabetElement(symbol="D", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['A', 'G', 'T'])))                                            
        self.append(DiscreteStateAlphabetElement(symbol="B", 
                                           multistate=DiscreteStateAlphabetElement.AMBIGUOUS_STATE,
                                           member_states=self.get_states(symbols=['C', 'G', 'T'])))

class Character(base.IdTagged):
    """                                                                                                                                                                                                                                                                                                                                                                           
    A character format or type of a particular column: i.e., maps
    a particular set of character state definitions to a column in a character matrix.
    """
  
    def __init__(self, elem_id=None,label=None, state_alphabet_set=None):
        base.IdTagged.__init__(self, elem_id=elem_id, label=label)
        self.state_alphabet_set = state_alphabet_set
                
       
class CharactersBlock(dict, taxa.TaxaLinked):
    """
    Character data container/manager manager.
    """

    def __init__(self, *args, **kwargs):
        """
        Inits. Handles keyword arguments: `elem_id`, `label` and `taxa_block`.
        """
        dict.__init__(self, *args)
        taxa.TaxaLinked.__init__(self, *args, **kwargs)
        self.state_alphabet_sets = []
        self.characters = []

class DnaCharactersBlock(CharactersBlock):
    """
    DNA nucleotide data.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Inits. Handles keyword arguments: `elem_id`, `label` and `taxa_block`.
        """
        CharactersBlock(*args, **kwargs)
        self.state_alphabet_sets.append(DnaStateAlphabetSet())
        

if __name__ == "__main__":
    dna = DnaStateAlphabets()
    for s in dna:
        print repr(s)
    print
    print
    input = "\n"
    while input:
        input = raw_input("Enter symbol(s): ")
        if input:
            input = input.upper()
            print repr(dna.match_state(symbols=input))