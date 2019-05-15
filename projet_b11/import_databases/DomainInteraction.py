class DomainInteraction:
    """
    Lightweight class to represent a domain-domain interaction.
    """

    def __init__(self, first_dom, second_dom):
        self.first_dom = first_dom
        self.second_dom = second_dom

    def __eq__(self, obj):
        """
        Redefine equals so we can compare each domain-domain interaction easily.

        How to define equals
        https://www.dimagi.com/blog/overriding-equals-in-python/
        """
        return isinstance(obj, DomainInteraction) and ((self.first_dom == obj.first_dom and
                                                        self.second_dom == obj.second_dom) or
                                                       (self.first_dom == obj.second_dom and
                                                        self.second_dom == obj.first_dom))

    def __str__(self):
        """
        Override of str
        """
        return "First domain : " + self.first_dom + "\nSecond domain : " + self.second_dom

    def __hash__(self):
        """
        To redefine Hash, we concatenate the two domains and hash the resulting string.
        """
        if self.first_dom == self.second_dom:
            return hash(self.first_dom)
        return hash(self.first_dom) ^ hash(self.second_dom)
